from config.logger import setup_logger
from db.crud_operations import ProductsCRUD
from src.monitoring.notification import Notification


logger = setup_logger(__name__, log_file_path='./logs/information.log')


class PriceComparer:
    @classmethod
    def compare_prices_and_notify_user(cls, is_any_change: bool, threshold_price: float,
                 product_last_price: float, product_price: float, product_id: int,
                                       user_id: int):
        """Возвращает (изменился ли продукт, оповестить ли пользователя)"""

        is_price_has_changed = cls._compare(product_price, product_last_price)

        if not is_price_has_changed:
            return

        elif is_any_change:
            cls._notify_user()
            logger.debug("Цена изменилась!")
            ProductsCRUD.set_new_product_price(product_id=product_id, new_price=product_price)

        elif product_price <= threshold_price:
            cls._notify_user()
            logger.info("Цена достигла нужного занчения!")
            # удалить эту напоминалку

    @classmethod
    def _compare(cls, new_price, product_last_price):
        return round(new_price) != round(product_last_price)

    @classmethod
    def _notify_user(cls):
        Notification.notify_user()
