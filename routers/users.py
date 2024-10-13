from aiogram import Router, types
from aiogram.filters import Command
import messages as ms
from middleware import CheckPrivateMessageMiddleware

router = Router()
router.message.middleware.register(CheckPrivateMessageMiddleware())


@router.message(Command("start"))
async def start_message(message: types.Message) -> None:
    await message.reply("Privet")


@router.message(Command("help"))
async def help_handler(message: types.Message) -> None:
    """Help message"""
    msg = ms.get_help_message()
    await message.answer(msg)