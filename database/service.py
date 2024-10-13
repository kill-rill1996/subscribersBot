from database import tables
from .database import Session
from .models import UserCreate, OperationCreate, User


# USER
def create_user(user_model: UserCreate) -> User:
    """Добавление пользователя"""
    with Session() as session:
        user = tables.User(**user_model.dict())
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_user_by_id(user_id: int) -> tables.User:
    """Получение юзера по id"""
    with Session() as session:
        user = session.query(tables.User) \
            .filter(tables.User.id == user_id) \
            .first()
        return user


def get_user_by_tg_id(tg_id: int) -> tables.User:
    """Получение юзера по tg_id"""
    with Session() as session:
        user = session.query(tables.User) \
            .filter(tables.User.tg_id == tg_id) \
            .first()
        return user


def delete_user(user_id: int) -> None:
    """Удаление юзера по id"""
    with Session() as session:
        user = get_user_by_tg_id(user_id)
        session.delete(user)
        session.commit()


# OPERATION
def create_operation(operation_model: OperationCreate) -> tables.Operation:
    """Добавление операции"""
    with Session() as session:
        operation = tables.Operation(**operation_model.dict())
        session.add(operation)
        session.commit()
        session.refresh(operation)
        return operation

