from typing import Type
from urllib.parse import urlparse

from config.config import DOMAINS
from config.logger import setup_logger
from src.monitoring.parsers.base_parser import BaseParser


logger = setup_logger(__name__)


def choose_parser_class(url: str) -> Type[BaseParser]:
    domain = get_domain(url)
    parser_instance = DOMAINS[domain]
    return parser_instance


def get_domain(url: str): #refactor etogo
    domain = extract_domain(url)

    if not domain:
        logger.warning(f'Не найден домен {url}')
        raise AttributeError()

    if domain not in DOMAINS:
        raise KeyError()

    return domain


def extract_domain(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.netloc

