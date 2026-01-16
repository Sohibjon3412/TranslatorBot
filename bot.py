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
    # Faqat bitta so‘z bo‘lsa TRUE
    words = text.strip().split()
    return len(words) == 1


def translate_text(text: str) -> str:
    lang = detect(text)
    single_word = is_single_word(text)

    if lang == "ru":
        target_lang = "o‘zbek"
        direction = "rus tilidan o‘zbek tiliga"
    else:
        target_lang = "rus"
        direction = "o‘zbek tilidan rus tiliga"

    if single_word:
        # FAQAT 1 TA SO‘Z BO‘LSA — TARJIMA VARIANTLARI
        prompt = f"""
Siz professional tarjimonsiz.

Quyidagi so‘zni {direction} tarjima qiling.

QOIDALAR:
- Faqat {target_lang} tilida yozing
- Asl tilidagi so‘zni qaytarmang
- 3–5 ta MA’NOLI tarjima variantini vergul bilan ajrating
- Sinonim emas, TARJIMA variantlari bo‘lsin
- Hech qanday izoh yoki qo‘shimcha yozmang

So‘z:
{text}
"""
    else:
        # 2 TA VA UNDAN KO‘P SO‘Z — HAR DOIM TARJIMA
        prompt = f"""
Siz professional tarjimonsiz.

Quyidagi matnni {direction} MA’NOLI qilib tarjima qiling.

QOIDALAR:
- Faqat {target_lang} tilida yozing
- So‘zma-so‘z emas, mazmunan tarjima qiling
- Asl matndan hech qanday so‘z qoldirmang
- Hech qanday izoh, sarlavha yoki belgi qo‘shmang

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
