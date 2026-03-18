def validate_message(message: str) -> str:
    text = (message or "").strip()
    if not text:
        raise ValueError("Message cannot be empty")
    return text


def is_safe_sql(sql: str) -> bool:
    if not sql:
        return False
    blocked = ["insert", "update", "delete", "drop", "alter", "truncate", "create"]
    text = sql.lower()
    return not any(word in text for word in blocked)