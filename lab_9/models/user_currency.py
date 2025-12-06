"""Модель подписки пользователя на валюту."""

from __future__ import annotations


class UserCurrency:
    """Класс, представляющий подписку пользователя на конкретную валюту."""

    def __init__(
            self, subscription_id: int, user_id: int, currency_id: int) -> None:
        """
        Создать объект подписки пользователя на валюту.

        Параметры:
            subscription_id: Уникальный ID записи подписки.
            user_id: ID пользователя.
            currency_id: ID валюты.
        """
        self.__subscription_id: int = 0
        self.__user_id: int = 0
        self.__currency_id: int = 0

        self.subscription_id = subscription_id
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def subscription_id(self) -> int:
        """Получить ID подписки."""
        return self.__subscription_id

    @subscription_id.setter
    def subscription_id(self, value: int) -> None:
        """
        Установить ID подписки.

        Вызывает:
            ValueError: если ID не является положительным целым числом.
        """
        if isinstance(value, int) and value > 0:
            self.__subscription_id = value
        else:
            raise ValueError(
                "ID подписки должен быть положительным целым числом.")

    @property
    def user_id(self) -> int:
        """Получить ID пользователя."""
        return self.__user_id

    @user_id.setter
    def user_id(self, value: int) -> None:
        """
        Установить ID пользователя.

        Вызывает:
            ValueError: если ID некорректный.
        """
        if isinstance(value, int) and value > 0:
            self.__user_id = value
        else:
            raise ValueError(
                "ID пользователя должен быть положительным целым числом.")

    @property
    def currency_id(self) -> int:
        """Получить ID валюты."""
        return self.__currency_id

    @currency_id.setter
    def currency_id(self, value: int) -> None:
        """
        Установить ID валюты.

        Вызывает:
            ValueError: если ID некорректный.
        """
        if isinstance(value, int) and value > 0:
            self.__currency_id = value
        else:
            raise ValueError(
                "ID валюты должен быть положительным целым числом.")
