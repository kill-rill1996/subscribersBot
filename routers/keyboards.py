from typing import List

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import tables


def buy_subscribe_keyboard() -> InlineKeyboardBuilder:
    """Создание клавиатуры для выбора группы"""
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text="Купить подписку💰", callback_data="buy_sub"))
    return keyboard


def payment_period_subscribe() -> InlineKeyboardBuilder:
    """Клавиатура для выбора длительности покупаемой подписки"""

    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="1 мес", callback_data=f"subPeriod_1"),
        InlineKeyboardButton(
            text="2 мес", callback_data=f"subPeriod_2"),
        InlineKeyboardButton(
            text="3 мес", callback_data=f"subPeriod_3"),
    )
    # keyboard.row(
    #     InlineKeyboardButton(
    #         text="6 мес", callback_data=f"subPeriod_6"),
    #     InlineKeyboardButton(
    #         text="12 мес", callback_data=f"subPeriod_12"),
    # )

    return keyboard
