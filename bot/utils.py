from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import TOKEN

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def send_photo_to_chat(chat_id: str, photo_file_id: str):
    await bot.send_photo(chat_id, photo_file_id)
    await bot.send_message(chat_id, 'Найди дефекты!')