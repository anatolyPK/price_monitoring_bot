from config.logger import setup_logger
from db.crud_operations import ProductsCRUD


logger = setup_logger(__name__)


class PriceComparer:
    @classmethod
    def compare_prices_and_notify_user(cls, is_any_change: bool, threshold_price: int,
                                       product_last_price: int, product_new_price: int, product_id: int,
                                       user_id: int):
        cls._validate_is_any_change(is_any_change)
        cls._validate_int(threshold_price)
        cls._validate_int(product_last_price)
        cls._validate_int(product_new_price)
        cls._validate_int(user_id)
        cls._validate_int(product_id)

        is_price_has_changed = cls._compare(product_new_price, product_last_price)

        if not is_price_has_changed: #возвращает None чтобв прекратить дальнейшее выполнение
            return
        # what to return

        elif is_any_change:
            cls._notify_user()
            logger.debug("Цена изменилась!")
            ProductsCRUD.set_new_product_price(product_id=product_id, new_price=product_new_price)

        elif product_new_price <= threshold_price:
            cls._notify_user()
            logger.info("Цена достигла нужного занчения!")
            # удалить эту напоминалку

    @classmethod
    def _compare(cls, new_price: int, product_last_price: int) -> bool:
        """Возвращает True если цена изменилась, иначе - False"""
        if not (isinstance(new_price, int) and isinstance(product_last_price,int)):
            raise ValueError
        return new_price != product_last_price

    @classmethod
    def _notify_user(cls):
        pass

    @classmethod
    def _validate_is_any_change(cls, value):
        if not isinstance(value, bool):
            raise ValueError(f'{value} not bool!')

    @classmethod
    def _validate_int(cls, number):
        if not isinstance(number, int):
            raise ValueError(f'{number} not int!')

