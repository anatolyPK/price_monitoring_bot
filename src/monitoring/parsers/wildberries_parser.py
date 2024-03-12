import time

from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from config.logger import setup_logger
from src.monitoring.custom_exceptions import ProductNotFound
from src.monitoring.parsers.base_parser import BaseParser


logger = setup_logger(__name__)


class WildberriesParser(BaseParser):
    MIN_TIME_WAIT = 3
    MAX_TIME_WAIT = 5

    def __init__(self, driver, product_url, is_consider_bonuses: bool = True):
        super().__init__(driver, product_url)
        self.is_consider_bonuses = is_consider_bonuses

    def _extract_product_prices(self, soup: BeautifulSoup) -> int:
        old_price = self._price_extractor(soup, '.price-block__old-price')
        final_price = self._price_extractor(soup, '.price-block__final-price')
        wallet_price = self._price_extractor(soup, '.price-block__wallet-price')

        if self.is_consider_bonuses and wallet_price:
            return wallet_price
        return final_price

    def _extract_product_name(self, soup: BeautifulSoup):
        return super()._extract_product_name(soup, ".product-page__title")
