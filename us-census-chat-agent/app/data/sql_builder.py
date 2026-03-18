from dataclasses import dataclass
from typing import List, Optional

from app.data.metric_catalog import get_metric
from app.llm.intent_parser import ParsedIntent


@dataclass
class BuiltSQL:
    sql: str
    table: Optional[str]
    metric_key: Optional[str]
    value_column: Optional[str]
    applied_filters: List[str]
    notes: List[str]


def _quote_ident(identifier: str) -> str:
    identifier = identifier.strip()
    if identifier.startswith('"') and identifier.endswith('"'):
        return identifier
    escaped = identifier.replace('"', '""')
    return f'"{escaped}"'


def _pick_value_column(metric_key: Optional[str]) -> Optional[str]:
    metric = get_metric(metric_key) if metric_key else None
    if not metric:
        return None

    if metric.default_value_column:
        return metric.default_value_column

    if metric.columns:
        return next(iter(metric.columns.keys()))

    return None


def _should_use_sum_by_default(metric_key: Optional[str]) -> bool:
    """
    Broad census metrics like population, housing units, households, etc.
    usually make more sense as totals than raw sampled rows.
    """
    if not metric_key:
        return False

    sum_like_metrics = {
        "population",
        "total_population",
        "housing_units",
        "households",
        "male_population",
        "female_population",
    }
    return metric_key in sum_like_metrics


def build_sql(intent: ParsedIntent) -> BuiltSQL:
    if not intent.metric_key or not intent.table:
        return BuiltSQL(
            sql="",
            table=None,
            metric_key=None,
            value_column=None,
            applied_filters=[],
            notes=["No metric/table could be inferred from the question."],
        )

    metric = get_metric(intent.metric_key)
    if metric is None:
        return BuiltSQL(
            sql="",
            table=None,
            metric_key=intent.metric_key,
            value_column=None,
            applied_filters=[],
            notes=[f"Metric '{intent.metric_key}' was not found in metric_catalog."],
        )

    value_column = _pick_value_column(intent.metric_key)
    if value_column is None:
        return BuiltSQL(
            sql="",
            table=metric.table,
            metric_key=metric.key,
            value_column=None,
            applied_filters=[],
            notes=[
                f"No default value column is configured for metric '{metric.key}'.",
                "Fill in default_value_column or columns in metric_catalog.py for this metric.",
            ],
        )

    notes: List[str] = []
    applied_filters: List[str] = []
    where_clauses: List[str] = []

    if intent.geography:
        applied_filters.append(f"geography_requested={intent.geography}")
        notes.append(
            "Geography was requested, but no geography-name join/filter is configured yet, so no geography filter was applied."
        )

    if intent.year is not None:
        applied_filters.append(f"year_requested={intent.year}")
        if metric.year_column:
            where_clauses.append(f"{_quote_ident(metric.year_column)} = {int(intent.year)}")
            notes.append("Applied year filter.")
        else:
            notes.append(
                "A year was requested, but no year column is configured for this metric, so no year filter was applied."
            )

    quoted_table = _quote_ident(metric.table)
    quoted_value_column = _quote_ident(value_column)

    aggregation = (intent.aggregation or "").lower().strip()

    # Better default behavior:
    # - explicit sum => SUM
    # - explicit avg => AVG
    # - explicit percent => percent calculation
    # - otherwise, use SUM for total-like metrics
    # - only use raw preview if you truly want sample rows
    if aggregation == "sum":
        select_expr = f"SUM({quoted_value_column}) AS value"
        notes.append("Using SUM aggregation.")
        limit_clause = ""

    elif aggregation == "avg":
        select_expr = f"AVG({quoted_value_column}) AS value"
        notes.append("Using AVG aggregation.")
        limit_clause = ""

    elif aggregation == "percent":
        denominator_col = metric.default_value_column or value_column
        quoted_denominator = _quote_ident(denominator_col)
        select_expr = (
            f"CASE WHEN SUM({quoted_denominator}) = 0 THEN NULL "
            f"ELSE 100.0 * SUM({quoted_value_column}) / SUM({quoted_denominator}) END AS value"
        )
        notes.append("Using percent-style aggregation.")
        limit_clause = ""

    elif _should_use_sum_by_default(metric.key):
        select_expr = f"SUM({quoted_value_column}) AS value"
        notes.append("No explicit aggregation requested; using SUM by default for this metric.")
        limit_clause = ""

    else:
        select_expr = f"{quoted_value_column} AS value"
        notes.append("No explicit aggregation requested; returning raw sample rows.")
        limit_clause = "LIMIT 50"

    sql_parts = [
        "SELECT",
        f"  {select_expr}",
        f"FROM {quoted_table}",
    ]

    if where_clauses:
        sql_parts.append("WHERE " + " AND ".join(where_clauses))

    if limit_clause:
        sql_parts.append(limit_clause)

    sql = "\n".join(sql_parts)

    return BuiltSQL(
        sql=sql,
        table=metric.table,
        metric_key=metric.key,
        value_column=value_column,
        applied_filters=applied_filters,
        notes=notes,
    )