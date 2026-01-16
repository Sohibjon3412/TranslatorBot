import logging
from aiogram import Bot, Dispatcher, executor, types
from langdetect import detect
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


UZ_RU = {
    "salom": ["Привет", "Здравствуйте", "Добрый день"],
    "rahmat": ["Спасибо", "Благодарю"],
}

RU_UZ = {
    "привет": ["Salom", "Assalomu alaykum"],
    "здравствуйте": ["Salom", "Assalomu alaykum"],
}


def is_single_word(text: str) -> bool:
    return len(text.strip().split()) == 1


@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer("Matn yuboring.")


@dp.message_handler()
async def translate(message: types.Message):
    text = message.text.strip()

    try:
        lang = detect(text)
    except:
        await message.answer("Tilni aniqlab bo‘lmadi.")
        return

    # --- O‘ZBEK → RUS ---
    if lang == "uz":
        key = text.lower()

        if is_single_word(text) and key in UZ_RU:
            await message.answer("\n".join(UZ_RU[key]))
        else:
            await message.answer("Bu matn rus tiliga tarjima qilinadi.")

    # --- RUS → O‘ZBEK ---
    elif lang == "ru":
        key = text.lower()

        if is_single_word(text) and key in RU_UZ:
            await message.answer("\n".join(RU_UZ[key]))
        else:
            await message.answer("Bu matn o‘zbek tiliga tarjima qilinadi.")

    else:
        await message.answer("Faqat o‘zbek yoki rus tilida yozing.")


if __name__ == "__main__":
    print("🔥 NEW BOT VERSION LOADED 🔥")
    executor.start_polling(dp, skip_updates=True)
