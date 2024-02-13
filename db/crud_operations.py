from contextlib import contextmanager
from functools import wraps

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

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


class UsersCRUD:
    @staticmethod
    @database_operation
    def add_new_user(telegram_id: int) -> Users.id:
        with db_session() as session:
            existing_user = session.query(Users).filter_by(telegram_id=telegram_id).first()
            if existing_user:
                return existing_user.id

            new_user = Users(telegram_id=telegram_id)
            session.add(new_user)
            session.commit()
            return new_user.id

    @staticmethod
    @database_operation
    def get_user(telegram_id) -> Users.id:
        with db_session() as session:
            user = session.query(Users).filter_by(telegram_id=telegram_id).first()
            return user.id if user else None


class ProductsCRUD:
    @staticmethod
    @database_operation
    def add_new_product(product_url: str, last_price: float, product_name: str) -> Products.id:
        with db_session() as session:
            product = Products(url=product_url, last_price=last_price, product_name=product_name)
            session.add(product)
            session.commit()
            return product.id

    @staticmethod
    @database_operation
    def get_product(product_url: str) -> Products.id:
        with db_session() as session:
            product = session.query(Products).filter_by(url=product_url).first()
            return product.id if product else None

    @staticmethod
    @database_operation
    def set_new_product_price(row_id: int, new_price: float):
        with db_session() as session:
            product = session.query(Products).get(row_id)

            if product:
                product.last_price = new_price
                session.commit()
            else:
                logger.info(f'Ошибка изменения строки {row_id}')


class UserProductsCRUD:
    @staticmethod
    @database_operation
    def get_user_products(telegram_id: int = None):
        with db_session() as session:
            if telegram_id:
                result = (
                    session.query(UserProducts, Users, Products)
                    .join(Users, UserProducts.user == Users.id)
                    .filter(Users.telegram_id == telegram_id)
                    .join(Products, UserProducts.product == Products.id)
                    .all()
                )
                return result

            result = (
                session.query(UserProducts, Users, Products)
                .join(Users, UserProducts.user == Users.id)
                .join(Products, UserProducts.product == Products.id)
                .all()
            )
            return result

    @staticmethod
    @database_operation  # когда пользователь скидывает ссылку и выбирает что с товаром делать
    def add_user_product(telegram_id: int, product_url: str, is_take_into_account_bonuses: bool,
                         threshold_price: float, last_product_price: float, product_name: str, is_any_change: bool):
        with db_session() as session:
            user_id = UsersCRUD.get_user(telegram_id=telegram_id)
            if user_id is None:
                user_id = UsersCRUD.add_new_user(telegram_id=telegram_id)

            product_id = ProductsCRUD.get_product(product_url=product_url)
            if product_id is None:
                product_id = ProductsCRUD.add_new_product(product_url=product_url,
                                                          product_name=product_name,
                                                          last_price=last_product_price)

            user_product = UserProducts(user=user_id, product=product_id, is_any_change=is_any_change,
                                        threshold_price=threshold_price,
                                        is_take_into_account_bonuses=is_take_into_account_bonuses)
            session.add(user_product)
            session.commit()

    @staticmethod
    @database_operation
    def delete_user_products(user_product_id: int):
        with db_session() as session:
            user_product = session.query(UserProducts).get(user_product_id)

            if user_product:
                session.delete(user_product)
                session.commit()

            return user_product
