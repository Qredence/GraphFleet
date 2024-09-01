import { entityKind } from "../../entity.cjs";
import type { Logger } from "../../logger.cjs";
import { PgDatabase } from "../../pg-core/db.cjs";
import { PgDialect } from "../../pg-core/dialect.cjs";
import type { DrizzleConfig } from "../../utils.cjs";
import type { AwsDataApiClient, AwsDataApiPgQueryResultHKT } from "./session.cjs";
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
