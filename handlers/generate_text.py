from openai import AsyncOpenAI, OpenAI
from openai import BadRequestError, AuthenticationError, APIStatusError, RateLimitError

from handlers.db.routers import take_info

import logging
import os

logger = logging.getLogger(__name__)

# load_dotenv('./.env')
# config = os.environ
# promt = 'Ты программист с огромным опытом программирования и готов поделиться опытом разработки на python, ты используешь фреймворки sqlalchemy, aiogram3, fastapi для разработки крутых продуктов. отвечай на как можно понятнее и кратко'
# promt = 'Ты самый умный бот в мире, который все знает со всего мира, отвечай на уровне студента колледжа'
promt = 'Ты программист с огромным опытом программирования и готов поделиться опытом разработки на python, отвечай на вопрос кратко, но так чтобы ответ на вопрос был полным. Если нужно писать код, то пиши больше код и краткое пояснение'
 
async def ai_generate(text: str, model: str, chat_id: int):

  client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("AI_KEY"),
  )
  try:
    memory = await take_info(chat_id)
    if memory is None:
      completion = await client.chat.completions.create(
        model=model,
        messages=[
            {
              "role": "system",
              "content": promt
            },
            # {"role": "assistant", 
            # "content": memory
            # },
            {
            "role": "user",
            "content": text
            }
        ],
        max_tokens=1500
        )
      
      
    completion = await client.chat.completions.create(
        model=model,
        messages=[
            {
              "role": "system",
              "content": memory
            },
            # {"role": "assistant", 
            # "content": memory
            # },
            {
            "role": "user",
            "content": text
            }
        ],
        max_tokens=1500
        )
    return(completion.choices[0].message.content, 
            completion.usage.completion_tokens, 
            completion.usage.prompt_tokens, 
            completion.usage.total_tokens)
    
  except BadRequestError as BE:
    logger.error(BE.message)
    return "Произошла ошибка на стороне бота, попробуйте попытку позже"
  except APIStatusError as AE:
    logger.error(AE.message)
    return "Произошла ошибка на стороне бота, попробуйте попытку позже"
  