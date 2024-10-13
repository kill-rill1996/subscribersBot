from datetime import datetime
import pytz

from aiogram import Router, types
from aiogram.filters import Command
import messages as ms
from database.models import UserCreate, OperationCreate
from middleware import CheckPrivateMessageMiddleware
from database import service as db


router = Router()
router.message.middleware.register(CheckPrivateMessageMiddleware())


@router.message(Command("start"))
async def start_message(message: types.Message) -> None:
    user_model = UserCreate(
        tg_id=str(message.from_user.id),
        username=message.from_user.username,
        firstname=message.from_user.first_name,
        lastname=message.from_user.last_name
    )
    user = db.create_user(user_model)

    operation_model = OperationCreate(
        created_at=datetime.now(pytz.timezone('Europe/Moscow')),
        amount=300,
        user_id=user.id
    )
    operation = db.create_operation(operation_model)
    operation = db.create_operation(operation_model)
    await message.answer(f"Operation {operation.id} {operation.amount} {operation.created_at} {operation.user_id} created")


@router.message(Command("delete"))
async def delete_handler(message: types.Message) -> None:
    """Help message"""
    db.delete_user(message.from_user.id)
    await message.answer("User deleted")


@router.message(Command("help"))
async def help_handler(message: types.Message) -> None:
    """Help message"""
    msg = ms.get_help_message()
    await message.answer(msg)