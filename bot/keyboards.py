from typing import List

from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_keyboard(buttons: List):
    keyboard = ReplyKeyboardBuilder()

    for item in buttons:
        keyboard.add(KeyboardButton(text=item))

    return keyboard.as_markup(resize_keyboard=True)


def get_callback_btns(btns: dict):
    keyboard = InlineKeyboardBuilder()

    for key, value in btns.items():
        keyboard.add(InlineKeyboardButton(text=key, callback_data=value))

    return keyboard.as_markup()
