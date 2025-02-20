from openai import AsyncOpenAI, OpenAI
from decouple import config
import os

# load_dotenv('./.env')
# config = os.environ

client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=config("AI_KEY"),
)
# promt = 'Ты программист с огромным опытом программирования и готов поделиться опытом разработки на python, ты используешь фреймворки sqlalchemy, aiogram3, fastapi для разработки крутых продуктов. отвечай на как можно понятнее и кратко'
# promt = 'Ты самый умный бот в мире, который все знает со всего мира, отвечай на уровне студента колледжа'

async def ai_generate(text: str, model: str):
    completion = await client.chat.completions.create(
      model=model,
      messages=[
          # {
          #   "role": "system",
          #   "content": promt
          # },
          {
          "role": "user",
          "content": text
          }
      ]
      )
    print(completion)
    print(f"completion_tokens: {completion.usage.completion_tokens}\nprompt_tokens: {completion.usage.prompt_tokens}\ntotal_tokens:{completion.usage.total_tokens}")
    return(completion.choices[0].message.content)