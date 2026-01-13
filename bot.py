import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command
from googletrans import Translator

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

translator = Translator()


@dp.message_handler(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Salom 👋\n"
        "Men avtomatik tarjimon botman.\n\n"
        "🇺🇿 Uzbek ↔ 🇷🇺 Russian\n"
        "Matn yuboring, men tarjima qilib beraman."
    )


@dp.message_handler(content_types=types.ContentType.TEXT)
async def translate_text(message: types.Message):
    text = message.text

    try:
        result = translator.translate(text)

        await message.answer(
            f"🔤 Asl matn:\n{text}\n\n"
            f"🌍 Tarjima ({result.dest}):\n{result.text}"
        )

    except Exception as e:
        await message.answer("❌ Tarjima vaqtida xatolik yuz berdi.")
        logging.error(e)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
