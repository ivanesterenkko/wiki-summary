import openai

from configs.config import openai_settings


async def gpt_summarize(content: str) -> str:
    client = openai.OpenAI(
        api_key=openai_settings.OPENAI_SECRET_KEY,
        base_url=openai_settings.OPENAI_URL,
    )
    response = client.chat.completions.create(
        model="gpt-4.1",
        store=True,
        messages=[
            {
                "role": "system",
                "content": "Сделай понятное summary для статьи Википедии на русском языке.",
            },
            {"role": "user", "content": content},
        ],
    )
    return response.choices[0].message.content
