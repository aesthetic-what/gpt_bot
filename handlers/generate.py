from openai import AsyncOpenAI, OpenAI
from dotenv import load_dotenv
from decouple import config
import os

# load_dotenv('./.env')
# config = os.environ

client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=config("AI_KEY"),
)

async def ai_generate(text: str, model: str):
    completion = await client.chat.completions.create(
    model=model,
    messages=[
        {
        "role": "user",
        "content": text
        }
    ]
    )
    print(completion)
    return(completion.choices[0].message.content)