from src.monitoring.parsers.mega_market_parser import MegaMarkerParser
from src.monitoring.parsers.ozon_parser import OzonParser
from src.monitoring.parsers.wildberries_parser import WildberriesParser


DOMAINS = {
    'megamarket.ru': MegaMarkerParser,
    'www.megamarket.ru': MegaMarkerParser,

    'www.ozon.ru': OzonParser,
    'ozon.ru': OzonParser,

    'www.wildberries.ru': WildberriesParser,
    'wildberries.ru': WildberriesParser,
    'https://wildberries.ru': WildberriesParser,

}