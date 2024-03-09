
from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

from config.logger import setup_logger


logger = setup_logger(__name__)

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

logger.debug(os.environ.keys())
logger.debug(f'ENV {DB_USER} {DB_PASS} {DB_HOST} {DB_NAME}')

if None in [DB_USER, DB_PASS, DB_HOST, DB_NAME]:
    raise ValueError("One or more required environment variables are missing.")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
# DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}_test"

engine = create_engine(DATABASE_URL, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# engine = create_async_engine(
#     DATABASE_URL,
#     echo=True
# )
# async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
#     engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
# )


class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols = []

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f'{col}={getattr(self, col)}')
        return f'<{self.__class__.__name__} {", ".join(cols)}'

# Base.metadata.drop_all(bind
def init_db():
    from db.models import Base
    engine.echo = False
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    engine.echo = True


# ______ASYNC______________
# async def get_session() -> AsyncSession:
#     async with async_session() as session:
#         return session


# async def get_user_products(session: AsyncSession, telegram_id: int = None):
#     result = (
#         await session.execute(
#             select(UserProducts, Users, Products)
#             .join(Users, UserProducts.user == Users.id)
#             .filter(Users.telegram_id == telegram_id)
#             .join(Products, UserProducts.product == Products.id)
#         ))
#
#     return result
#
#
# async def main():
#     # Initialize the database asynchronously
#     await init_db()
#
#     # Use the asynchronous session to query user products
#     async with async_session() as session:
#         telegram_id = 5139738902  # Replace with the actual Telegram ID
#         result = await get_user_products(session, telegram_id)
#         print('WHOAAAA')
#         print([x.id for x in result.scalars().all()])
#
# if __name__ == '__main__':
#
#     asyncio.run(main())
