
from database import service as db


def is_user_exists(user_tg_id: str) -> bool:
    """Проверяет есть ли уже такой user в базе данных"""
    user = db.get_user_by_tg_id(user_tg_id)
    if user:
        return True
    return False

