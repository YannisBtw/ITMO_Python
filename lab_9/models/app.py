"""Модель приложения и его метаданных."""

from __future__ import annotations

from .author import Author


class App:
    """Класс, описывающий приложение."""

    def __init__(self, name: str, version: str, author: Author) -> None:
        """
        Создать объект приложения.

        Параметры:
            name: Название приложения.
            version: Версия приложения.
            author: Объект класса Author — автор приложения.
        """
        self.__name: str = ""
        self.__version: str = ""
        self.__author: Author | None = None

        self.name = name
        self.version = version
        self.author = author

    @property
    def name(self) -> str:
        """Получить название приложения."""
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """
        Установить название приложения.

        Вызывает:
            ValueError: при передаче пустой строки.
        """
        if isinstance(name, str) and name.strip():
            self.__name = name.strip()
        else:
            raise ValueError(
                "Ошибка: название приложения не может быть пустым.")

    @property
    def version(self) -> str:
        """Получить версию приложения."""
        return self.__version

    @version.setter
    def version(self, version: str) -> None:
        """
        Установить версию приложения.

        Вызывает:
            ValueError: при передаче пустой строки.
        """
        if isinstance(version, str) and version.strip():
            self.__version = version.strip()
        else:
            raise ValueError("Ошибка: версия приложения не может быть пустой.")

    @property
    def author(self) -> Author:
        """Получить объект автора приложения."""
        return self.__author

    @author.setter
    def author(self, author: Author) -> None:
        """
        Установить автора приложения.

        Вызывает:
            TypeError: если author не является экземпляром Author.
        """
        if isinstance(author, Author):
            self.__author = author
        else:
            raise TypeError(
                "Ошибка: author должен быть объектом класса Author.")
