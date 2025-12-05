"""Модель валюты и её курса."""

from __future__ import annotations


class Currency:
    """Класс, описывающий валюту и её текущий курс."""

    def __init__(
            self,
            currency_id: int | None,
            char_code: str,
            value: float,
            nominal: int = 1,
            num_code: str | None = None,
            name: str | None = None,
    ) -> None:
        """
        Создать объект валюты.

        Параметры:
            currency_id: Уникальный ID валюты или None.
            char_code: Символьный код (например, 'USD').
            value: Курс валюты.
            nominal: Номинал, за который указан курс.
            num_code: Числовой код валюты (например, '840') или None.
            name: Название валюты.
        """

        self.__id: int | None = None
        self.__num_code: str | None = None
        self.__char_code: str = ""
        self.__name: str | None = None
        self.__value: float = 0.0
        self.__nominal: int = 1

        self.id = currency_id
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def id(self) -> int | None:
        """Получить ID валюты."""
        return self.__id

    @id.setter
    def id(self, value: int | None) -> None:
        """Установить ID валюты."""
        if value is None or (isinstance(value, int) and value > 0):
            self.__id = value
        else:
            raise ValueError(
                "ID валюты должен быть положительным числом или None.")

    @property
    def num_code(self) -> str | None:
        """Получить числовой код валюты (NumCode)."""
        return self.__num_code

    @num_code.setter
    def num_code(self, value: str | None) -> None:
        """
        Установить числовой код валюты.

        NumCode может быть None или строкой из цифр.
        """
        if value is None or (isinstance(value, str) and value.isdigit()):
            self.__num_code = value
        else:
            raise ValueError("Числовой код валюты должен быть строкой из цифр.")

    @property
    def char_code(self) -> str:
        """Получить символьный код валюты (например, USD)."""
        return self.__char_code

    @char_code.setter
    def char_code(self, value: str) -> None:
        """
        Установить символьный код валюты.

        Значение должно быть строкой длиной 2–5 символов.
        """
        if isinstance(value, str) and 2 <= len(value) <= 5:
            self.__char_code = value.upper()
        else:
            raise ValueError(
                "Символьный код валюты должен содержать 2–5 символов.")

    @property
    def name(self) -> str | None:
        """Получить название валюты."""
        return self.__name

    @name.setter
    def name(self, value: str | None) -> None:
        """
        Установить название валюты.

        Название может быть None или строкой длиной ≥ 2.
        """
        if value is None or (
                isinstance(value, str) and len(value.strip()) >= 2):
            self.__name = value.strip() if value else None
        else:
            raise ValueError("Название валюты слишком короткое.")

    @property
    def value(self) -> float:
        """Получить курс валюты."""
        return self.__value

    @value.setter
    def value(self, val: float) -> None:
        """
        Установить курс валюты.

        Курс должен быть положительным числом.
        """
        if not isinstance(val, (int, float)):
            raise TypeError("Курс валюты должен быть числом (int или float).")
        if val <= 0:
            raise ValueError("Курс валюты должен быть положительным числом.")
        self.__value = float(val)

    @property
    def nominal(self) -> int:
        """Получить номинал валюты."""
        return self.__nominal

    @nominal.setter
    def nominal(self, val: int) -> None:
        """
        Установить номинал валюты.

        Номинал должен быть положительным целым числом.
        """
        if isinstance(val, int) and val > 0:
            self.__nominal = val
        else:
            raise ValueError("Номинал должен быть положительным целым числом.")
