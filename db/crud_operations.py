from contextlib import contextmanager
from typing import Union

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


class UsersCRUD:
    @classmethod
    @database_operation
    def add_new_user(cls, telegram_id: int) -> int:
        cls._validate_telegram_id(telegram_id)

        with db_session() as session:
            existing_user = session.query(Users).filter_by(telegram_id=telegram_id).first()
            if existing_user:
                return existing_user.id

            new_user = Users(telegram_id=telegram_id)
            session.add(new_user)
            session.commit()
            return new_user.id

    @classmethod
    @database_operation
    def get_user_id(cls, telegram_id: int) -> int | None:
        cls._validate_telegram_id(telegram_id)

        with db_session() as session:
            user = session.query(Users).filter_by(telegram_id=telegram_id).first()
            return user.id if user else None

    @staticmethod
    def _validate_telegram_id(telegram_id: int):
        if not isinstance(telegram_id, int):
            logger.warning(f'telegram_id {telegram_id} должен быть целым числом')
            raise ValueError("telegram_id должен быть целым числом")


class ProductsCRUD:
    @classmethod
    @database_operation
    def add_new_product(cls, product_url: str, last_price: float, product_name: str) -> Products.id:

        cls._validate_product_url(product_url)
        cls._validate_last_price(last_price)
        cls._validate_product_name(product_name)

        with db_session() as session:
            product = session.query(Products).filter_by(url=product_url).first()

            if not product:
                product = Products(url=product_url, last_price=last_price, product_name=product_name)
                session.add(product)
                session.commit()
                return product.id

            product.last_price = last_price
            product.product_name = product_name
            session.commit()
            return product.id

    @classmethod
    @database_operation
    def get_product_id(cls, product_url: str) -> int | None:
        cls._validate_product_url(product_url)

        with db_session() as session:
            product = session.query(Products).filter_by(url=product_url).first()
            return product.id if product else None

    @staticmethod
    @database_operation
    def set_new_product_price(product_id: int, new_price: float):
        with db_session() as session:
            product = session.query(Products).get(product_id)

            if product:
                product.last_price = new_price
                session.commit()
            else:
                logger.info(f'Ошибка изменения строки {product_id}')

    @staticmethod
    def _validate_product_url(product_url):
        if not isinstance(product_url, str) or not product_url:
            logger.warning(f'product_url {product_url} должен быть непустой строкой')
            raise ValueError("product_url должен быть непустой строкой")

    @staticmethod
    def _validate_last_price(last_price):
        if not isinstance(last_price, (int, float)) or last_price < 0:
            logger.warning(f'last_price {last_price} должен быть неотрицательным числом')
            raise ValueError("last_price должен быть неотрицательным числом")

    @staticmethod
    def _validate_product_name(product_name):
        if not isinstance(product_name, str) or not product_name:
            logger.warning(f'product_name {product_name} должен быть неотрицательным числом')
            raise ValueError("product_name должен быть непустой строкой")


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
            user_id = UsersCRUD.get_user_id(telegram_id=telegram_id)
            if user_id is None:
                user_id = UsersCRUD.add_new_user(telegram_id=telegram_id)

            product_id = ProductsCRUD.get_product_id(product_url=product_url)
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
