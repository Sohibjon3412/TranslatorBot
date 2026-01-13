import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from langdetect import detect
from openai import OpenAI

# ================== SOZLAMALAR ==================
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

client = OpenAI(api_key=OPENAI_API_KEY)

# ================== /start ==================
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.reply("Matn yuboring.")

# ================== TARJIMA ==================
def translate_text(text: str) -> str:
    lang = detect(text)

    if lang == "ru":
        direction = "rus tilidan o‘zbek tiliga"
    else:
        direction = "o‘zbek tilidan rus tiliga"

    prompt = f"""
Siz professional tarjimonsiz.
Matnni {direction} tabiiy, insondek va ma'noli tarjima qiling.

Agar bitta so‘z bo‘lsa — 3–5 ta mos tarjima variantini vergul bilan ajrating.
Hech qanday izoh, sarlavha yoki qo‘shimcha so‘z yozmang.

Matn:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional human translator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()

# ================== ODDIY MATN ==================
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def text_handler(message: types.Message):
    try:
        result = translate_text(message.text)
        await message.reply(result)
    except Exception as e:
        logging.error(e)
        await message.reply("Xatolik yuz berdi, keyinroq urinib ko‘ring.")

# ================== START ==================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
