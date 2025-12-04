from __future__ import annotations

import io
import unittest

from logging_utils import (
    get_currencies,
    logger,
    solve_quadratic,
)

MAX_RATE_VALUE = 1000.0


class TestGetCurrencies(unittest.TestCase):
    """Тесты бизнес-логики функции get_currencies."""

    def test_real_usd_rate(self) -> None:
        """Проверяем, что курс USD возвращается и имеет разумное значение."""
        data = get_currencies(["USD"])
        self.assertIn("USD", data)
        self.assertIsInstance(data["USD"], float)
        self.assertGreaterEqual(data["USD"], 0.0)
        self.assertLessEqual(data["USD"], MAX_RATE_VALUE)

    def test_missing_currency_raises_key_error(self) -> None:
        """Неизвестная валюта должна вызывать KeyError."""
        with self.assertRaises(KeyError):
            get_currencies(["NON_EXISTENT_CURRENCY_CODE"])

    def test_connection_error(self) -> None:
        """
        Неверный URL должен приводить к ConnectionError.

        В реальном тесте лучше мокать requests.get,
        но для простоты используем заведомо некорректный URL.
        """
        with self.assertRaises(ConnectionError):
            get_currencies(["USD"], url="https://invalid-url")


class TestLoggerDecorator(unittest.TestCase):
    """Тестирование поведения декоратора logger через io.StringIO."""

    def setUp(self) -> None:
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def test_function(x: int) -> int:
            return x * 2

        @logger(handle=self.stream)
        def failing_function() -> None:
            raise ValueError("triple T big sahur")

        self.test_function = test_function
        self.failing_function = failing_function

    def test_logging_success(self) -> None:
        """При успешном выполнении должны быть INFO-логи о старте и завершении."""
        result = self.test_function(3)
        self.assertEqual(result, 6)

        logs = self.stream.getvalue()
        self.assertIn("INFO:", logs)
        self.assertIn("Calling test_function", logs)
        self.assertIn("returned 6", logs)

        print("\n=== SUCCESS LOGS ===")
        print(logs)


    def test_logging_error_and_exception_propagation(self) -> None:
        """При ошибке должен быть ERROR и исключение проброшено дальше."""
        with self.assertRaises(ValueError):
            self.failing_function()

        logs = self.stream.getvalue()
        self.assertIn("ERROR:", logs)
        self.assertIn("ValueError", logs)
        self.assertIn("triple T big sahur", logs)

        print("\n=== ERROR LOGS ===")
        print(logs)


class TestStreamWriteExample(unittest.TestCase):
    """
    Пример теста с контекстом из задания.

    Используем декоратор logger и StringIO.
    """

    def setUp(self) -> None:
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def wrapped() -> dict[str, float]:
            return get_currencies(["USD"],
                                  url="https://invalid-url")

        self.wrapped = wrapped

    def test_logging_error(self) -> None:
        """Проверяем, что ошибка логируется и исключение пробрасывается."""
        with self.assertRaises(ConnectionError):
            self.wrapped()

        logs = self.stream.getvalue()
        self.assertIn("ERROR:", logs)
        self.assertIn("ConnectionError", logs)

        print("\n=== STREAM LOGS ===")
        print(logs)


class TestSolveQuadratic(unittest.TestCase):
    """Краткая проверка solve_quadratic."""

    def test_two_roots(self) -> None:
        """Уравнение x^2 - 3x + 2 = 0 имеет два корня: 1 и 2."""
        roots = solve_quadratic(1, -3, 2)
        self.assertIsNotNone(roots)
        self.assertAlmostEqual(sorted(roots)[0], 1.0)
        self.assertAlmostEqual(sorted(roots)[1], 2.0)

    def test_negative_discriminant(self) -> None:
        """При d < 0 возвращается None."""
        roots = solve_quadratic(1, 0, 1)
        self.assertIsNone(roots)

    def test_invalid_coefficients(self) -> None:
        """Некорректные коэффициенты должны вызывать исключения."""
        with self.assertRaises(TypeError):
            solve_quadratic("abc", 2, 3)

        with self.assertRaises(ValueError):
            solve_quadratic(0, 0, 1)


if __name__ == "__main__":
    unittest.main()
