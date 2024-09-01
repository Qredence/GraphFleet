import { entityKind } from "../../entity.js";
import { DefaultLogger } from "../../logger.js";
import { PgDatabase } from "../../pg-core/db.js";
import { PgDialect } from "../../pg-core/dialect.js";
import {
  createTableRelationsHelpers,
  extractTablesRelationalConfig
} from "../../relations.js";
import { AwsDataApiSession } from "./session.js";
class AwsPgDialect extends PgDialect {
  static [entityKind] = "AwsPgDialect";
  escapeParam(num) {
    return `:${num + 1}`;
  }
}
function drizzle(client, config) {
  const dialect = new AwsPgDialect();
  let logger;
  if (config.logger === true) {
    logger = new DefaultLogger();
  } else if (config.logger !== false) {
    logger = config.logger;
  }
  let schema;
  if (config.schema) {
    const tablesConfig = extractTablesRelationalConfig(
      config.schema,
      createTableRelationsHelpers
    );
    schema = {
      fullSchema: config.schema,
      schema: tablesConfig.tables,
      tableNamesMap: tablesConfig.tableNamesMap
    };
  }
  const session = new AwsDataApiSession(client, dialect, schema, { ...config, logger }, void 0);
  return new PgDatabase(dialect, session, schema);
}
export {
  AwsPgDialect,
  drizzle
};
//# sourceMappingURL=driver.js.map