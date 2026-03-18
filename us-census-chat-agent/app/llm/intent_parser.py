from dataclasses import dataclass
from typing import List, Optional

from app.data.metric_catalog import MetricDefinition, find_metric_by_keyword, list_metrics


@dataclass
class ParsedIntent:
    raw_question: str
    metric_key: Optional[str]
    table: Optional[str]
    geography: Optional[str]
    year: Optional[int]
    aggregation: str
    matched_keywords: List[str]
    confidence: float


def _extract_year(question: str) -> Optional[int]:
    import re

    match = re.search(r"\b(20\d{2}|19\d{2})\b", question)
    if match:
        return int(match.group(1))
    return None


def _extract_geography(question: str) -> Optional[str]:
    q = question.strip()

    geography_markers = [
        " in ",
        " for ",
        " at ",
        " within ",
        " across ",
    ]

    lowered = q.lower()
    for marker in geography_markers:
        idx = lowered.find(marker)
        if idx != -1:
            geo = q[idx + len(marker):].strip(" ?,.")
            if geo:
                return geo

    return None


def _infer_aggregation(question: str) -> str:
    q = question.lower()

    if any(phrase in q for phrase in ["average", "mean"]):
        return "avg"
    if any(phrase in q for phrase in ["sum", "total", "how many", "number of"]):
        return "sum"
    if any(phrase in q for phrase in ["percent", "percentage", "ratio", "share"]):
        return "percent"

    return "value"


def _matched_keywords(question: str, metric: MetricDefinition) -> List[str]:
    q = question.lower()
    return [kw for kw in metric.keywords if kw in q]


def _score_metric(question: str, metric: MetricDefinition) -> float:
    matches = _matched_keywords(question, metric)
    if not matches:
        return 0.0

    base = float(len(matches))

    q = question.lower()
    if metric.key in q:
        base += 1.5
    if metric.label.lower() in q:
        base += 1.0

    return base


def parse_intent(question: str) -> ParsedIntent:
    metric = find_metric_by_keyword(question)

    if metric is None:
        return ParsedIntent(
            raw_question=question,
            metric_key=None,
            table=None,
            geography=_extract_geography(question),
            year=_extract_year(question),
            aggregation=_infer_aggregation(question),
            matched_keywords=[],
            confidence=0.0,
        )

    matched = _matched_keywords(question, metric)
    score = _score_metric(question, metric)

    confidence = min(1.0, 0.2 + 0.15 * len(matched) + 0.1 * (score > 2))

    return ParsedIntent(
        raw_question=question,
        metric_key=metric.key,
        table=metric.table,
        geography=_extract_geography(question),
        year=_extract_year(question),
        aggregation=_infer_aggregation(question),
        matched_keywords=matched,
        confidence=confidence,
    )


def rank_candidate_metrics(question: str) -> List[MetricDefinition]:
    scored = []
    for metric in list_metrics():
        score = _score_metric(question, metric)
        if score > 0:
            scored.append((score, metric))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [metric for _, metric in scored]