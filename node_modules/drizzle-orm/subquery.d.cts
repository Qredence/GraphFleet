import { entityKind } from "./entity.cjs";
import type { SQL, SQLWrapper } from "./sql/sql.cjs";
export declare const SubqueryConfig: unique symbol;
export interface Subquery<TAlias extends string = string, TSelectedFields = unknown> extends SQLWrapper {
}
export declare class Subquery<TAlias extends string = string, TSelectedFields = unknown> implements SQLWrapper {
    static readonly [entityKind]: string;
    _: {
        brand: 'Subquery';
        selectedFields: TSelectedFields;
        alias: TAlias;
    };
    constructor(sql: SQL, selection: Record<string, unknown>, alias: string, isWith?: boolean);
}
export declare class WithSubquery<TAlias extends string = string, TSelection = unknown> extends Subquery<TAlias, TSelection> {
    static readonly [entityKind]: string;
}
