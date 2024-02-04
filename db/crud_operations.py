from sqlalchemy.exc import SQLAlchemyError

from config.database_config import db_session
from config.logger import setup_logger
from db.models import UserProducts, Users, Products


logger = setup_logger(__name__)


def read_user_products():
    try:
        with db_session() as session:
            result = (
                session.query(UserProducts, Users, Products)
                .join(Users, UserProducts.user == Users.id)
                .join(Products, UserProducts.product == Products.id)
                .scalar()
            )
            logger.debug(result)

    except SQLAlchemyError as e:
        print(f"Ошибка базы данных: {e}")
