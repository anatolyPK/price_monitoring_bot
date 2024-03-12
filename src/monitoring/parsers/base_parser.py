import datetime
import random
import time
from abc import ABC

from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from config.logger import setup_logger
from src.monitoring.custom_exceptions import ProductNotFound


logger = setup_logger(__name__)


class BaseParser(ABC):
    MIN_TIME_WAIT = None
    MAX_TIME_WAIT = None
    # продумать классы для скидок. как будет осущ выбор

    def __init__(self, driver: WebDriver, product_url: str):
        self.driver = driver
        self.product_url = product_url

    def get_product_prices_and_name(self) -> tuple[int, str]:
        soup = self._get_soup_page_instance()

        product_price = self._extract_product_prices(soup)
        product_name = self._extract_product_name(soup)

        if not product_price or not product_name:
            raise ProductNotFound('Exception in get product price and name!')

        return product_price, product_name

    def _get_soup_page_instance(self):
        try:
            self.driver.get(url=self.product_url)
        except TimeoutException:
            pass

        time.sleep(random.randint(self.MIN_TIME_WAIT, self.MAX_TIME_WAIT))

        html_content = self.driver.page_source
        return BeautifulSoup(html_content, 'html.parser')

    def _extract_product_name(self, soup: BeautifulSoup, class_name: str):
        name = soup.select_one(class_name)
        if name:
            return name.text.strip()
        logger.debug(f'Не удалось извлечь наименование товара! {soup}')
        raise ProductNotFound("Не удалось извлечь наименование товара!")

    def _price_extractor(self, soup: BeautifulSoup, class_name):
        price = soup.select_one(class_name)
        if price:
            return self._parse_price_to_int(price.text.strip())

    def _extract_product_prices(self, soup: BeautifulSoup):
        pass

    def _parse_price_to_int(self, price_str: str, old_space: str = '\xa0') -> int:
        price_str = price_str.replace(old_space, ' ')
        price_str = ''.join(c for c in price_str if c.isdigit())
        int_price = int(price_str)
        return int_price


