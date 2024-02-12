from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, func, BigInteger
from sqlalchemy.ext.declarative import declarative_base, declared_attr


Base = declarative_base()


class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), onupdate=func.now())


class Users(Base, TimestampMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)


class Products(Base, TimestampMixin):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(255))
    url = Column(String(500), unique=True)
    last_price = Column(Float)


class UserProducts(Base, TimestampMixin):
    __tablename__ = 'user_products'
    id = Column(Integer, primary_key=True)
    user = Column(ForeignKey('users.id'))
    product = Column(ForeignKey('products.id'))
    is_any_change = Column(Boolean)
    threshold_price = Column(Float)
    is_take_into_account_bonuses = Column(Boolean)

