import os
import unittest
from unittest.mock import patch

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()


DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

TEST_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}_test"
engine = create_engine(TEST_DATABASE_URL)
Session = sessionmaker(bind=engine)


class TestUsersCRUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from db.models import Base
        Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        from db.models import Base
        # Drop tables after all tests are done
        Base.metadata.drop_all(bind=engine)

    def setUp(self):
        # Create a new session for each test
        self.session = Session()

    def tearDown(self):
        # Roll back the session after each test
        self.session.rollback()

    def test_add_new_user(self):
        from config.database_config import DATABASE_URL
        from db.crud_operations import UsersCRUD
        from db.models import Users
        telegram_id = 123

        with self.session as session:
            user_id = UsersCRUD.add_new_user(telegram_id)
            print(DATABASE_URL)
            print(TEST_DATABASE_URL)
            assert DATABASE_URL == TEST_DATABASE_URL

            self.assertIsNotNone(user_id)
            user = session.query(Users).first()
            users = session.query(Users).all()
            print(user)
            print(users)
            # self.assertEqual(len(users), 1)
            self.assertEqual(user.id, user_id)
            # self.assertEqual(user.telegram_id, telegram_id)

    # добавление использует реальную БД. Для тестов изменить  DATABASE_URL в конфиге

    # def test_get_user(self):
    #     telegram_id = 123
    #
    #     # Создаем тестовую сессию
    #     with self.Session() as session:
    #         # Инициализируем тестовую базу данных
    #         Users.metadata.create_all(self.engine)
    #
    #         # Добавляем пользователя в тестовую базу данных
    #         new_user = Users(telegram_id=telegram_id)
    #         session.add(new_user)
    #         session.commit()
    #
    #         # Вызываем функцию
    #         user_id = UsersCRUD.get_user(session, telegram_id)
    #
    #         # Проверки
    #         self.assertIsNotNone(user_id)
    #         self.assertEqual(user_id, new_user.id)


if __name__ == '__main__':
    with patch('config.database_config.DATABASE_URL', new=TEST_DATABASE_URL):
        unittest.main()
