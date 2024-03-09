import datetime
from typing import Annotated

from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, func, BigInteger, text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped

from config.database_config import Base


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.utcnow)
]


class TimestampMixin:
    id: Mapped[intpk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class Users(Base, TimestampMixin):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(unique=True)

    users_product: Mapped[list['UserProducts']] = relationship()


class Products(Base, TimestampMixin):
    __tablename__ = 'products'

    product_name: Mapped[str] = mapped_column(String(256))
    url: Mapped[str] = mapped_column(String(512), unique=True)
    last_price: Mapped[int]

    user_product: Mapped[list['UserProducts']] = relationship()


class UserProducts(Base, TimestampMixin):
    __tablename__ = 'user_products'

    user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    product: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
    is_any_change: Mapped[bool]
    threshold_price: Mapped[int]
    is_take_into_account_bonuses: Mapped[bool]

    users: Mapped['Users'] = relationship(back_populates='users_product')
    products: Mapped['Products'] = relationship(back_populates='user_product')

