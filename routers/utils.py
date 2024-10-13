from datetime import datetime, timedelta
import pytz
import aiogram

from database import service as db
from settings import settings


def is_user_exists(user_tg_id: str) -> bool:
    """Проверяет есть ли уже такой user в базе данных"""
    user = db.get_user_by_tg_id(user_tg_id)
    if user:
        return True
    return False


async def generate_invite_link(bot: aiogram.Bot, name: str) -> str:
    """Создание ссылки для подписки на группу"""
    # время окончание действия ссылки на вступление
    expire_date = datetime.now(tz=pytz.timezone('Europe/Moscow')) + timedelta(days=1)

    invite_link = await bot.create_chat_invite_link(chat_id=settings.channel_id,
                                                    name=name,
                                                    expire_date=int(expire_date.timestamp()),
                                                    member_limit=1)
    return invite_link.invite_link

