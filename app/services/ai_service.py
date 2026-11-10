
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)


def get_ai_response(question: str) -> str:
    response = client.chat.completions.create(
        model="qwen3:1.7b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a friendly AI assistant for an online store. "
                    "Always respond in Serbian. "
                    "Use clear, concise, and helpful language. "
                    "Help customers find and choose products."
                ),
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    return response.choices[0].message.content
