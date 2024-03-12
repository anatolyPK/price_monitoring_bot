import random
import re
import time

from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

from config.logger import setup_logger
from src.monitoring.custom_exceptions import ProductNotFound
from src.monitoring.parsers.base_parser import BaseParser


logger = setup_logger(__name__)


class OzonParser(BaseParser):
    MIN_TIME_WAIT = 2
    MAX_TIME_WAIT = 4

    def __init__(self, driver, product_url):
        super().__init__(driver, product_url)

    def get_product_prices_and_name(self) -> tuple[int, str]:
        try:
            return self.get_product_price_and_name_with_bs(2, 4)
        except ProductNotFound:
            return self.get_product_price_and_name_with_bs(2, 4)

    def get_product_price_and_name_with_bs(self, min_time_wait: int = 4, max_time_wait: int = 7) -> tuple[int, str]:
        try:
            self.driver.get(url=self.product_url)
        except TimeoutException:
            pass

        time.sleep(random.randint(min_time_wait, max_time_wait))

        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        product_price = self._extract_product_prices(soup)
        product_name = self._extract_product_name(soup)

        if not product_price or not product_name:
            raise ProductNotFound('Exception in get product price and name!')

        return product_price, product_name

    def _extract_product_prices(self, soup: BeautifulSoup):
        relevant_elements_price_with_card = soup.find_all(lambda tag: tag.name == 'div' and 'c Ozon Картой' in tag.text)
        price_with_card = self._price_extractor(relevant_elements_price_with_card)
        #возвращает цену с картой. для извлечения другиъ цен, нужн продумать как он булет их искать
        # relevant_elements_price_without_card = soup.find_all(lambda tag: tag.name == 'div' and 'без Ozon Карты' in tag.text)
        # price_without_card = self._price_extractor(relevant_elements_price_without_card)
        #
        # relevant_elements_old_price = soup.find_all(lambda tag: tag.name == 'div' and 'без Ozon Карты' in tag.text)[1]
        # old_price = self._price_extractor(relevant_elements_price_without_card)
        return price_with_card

    def _price_extractor(self, relevant_elements):
        for element in relevant_elements:
            price_match = re.search(r'(\d[\d\s]*)\s*₽', element.text)
            if price_match:
                return self._parse_price_to_int(price_match[0])
        raise ProductNotFound('Price not found')

    def _extract_product_name(self, soup: BeautifulSoup):
        grid_element = soup.find('div', {'data-widget': 'webProductHeading'})

        if grid_element:
            title_element = grid_element.find('h1')
            product_title = title_element.text.strip() if title_element else None
            return product_title
        raise ProductNotFound('Product name not found!')

    def _parse_price_to_int(self, price_str: str):
        return super()._parse_price_to_int(price_str, '\u2009')

    def _choose_price_classes(self, is_consider_bonuses):
        if is_consider_bonuses:
            return self.product_price_with_card_classes
        return self.product_price_without_card_classes


