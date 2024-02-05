from config.database_config import init_db
from src.monitoring.monitoring import start_monitoring, add_new_product


def main():
    # start_bot
    init_db()
    # start_monitoring()
    add_new_product('https://megamarket.ru/catalog/details/pristavka-igrovaya-microsoft-xbox-series-x-diablo-iv-bundle-100061636297/',
                    123469)


if __name__ == '__main__':
    main()

# TODO тесты
# TODO дописать озон и вайлд
# TODO бд добавление
# TODO взаимод бота с парс
# TODO удаление оповещений