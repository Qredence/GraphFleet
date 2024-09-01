import type { Field } from '@aws-sdk/client-rds-data';
import { TypeHint } from '@aws-sdk/client-rds-data';
import type { QueryTypingsValue } from "../../sql/sql.js";
export declare function getValueFromDataApi(field: Field): string | number | boolean | string[] | Uint8Array | null;
export declare function typingsToAwsTypeHint(typings?: QueryTypingsValue): TypeHint | undefined;
export declare function toValueParam(value: any, typings?: QueryTypingsValue): {
    value: Field;
    typeHint?: TypeHint;
};
