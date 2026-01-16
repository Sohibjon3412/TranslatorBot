print("🔥 NEW BOT VERSION LOADED 🔥")
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


def is_single_word(text: str) -> bool:
    return len(text.strip().split()) == 1


def translate(text: str) -> str:
    src_lang = detect(text)
    single_word = is_single_word(text)

    if src_lang == "ru":
        target_lang = "o‘zbek"
        direction = "rus tilidan o‘zbek tiliga"
    else:
        target_lang = "rus"
        direction = "o‘zbek tilidan rus tiliga"

    if single_word:
        # 🔒 FAQAT TARJIMA VARIANTLARI (ASL TIL QAYTMASIN)
        prompt = f"""
Siz professional tarjimonsiz.

Quyidagi so‘zni {direction} tarjima qiling.

QOIDALAR:
- Faqat {target_lang} tilida yozing
- Asl tilidagi so‘zlarni QAYTARMANG
- 3–5 ta MA’NOLI TARJIMA variantini vergul bilan ajrating
- Sinonim emas, TARJIMA bo‘lsin
- Hech qanday izoh, belgi yoki tushuntirish yozmang

So‘z:
{text}
"""
    else:
        # 🔒 HAR DOIM ODDIY TARJIMA
        prompt = f"""
Siz professional tarjimonsiz.

Quyidagi matnni {direction} MA’NOLI qilib tarjima qiling.

QOIDALAR:
- Faqat {target_lang} tilida yozing
- So‘zma-so‘z emas, mazmunan tarjima qiling
- Asl tilidagi iboralarni qoldirmang
- Hech qanday izoh yoki qo‘shimcha yozmang

Matn:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a strict professional translator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def text_handler(message: types.Message):
    try:
        result = translate(message.text)
        await message.reply(result)
    except Exception as e:
        logging.error(e)
        await message.reply("Xatolik yuz berdi.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
