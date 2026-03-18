from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import snowflake.connector
from snowflake.connector import SnowflakeConnection

from app.core.config import settings


@dataclass
class QueryResult:
    columns: List[str]
    rows: List[Dict[str, Any]]
    row_count: int


def _quote_ident(identifier: str) -> str:
    identifier = identifier.strip()
    if identifier.startswith('"') and identifier.endswith('"'):
        return identifier
    escaped = identifier.replace('"', '""')
    return f'"{escaped}"'


class SnowflakeClient:
    def __init__(self) -> None:
        self._connection: Optional[SnowflakeConnection] = None

    def connect(self) -> SnowflakeConnection:
        if self._connection is None:
            missing = []
            if not settings.snowflake_user:
                missing.append("SNOWFLAKE_USER")
            if not settings.snowflake_password:
                missing.append("SNOWFLAKE_PASSWORD")
            if not settings.snowflake_account:
                missing.append("SNOWFLAKE_ACCOUNT")

            if missing:
                raise RuntimeError(
                    f"Missing Snowflake settings: {', '.join(missing)}"
                )

            connect_kwargs = {
                "user": settings.snowflake_user,
                "password": settings.snowflake_password,
                "account": settings.snowflake_account,
            }

            if settings.snowflake_warehouse:
                connect_kwargs["warehouse"] = settings.snowflake_warehouse
            if settings.snowflake_database:
                connect_kwargs["database"] = settings.snowflake_database
            if settings.snowflake_schema:
                connect_kwargs["schema"] = settings.snowflake_schema
            if settings.snowflake_role:
                connect_kwargs["role"] = settings.snowflake_role

            self._connection = snowflake.connector.connect(**connect_kwargs)
            self._ensure_context()

        return self._connection

    def _ensure_context(self) -> None:
        if self._connection is None:
            return

        with self._connection.cursor() as cur:
            if settings.snowflake_role:
                cur.execute(f"USE ROLE {_quote_ident(settings.snowflake_role)}")

            if settings.snowflake_warehouse:
                cur.execute(f"USE WAREHOUSE {_quote_ident(settings.snowflake_warehouse)}")

            if settings.snowflake_database:
                cur.execute(f"USE DATABASE {_quote_ident(settings.snowflake_database)}")

            if settings.snowflake_schema:
                cur.execute(f"USE SCHEMA {_quote_ident(settings.snowflake_schema)}")

    def close(self) -> None:
        if self._connection is not None:
            try:
                self._connection.close()
            except Exception:
                pass
        self._connection = None

    def get_context(self) -> Dict[str, Any]:
        conn = self.connect()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    CURRENT_ACCOUNT(),
                    CURRENT_USER(),
                    CURRENT_ROLE(),
                    CURRENT_WAREHOUSE(),
                    CURRENT_DATABASE(),
                    CURRENT_SCHEMA()
                """
            )
            row = cur.fetchone()

        return {
            "current_account": row[0],
            "current_user": row[1],
            "current_role": row[2],
            "current_warehouse": row[3],
            "current_database": row[4],
            "current_schema": row[5],
        }

    def run_query(self, sql: str) -> QueryResult:
        conn = self.connect()

        try:
            self._ensure_context()

            with conn.cursor() as cur:
                cur.execute(sql)
                columns = [desc[0] for desc in cur.description] if cur.description else []
                raw_rows = cur.fetchall()
        except Exception as exc:
            try:
                context = self.get_context()
                raise RuntimeError(
                    f"Snowflake query failed: {exc}. "
                    f"Context: database={context['current_database']}, "
                    f"schema={context['current_schema']}, "
                    f"warehouse={context['current_warehouse']}, "
                    f"role={context['current_role']}. "
                    f"SQL: {sql}"
                ) from exc
            except Exception:
                raise RuntimeError(
                    f"Snowflake query failed: {exc}. SQL: {sql}"
                ) from exc

        rows = [dict(zip(columns, row)) for row in raw_rows]

        return QueryResult(
            columns=columns,
            rows=rows,
            row_count=len(rows),
        )

    def run_query_as_rows(self, sql: str) -> List[Dict[str, Any]]:
        return self.run_query(sql).rows

    def list_tables(self) -> List[Dict[str, Any]]:
        return self.run_query(
            """
            SELECT table_catalog, table_schema, table_name, table_type
            FROM information_schema.tables
            ORDER BY table_schema, table_name
            """
        ).rows

    def describe_table(self, table_name: str) -> List[Dict[str, Any]]:
        sql = f"DESCRIBE TABLE {_quote_ident(table_name)}"
        return self.run_query(sql).rows

    def preview_table(self, table_name: str, limit: int = 10) -> QueryResult:
        safe_limit = max(1, min(limit, 100))
        sql = f"SELECT * FROM {_quote_ident(table_name)} LIMIT {safe_limit}"
        return self.run_query(sql)


_client: Optional[SnowflakeClient] = None


def get_snowflake_client() -> SnowflakeClient:
    global _client
    if _client is None:
        _client = SnowflakeClient()
    return _client