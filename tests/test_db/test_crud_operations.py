import os
import unittest
from unittest.mock import patch

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.crud_operations import UsersCRUD, ProductsCRUD
from db.models import Users, Products

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
        telegram_id = 123

        with self.session as session:
            user_id = UsersCRUD.add_new_user(telegram_id)
            self.assertIsNotNone(user_id)
            self.assertIsInstance(user_id, int)

            user = session.query(Users).first()
            self.assertEqual(user.id, user_id)
            self.assertEqual(user.telegram_id, telegram_id)

            new_user_id = UsersCRUD.add_new_user(telegram_id)
            users = session.query(Users).all()
            self.assertEqual(new_user_id, user_id)
            self.assertEqual(len(users), 1)

            existing_user = session.query(Users).filter_by(telegram_id=telegram_id).first()
            self.assertEqual(existing_user.id, user_id)

    def test_get_user(self):
        telegram_id = 123

        new_user_id = UsersCRUD.add_new_user(telegram_id)
        new_user2_id = UsersCRUD.add_new_user(321)

        user_id = UsersCRUD.get_user_id(telegram_id)

        self.assertIsNotNone(user_id)
        self.assertIsInstance(user_id, int)
        self.assertEqual(user_id, new_user_id)
        self.assertNotEqual(user_id, new_user2_id)


class TestUsersCRUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from db.models import Base
        Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        from db.models import Base
        Base.metadata.drop_all(bind=engine)

    def setUp(self):
        self.session = Session()

    def tearDown(self):
        self.session.rollback()

    def test_add_new_product(self):
        product_url = "https://example.com/product"
        last_price = 100.0
        product_name = "Example Product"

        product_id = ProductsCRUD.add_new_product(product_url, last_price, product_name)

        self.assertIsNotNone(product_id)
        self.assertIsInstance(product_id, int)

        product = self.session.query(Products).filter_by(id=product_id).first()

        self.assertIsNotNone(product)
        self.assertEqual(product.url, product_url)
        self.assertEqual(product.last_price, last_price)
        self.assertEqual(product.product_name, product_name)

    def test_add_new_product_duplicate_url(self):
        product_url = "https://example.com/product"
        last_price = 100.0
        product_name = "Example Product"

        product_id_1 = ProductsCRUD.add_new_product(product_url, last_price, product_name)
        product_id_2 = ProductsCRUD.add_new_product(product_url, last_price + 10, product_name + " Updated")
        product_1 = self.session.query(Products).filter_by(url=product_url).first()
        product_2 = self.session.query(Products).filter_by(url=product_url).first()

        self.assertEqual(product_id_1, product_id_2)
        self.assertEqual(product_1.id, product_2.id)
        self.assertEqual(product_1.product_name, product_name + " Updated")
        self.assertEqual(product_1.last_price, last_price + 10)

    def test_add_new_product_invalid_input(self):
        product_url = "https://example.com/product"
        invalid_product_url = [1]
        last_price = 110.0
        invalid_last_price = -10.0
        product_name = "Invalid Product"
        invalid_product_name = 123

        with self.assertRaises(ValueError):
            ProductsCRUD.add_new_product(product_url, invalid_last_price, product_name)
        with self.assertRaises(ValueError):
            ProductsCRUD.add_new_product(invalid_product_url, last_price, product_name)
        with self.assertRaises(ValueError):
            ProductsCRUD.add_new_product(product_url, last_price, invalid_product_name)

    def test_get_product_id(self):
        product_url = 'abc'
        product_last_price = 9999
        product_name = 'AAAAA'
        product_id = ProductsCRUD.add_new_product(product_url, product_last_price, product_name)

        incorrect_product_url = 123
        non_existent_product_url = 'cba'

        product_id_bd = ProductsCRUD.get_product_id(product_url)

        self.assertEqual(product_id_bd, product_id)
        self.assertIsNone(ProductsCRUD.get_product_id(non_existent_product_url))

        with self.assertRaises(ValueError):
            ProductsCRUD.get_product_id(incorrect_product_url)


if __name__ == '__main__':
    unittest.main()
