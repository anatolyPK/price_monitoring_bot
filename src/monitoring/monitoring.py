from contextlib import contextmanager
from typing import Type

from selenium.webdriver.remote.webdriver import WebDriver

from config.config import DOMAINS
from config.logger import setup_logger
from urllib.parse import urlparse

from config.selenium_config import driver_sel
from db.crud_operations import UserProductsCRUD, ProductsCRUD
from db.models import UserProducts, Users, Products
from src.monitoring.comparer import PriceComparer
from src.monitoring.notification import Notification
from src.monitoring.parsers.base_parser import BaseParser


logger = setup_logger(__name__)


@contextmanager
def driver_context():
    driver_cont = driver_sel
    try:
        yield driver_cont
    finally:
        driver_cont.execute_script("window.close();") #JavaScript-команду window.close() для закрытия текущего окна


def start_monitoring():
    products_to_monitoring = UserProductsCRUD.get_user_products()

    with driver_context() as driver:
        for user_products, users, products in products_to_monitoring:
            parse_and_compare(driver, user_products, users, products)


def parse_and_compare(driver: WebDriver, user_products: UserProducts, users: Users, products: Products):
    parser_class = choose_parser_class(products.url)
    parser = parser_class(driver=driver, product_url=products.url)
    product_price = parser.get_product_price_and_name()
    logger.debug(f'PRICE: {product_price}')

    PriceComparer.compare_prices_and_notify_user(product_last_price=products.last_price,
                                                 is_any_change=user_products.is_any_change,
                                                 threshold_price=user_products.threshold_price,
                                                 product_id=products.id,
                                                 product_price=product_price,
                                                 user_id=users.id)


def add_new_product(url: str, telegram_id: int):
    product_price, product_name = get_product_price_and_name(url)

    ProductsCRUD.add_new_product(product_url=url, last_price=product_price, product_name=product_name)
    Notification.send_price(telegram_id=telegram_id, product_price=product_price) #// TODO wtf eto


def get_product_price_and_name(url: str) -> tuple[int, str]:
    with driver_context() as driver:
        parser_class = choose_parser_class(url)
        parser = parser_class(driver=driver, product_url=url)
        product_price, product_name = parser.get_product_price_and_name()
        return product_price, product_name


def choose_parser_class(url: str) -> Type[BaseParser]:
    domain = get_domain(url)
    parser_instance = DOMAINS[domain]
    return parser_instance


def get_domain(url: str): #refactor etogo
    domain = extract_domain(url)

    if not domain:
        logger.warning(f'Не найден домен {url}')
        raise AttributeError()

    if domain not in DOMAINS:
        raise KeyError()

    return domain


def extract_domain(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.netloc

