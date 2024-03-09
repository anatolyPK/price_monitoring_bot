import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from config.logger import setup_logger
from src.monitoring.custom_exceptions import ProductNotFound
from src.monitoring.parsers.base_parser import BaseParser


logger = setup_logger(__name__)


class WildberriesClasses:
    product_price_with_card_classes = ['sales-block-offer-price__price-final',
                                       'price-block__final-price',
                                       'price-block__wallet-price']
    product_price_without_card_classes = ['price-block__final-price',
                                          'price-block__wallet-price.wallet']
    product_name_classes = ['pdp-header__title_only-title',
                            'product-page__title']


class WildberriesParser(BaseParser, WildberriesClasses):
    def __init__(self, driver, product_url, is_consider_bonuses: bool = True):
        super().__init__(driver, product_url)

        self.product_name_classes = self.product_name_classes
        self.product_price_classes = self._choose_price_classes(is_consider_bonuses)
    #
    # def get_product_price_and_name(self) -> tuple[int, str]:
    #     return super().get_product_price_and_name()

    def get_product_price_and_name(self):
        return super().get_product_price_and_name(3, 5)

    def _choose_price_classes(self, is_consider_bonuses):
        if is_consider_bonuses:
            return self.product_price_with_card_classes
        return self.product_price_without_card_classes


