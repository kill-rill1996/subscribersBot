import datetime

import aiogram
import requests
from aiogram import Router, types
from aiogram.filters import Command

from settings import settings

router = Router()


@router.message(Command("start"))
async def start_message(message: types.Message) -> None:
    await message.reply("Privet")


@router.message(Command("block_user"))
async def block_user_in_channel(message: types.Message) -> None:
    params = {
        "chat_id": settings.channel_id,
        "user_id": 714371204,
        "revoke_messages": False,
    }
    res = requests.post(f"https://api.telegram.org/bot{settings.bot_token}/banChatMember", data=params)
    print(res)
    print(res.text)

    res = requests.post(f"https://api.telegram.org/bot{settings.bot_token}/unbanChatMember", data=params)
    print(res)
    print(res.text)
    await message.answer("Пользователь забанен")


@router.message(Command("get_invite_link"))
async def get_invite_link(message: types.Message, bot: aiogram.Bot) -> None:
    expire_date = datetime.datetime.now() + datetime.timedelta(seconds=120)
    invite_link = await bot.create_chat_invite_link(chat_id=settings.channel_id,
                                      name="Username1",
                                      expire_date=int(expire_date.timestamp()),
                                      member_limit=1)
    await message.answer(f"{invite_link}")


@router.message(Command("delete_link"))
async def delete_link(message: types.Message, bot: aiogram.Bot) -> None:
    await bot.revoke_chat_invite_link(settings.channel_id, 'https://t.me/+JEfhPfCUIB0wZThi')
    await message.answer("Ссылка 'https://t.me/+JEfhPfCUIB0wZThi' удалена")
