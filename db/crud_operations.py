from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError

from config.database_config import db_session
from config.logger import setup_logger
from db.models import UserProducts, Users, Products


logger = setup_logger(__name__)


@contextmanager
def handle_database_errors():
    try:
        yield
    except SQLAlchemyError as e:
        logger.warning(f"Ошибка базы данных: {e}")


def database_operation(func):
    def wrapper(*args, **kwargs):
        with handle_database_errors():
            return func(*args, **kwargs)
    return wrapper


@database_operation
def get_user_products():
    with db_session() as session:
        result = (
            session.query(UserProducts, Users, Products)
            .join(Users, UserProducts.user == Users.id)
            .join(Products, UserProducts.product == Products.id)
            .all()
        )
        return result


@database_operation
def set_new_product_price(row_id: int, new_price: float):
    with db_session() as session:
        product = session.query(Products).get(row_id)

        if product:
            product.last_price = new_price
            session.commit()
        else:
            logger.info(f'Ошибка изменения строки {row_id}')
