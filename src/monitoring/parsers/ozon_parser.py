import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from config.logger import setup_logger
from src.monitoring.parsers.base_parser import BaseParser


logger = setup_logger(__name__)


class OzonParser(BaseParser):
    possible_product_price_class = ['l8o.ol8.l2p', 'l8o.o8l.p12', 'o3l.lo2', 'lo4.l3o', 'lp.l8o', 'pl0.l9o']
    possible_product_name_class = ['pl9', 'lq0']

    def __init__(self, driver, product_url):
        super().__init__(driver, product_url)

    def _parse_price_to_int(self, price_str: str):
        return super()._parse_price_to_int(price_str, '\u2009')





