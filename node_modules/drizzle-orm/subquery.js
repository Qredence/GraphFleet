import { entityKind } from "./entity.js";
const SubqueryConfig = Symbol.for("drizzle:SubqueryConfig");
class Subquery {
  static [entityKind] = "Subquery";
  /** @internal */
  [SubqueryConfig];
  constructor(sql, selection, alias, isWith = false) {
    this[SubqueryConfig] = {
      sql,
      selection,
      alias,
      isWith
    };
  }
  // getSQL(): SQL<unknown> {
  // 	return new SQL([this]);
  // }
}
class WithSubquery extends Subquery {
  static [entityKind] = "WithSubquery";
}
export {
  Subquery,
  SubqueryConfig,
  WithSubquery
};
//# sourceMappingURL=subquery.js.map