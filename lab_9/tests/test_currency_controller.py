import unittest
from unittest.mock import MagicMock
from controllers.currencycontroller import CurrencyController


class TestCurrencyController(unittest.TestCase):

    def test_list_currencies(self):
        """Проверяем, что контроллер вызывает метод базы _read()."""

        mock_db = MagicMock()
        mock_db.read_all.return_value = [
            {"id": 1, "char_code": "USD", "value": 90.0}
        ]

        controller = CurrencyController(mock_db)
        result = controller.list_currencies()

        self.assertEqual(result[0]["char_code"], "USD")
        mock_db.read_all.assert_called_once()

    def test_update_currency(self):
        mock_db = MagicMock()

        controller = CurrencyController(mock_db)
        controller.update_currency("USD", 95.5)

        mock_db.update.assert_called_once_with("USD", 95.5)

    def test_delete_currency(self):
        mock_db = MagicMock()

        controller = CurrencyController(mock_db)
        controller.delete_currency(3)

        mock_db.delete.assert_called_once_with(3)
