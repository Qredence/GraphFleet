import psycopg2
from psycopg2.extras import Json
from ..storage import StorageBackend
from typing import Dict, Any, List


class PostgresStorage(StorageBackend):
    def __init__(self, host, port, user, password, dbname):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname
        )
        self.create_tables()

    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    content JSONB NOT NULL
                );
                CREATE TABLE IF NOT EXISTS parquet_files (
                    filename TEXT PRIMARY KEY,
                    data BYTEA NOT NULL
                );
            """)
        self.conn.commit()

    def store_document(self, document: Dict[str, Any]) -> str:
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO documents (content) VALUES (%s) RETURNING id",
                (Json(document),)
            )
            doc_id = cur.fetchone()[0]
        self.conn.commit()
        return str(doc_id)

    def get_document(self, doc_id: str) -> Dict[str, Any]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT content FROM documents WHERE id = %s", (int(doc_id),))
            result = cur.fetchone()
        return result[0] if result else None

    def search_documents(self, query: str, limit: int, offset: int) -> List[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT content FROM documents WHERE content::text ILIKE %s LIMIT %s OFFSET %s",
                (f"%{query}%", limit, offset)
            )
            results = cur.fetchall()
        return [row[0] for row in results]

    def store_parquet(self, parquet_data: bytes, filename: str) -> str:
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO parquet_files (filename, data) VALUES (%s, %s) ON CONFLICT (filename) DO UPDATE SET data = EXCLUDED.data",
                (filename, psycopg2.Binary(parquet_data))
            )
        self.conn.commit()
        return filename

    def get_parquet(self, filename: str) -> bytes:
        with self.conn.cursor() as cur:
            cur.execute("SELECT data FROM parquet_files WHERE filename = %s", (filename,))
            result = cur.fetchone()
        return result[0] if result else None