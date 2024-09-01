import { entityKind } from "../../entity.js";
import { PgColumn, PgColumnBuilder } from "./common.js";
const isPgEnumSym = Symbol.for("drizzle:isPgEnum");
function isPgEnum(obj) {
  return !!obj && typeof obj === "function" && isPgEnumSym in obj && obj[isPgEnumSym] === true;
}
class PgEnumColumnBuilder extends PgColumnBuilder {
  static [entityKind] = "PgEnumColumnBuilder";
  constructor(name, enumInstance) {
    super(name, "string", "PgEnumColumn");
    this.config.enum = enumInstance;
  }
  /** @internal */
  build(table) {
    return new PgEnumColumn(
      table,
      this.config
    );
  }
}
class PgEnumColumn extends PgColumn {
  static [entityKind] = "PgEnumColumn";
  enum = this.config.enum;
  enumValues = this.config.enum.enumValues;
  constructor(table, config) {
    super(table, config);
    this.enum = config.enum;
  }
  getSQLType() {
    return this.enum.enumName;
  }
}
function pgEnum(enumName, values) {
  const enumInstance = Object.assign(
    (name) => new PgEnumColumnBuilder(name, enumInstance),
    {
      enumName,
      enumValues: values,
      [isPgEnumSym]: true
    }
  );
  return enumInstance;
}
export {
  PgEnumColumn,
  PgEnumColumnBuilder,
  isPgEnum,
  pgEnum
};
//# sourceMappingURL=enum.js.map