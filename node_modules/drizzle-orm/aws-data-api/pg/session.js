import {
  BeginTransactionCommand,
  CommitTransactionCommand,
  ExecuteStatementCommand,
  RollbackTransactionCommand
} from "@aws-sdk/client-rds-data";
import { entityKind } from "../../entity.js";
import {
  PgPreparedQuery,
  PgSession,
  PgTransaction
} from "../../pg-core/index.js";
import { fillPlaceholders, sql } from "../../sql/sql.js";
import { mapResultRow } from "../../utils.js";
import { getValueFromDataApi, toValueParam } from "../common/index.js";
class AwsDataApiPreparedQuery extends PgPreparedQuery {
  constructor(client, queryString, params, typings, options, fields, transactionId, customResultMapper) {
    super({ sql: queryString, params });
    this.client = client;
    this.params = params;
    this.typings = typings;
    this.options = options;
    this.fields = fields;
    this.transactionId = transactionId;
    this.customResultMapper = customResultMapper;
    this.rawQuery = new ExecuteStatementCommand({
      sql: queryString,
      parameters: [],
      secretArn: options.secretArn,
      resourceArn: options.resourceArn,
      database: options.database,
      transactionId,
      includeResultMetadata: !fields && !customResultMapper
    });
  }
  static [entityKind] = "AwsDataApiPreparedQuery";
  rawQuery;
  async execute(placeholderValues = {}) {
    const { fields, joinsNotNullableMap, customResultMapper } = this;
    const rows = await this.values(placeholderValues);
    if (!fields && !customResultMapper) {
      return rows;
    }
    return customResultMapper ? customResultMapper(rows) : rows.map((row) => mapResultRow(fields, row, joinsNotNullableMap));
  }
  all(placeholderValues) {
    return this.execute(placeholderValues);
  }
  async values(placeholderValues = {}) {
    const params = fillPlaceholders(this.params, placeholderValues ?? {});
    this.rawQuery.input.parameters = params.map((param, index) => ({
      name: `${index + 1}`,
      ...toValueParam(param, this.typings[index])
    }));
    this.options.logger?.logQuery(this.rawQuery.input.sql, this.rawQuery.input.parameters);
    const { fields, rawQuery, client, customResultMapper } = this;
    if (!fields && !customResultMapper) {
      const result2 = await client.send(rawQuery);
      if (result2.columnMetadata && result2.columnMetadata.length > 0) {
        return this.mapResultRows(result2.records ?? [], result2.columnMetadata);
      }
      return result2.records ?? [];
    }
    const result = await client.send(rawQuery);
    return result.records?.map((row) => {
      return row.map((field) => getValueFromDataApi(field));
    });
  }
  /** @internal */
  mapResultRows(records, columnMetadata) {
    return records.map((record) => {
      const row = {};
      for (const [index, field] of record.entries()) {
        const { name } = columnMetadata[index];
        row[name ?? index] = getValueFromDataApi(field);
      }
      return row;
    });
  }
}
class AwsDataApiSession extends PgSession {
  constructor(client, dialect, schema, options, transactionId) {
    super(dialect);
    this.client = client;
    this.schema = schema;
    this.options = options;
    this.transactionId = transactionId;
    this.rawQuery = {
      secretArn: options.secretArn,
      resourceArn: options.resourceArn,
      database: options.database
    };
  }
  static [entityKind] = "AwsDataApiSession";
  /** @internal */
  rawQuery;
  prepareQuery(query, fields, transactionId, customResultMapper) {
    return new AwsDataApiPreparedQuery(
      this.client,
      query.sql,
      query.params,
      query.typings ?? [],
      this.options,
      fields,
      transactionId,
      customResultMapper
    );
  }
  execute(query) {
    return this.prepareQuery(
      this.dialect.sqlToQuery(query),
      void 0,
      this.transactionId
    ).execute();
  }
  async transaction(transaction, config) {
    const { transactionId } = await this.client.send(new BeginTransactionCommand(this.rawQuery));
    const session = new AwsDataApiSession(this.client, this.dialect, this.schema, this.options, transactionId);
    const tx = new AwsDataApiTransaction(this.dialect, session, this.schema);
    if (config) {
      await tx.setTransaction(config);
    }
    try {
      const result = await transaction(tx);
      await this.client.send(new CommitTransactionCommand({ ...this.rawQuery, transactionId }));
      return result;
    } catch (e) {
      await this.client.send(new RollbackTransactionCommand({ ...this.rawQuery, transactionId }));
      throw e;
    }
  }
}
class AwsDataApiTransaction extends PgTransaction {
  static [entityKind] = "AwsDataApiTransaction";
  transaction(transaction) {
    const savepointName = `sp${this.nestedIndex + 1}`;
    const tx = new AwsDataApiTransaction(this.dialect, this.session, this.schema, this.nestedIndex + 1);
    this.session.execute(sql`savepoint ${savepointName}`);
    try {
      const result = transaction(tx);
      this.session.execute(sql`release savepoint ${savepointName}`);
      return result;
    } catch (e) {
      this.session.execute(sql`rollback to savepoint ${savepointName}`);
      throw e;
    }
  }
}
export {
  AwsDataApiPreparedQuery,
  AwsDataApiSession,
  AwsDataApiTransaction
};
//# sourceMappingURL=session.js.map