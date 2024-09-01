import { PgDatabase } from "../pg-core/db.cjs";
import type { DrizzleConfig } from "../utils.cjs";
import { type PgRemoteQueryResultHKT } from "./session.cjs";
export type PgRemoteDatabase<TSchema extends Record<string, unknown> = Record<string, never>> = PgDatabase<PgRemoteQueryResultHKT, TSchema>;
export type RemoteCallback = (sql: string, params: any[], method: 'all' | 'execute') => Promise<{
    rows: any[];
}>;
export declare function drizzle<TSchema extends Record<string, unknown> = Record<string, never>>(callback: RemoteCallback, config?: DrizzleConfig<TSchema>): PgRemoteDatabase<TSchema>;
