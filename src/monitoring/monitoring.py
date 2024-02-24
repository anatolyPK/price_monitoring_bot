from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from config.logger import setup_logger
from config.selenium_config import options, add_script
from db.crud_operations import UserProductsCRUD, ProductsCRUD
from db.models import UserProducts, Users, Products
from src.monitoring.comparer import PriceComparer
from src.monitoring.custom_exceptions import ProductNotFound
from src.monitoring.services.utils import choose_parser_class
from src.notifications.utils import send_message_price_changed

logger = setup_logger(__name__)


@contextmanager
def driver_context():
    # driver_sel = webdriver.Chrome(options=options)

    driver_sel = webdriver.Remote(
        command_executor='http://172.19.0.3:4444/wd/hub',
        options=options
    )

    driver_sel.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

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
    finally:
        ...
        driver_cont.quit()  # JavaScript-команду window.close() для закрытия текущего окна


async def start_monitoring():
    products_to_monitoring = UserProductsCRUD.get_user_products()
    if products_to_monitoring is None:
        return
    with driver_context() as driver:
        for user_products, users, products in products_to_monitoring:
            await parse_and_compare(driver, user_products, users, products)


async def parse_and_compare(driver: WebDriver, user_products: UserProducts, users: Users, products: Products):
    parser_class = choose_parser_class(products.url)
    parser = parser_class(driver=driver, product_url=products.url)
    try:
        product_price, product_name = parser.get_product_price_and_name()

        await PriceComparer.compare_prices_and_notify_user(product_last_price=products.last_price,
                                                     is_any_change=user_products.is_any_change,
                                                     threshold_price=user_products.threshold_price,
                                                     product_id=products.id,
                                                     product_new_price=product_price,
                                                     product_name=product_name,
                                                     user_id=users.id,
                                                     product_url=products.url)
        logger.debug(f'PRICE: {product_price}')
    except ProductNotFound as ex:
        logger.warning(f'{ex} {products.url}')


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
