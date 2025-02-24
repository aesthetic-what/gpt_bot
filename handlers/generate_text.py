from openai import AsyncOpenAI, OpenAI
from openai import BadRequestError, AuthenticationError, APIStatusError, RateLimitError
from decouple import config
import logging

logger = logging.getLogger(__name__)

# load_dotenv('./.env')
# config = os.environ

client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=config("AI_KEY"),
)
# promt = 'Ты программист с огромным опытом программирования и готов поделиться опытом разработки на python, ты используешь фреймворки sqlalchemy, aiogram3, fastapi для разработки крутых продуктов. отвечай на как можно понятнее и кратко'
# promt = 'Ты самый умный бот в мире, который все знает со всего мира, отвечай на уровне студента колледжа'
promt = 'Ты программист с огромным опытом программирования и готов поделиться опытом разработки на python, отвечай на вопрос кратко, но так чтобы ответ на вопрос был полным. Если нужно писать код, то пиши больше код и краткое пояснение'
 
async def ai_generate(text: str, model: str):
  try:
      completion = await client.chat.completions.create(
        model=model,
        messages=[
            {
              "role": "system",
              "content": promt
            },
            {"role": "assistant", 
             "content": "Сегодня понедельник."
            },
            {
            "role": "user",
            "content": text
            }
        ],
        max_tokens=1500
        )
      # print(completion)
      # print(f"completion_tokens: {completion.usage.completion_tokens}\nprompt_tokens: {completion.usage.prompt_tokens}\ntotal_tokens:{completion.usage.total_tokens}")
      # logger.info(f"completion_tokens: {completion.usage.completion_tokens}")
      # logger.info(f"prompt_tokens: {completion.usage.prompt_tokens}")
      # logger.info(f"total_tokens:{completion.usage.total_tokens}")
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
  