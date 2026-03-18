from app.data.sql_builder import build_basic_query


def test_build_query():
    sql = build_basic_query("population", "California")
    assert "population" in sql
    assert "California" in sql
    assert "LIMIT 50" in sql