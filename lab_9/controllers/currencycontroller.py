"""Контроллер бизнес-логики для работы с валютами.

Модуль содержит класс CurrencyController, который использует
CurrencyRatesCRUD для доступа к базе данных и предоставляет
удобные методы для слоя веб-приложения (myapp.py).
"""

from __future__ import annotations

from typing import Iterable

from controllers.databasecontroller import CurrencyRatesCRUD
from models.currency import Currency


class CurrencyController:
    """
    Контроллер бизнес-логики для сущности Currency.

    Данный класс не выполняет прямые SQL-запросы и не знает о структуре
    таблиц. Вместо этого он использует CurrencyRatesCRUD для работы
    с базой данных и предоставляет более высокоуровневый интерфейс
    для HTTP-обработчика и шаблонов.
    """

    def __init__(self, db: CurrencyRatesCRUD) -> None:
        """
        Инициализировать контроллер валют.

        Parameters
        ----------
        db : CurrencyRatesCRUD
            Экземпляр контроллера доступа к данным, который инкапсулирует
            работу с SQLite.
        """
        self._db = db

    def list_currencies(self) -> list[dict]:
        """
        Получить список всех валют для отображения.

        Returns
        -------
        list[dict]
            Список словарей с данными валют. Формат подходит для передачи
            напрямую в шаблон Jinja2 (currencies.html).
        """
        return self._db.read_all()

    def get_currency(self, char_code: str) -> dict | None:
        """
        Найти валюту по символьному коду.

        Parameters
        ----------
        char_code : str
            Символьный код валюты (например, 'USD').

        Returns
        -------
        dict | None
            Словарь с данными валюты или None, если запись не найдена.
        """
        return self._db.get_by_char_code(char_code)

    def add_currency(self, currency: Currency) -> int:
        """
        Добавить одну валюту в базу данных.

        Parameters
        ----------
        currency : Currency
            Экземпляр модели Currency, содержащий данные о новой валюте.

        Returns
        -------
        int
            Идентификатор созданной записи (поле id).
        """
        return self._db.create(currency)

    def add_many(self, currencies: Iterable[Currency]) -> None:
        """
        Добавить несколько валют за один вызов.

        Parameters
        ----------
        currencies : Iterable[Currency]
            Набор объектов Currency, которые нужно сохранить в базе.
        """
        self._db.create_many(currencies)

    def update_currency(self, char_code: str, value: float) -> bool:
        """
        Обновить курс валюты по её символьному коду.

        Parameters
        ----------
        char_code : str
            Символьный код валюты (например, 'USD').
        value : float
            Новое значение курса.

        Returns
        -------
        bool
            True, если курс был успешно обновлён.
            False, если валюты с таким кодом не существует.
        """
        return self._db.update(char_code, value)

    # ====================== DELETE ======================

    def delete_currency(self, currency_id: int) -> bool:
        """
        Удалить валюту по её идентификатору.

        Parameters
        ----------
        currency_id : int
            Значение поля id строки, которую нужно удалить.

        Returns
        -------
        bool
            True, если запись была удалена.
            False, если запись с таким id не найдена.
        """
        return self._db.delete(currency_id)
