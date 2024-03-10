import datetime
from contextlib import contextmanager

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

from config.logger import setup_logger
from config.selenium_config import options, add_script
from db.crud_operations import UserProductsCRUD, ProductsCRUD
from db.models import UserProducts, Users, Products
from src.monitoring.comparer import PriceComparer
from src.monitoring.custom_exceptions import ProductNotFound
from src.monitoring.services.utils import choose_parser_class, find_url_in_text
from src.notifications.utils import send_message_price_changed

logger = setup_logger(__name__)


# class WebDriverManager:
#     _instance = None
#
#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(WebDriverManager, cls).__new__(cls)
#             cls._instance._driver = None
#         return cls._instance
#
#     @property
#     def driver(self):
#         if self._driver is None:
#             self._driver = webdriver.Remote(
#                 command_executor='http://172.19.0.3:4444/wd/hub',
#                 options=options
#             )
#             self._driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#             self.add_script(self._driver,
#                             '''
#                                   delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
#                                   delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
#                                   delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
#                                   delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
#                                   delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
#                                   delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
#                             '''
#                             )
#         return self._driver
#
#     def add_script(self, driver, script):
#         # Добавьте вашу реализацию функции add_script
#         pass
#
#     @staticmethod
#     @contextmanager
#     def driver_context():
#         try:
#             yield WebDriverManager()._instance.driver
#         except WebDriverException:
#             WebDriverManager()._instance.driver.close()
#         finally:
#             WebDriverManager()._instance.driver.close()
#             ...   # Ничего не делаем здесь, чтобы сохранить драйвер открытым
#

@contextmanager
def driver_context():
    driver_sel = webdriver.Chrome(options=options)

    # driver_sel = webdriver.Remote(
    #     command_executor='http://172.19.0.3:4444/wd/hub',
    #     options=options
    # )

    driver_sel.maximize_window()
    driver_sel.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver_sel.set_page_load_timeout(8)

    add_script(driver_sel,
               '''
                      delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                      delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                      delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                      delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
                      delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
                      delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
                '''
               )
    driver_cont = driver_sel

    try:
        yield driver_cont
    except WebDriverException:
        driver_cont.close()
    # except Exception as ex:
    #     logger.debug(f'AAAA {ex}')
    finally:
        driver_cont.quit()


def start_monitoring():
    products_to_monitoring = UserProductsCRUD.get_user_products_for_monitoring()
    if products_to_monitoring is None:
        return

    with driver_context() as driver:
        for user_product in products_to_monitoring:
            parse_and_compare(driver, user_product)


def parse_and_compare(driver: WebDriver, user_product: UserProducts):
    parser_class = choose_parser_class(user_product.products.url)
    parser = parser_class(driver=driver, product_url=user_product.products.url)
    try:
        product_price, product_name = parser.get_product_price_and_name()

        PriceComparer.compare_prices_and_notify_user(product_last_price=user_product.products.last_price,
                                                     is_any_change=user_product.is_any_change,
                                                     threshold_price=user_product.threshold_price,
                                                     product_id=user_product.products.id,
                                                     product_new_price=product_price,
                                                     product_name=product_name,
                                                     chat_id=user_product.users.telegram_id,
                                                     product_url=user_product.products.url)
        logger.debug(f'PRICE: {product_price}')
    except ProductNotFound as ex:
        logger.warning(f'{ex} {user_product.products.url}')


# def add_new_product(url: str, telegram_id: int):
#     product_price, product_name = get_product_price_and_name(url)
#
#     ProductsCRUD.add_new_product(product_url=url, last_price=product_price, product_name=product_name)
#     send_message_price_changed(telegram_id=telegram_id, product_price=product_price) #// TODO wtf eto


def get_product_price_and_name_from_handlers(url: str) -> tuple[int, str]:
    with driver_context() as driver:
        parser_class = choose_parser_class(url)
        parser = parser_class(driver=driver, product_url=url)
        product_price, product_name = parser.get_product_price_and_name()
        return product_price, product_name
