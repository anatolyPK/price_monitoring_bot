import random
import time

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

from config.logger import setup_logger


logger = setup_logger(__name__)


class BaseParser:
    possible_price_class = []

    def __init__(self,
                 driver,
                 product_url: str):
        self.driver = driver
        self.product_url = product_url

    def get_product_price(self):
        try:
            self.driver.set_page_load_timeout(15)
            self.driver.get(url=self.product_url)
            self.driver.execute_script("return document.readyState === 'complete';")

            time.sleep(random.randint(4, 9))
            product_price = self._extract_product_price()
            return product_price
        except TimeoutException:
            logger.debug("Время ожидания загрузки страницы истекло. Страница не загружена.")
            return 0  # Или какое-то значение по умолчанию или исключение, в зависимости от вашей логики
        finally:
            # Сбрасываем ограничение времени ожидания для следующих загрузок страниц
            self.driver.set_page_load_timeout(0)

    def _extract_product_price(self):
        for class_name in self.possible_price_class:
            try:
                product_price = self.driver.find_element(By.CLASS_NAME, class_name)
                string_price = product_price.get_attribute("innerText")
                return self._parse_price_to_int(string_price)
            except NoSuchElementException:
                continue

    def _parse_price_to_int(self, price_str: str, old_space: str = '\xa0') -> int:
        price_str = price_str.replace(old_space, ' ')
        price_str = ''.join(c for c in price_str if c.isdigit())
        price = int(price_str)
        return price

