import requests
from bs4 import BeautifulSoup
from ..config.logger import setup_logger

logger = setup_logger(__name__)


def start_parse():
    url = 'https://www.ozon.ru/product/nastolnaya-igra-zelenyy-mir-1362989901/'
    response = requests.get(url)

    logger.debug(response.text)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        price_elements = soup.select('.18m')  # Замените это на актуальный CSS-селектор вашего сайта
        logger.debug(price_elements)

        if price_elements:
            price = price_elements[0].text.strip()
            logger.debug(price)
            return price
        else:
            return "Цена не найдена"


