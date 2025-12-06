"""Контроллер для работы с базой данных SQLite.

Этот модуль содержит класс CurrencyRatesCRUD, который отвечает
за создание структуры БД и выполнение CRUD-операций (Create, Read,
Update, Delete) над таблицей currency. Контроллер является уровнем
доступа к данным (Data Access Layer) и не содержит бизнес-логики.
"""

from __future__ import annotations

import sqlite3
from typing import Iterable

from models.currency import Currency


class CurrencyRatesCRUD:
    """
    Контроллер для выполнения CRUD-операций над таблицей `currency`.

    Класс инкапсулирует работу с базой данных SQLite: создаёт необходимые
    таблицы при инициализации и предоставляет методы для вставки, чтения,
    обновления и удаления данных. Используется другими слоями приложения
    (например, контроллером бизнес-логики и веб-сервером).
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        """
        Инициализация контроллера.

        Parameters
        ----------
        connection : sqlite3.Connection
            Открытое подключение к базе данных SQLite. Может быть подключением
            к базе в памяти (:memory:) или к файлу.
        """
        self._conn = connection
        self._conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        """
        Создать структуру таблиц `user`, `currency` и `user_currency`,
        если они ещё не существуют.

        Таблица `currency` содержит данные о валютах.
        Таблица `user` содержит пользователей.
        Таблица `user_currency` реализует связь «многие ко многим»
        между пользователями и валютами.
        """
        cursor = self._conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS currency (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code  TEXT NOT NULL,
                char_code TEXT NOT NULL,
                name      TEXT NOT NULL,
                value     REAL,
                nominal   INTEGER
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_currency (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (currency_id) REFERENCES currency(id)
            );
            """
        )

        self._conn.commit()

    # ===================== CREATE =====================

    def create(self, currency: Currency) -> int:
        """
        Создать новую запись в таблице `currency`.

        Parameters
        ----------
        currency : Currency
            Экземпляр модели Currency, содержащий данные о валюте.

        Returns
        -------
        int
            Значение поля id для созданной строки.
        """
        sql = """
            INSERT INTO currency(num_code, char_code, name, value, nominal)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor = self._conn.cursor()
        cursor.execute(
            sql,
            (
                currency.num_code,
                currency.char_code,
                currency.name,
                currency.value,
                currency.nominal,
            ),
        )
        self._conn.commit()
        return int(cursor.lastrowid)

    def create_many(self, currencies: Iterable[Currency]) -> None:
        """
        Создать (добавить) несколько валют в таблицу `currency`.

        Parameters
        ----------
        currencies : Iterable[Currency]
            Коллекция моделей Currency, каждая из которых будет вставлена
            в таблицу. Все вставки выполняются одной SQL-командой executemany().
        """
        sql = """
            INSERT INTO currency(num_code, char_code, name, value, nominal)
            VALUES (:num_code, :char_code, :name, :value, :nominal)
        """

        data = [
            {
                "num_code": c.num_code,
                "char_code": c.char_code,
                "name": c.name,
                "value": c.value,
                "nominal": c.nominal,
            }
            for c in currencies
        ]

        cursor = self._conn.cursor()
        cursor.executemany(sql, data)
        self._conn.commit()


    def read_all(self) -> list[dict]:
        """
        Получить список всех валют из таблицы `currency`.

        Returns
        -------
        list[dict]
            Список словарей, где каждый словарь представляет одну строку
            таблицы `currency`. Ключи словаря соответствуют названиям столбцов.
        """
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM currency")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def get_by_char_code(self, char_code: str) -> dict | None:
        """
        Найти валюту по её символьному коду.

        Parameters
        ----------
        char_code : str
            Символьный код валюты (например, 'USD'). Регистр не важен,
            значение автоматически преобразуется к верхнему регистру.

        Returns
        -------
        dict | None
            Словарь с данными валюты, если запись существует.
            Если валюта не найдена — возвращается None.
        """
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT * FROM currency WHERE char_code = ?",
            (char_code.upper(),),
        )
        row = cursor.fetchone()
        if row is not None:
            return dict(row)
        return None


    def update(self, char_code: str, value: float) -> bool:
        """
        Обновить курс валюты по её символьному коду.

        Parameters
        ----------
        char_code : str
            Символьный код валюты, курс которой нужно обновить.
        value : float
            Новое значение курса.

        Returns
        -------
        bool
            True, если обновлена хотя бы одна строка.
            False, если валюты с таким кодом не существует.
        """
        cursor = self._conn.cursor()
        cursor.execute(
            "UPDATE currency SET value = ? WHERE char_code = ?",
            (value, char_code.upper()),
        )
        self._conn.commit()
        return cursor.rowcount > 0


    def delete(self, currency_id: int) -> bool:
        """
        Удалить валюту по её идентификатору.

        Parameters
        ----------
        currency_id : int
            Значение поля id из таблицы currency.

        Returns
        -------
        bool
            True, если одна строка была удалена.
            False, если запись не найдена.
        """
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM currency WHERE id = ?", (currency_id,))
        self._conn.commit()
        return cursor.rowcount > 0
