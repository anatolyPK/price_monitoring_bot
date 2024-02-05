from contextlib import contextmanager

from config.config import DOMAINS
from config.logger import setup_logger
from selenium import webdriver
from urllib.parse import urlparse

from db.crud_operations import UserProductsCRUD, ProductsCRUD
from src.monitoring.comparer import PriceComparer
from src.monitoring.notification import Notification


logger = setup_logger(__name__)


# это общий файл, из которого будут выхываться другие модули для парсинга определенного мегамаркета

@contextmanager
def driver_context():
    driver = start_driver()
    try:
        yield driver
    finally:
        driver.quit()


def start_monitoring():
    products_to_monitoring = UserProductsCRUD.get_user_products()

    with driver_context() as driver:
        for user_products, users, products in products_to_monitoring:
            parse_and_compare(driver, user_products, users, products)


def parse_and_compare(driver, user_products, users, products):
    parser_class = choose_parser_class(products.url)
    parser = parser_class(driver=driver, product_url=products.url)
    product_price = parser.get_product_price()

    PriceComparer.compare_prices_and_notify_user(product_last_price=products.last_price,
                                                 is_any_change=user_products.is_any_change,
                                                 threshold_price=user_products.threshold_price,
                                                 product_id=products.id,
                                                 product_price=product_price,
                                                 user_id=users.id)


def add_new_product(url: str, telegram_id: int):
    with driver_context() as driver:
        parser_class = choose_parser_class(url)
        parser = parser_class(driver=driver, product_url=url)
        product_price = parser.get_product_price()

    ProductsCRUD.add_new_product(product_url=url, last_price=product_price)
    Notification.send_price(telegram_id=telegram_id, product_price=product_price)


def start_driver():
    return webdriver.Chrome()


def choose_parser_class(url):
    domain = get_domain(url)
    parser_instance = DOMAINS[domain]
    return parser_instance


def get_domain(url):
    domain = extract_domain(url)
    if domain not in DOMAINS:
        # ответ боту, что сслыка некорректна
        logger.info(f"No parser found for domain: {domain}")
    return domain


def extract_domain(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.netloc


