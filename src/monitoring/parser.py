from config.config import DOMAINS
from config.logger import setup_logger
from selenium import webdriver
from urllib.parse import urlparse

from db.crud_operations import get_user_products


logger = setup_logger(__name__)


# это общий файл, из которого будут выхываться другие модули для парсинга определенного мегамаркета


def start_parse():
    driver = start_driver()
    try:
        products_to_parsing = get_user_products()

        for parsed_product in products_to_parsing:
            parse_product(parsed_product, driver)

    except Exception as e:
        logger.warning(f"Error parsing domain: {e}")
    finally:
        driver.quit()


def start_driver():
    return webdriver.Chrome()


def parse_product(parsed_product, driver):
    user_products, users, products = parsed_product
    domain = get_domain(products.url)
    parser_instance = DOMAINS[domain](driver, products.url, products.last_price,
                                      user_products.is_any_change, user_products.threshold_price,
                                      products.id)
    parser_instance.parse_product()


def get_domain(url):
    domain = extract_domain(url)
    if domain not in DOMAINS:
        # ответ боту, что сслыка некорректна
        logger.info(f"No parser found for domain: {domain}")
    return domain


def extract_domain(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.netloc
