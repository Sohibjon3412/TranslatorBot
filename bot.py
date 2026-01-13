# ==== TELEGRAM_BOT_TOKEN = "8342487953:AAF-2vuHrkiA7020Dw78sxmX29rug__AzlQ" ====
import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Bot ishga tushdi 🚀")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
from openai import OpenAI

# ================== SOZLAMALAR ==================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = "8342487953:AAF-2vuHrkiA7020Dw78sxmX29rug__AzlQ"

client = OpenAI(api_key=OPENAI_API_KEY)
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# ================== PROMPT ==================
SYSTEM_PROMPT = (
    "Sen professional tarjimonsan. "
    "Foydalanuvchi yuborgan matn O'zbekcha bo'lsa → Rus tiliga tarjima qil. "
    "Foydalanuvchi yuborgan matn Ruscha bo'lsa → O'zbek tiliga tarjima qil. "
    "Tarjima tabiiy, insoncha bo'lsin, so'zma-so'z emas. "
    "RP va kundalik dialoglar uchun ham mos bo'lsin."
)

# ================== START ==================
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Salom!\n"
        "🇺🇿 O‘zbekcha → 🇷🇺 Ruscha\n"
        "🇷🇺 Ruscha → 🇺🇿 O‘zbekcha\n"
        "🧠 AI yordamida tabiiy tarjima qilinadi\n"
        "⚡ Agar bitta so‘z yuborsangiz — u bir nechta tarjima variantlarini beradi\n"
        "😊 Matn oxirida '))' bo‘lsa — biroz pozitiv kayfiyat qo‘shiladi"
    )

# ================== AI TARJIMA ==================
async def translate_ai(text: str):
    """GPT-4o-mini orqali aniq tilni aniqlab tarjima"""
    extra_prompt = ""
    if text.strip().endswith("))"):
        extra_prompt = " Shu matnni biroz pozitiv, iliq kayfiyat bilan tarjima qil, lekin ortiqcha kulgili yoki g‘alati bo‘lmasin."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text + extra_prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

# ================== MAIN TRANSLATE ==================
@dp.message()
async def translate(message: types.Message):
    text = message.text.strip()

    try:
        # Bir so'zli matnlar → bir nechta variant
        if len(text.split()) == 1:
            prompt = (
                f"Matn: {text}\n"
                "Shuni bir nechta tarjima variantlari bilan bera olasanmi? "
                "Har bir variantni alohida qator bilan yoz."
            )
            result = await translate_ai(prompt)
            await message.answer(f"📝 Tarjima variantlari:\n{result}")
            return

        # Barcha matnlar → AI orqali tarjima
        result = await translate_ai(text)
        await message.answer(result)

    except Exception as e:
        print("Error:", e)
        await message.answer("⚠️ Tarjima qilishda xatolik yuz berdi")

# ================== ISHGA TUSHIRISH ==================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
