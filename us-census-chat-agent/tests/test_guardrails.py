from app.core.guardrails import validate_message, is_safe_sql


def test_validate_message():
    assert validate_message("hello") == "hello"


def test_validate_message_empty():
    try:
        validate_message("")
        assert False
    except ValueError:
        assert True


def test_safe_sql():
    assert is_safe_sql("select * from table")


def test_unsafe_sql():
    assert not is_safe_sql("drop table users")