from config.database_config import init_db
from src.monitoring.parser import start_parse


def main():
    # start_bot
    init_db()
    start_parse()


if __name__ == '__main__':
    main()

# TODO тесты
# TODO дописать озон и вайлд
# TODO бд добавление
# TODO взаимод бота с парс
# TODO удаление оповещений