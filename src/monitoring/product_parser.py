import requests
from bs4 import BeautifulSoup
from ..config.logger import setup_logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import time
import random


logger = setup_logger(__name__)


def start_parse():
    user_agent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent.random}')
    # options.add_argument('--proxy-server=138.128.91.65:8000')

    driver = webdriver.Chrome(options=options)

    url = 'https://megamarket.ru/catalog/?q=iphone%2015%20128'

    try:
        driver.get(url=url)

        time.sleep(3)
        elements = driver.find_elements(By.CLASS_NAME, 'item-price')

        prices = []
        for element in elements:
            elemement_string_price = element.get_attribute("innerText")
            element_int_price = parse_price_string(elemement_string_price)
            prices.append(element_int_price)
        logger.debug(prices)
    except Exception as ex:
        print(ex)
    else:
        driver.close()
        driver.quit()


def parse_price_string(price_string):
    price_string = price_string.replace('\xa0', ' ')
    price_string = ''.join(c for c in price_string if c.isdigit() or c.isspace())
    price = int(price_string.replace(' ', ''))
    return price
