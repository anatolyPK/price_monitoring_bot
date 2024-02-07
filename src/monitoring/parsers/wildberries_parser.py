import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from config.logger import setup_logger
from src.monitoring.parsers.base_parser import BaseParser


logger = setup_logger(__name__)


class WildberriesParser(BaseParser):
    possible_item_classes = ['price-block__price']

    possible_price_class = ['price-block__wallet-price', 'price-block__final-price']

    def __init__(self, driver, product_url):
        super().__init__(driver, product_url)


    def get_product_price(self):
        self.driver.get(url=self.product_url)
        time.sleep(5)
        item_price = self._get_item_price()
        product_price = self._extract_product_price(item_price)
        return product_price

    def _get_item_price(self):
        for class_name in self.possible_item_classes:
            try:
                items_price = self.driver.find_elements(By.CLASS_NAME, class_name)
                return items_price
            except NoSuchElementException:
                continue

    def _extract_product_price(self, items_price):
        for item_price in items_price:
            for class_name in self.possible_price_class:
                try:
                    product_price = item_price.find_element(By.CLASS_NAME, class_name)
                    string_price = product_price.get_attribute("innerText")
                    return self._parse_price_to_int(string_price)
                except NoSuchElementException:
                    continue
