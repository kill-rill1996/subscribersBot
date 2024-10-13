from datetime import datetime
import pytz
from aiogram import Router, types, Bot, F
from aiogram.filters import Command
import messages as ms
from middleware import CheckPrivateMessageMiddleware
from database import service as db

from database.models import UserCreate, OperationCreate
from .utils import is_user_exists
from routers import keyboards as kb
from .payments import create_payment_invoice


router = Router()
router.message.middleware.register(CheckPrivateMessageMiddleware())


@router.message(Command("start"))
async def start_message(message: types.Message) -> None:
    """Команда /start"""
    if is_user_exists(str(message.from_user.id)):
        await message.answer("Hello message")
        await message.answer("Вы можете приобрести подписку на канал",
                             reply_markup=kb.buy_subscribe_keyboard().as_markup())
        return

    user_model = UserCreate(
        tg_id=str(message.from_user.id),
        username=message.from_user.username,
        firstname=message.from_user.first_name,
        lastname=message.from_user.last_name
    )
    db.create_user(user_model)
    await message.answer("Hello message")
    await message.answer("Вы можете приобрести подписку на канал",
                         reply_markup=kb.buy_subscribe_keyboard().as_markup())


@router.callback_query(lambda callback: callback.data == "buy_sub")
async def buy_menu(callback: types.CallbackQuery) -> None:
    """Меню выбора периода подписки"""
    await callback.message.edit_text("Выберите период подписки📆", reply_markup=kb.payment_period_subscribe().as_markup())


@router.callback_query(lambda callback: callback.data.split('_')[0] == "subPeriod")
async def create_invoice_handler(callback: types.CallbackQuery) -> None:
    """Формирование заказа для оплаты"""
    sub_period = callback.data.split("_")[1]
    payment_invoice = create_payment_invoice(sub_period)

    await callback.message.answer_invoice(**payment_invoice)
    await callback.message.delete()


@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: types.Message):
    await message.answer("Оплата прошла успешно")
    await message.delete()



# @router.message(Command("start"))
# async def start_message(message: types.Message) -> None:
#     user_model = UserCreate(
#         tg_id=str(message.from_user.id),
#         username=message.from_user.username,
#         firstname=message.from_user.first_name,
#         lastname=message.from_user.last_name
#     )
#     user = db.create_user(user_model)
#
#     operation_model = OperationCreate(
#         created_at=datetime.now(pytz.timezone('Europe/Moscow')),
#         amount=300,
#         user_id=user.id
#     )
#     operation = db.create_operation(operation_model)
#     operation = db.create_operation(operation_model)
#     await message.answer(f"Operation {operation.id} {operation.amount} {operation.created_at} {operation.user_id} created")


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