import asyncio

import aiogram as io
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from settings import settings
from routers import admin, users



async def start_bot() -> None:
    """Запуск бота"""
    bot = io.Bot(settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # await set_commands(bot)

    storage = MemoryStorage()
    dispatcher = io.Dispatcher(storage=storage)

    dispatcher.include_routers(admin.router, users.router)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start_bot())
