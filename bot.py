import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from langdetect import detect
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

client = OpenAI(api_key=OPENAI_API_KEY)


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.reply("Matn yuboring.")


def translate_text(text: str) -> str:
    lang = detect(text)

    if lang == "ru":
        # RUS -> O‘ZBEK
        prompt = f"""
Siz professional tarjimonsiz.
Quyidagi ruscha matnni FAQAT o‘zbek tiliga tarjima qiling.

MUHIM QOIDALAR:
- Ruscha so‘zlarni QAYTA YOZMANG
- Faqat o‘zbekcha tarjimalarni yozing
- Agar bitta so‘z bo‘lsa — 3–5 ta O‘ZBEKCHA tarjima variantini pastki qatordan yozing
- Hech qanday izoh, sarlavha yoki qo‘shimcha yozmang

Matn:
{text}
"""
    else:
        # O‘ZBEK -> RUS
        prompt = f"""
Siz professional tarjimonsiz.
Quyidagi o‘zbekcha matnni FAQAT rus tiliga tarjima qiling.

MUHIM QOIDALAR:
- O‘zbekcha so‘zlarni QAYTA YOZMANG
- Faqat ruscha tarjimalarni yozing
- Agar bitta so‘z bo‘lsa — 3–5 ta RUSCHA tarjima variantini pastki qatordan yozing
- Hech qanday izoh, sarlavha yoki qo‘shimcha yozmang

Matn:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a strict professional translator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def text_handler(message: types.Message):
    try:
        result = translate_text(message.text)
        await message.reply(result)
    except Exception as e:
        logging.error(e)
        await message.reply("Xatolik yuz berdi.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
