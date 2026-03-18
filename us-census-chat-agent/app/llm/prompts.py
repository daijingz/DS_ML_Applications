from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.data.metric_catalog import MetricDefinition


def build_intent_selection_prompt(
    question: str,
    metric_summaries: List[MetricDefinition],
) -> str:
    catalog_text = "\n".join(
        [
            f"- key={metric.key}, table={metric.table}, label={metric.label}, "
            f"description={metric.description}, keywords={', '.join(metric.keywords)}"
            for metric in metric_summaries
        ]
    )

    return f"""
You are helping route a user question to the correct US Census table.

Available metrics:
{catalog_text}

User question:
{question}

Your job:
1. Choose the best metric key.
2. Explain briefly why it matches.
3. Mention the best Snowflake table for it.

Return a concise JSON object with:
- metric_key
- table
- reason
""".strip()


def build_sql_generation_prompt(
    question: str,
    metric: MetricDefinition,
    geography: Optional[str] = None,
    year: Optional[int] = None,
    aggregation: Optional[str] = None,
) -> str:
    column_text = "\n".join(
        [f"- {col}: {desc}" for col, desc in metric.columns.items()]
    ) or "- No detailed columns are registered yet."

    return f"""
You are a careful SQL assistant for a Snowflake-hosted US Census dataset.

Selected metric:
- key: {metric.key}
- table: {metric.table}
- label: {metric.label}
- description: {metric.description}

Known columns:
{column_text}

User question:
{question}

Parsed constraints:
- geography: {geography}
- year: {year}
- aggregation: {aggregation}

Rules:
1. Use only the selected table unless there is a very strong reason not to.
2. Prefer known columns from the catalog.
3. Keep the SQL simple and readable.
4. If the request is ambiguous, prefer the metric's default value column.
5. Do not invent columns not supported by the schema.

Return only SQL.
""".strip()


def build_answer_generation_prompt(
    question: str,
    metric: Optional[MetricDefinition],
    sql: str,
    rows: List[Dict[str, Any]],
    notes: Optional[List[str]] = None,
) -> str:
    metric_block = (
        f"""
Metric context:
- key: {metric.key}
- table: {metric.table}
- label: {metric.label}
- description: {metric.description}
"""
        if metric is not None
        else "Metric context:\n- unavailable"
    )

    notes_block = "\n".join(f"- {note}" for note in (notes or [])) or "- none"

    preview_rows = rows[:5]
    preview_text = "\n".join(str(row) for row in preview_rows) if preview_rows else "[]"

    return f"""
You are generating a final answer for a US Census chat agent.

User question:
{question}

{metric_block}

Executed SQL:
{sql}

Query notes:
{notes_block}

Preview of returned rows:
{preview_text}

Instructions:
1. Answer using only the SQL result and the metric context.
2. Be direct and factual.
3. If multiple rows are returned, summarize the most relevant pattern briefly.
4. If no rows are returned, say that clearly.
5. Do not claim certainty beyond the returned data.
6. Do not mention internal implementation details unless helpful.

Write a short answer for the user.
""".strip()