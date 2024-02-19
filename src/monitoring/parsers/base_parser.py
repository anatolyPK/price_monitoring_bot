import pickle
import random
import time
from selenium.webdriver.support import expected_conditions as EC

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from config.logger import setup_logger
from src.monitoring.custom_exceptions import ProductNotFound

logger = setup_logger(__name__)


class BaseParser:
    possible_product_price_class = []
    possible_product_name_class = []

    def __init__(self, driver: WebDriver, product_url: str):
        self.driver = driver
        self.product_url = product_url

    def get_product_price_and_name(self) -> tuple[int, str]:

        self.driver.get(url=self.product_url)
        # time.sleep(2)
        # for cookie in pickle.load(open('cookies', 'rb')):
        #     self.driver.add_cookie(cookie)
        #
        # cookies_to_add = pickle.load(open('cookies', 'rb'))
        #
        # for cookie in cookies_to_add:
        #     cookie_name = cookie['name']
        #     existing_cookie = self.driver.get_cookie(cookie_name)
        #     if existing_cookie:
        #         self.driver.delete_cookie(cookie_name)
        #         self.driver.add_cookie(cookie)
        time.sleep(3)
        self.driver.refresh()
        time.sleep(random.randint(4, 7))
        # self.driver.refresh()
        # pickle.dump(self.driver.get_cookies(), open('cookies', 'wb'))

        product_price = self._extract_product_price()
        product_name = self._extract_product_name()

        return product_price, product_name

    def _extract_product_price(self):
        for class_name in self.possible_product_price_class:
            try:
                product_price = self.driver.find_element(By.CLASS_NAME, class_name)
                string_price = product_price.get_attribute("innerText")
                return self._parse_price_to_int(string_price)
            except NoSuchElementException:
                continue
        raise ProductNotFound(f'Не определена цена товара!')

    def _extract_product_name(self):
        for class_name in self.possible_product_name_class:
            try:
                product_price = self.driver.find_element(By.CLASS_NAME, class_name)
                return product_price.get_attribute("innerText")
            except NoSuchElementException:
                continue
        raise ProductNotFound(f'Не определено наименование товара!')

    def _parse_price_to_int(self, price_str: str, old_space: str = '\xa0') -> int:
        price_str = price_str.replace(old_space, ' ')
        price_str = ''.join(c for c in price_str if c.isdigit())
        int_price = int(price_str)
        return int_price


