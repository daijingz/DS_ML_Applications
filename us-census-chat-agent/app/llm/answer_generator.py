import json
from openai import OpenAI
from app.core.config import settings
from app.llm.prompts import ANSWER_SYSTEM_PROMPT

client = OpenAI(api_key=settings.openai_api_key)


def generate_answer(question: str, sql: str, rows: list[dict]) -> str:
    response = client.responses.create(
        model=settings.openai_model,
        input=[
            {"role": "system", "content": ANSWER_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": json.dumps(
                    {"question": question, "sql": sql, "rows": rows},
                    default=str,
                ),
            },
        ],
    )
    return response.output_text.strip()