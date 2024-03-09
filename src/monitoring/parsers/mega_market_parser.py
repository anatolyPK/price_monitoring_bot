import random
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from config.logger import setup_logger
from src.monitoring.parsers.base_parser import BaseParser

logger = setup_logger(__name__)


class MegaMarketClasses:
    product_price_classes = ['sales-block-offer-price__price-final']
    product_name_classes = ['pdp-header__title_only-title']


class MegaMarkerParser(BaseParser, MegaMarketClasses):
    def __init__(self, driver, product_url, is_consider_bonuses: bool = True):
        super().__init__(driver, product_url)
        self.is_consider_bonuses = is_consider_bonuses

    def get_product_price_and_name(self):
        product_price, product_name = super().get_product_price_and_name(1,2)

        if self.is_consider_bonuses:
            bonuses = self._get_product_bonuses()
            product_price -= bonuses
        return product_price, product_name

    def _get_product_bonuses(self):
        bonus_element = self.driver.find_elements(By.CLASS_NAME, 'money-bonus_loyalty')
        if bonus_element:
            bonus_amount = bonus_element[0].find_element(By.CLASS_NAME, 'bonus-amount')
            element_string_bonus = bonus_amount.get_attribute("innerText")
            elements_int_bonuses = self._parse_price_to_int(element_string_bonus)
        else:
            elements_int_bonuses = 0
        return elements_int_bonuses


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

