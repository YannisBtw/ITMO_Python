import unittest
from models.currency import Currency


class TestCurrencyModel(unittest.TestCase):

    def test_create_valid_currency(self):
        c = Currency(
            currency_id=1,
            char_code="USD",
            value=92.5,
            nominal=1,
            num_code="840",
            name="Доллар США",
        )
        self.assertEqual(c.id, 1)
        self.assertEqual(c.char_code, "USD")
        self.assertEqual(c.value, 92.5)
        self.assertEqual(c.nominal, 1)
        self.assertEqual(c.num_code, "840")
        self.assertEqual(c.name, "Доллар США")

    def test_invalid_value_raises(self):
        """Отрицательный курс должен вызывать ValueError."""
        with self.assertRaises(ValueError):
            Currency(
                currency_id=1,
                char_code="USD",
                value=-5,
                nominal=1,
            )

    def test_invalid_char_code(self):
        """Символьный код должен быть 2–5 символов."""
        with self.assertRaises(ValueError):
            Currency(
                currency_id=1,
                char_code="U",
                value=80,
                nominal=1,
            )
