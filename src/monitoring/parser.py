from .mega_market_parser import MegaMarkerParser
from .ozon_parser import OzonParser
from .wildberries_parser import WildberriesParser
from config.logger import setup_logger
from selenium import webdriver
from urllib.parse import urlparse


logger = setup_logger(__name__)


# это общий файл, из которого будут выхываться другие модули для парсинга определенного мегамаркета


DOMAINS = { #как то нужно вынести в конфиг это
    'megamarket.ru': MegaMarkerParser,
    'www.ozon.ru': OzonParser,
    'www.wildberries.ru': WildberriesParser,
}


def start_parse(url: str, last_price: float):
    driver = webdriver.Chrome()
    try:
        domain = extract_domain(url)
        if domain in DOMAINS:
            parser_instance = DOMAINS[domain]
            parser_instance.start(url, last_price, driver)
        else:
            #ответ боту, что сслыка некорректна
            logger.info(f"No parser found for domain: {domain}")
    except Exception as e:
        logger.warning(f"Error parsing domain: {e}")
    finally:
        driver.close()


def extract_domain(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.netloc
