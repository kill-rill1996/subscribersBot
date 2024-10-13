from aiogram.types import LabeledPrice

from settings import settings


def create_payment_invoice(sub_period: str) -> dict:
    label = sub_period
    description = f"Оплата подписки на {sub_period}"

    if sub_period in ["2", "3"]:
        label += " месяца"
        description += " месяца"
    elif sub_period in ["6", "12"]:
        label += " месяцев"
        description += " месяцев"
    else:
        label += " месяц"
        description += " месяц"

    payment_invoice = {"title": "Подписка на канал",
                       "description": description,
                       "payload": f"{int(sub_period) * 100}",
                       "currency": "RUB",
                       "provider_token": settings.payment_token,
                       "prices": [LabeledPrice(label=label, amount=int(sub_period)*100 * 100)]
                       }

    return payment_invoice