import logging
import asyncio

from config.database_config import init_db
from src.monitoring.monitoring import start_monitoring
from src.notifications.bot_start_up import start_bot


def main():
    init_db()
    # start_monitoring()
    # for_personal()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start_bot())


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
# TODO почистить requiremrntsd=
# TODO раз в 4 минуты заходить на любой сайт, если не заходил на другие
# TODO при каждом новом вызове создавался новый драйвер
