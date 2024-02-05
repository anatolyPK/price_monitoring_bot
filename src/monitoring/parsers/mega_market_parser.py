from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from config.logger import setup_logger
from src.monitoring.comparer import PriceComparer
from src.monitoring.parsers.base_parser import BaseParser

logger = setup_logger(__name__)


class MegaMarkerParser(BaseParser):
    possible_item_classes = ['pdp-sales-block-default',
                             'pdp-sales-block-cnd',
                             'other-class2']
    possible_price_class = 'sales-block-offer-price__price-final'

    def __init__(self, driver, product_url, is_consider_bonuses: bool = True):
        super().__init__(driver, product_url)
        self.is_consider_bonuses = is_consider_bonuses

    def get_product_price(self):
        self.driver.get(url=self.product_url)
        item_price = self._get_item_price()
        product_price = self._extract_product_price(item_price)

        if self.is_consider_bonuses:
            bonuses = self._get_product_bonuses(item_price)
            product_price -= bonuses
        logger.debug(f'PRICE {product_price}')
        return product_price

    def _get_item_price(self):
        return super()._get_item_price()

    def _extract_product_price(self, item_price):
        product_price = item_price.find_element(By.CLASS_NAME, self.possible_price_class)
        string_price = product_price.get_attribute("innerText")
        return self._parse_price_to_int(string_price)

    def _get_product_bonuses(self, item_price):
        bonus_element = item_price.find_elements(By.CLASS_NAME, 'money-bonus_loyalty')
        if bonus_element:
            bonus_amount = bonus_element[0].find_element(By.CLASS_NAME, 'bonus-amount')
            element_string_bonus = bonus_amount.get_attribute("innerText")
            elements_int_bonuses = self._parse_price_to_int(element_string_bonus)
        else:
            elements_int_bonuses = 0
        return elements_int_bonuses













    def parse_product(self):
        self.driver.get(url=self.product_url)
        item_price = self._get_item_price()

        product_price = self._get_product_price(item_price)
        product_bonuses = self._get_product_bonuses(item_price)
        finally_price = PriceCalculator.count_finally_price(product_price, product_bonuses, True)

        self.comparer.compare_prices(finally_price)
        logger.debug(f'PRICE:{finally_price}')

    def _get_item_price(self):
        possible_classes = ['pdp-sales-block-default',
                            'pdp-sales-block-cnd',
                            'other-class2']

        for class_name in possible_classes:
            try:
                item_price = self.driver.find_element(By.CLASS_NAME, class_name)
                return item_price
            except NoSuchElementException:
                continue

    def _get_product_price(self, item_price):
        product_price = item_price.find_element(By.CLASS_NAME, 'sales-block-offer-price__price-final')
        string_price = product_price.get_attribute("innerText")
        return self._parse_price_to_int(string_price)



    def _parse_price_to_int(self, price_str):
        price_str = price_str.replace('\xa0', ' ')
        price_str = ''.join(c for c in price_str if c.isdigit() or c.isspace())
        price = int(price_str.replace(' ', ''))
        return price


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

