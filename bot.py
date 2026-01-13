import os
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command
from langdetect import detect

from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

client = OpenAI(api_key=OPENAI_API_KEY)


@dp.message_handler(Command("start"))
async def start(message: types.Message):
    await message.answer("Matn yuboring.")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def translate(message: types.Message):
    text = message.text.strip()

    try:
        lang = detect(text)
    except:
        return

    # 🇷🇺 → 🇺🇿
    if lang == "ru":
        prompt = f"""
Sen professional tarjimonsan.
Agar bitta so‘z bo‘lsa — uning 3-5 ta eng mos, tabiiy o‘zbekcha variantlarini chiqar.
Agar gap bo‘lsa — uni chiroyli va odamga o‘xshab tarjima qil.
Hech qanday izoh yozma, faqat tarjimani yoz.

Matn: {text}
"""

    # 🇺🇿 → 🇷🇺
    elif lang == "uz":
        prompt = f"""
Ты профессиональный переводчик.
Если это одно слово — дай 3–5 наиболее естественных вариантов перевода.
Если это предложение — переведи его живо, по-человечески.
Без объяснений, только перевод.

Текст: {text}
"""

    else:
        return

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    result = response.choices[0].message.content.strip()
    await message.answer(result)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
