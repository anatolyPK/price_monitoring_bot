from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


class BaseParser:
    possible_item_classes = []

    possible_price_class = ''

    def __init__(self,
                 driver,
                 product_url: str):
        self.driver = driver
        self.product_url = product_url

    def get_product_price(self):
        self.driver.get(url=self.product_url)
        item_price = self._get_item_price()
        product_price = self._extract_product_price(item_price)
        return product_price

    def _get_item_price(self):
        for class_name in self.possible_item_classes:
            try:
                item_price = self.driver.find_element(By.CLASS_NAME, class_name)
                return item_price
            except NoSuchElementException:
                continue

    def _extract_product_price(self, item_price):
        product_price = item_price.find_element(By.CLASS_NAME, self.possible_price_class)
        string_price = product_price.get_attribute("innerText")
        return self._parse_price_to_int(string_price)

    def _parse_price_to_int(self, price_str):
        price_str = price_str.replace('\xa0', ' ')
        price_str = ''.join(c for c in price_str if c.isdigit() or c.isspace())
        price = int(price_str.replace(' ', ''))
        return price

