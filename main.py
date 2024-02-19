import logging
import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config.tlg_bot_config import TOKEN
from config.database_config import init_db
from src.monitoring.parsers.mega_market_filter import for_personal
from src.notifications.handlers import router


def main():
    # init_db()
    # start_monitoring()
    # for_personal()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start_bot())


async def start_bot():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    # удаляет все обновления, которые пришли когда бот не работал
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    main()


# TODO тесты
# TODO удаление оповещений
# TODO учитывать/не учитывать бонусы, карты
# TODO ограничение по загрузке страниц !!!!
# TODO каскадное удаление
# TODO обработка ошибок (страницы нет, товара нет)
# TODO ТЕСТОВАЯ БД!!!
# TODO тесты входных данных
