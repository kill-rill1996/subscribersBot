from datetime import datetime, timedelta

import pytz
from aiogram import Router, types, Bot, F
from aiogram.filters import Command
import messages as ms
from middleware import CheckPrivateMessageMiddleware
from database import service as db

from database.models import UserCreate, OperationCreate, SubscriptionCreate
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
    amount = int(message.successful_payment.invoice_payload)
    months = amount / 100

    # создание операции
    user = db.get_user_by_tg_id(str(message.from_user.id))
    operation_model = OperationCreate(
        created_at=datetime.now(pytz.timezone('Europe/Moscow')),
        amount=amount,
        user_id=user.id
    )
    db.create_operation(operation_model)

    # создание подписки
    expire_date = datetime.now(pytz.timezone('Europe/Moscow')) + timedelta(days=30*months)
    subscription_model = SubscriptionCreate(
        expire_date=expire_date,
        is_active=True,
        user_id=user.id
    )
    new_subscription = db.create_subscription(subscription_model)

    await message.answer(f"Оплата прошла успешно ✅\n\n"
                         f"Подписка оформлена до {datetime.strftime(new_subscription.expire_date, '%d.%m.%Y')} 🗓️")
    await message.delete()


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