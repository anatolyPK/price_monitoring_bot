import unittest
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from src.monitoring.comparer import PriceComparer


class TestPriceComparer(unittest.TestCase):
    def test_compare_prices_and_notify_user_any_change_invalid_input(self):
        is_any_change = True
        invalid_is_any_change = 'yes'
        threshold_price = 500
        invalid_threshold_price = '500'
        product_last_price = 600
        invalid_product_last_price = [1]
        product_price = 400
        invalid_product_price = {'a': 1}
        product_id = 1
        invalid_product_id = 2.2
        user_id = 123
        invalid_user_id = '1'

        with self.assertRaises(ValueError):
            PriceComparer.compare_prices_and_notify_user(invalid_is_any_change,
                                                         threshold_price,
                                                         product_last_price,
                                                         product_price,
                                                         product_id,
                                                         user_id)
        with self.assertRaises(ValueError):
            PriceComparer.compare_prices_and_notify_user(is_any_change,
                                                         invalid_threshold_price,
                                                         product_last_price,
                                                         product_price,
                                                         product_id,
                                                         user_id)
        with self.assertRaises(ValueError):
            PriceComparer.compare_prices_and_notify_user(is_any_change,
                                                         invalid_threshold_price,
                                                         product_last_price,
                                                         product_price,
                                                         product_id,
                                                         user_id)
        with self.assertRaises(ValueError):
            PriceComparer.compare_prices_and_notify_user(is_any_change,
                                                         threshold_price,
                                                         invalid_product_last_price,
                                                         product_price,
                                                         product_id,
                                                         user_id)
        with self.assertRaises(ValueError):
            PriceComparer.compare_prices_and_notify_user(is_any_change,
                                                         threshold_price,
                                                         product_last_price,
                                                         invalid_product_price,
                                                         product_id,
                                                         user_id)
        with self.assertRaises(ValueError):
            PriceComparer.compare_prices_and_notify_user(is_any_change,
                                                         threshold_price,
                                                         product_last_price,
                                                         product_price,
                                                         invalid_product_id,
                                                         user_id)
        with self.assertRaises(ValueError):
            PriceComparer.compare_prices_and_notify_user(is_any_change,
                                                         threshold_price,
                                                         product_last_price,
                                                         product_price,
                                                         product_id,
                                                         invalid_user_id)

    @patch('src.monitoring.comparer.PriceComparer._notify_user')
    @patch('db.crud_operations.ProductsCRUD.set_new_product_price')
    def test_compare_prices_and_notify_user_any_change(self, mock_set_new_price, mock_notify_user):
        is_any_change = True
        threshold_price = 500
        product_last_price = 600
        product_price = 400
        product_id = 1
        user_id = 123

        PriceComparer.compare_prices_and_notify_user(is_any_change, threshold_price,
                                                     product_last_price, product_price,
                                                     product_id, user_id)

        mock_notify_user.assert_called_once()
        mock_set_new_price.assert_called_once_with(product_id=product_id, new_price=product_price)

    @patch('src.monitoring.comparer.PriceComparer._notify_user')
    @patch('db.crud_operations.ProductsCRUD.set_new_product_price')
    def test_compare_prices_and_notify_user_without_change(self, mock_set_new_price, mock_notify_user):
        is_any_change = True
        threshold_price = 500
        product_last_price = 600
        product_price = 600
        product_id = 1
        user_id = 123

        value = PriceComparer.compare_prices_and_notify_user(is_any_change, threshold_price,
                                                             product_last_price, product_price,
                                                             product_id, user_id)

        mock_notify_user.assert_not_called()
        mock_set_new_price.assert_not_called()
        self.assertIsNone(value)

    def test_compare_invalid_input(self):
        num_1 = 100
        num_2 = 200.1
        num_3 = [200]
        num_4 = '100'
        num_5 = {}

        with self.assertRaises(ValueError):
            PriceComparer._compare(num_1, num_2)

        with self.assertRaises(ValueError):
            PriceComparer._compare(num_1, num_3)

        with self.assertRaises(ValueError):
            PriceComparer._compare(num_1, num_4)

        with self.assertRaises(ValueError):
            PriceComparer._compare(num_1, num_5)

        with self.assertRaises(ValueError):
            PriceComparer._compare(num_3, num_3)

        with self.assertRaises(ValueError):
            PriceComparer._compare(num_4, num_2)

    def test_compare(self):
        num_1 = 1001
        num_2 = 200

        val_1 = PriceComparer._compare(num_1, num_1)
        val_2 = PriceComparer._compare(num_1, num_2)

        self.assertTrue(val_2)
        self.assertFalse(val_1)

# // TODO test _notify_user
    def test_validate_is_any_change(self):
        v_1 = 'as'
        v_2 = []
        v_3 = {}
        v_4 = 12
        v_5 = True

        with self.assertRaises(ValueError):
            PriceComparer._validate_is_any_change(v_1)

        with self.assertRaises(ValueError):
            PriceComparer._validate_is_any_change(v_2)

        with self.assertRaises(ValueError):
            PriceComparer._validate_is_any_change(v_3)

        with self.assertRaises(ValueError):
            PriceComparer._validate_is_any_change(v_4)

        self.assertIsNone(PriceComparer._validate_is_any_change(v_5))

    def test_validate_int(self):
        v_1 = 'as'
        v_2 = []
        v_3 = {}
        v_4 = 12
        v_5 = ()
        v_6 = 12.3

        with self.assertRaises(ValueError):
            PriceComparer._validate_int(v_1)

        with self.assertRaises(ValueError):
            PriceComparer._validate_int(v_2)

        with self.assertRaises(ValueError):
            PriceComparer._validate_int(v_3)

        with self.assertRaises(ValueError):
            PriceComparer._validate_int(v_5)

        with self.assertRaises(ValueError):
            PriceComparer._validate_int(v_6)

        self.assertIsNone(PriceComparer._validate_int(v_4))


class TestPriceComparer(IsolatedAsyncioTestCase):
    @patch('db.crud_operations.ProductsCRUD.set_new_product_price')
    async def test_compare_prices_and_notify_user_real_price_more(self, mock_set_new_price):
        is_any_change = True
        threshold_price = 500
        product_last_price = 600
        product_price = 700
        product_id = 1
        user_id = 708715576
        product_name = 'ASUS PRO MAX'
        product_url = 'www.goolge.com'

        await PriceComparer.compare_prices_and_notify_user(
            is_any_change, threshold_price, product_last_price, product_price,
            product_id, user_id, product_url, product_name
        )

        mock_set_new_price.assert_called_once()

    @patch('db.crud_operations.ProductsCRUD.set_new_product_price')
    async def test_compare_prices_and_notify_user_real_price_lower(self, mock_set_new_price):
        is_any_change = True
        threshold_price = 500
        product_last_price = 600
        product_price = 500
        product_id = 1
        user_id = 708715576
        product_name = 'ASUS PRO MAX'
        product_url = 'www.goolge.com'

        await PriceComparer.compare_prices_and_notify_user(
            is_any_change, threshold_price, product_last_price, product_price,
            product_id, user_id, product_url, product_name
        )

        mock_set_new_price.assert_called_once()


if __name__ == '__main__':
    unittest.main()
