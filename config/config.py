from src.monitoring.mega_market_parser import MegaMarkerParser
from src.monitoring.ozon_parser import OzonParser
from src.monitoring.wildberries_parser import WildberriesParser


DOMAINS = { #как то нужно вынести в конфиг это
    'megamarket.ru': MegaMarkerParser,
    'www.ozon.ru': OzonParser,
    'www.wildberries.ru': WildberriesParser,
}