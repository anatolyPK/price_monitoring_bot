import requests
from bs4 import BeautifulSoup
from ..config.logger import setup_logger

logger = setup_logger(__name__)


def start_parse():
    url = 'https://www.ozon.ru/product/nastolnaya-igra-zelenyy-mir-1362989901/?asb=1oCKgerKqUiyUPnxSJ60H%252BDJuB6gg%252FkdhqWdwQfdlHs%253D&asb2=eI-kdh1w0UHRKqZmyDYLLjtOb6mvfGUrvw2xWYTYpMGVYRTj41qkErf2gW9BBuF7&avtc=1&avte=2&avts=1706692380&keywords=%D0%B7%D0%B5%D0%BB%D1%91%D0%BD%D1%8B%D0%B9+%D0%BC%D0%B8%D1%80+%D0%BD%D0%B0%D1%81%D1%82%D0%BE%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%B8%D0%B3%D1%80%D0%B0'
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

