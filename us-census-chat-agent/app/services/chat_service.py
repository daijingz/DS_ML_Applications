from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List

from app.data.snowflake_client import get_snowflake_client
from app.data.sql_builder import build_sql
from app.llm.intent_parser import parse_intent, rank_candidate_metrics


class ChatService:
    def __init__(self) -> None:
        self.client = get_snowflake_client()

    def handle_message(self, message: str, session_id: str | None = None) -> Dict[str, Any]:
        intent = parse_intent(message)
        built = build_sql(intent)

        if not intent.metric_key or not intent.table:
            candidates = rank_candidate_metrics(message)
            return {
                "answer": (
                    "I could not confidently determine which census topic you want. "
                    "Try asking about population, race, ethnicity, income, education, or housing."
                ),
                "intent": asdict(intent),
                "sql": "",
                "rows": [],
                "columns": [],
                "notes": [
                    "No metric/table could be inferred from the question."
                ],
                "candidate_metrics": [metric.key for metric in candidates[:5]],
                "session_id": session_id,
            }

        if not built.sql:
            return {
                "answer": (
                    f"I identified the topic as '{intent.metric_key}', but I could not build a valid SQL query yet."
                ),
                "intent": asdict(intent),
                "sql": "",
                "rows": [],
                "columns": [],
                "notes": built.notes,
                "candidate_metrics": [],
                "session_id": session_id,
            }

        try:
            result = self.client.run_query(built.sql)
        except Exception as exc:
            error_text = str(exc)
            return {
                "answer": f"Snowflake query failed: {error_text}",
                "intent": asdict(intent),
                "sql": built.sql,
                "rows": [],
                "columns": [],
                "notes": built.notes + [error_text],
                "candidate_metrics": [],
                "session_id": session_id,
            }

        answer = self._format_answer(
            message=message,
            metric_key=intent.metric_key,
            table=intent.table,
            rows=result.rows,
            row_count=result.row_count,
        )

        return {
            "answer": answer,
            "intent": asdict(intent),
            "sql": built.sql,
            "rows": result.rows,
            "columns": result.columns,
            "notes": built.notes,
            "candidate_metrics": [],
            "session_id": session_id,
        }

    def _format_answer(
        self,
        message: str,
        metric_key: str,
        table: str,
        rows: List[Dict[str, Any]],
        row_count: int,
    ) -> str:
        if row_count == 0:
            return (
                f"I mapped your question to the '{metric_key}' topic in table '{table}', "
                "but the query returned no rows."
            )

        first_row = rows[0]

        if "value" in first_row:
            value = first_row["value"]

            if "NAME" in first_row:
                return (
                    f"I found {row_count} result rows for the '{metric_key}' topic from table '{table}'. "
                    f"The first result is {first_row['NAME']}: {value}."
                )

            return (
                f"I found {row_count} result rows for the '{metric_key}' topic from table '{table}'. "
                f"The first value is {value}."
            )

        preview_items = ", ".join(f"{k}={v}" for k, v in list(first_row.items())[:4])
        return (
            f"I found {row_count} result rows for the '{metric_key}' topic from table '{table}'. "
            f"The first row looks like: {preview_items}."
        )


_chat_service: ChatService | None = None


def get_chat_service() -> ChatService:
    global _chat_service
    if _chat_service is None:
        _chat_service = ChatService()
    return _chat_service