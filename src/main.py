import logging
import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config.tlg_bot_config import TOKEN
from config.database_config import init_db
# from db.crud_operations import UsersCRUD
# from src.monitoring.monitoring import start_monitoring, add_new_product
from src.monitoring.parsers.mega_market_filter import for_personal
from src.notifications.handlers import router


def main():
    init_db()
    # start_monitoring()

    # UsersCRUD.add_new_user(235531)
    # add_new_product('https://www.ozon.ru/product/nastolnaya-kartochnaya-igra-gvint-gwent-the-witcher-card-game-1152599194/?advert=MXpl-haP6KpRblK7ZAWajWKyBlFveQO7-cG0wHz7BP_EmJorfHGtNzE3ThEBT0SsFUoB7W96IpAgTrPonUhSjJuKw-cYZL5dVXTPUkdfjlMF1lxOf4xI8CZfhIQXgHTwF3F4A3_TfhsgptcriB73_3OVuR5EDn8IoOe1ee8_TIIhRgLcafvLH0msyAK9q62TUO9Y0rl1lsQ&avtc=1&avte=2&avts=1707303640',
    #                 123469)

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
# TODO убрать сообщения пользователя
# TODO убрать ссылку
# TODO удаление оповещений
# TODO ограничение по загрузке страниц !!!!
# TODO обработка ошибок (страницы нет, товара нет)
# TODO ТЕСТОВАЯ БД!!!
