"""
Пакет моделей предметной области приложения.

Содержит классы:
- Author — автор приложения
- App — информация о приложении
- User — пользователь
- Currency — валюта и её курс
- UserCurrency — подписка пользователя на валюту
"""

from .app import App
from .author import Author
from .currency import Currency
from .user import User
from .user_currency import UserCurrency

__all__ = ["Author", "App", "User", "Currency", "UserCurrency"]
