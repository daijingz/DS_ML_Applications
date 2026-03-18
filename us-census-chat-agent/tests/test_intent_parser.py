from app.llm.intent_parser import generate_sql


def test_generate_sql_mock():
    question = "What is population of California?"
    sql = generate_sql(question)
    assert isinstance(sql, str)