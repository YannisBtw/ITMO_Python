"""Модель пользователя приложения."""

from __future__ import annotations


class User:
    """Класс, представляющий пользователя."""

    def __init__(self, user_id: int, name: str) -> None:
        """
        Создать объект пользователя.

        Параметры:
            user_id: Уникальный идентификатор пользователя.
            name: Имя пользователя.
        """
        self.__id: int = 0
        self.__name: str = ""

        self.id = user_id
        self.name = name

    @property
    def id(self) -> int:
        """Получить ID пользователя."""
        return self.__id

    @id.setter
    def id(self, user_id: int) -> None:
        """
        Установить ID пользователя.

        Вызывает:
            ValueError: если ID не является положительным целым числом.
        """
        if not isinstance(user_id, int):
            raise TypeError(
                "Ошибка: ID пользователя должен быть целым числом (int).")
        if user_id <= 0:
            raise ValueError(
                "Ошибка: ID пользователя должен быть положительным числом.")
        self.__id = user_id

    @property
    def name(self) -> str:
        """Получить имя пользователя."""
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """
        Установить имя пользователя.

        Вызывает:
            ValueError: если имя слишком короткое или не является строкой.
        """
        if isinstance(name, str) and len(name.strip()) >= 2:
            self.__name = name.strip()
        else:
            raise ValueError(
                "Ошибка: имя пользователя должно быть длиной минимум 2 символа."
            )
