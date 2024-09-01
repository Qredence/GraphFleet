"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);
var session_exports = {};
__export(session_exports, {
  AwsDataApiPreparedQuery: () => AwsDataApiPreparedQuery,
  AwsDataApiSession: () => AwsDataApiSession,
  AwsDataApiTransaction: () => AwsDataApiTransaction
});
module.exports = __toCommonJS(session_exports);
var import_client_rds_data = require("@aws-sdk/client-rds-data");
var import_entity = require("../../entity.cjs");
var import_pg_core = require("../../pg-core/index.cjs");
var import_sql = require("../../sql/sql.cjs");
var import_utils = require("../../utils.cjs");
var import_common = require("../common/index.cjs");
class AwsDataApiPreparedQuery extends import_pg_core.PgPreparedQuery {
  constructor(client, queryString, params, typings, options, fields, transactionId, customResultMapper) {
    super({ sql: queryString, params });
    this.client = client;
    this.params = params;
    this.typings = typings;
    this.options = options;
    this.fields = fields;
    this.transactionId = transactionId;
    this.customResultMapper = customResultMapper;
    this.rawQuery = new import_client_rds_data.ExecuteStatementCommand({
      sql: queryString,
      parameters: [],
      secretArn: options.secretArn,
      resourceArn: options.resourceArn,
      database: options.database,
      transactionId,
      includeResultMetadata: !fields && !customResultMapper
    });
  }
  static [import_entity.entityKind] = "AwsDataApiPreparedQuery";
  rawQuery;
  async execute(placeholderValues = {}) {
    const { fields, joinsNotNullableMap, customResultMapper } = this;
    const rows = await this.values(placeholderValues);
    if (!fields && !customResultMapper) {
      return rows;
    }
    return customResultMapper ? customResultMapper(rows) : rows.map((row) => (0, import_utils.mapResultRow)(fields, row, joinsNotNullableMap));
  }
  all(placeholderValues) {
    return this.execute(placeholderValues);
  }
  async values(placeholderValues = {}) {
    const params = (0, import_sql.fillPlaceholders)(this.params, placeholderValues ?? {});
    this.rawQuery.input.parameters = params.map((param, index) => ({
      name: `${index + 1}`,
      ...(0, import_common.toValueParam)(param, this.typings[index])
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
      return row.map((field) => (0, import_common.getValueFromDataApi)(field));
    });
  }
  /** @internal */
  mapResultRows(records, columnMetadata) {
    return records.map((record) => {
      const row = {};
      for (const [index, field] of record.entries()) {
        const { name } = columnMetadata[index];
        row[name ?? index] = (0, import_common.getValueFromDataApi)(field);
      }
      return row;
    });
  }
}
class AwsDataApiSession extends import_pg_core.PgSession {
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
  static [import_entity.entityKind] = "AwsDataApiSession";
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
    const { transactionId } = await this.client.send(new import_client_rds_data.BeginTransactionCommand(this.rawQuery));
    const session = new AwsDataApiSession(this.client, this.dialect, this.schema, this.options, transactionId);
    const tx = new AwsDataApiTransaction(this.dialect, session, this.schema);
    if (config) {
      await tx.setTransaction(config);
    }
    try {
      const result = await transaction(tx);
      await this.client.send(new import_client_rds_data.CommitTransactionCommand({ ...this.rawQuery, transactionId }));
      return result;
    } catch (e) {
      await this.client.send(new import_client_rds_data.RollbackTransactionCommand({ ...this.rawQuery, transactionId }));
      throw e;
    }
  }
}
class AwsDataApiTransaction extends import_pg_core.PgTransaction {
  static [import_entity.entityKind] = "AwsDataApiTransaction";
  transaction(transaction) {
    const savepointName = `sp${this.nestedIndex + 1}`;
    const tx = new AwsDataApiTransaction(this.dialect, this.session, this.schema, this.nestedIndex + 1);
    this.session.execute(import_sql.sql`savepoint ${savepointName}`);
    try {
      const result = transaction(tx);
      this.session.execute(import_sql.sql`release savepoint ${savepointName}`);
      return result;
    } catch (e) {
      this.session.execute(import_sql.sql`rollback to savepoint ${savepointName}`);
      throw e;
    }
  }
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  AwsDataApiPreparedQuery,
  AwsDataApiSession,
  AwsDataApiTransaction
});
//# sourceMappingURL=session.cjs.map