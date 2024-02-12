import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from config.logger import setup_logger
from src.monitoring.parsers.base_parser import BaseParser


logger = setup_logger(__name__)


class WildberriesParser(BaseParser):
    possible_product_price_class = ['price-block__wallet-price', 'price-block__final-price']
    possible_product_name_class = ['product-page__title']

    def __init__(self, driver, product_url):
        super().__init__(driver, product_url)


