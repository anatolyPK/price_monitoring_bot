import unittest
from unittest.mock import MagicMock, patch

from selenium.webdriver.chrome.webdriver import WebDriver

from src.monitoring.monitoring import driver_context, start_monitoring


class TestDriverContext(unittest.TestCase):

    def test_driver_context(self):
        with driver_context() as driver:
            self.assertIsInstance(driver, WebDriver)
            self.assertIsNotNone(driver)


# class TestStartMonitoring(unittest.TestCase):
#     @patch('src.monitoring.monitoring.driver_context')
#     @patch('src.monitoring.monitoring.parse_and_compare')
#     @patch('db.crud_operations.UserProductsCRUD.get_user_products')
#     def test_start_monitoring(self, mock_get_user_products, mock_parse_and_compare, mock_driver_context):
#         mock_get_user_products.
#
#         start_monitoring()
#
#         mock_notify_user.assert_not_called()
#         mock_set_new_price.assert_not_called()

if __name__ == '__main__':
    unittest.main()
