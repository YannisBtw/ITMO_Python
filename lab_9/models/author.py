"""Модель автора приложения."""

from __future__ import annotations


class Author:
    """Класс, описывающий автора приложения."""

    def __init__(self, name: str, group: str) -> None:
        """
        Создать объект автора.

        Args:
            name: Имя автора.
            group: Учебная группа автора.
        """
        self.__name: str = ""
        self.__group: str = ""

        self.name = name
        self.group = group

    @property
    def name(self) -> str:
        """Получить имя автора."""
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """
        Установить имя автора.

        Вызывает:
            ValueError: если имя не является строкой или слишком короткое.
        """
        if isinstance(name, str) and len(name.strip()) >= 2:
            self.__name = name.strip()
        else:
            raise ValueError("Ошибка: имя автора должно содержать минимум"
                             " 2 символа.")

    @property
    def group(self) -> str:
        """Получить группу автора."""
        return self.__group

    @group.setter
    def group(self, group: str) -> None:
        """
        Установить учебную группу автора.

        Вызывает:
            ValueError: если группа указана некорректно.
        """
        if isinstance(group, str) and len(group.strip()) >= 3:
            self.__group = group.strip()
        else:
            raise ValueError("Ошибка: группа автора должна содержать минимум"
                             " 3 символа.")
