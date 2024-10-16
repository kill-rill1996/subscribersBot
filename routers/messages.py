from datetime import datetime

from database import tables


def get_help_message() -> str:
    """Help message"""
    message = "<b>Возможности бота:</b>\n" \
              "- Принимает оплату за подписку\n" \
              "- Осуществляет менеджмент приватных каналов/групп\n\n" \
              "<b>Инструкция использования:</b>\n" \
              "- Для начала работы отправьте команду /start и следуйте инструкциям\n" \
              "- Для перехода в главное меню отправьте команду /menu\n" \
              "- Для покупки или продления подписки в главном меню нажмите \"Купить 💸\"\n" \
              "- Для проверки своего статуса подписки в главном меню нажмите \"Статус 🎫\"\n\n" \
              "<b>Контакт поддержки:</b>\n" \
              "Если у вас есть вопросы или предложения, свяжитесь с нашей поддержкой в телеграм: @aleksandr_andreew"
    return message


def get_start_message() -> str:
    """Start message"""
    message = "Для управления подпиской на канал выберите команду /menu во вкладке \"Меню\" или нажмите на команду прямо в сообщении\n\n"
    "Для просмотра инструкции и обращения в поддержку выберите команду /help"
    return message


def subscription_info(user: tables.User) -> str:
    if not user.subscription:
        return "У вас пока нет подписки, вы можете приобрести ее в главном меню по кнопке \"Купить 💸\""

    message = ""
    expire_date = datetime.strftime(user.subscription[0].expire_date, '%d.%m.%Y')

    if user.subscription[0].is_active:
        message += f"🟢 Ваша подписка <b>Активна</b> до <b>{expire_date}</b>"
    else:
        message += f"🔴 Срок действия вашей подписки истек <b>{expire_date}</b>\n" \
                   f"Вы можете приобрести подписку в главном меню /start"

    return message
