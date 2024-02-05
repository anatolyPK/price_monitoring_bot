import os
import unittest

from dotenv import load_dotenv
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from db.models import Base, Users, Products, UserProducts


load_dotenv()


DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}_test"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        # Drop tables after all tests are done
        Base.metadata.drop_all(bind=engine)

    def setUp(self):
        # Create a new session for each test
        self.session = Session()

    def tearDown(self):
        # Roll back the session after each test
        self.session.rollback()

    def test_users_model(self):
        user = Users(telegram_id=123456789)
        self.session.add(user)
        self.session.commit()
        retrieved_user = ((self.session.query(Users).
                          order_by(desc(Users.created_at)))
                          .first())
        self.assertEqual(retrieved_user.telegram_id, 123456789)

    def test_products_model(self):
        product = Products(url='https://example.com/product1', last_price=29.99)
        self.session.add(product)
        self.session.commit()

        retrieved_product = self.session.query(Products).first()
        self.assertEqual(retrieved_product.url, 'https://example.com/product1')
        self.assertEqual(retrieved_product.last_price, 29.99)

    def test_user_products_model(self):
        user = Users(telegram_id=987654321)
        product = Products(url='https://example.com/product2', last_price=19.99)

        self.session.add_all([user, product])
        self.session.commit()

        user_product = UserProducts(user=user.id, product=product.id, is_any_change=True, threshold_price=15.0)
        self.session.add(user_product)
        self.session.commit()

        retrieved_user_product = (
            self.session.query(UserProducts, Users, Products)
            .join(Users, UserProducts.user == Users.id)
            .join(Products, UserProducts.product == Products.id)
            .first()
        )

        user_products, users, products = retrieved_user_product
        self.assertEqual(users.telegram_id, 987654321)
        self.assertEqual(products.url, 'https://example.com/product2')
        self.assertTrue(user_products.is_any_change)
        self.assertEqual(user_products.threshold_price, 15.0)


if __name__ == '__main__':
    unittest.main()
