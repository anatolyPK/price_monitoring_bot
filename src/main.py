from config.database_config import init_db
from src.monitoring.monitoring import start_monitoring, add_new_product


def main():
    # start_bot
    init_db()
    start_monitoring()
    # add_new_product('https://www.ozon.ru/product/nastolnaya-kartochnaya-igra-gvint-gwent-the-witcher-card-game-1152599194/?advert=MXpl-haP6KpRblK7ZAWajWKyBlFveQO7-cG0wHz7BP_EmJorfHGtNzE3ThEBT0SsFUoB7W96IpAgTrPonUhSjJuKw-cYZL5dVXTPUkdfjlMF1lxOf4xI8CZfhIQXgHTwF3F4A3_TfhsgptcriB73_3OVuR5EDn8IoOe1ee8_TIIhRgLcafvLH0msyAK9q62TUO9Y0rl1lsQ&avtc=1&avte=2&avts=1707303640',
    #                 123469)


if __name__ == '__main__':
    main()

# TODO тесты
# TODO взаимод бота с парс
# TODO удаление оповещений
# TODO ограничение по загрузке страниц
# TODO обработка ошибок (страницы нет, товара нет)
