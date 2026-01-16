import os
import logging
import requests
import re
from aiogram import Bot, Dispatcher, executor, types

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


def is_cyrillic(text: str) -> bool:
    return bool(re.search(r"[А-Яа-я]", text))


def is_single_word(text: str) -> bool:
    return len(text.strip().split()) == 1


def ai_translate(text: str) -> str:
    system_prompt = """
You are a professional human translator.

Rules:
- If the input is Russian, translate it to Uzbek.
- If the input is Uzbek, translate it to Russian.
- Translate naturally, like a real human, not word-by-word.
- Do NOT repeat the original text.
- Do NOT explain anything.
- Do NOT add labels or extra words.
- If the input is ONE WORD, return several natural translation variants separated by commas.
- If the input is a sentence or longer, return ONE smooth translation.
"""

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            "temperature": 0.7,
        },
        timeout=30,
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer("Matn yuboring.")


@dp.message_handler()
async def translate_handler(message: types.Message):
    text = message.text.strip()

    try:
        result = ai_translate(text)
        await message.answer(result)
    except Exception as e:
        logging.error(e)
        await message.answer("Xatolik yuz berdi.")


if __name__ == "__main__":
    print("✅ AI Translator bot started (FINAL, HUMAN-LIKE)")
    executor.start_polling(dp, skip_updates=True)
