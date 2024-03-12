import random
import time

from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from config.logger import setup_logger
from src.monitoring.custom_exceptions import ProductNotFound
from src.monitoring.parsers.base_parser import BaseParser

logger = setup_logger(__name__)


class MegaMarketClasses:

    product_price_classes = ['sales-block-offer-price__price-final']
    product_name_classes = ['pdp-header__title_only-title']


class MegaMarkerParser(BaseParser):
    MIN_TIME_WAIT = 2
    MAX_TIME_WAIT = 3

    def __init__(self, driver, product_url, is_consider_bonuses: bool = True):
        super().__init__(driver, product_url)
        self.is_consider_bonuses = is_consider_bonuses

    def _extract_product_prices(self, soup: BeautifulSoup) -> int:
        product_price = self._price_extractor(soup, '.sales-block-offer-price__price-final')

        # bonuses_item = soup.select_one('pdp-sales-block__cashback-table')
        rows = soup.find_all('div', class_='pdp-cashback-table__row')
        result_dict = {}
        for row in rows:
            label = row.find('div', class_='pdp-cashback-table__label').get_text(strip=True)
            bonus_amount = row.find('span', class_='bonus-amount').get_text(strip=True).replace(' ', '')
            result_dict[label] = int(bonus_amount)
        if self.is_consider_bonuses:
            bonuses = result_dict.get('Оплата Сбером', None)
            if not bonuses:
                bonuses = result_dict.get('Начислим за товар', 0)
            product_price -= bonuses
        return product_price

    def _extract_product_name(self, soup: BeautifulSoup):
        return super()._extract_product_name(soup, ".pdp-header__title_only-title")


class PriceCalculator:
    @classmethod
    def count_finally_price(cls, price, bonuses, coupon=None):
        if coupon:
            bonuses_percent = cls._count_percent_of_prices_bonuses(price, bonuses)
            price = Coupon.get_price_with_coupon_ikra(price)
            bonuses = bonuses_percent * price

        return round(price - bonuses, 0)

    @classmethod
    def _count_percent_of_prices_bonuses(cls, price, bonuses):
        return bonuses / price


class Coupon:
    @staticmethod
    def get_price_with_coupon_ikra(price):
        if price < 11000:
            return price
        elif price < 30000:
            return price - 2000
        elif price < 50000:
            return price - 5000
        elif price < 7000:
            return price - 9000
        return price - 12000

