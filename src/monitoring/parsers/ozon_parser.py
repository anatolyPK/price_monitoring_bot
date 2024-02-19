import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from config.logger import setup_logger
from src.monitoring.custom_exceptions import ProductNotFound
from src.monitoring.parsers.base_parser import BaseParser


logger = setup_logger(__name__)


class OzonParser(BaseParser):
    possible_product_price_class = ['l8o.ol8.l2p', 'l8o.o8l.p12', 'o3l.lo2', 'lo4.l3o', 'lp.l8o', 'pl0.l9o', 'pl1.pl']
    possible_product_name_class = ['pl9', 'lq0', 'lq1']

    def __init__(self, driver, product_url):
        super().__init__(driver, product_url)

    def get_product_price_and_name(self) -> tuple[int, str]:
        try:
            return super().get_product_price_and_name()

        except ProductNotFound:
            product_price = self._extract_ozon_product_price()
            product_name = self._extract_ozon_product_name()

            return product_price, product_name

    def _extract_ozon_product_price(self):
        try:
            product_price = self.driver.find_element(By.XPATH,
                                                     '/html/body/div[1]/div/div[1]/div[4]/div[3]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span')
            string_price = product_price.get_attribute("innerText")
            logger.warning(f'ADD TO OZON PRICE CLASSES {product_price.get_attribute("class")}')
            return self._parse_price_to_int(string_price)
        except NoSuchElementException:
            raise ProductNotFound(f'Не определена цена товара!')

    def _extract_ozon_product_name(self):
        try:
            product_price = self.driver.find_element(By.XPATH,
                                                     '/html/body/div[1]/div/div[1]/div[4]/div[2]/div/div/div[1]/div/h1')
            logger.warning(f'ADD TO OZON NAME CLASSES {product_price.get_attribute("class")}')
            return product_price.get_attribute("innerText")

        except NoSuchElementException:
            raise ProductNotFound(f'Не определено наименование товара!')

    def _parse_price_to_int(self, price_str: str):
        return super()._parse_price_to_int(price_str, '\u2009')





