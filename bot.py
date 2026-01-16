import logging
import os
import re
from aiogram import Bot, Dispatcher, executor, types
from googletrans import Translator

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
translator = Translator()


def is_cyrillic(text: str) -> bool:
    return bool(re.search(r"[А-Яа-я]", text))


def is_single_word(text: str) -> bool:
    return len(text.strip().split()) == 1


@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer("Matn yuboring.")


@dp.message_handler()
async def translate(message: types.Message):
    text = message.text.strip()

    try:
        # 🇷🇺 RUS → 🇺🇿
        if is_cyrillic(text):
            if is_single_word(text):
                result = translator.translate(text, src="ru", dest="uz")
                variants = result.extra_data.get("all-translations")

                if variants:
                    translations = {t[0] for group in variants for t in group[1]}
                    await message.answer("\n".join(list(translations)[:5]))
                else:
                    await message.answer(result.text)
            else:
                await message.answer(
                    translator.translate(text, src="ru", dest="uz").text
                )

        # 🇺🇿 O‘ZBEK → 🇷🇺
        else:
            if is_single_word(text):
                result = translator.translate(text, src="uz", dest="ru")
                variants = result.extra_data.get("all-translations")

                if variants:
                    translations = {t[0] for group in variants for t in group[1]}
                    await message.answer("\n".join(list(translations)[:5]))
                else:
                    await message.answer(result.text)
            else:
                await message.answer(
                    translator.translate(text, src="uz", dest="ru").text
                )

    except Exception as e:
        logging.error(e)
        await message.answer("Xatolik yuz berdi.")


if __name__ == "__main__":
    print("✅ Translator bot started (FINAL VERSION)")
    executor.start_polling(dp, skip_updates=True)
