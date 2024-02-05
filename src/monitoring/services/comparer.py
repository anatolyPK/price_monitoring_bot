from config.logger import setup_logger
from db.crud_operations import set_new_product_price


logger = setup_logger(__name__)


class PriceComparer:
    def __init__(self, is_any_change: bool, threshold_price: float,
                 product_last_price: float, product_id: int):
        self.threshold_price = threshold_price
        self.product_last_price = product_last_price
        self.is_any_change = is_any_change
        self.threshold_price = threshold_price
        self.product_id = product_id

    def compare_prices(self, new_price):
        is_price_has_changed = self.compare(new_price)
        logger.debug(is_price_has_changed)

        if not is_price_has_changed:
            return

        elif self.is_any_change:
            logger.debug("Цена изменилась!")

        elif new_price <= self.threshold_price:
            logger.info("Цена достигла нужного занчения!")
            # удалить эту напоминалку

        set_new_product_price(row_id=self.product_id, new_price=new_price)

    def compare(self, new_price):
        return round(new_price) != round(self.product_last_price)
