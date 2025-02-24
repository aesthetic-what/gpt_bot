import re

def split_text(text, max_length=4096):
    # Разделяем текст на предложения
    sentences = re.split(r'(?<=[.!?]) +', text)
    parts = []
    current_part = ""

    for sentence in sentences:
        if len(current_part) + len(sentence) <= max_length:
            current_part += sentence + " "
        else:
            parts.append(current_part.strip())
            current_part = sentence + " "

    if current_part:
        parts.append(current_part.strip())

    return parts

async def send_large_message(bot, chat_id, text):
    parts = split_text(text)
    for part in parts:
        await bot.send_message(chat_id, part)

