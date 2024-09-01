import { entityKind } from "../../entity.js";
import type { Logger } from "../../logger.js";
import { PgDatabase } from "../../pg-core/db.js";
import { PgDialect } from "../../pg-core/dialect.js";
import type { DrizzleConfig } from "../../utils.js";
import type { AwsDataApiClient, AwsDataApiPgQueryResultHKT } from "./session.js";
export interface PgDriverOptions {
    logger?: Logger;
    database: string;
    resourceArn: string;
    secretArn: string;
}
export interface DrizzleAwsDataApiPgConfig<TSchema extends Record<string, unknown> = Record<string, never>> extends DrizzleConfig<TSchema> {
    database: string;
    resourceArn: string;
    secretArn: string;
}
export type AwsDataApiPgDatabase<TSchema extends Record<string, unknown> = Record<string, never>> = PgDatabase<AwsDataApiPgQueryResultHKT, TSchema>;
export declare class AwsPgDialect extends PgDialect {
    static readonly [entityKind]: string;
    escapeParam(num: number): string;
}
export declare function drizzle<TSchema extends Record<string, unknown> = Record<string, never>>(client: AwsDataApiClient, config: DrizzleAwsDataApiPgConfig<TSchema>): AwsDataApiPgDatabase<TSchema>;
