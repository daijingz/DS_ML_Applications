from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class MetricDefinition:
    key: str
    table: str
    label: str
    description: str
    keywords: List[str] = field(default_factory=list)
    columns: Dict[str, str] = field(default_factory=dict)
    default_value_column: Optional[str] = None
    geography_column: Optional[str] = None
    year_column: Optional[str] = None


METRIC_CATALOG: Dict[str, MetricDefinition] = {
    "population": MetricDefinition(
        key="population",
        table='"2019_CBG_B01"',
        label="Population by age and sex",
        description="Detailed population counts broken down by sex and age group.",
        keywords=[
            "population", "people", "residents", "male", "female",
            "age", "ages", "senior", "elderly", "children"
        ],
        columns={
            '"B01001e1"': "total population",
            '"B01001e2"': "male population",
            '"B01001e26"': "female population",
        },
        default_value_column='"B01001e1"',
        geography_column='"CENSUS_BLOCK_GROUP"',
        year_column=None,
    ),
    "race": MetricDefinition(
        key="race",
        table='"2019_CBG_B02"',
        label="Race",
        description="Population counts by race categories.",
        keywords=[
            "race", "racial", "white", "black", "asian",
            "native", "hawaiian", "other race"
        ],
        columns={},
        default_value_column=None,
        geography_column='"CENSUS_BLOCK_GROUP"',
        year_column=None,
    ),
    "ethnicity": MetricDefinition(
        key="ethnicity",
        table='"2019_CBG_B03"',
        label="Hispanic or Latino origin",
        description="Population counts by Hispanic or Latino origin.",
        keywords=[
            "hispanic", "latino", "ethnicity", "origin"
        ],
        columns={},
        default_value_column=None,
        geography_column='"CENSUS_BLOCK_GROUP"',
        year_column=None,
    ),
    "education": MetricDefinition(
        key="education",
        table='"2019_CBG_B15"',
        label="Educational attainment",
        description="Educational attainment for the population.",
        keywords=[
            "education", "school", "college", "degree",
            "bachelor", "graduate", "high school"
        ],
        columns={},
        default_value_column=None,
        geography_column='"CENSUS_BLOCK_GROUP"',
        year_column=None,
    ),
    "income": MetricDefinition(
        key="income",
        table='"2019_CBG_B19"',
        label="Household income",
        description="Income-related household measures including median household income.",
        keywords=[
            "income", "earnings", "salary", "median income",
            "household income", "money"
        ],
        columns={},
        default_value_column=None,
        geography_column='"CENSUS_BLOCK_GROUP"',
        year_column=None,
    ),
    "housing": MetricDefinition(
        key="housing",
        table='"2019_CBG_B25"',
        label="Housing and occupancy",
        description="Housing unit and occupancy characteristics.",
        keywords=[
            "housing", "home", "house", "rent", "owner",
            "occupied", "vacant", "occupancy"
        ],
        columns={},
        default_value_column=None,
        geography_column='"CENSUS_BLOCK_GROUP"',
        year_column=None,
    ),
}


def get_metric(metric_key: str) -> Optional[MetricDefinition]:
    return METRIC_CATALOG.get(metric_key)


def list_metrics() -> List[MetricDefinition]:
    return list(METRIC_CATALOG.values())


def find_metric_by_keyword(question: str) -> Optional[MetricDefinition]:
    q = question.lower()

    best_metric = None
    best_score = 0

    for metric in METRIC_CATALOG.values():
        score = sum(1 for kw in metric.keywords if kw in q)
        if score > best_score:
            best_score = score
            best_metric = metric

    return best_metric


def get_table_for_metric(metric_key: str) -> Optional[str]:
    metric = get_metric(metric_key)
    return metric.table if metric else None