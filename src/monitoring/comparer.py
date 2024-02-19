from config.logger import setup_logger
from db.crud_operations import ProductsCRUD
from src.monitoring.notification import Notification


logger = setup_logger(__name__)


class PriceComparer:
    @classmethod
    def compare_prices_and_notify_user(cls, is_any_change: bool, threshold_price: float,
                                       product_last_price: float, product_new_price: float, product_id: int,
                                       user_id: int):
        """Возвращает (изменился ли продукт, оповестить ли пользователя)"""
        cls._validate_is_any_change(is_any_change)
        cls._validate_price(threshold_price)
        cls._validate_price(product_last_price)
        cls._validate_price(product_new_price)
        cls._validate_int(user_id)
        cls._validate_int(product_id)

        is_price_has_changed = cls._compare(product_new_price, product_last_price)

        if not is_price_has_changed:
            return

        elif is_any_change:
            cls._notify_user()
            logger.debug("Цена изменилась!")
            ProductsCRUD.set_new_product_price(product_id=product_id, new_price=product_new_price)

        elif product_new_price <= threshold_price:
            cls._notify_user()
            logger.info("Цена достигла нужного занчения!")
            # удалить эту напоминалку

    @classmethod
    def _compare(cls, new_price, product_last_price):
        return round(new_price) != round(product_last_price)

    @classmethod
    def _notify_user(cls):
        Notification.notify_user()

    @classmethod
    def _validate_is_any_change(cls, is_any_change):
        if not isinstance(is_any_change, bool):
            raise ValueError(f'{is_any_change} not bool!')

    @classmethod
    def _validate_price(cls, price):
        if not (isinstance(price, float) or isinstance(price, int)):
            raise ValueError(f'{price} not int or bool!')

    @classmethod
    def _validate_int(cls, number):
        if not isinstance(number, int):
            raise ValueError(f'{number} not int!')

