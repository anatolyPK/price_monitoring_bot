import unittest
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
        num_1 = 100
        num_2 = 200

        val_1 = PriceComparer._compare(num_1, num_1)
        val_2 = PriceComparer._compare(num_1, num_2)

        self.assertTrue(val_2)
        self.assertFalse(val_1)

# // TODO test _notify_user


if __name__ == '__main__':
    unittest.main()
