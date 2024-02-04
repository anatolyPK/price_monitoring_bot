from config.database_config import init_db
from db.crud_operations import read_user_products
from src.monitoring.parser import start_parse


def main():
    init_db()
    read_user_products()
    # start_parse()


if __name__ == '__main__':
    main()
