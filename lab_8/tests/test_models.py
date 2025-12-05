import unittest

from models import Author, App, User, UserCurrency


class TestAuthorModel(unittest.TestCase):
    """Тесты для модели Author."""

    def test_author_getters_setters_ok(self) -> None:
        author = Author(name="Иван Иванов", group="P3120")
        self.assertEqual(author.name, "Иван Иванов")
        self.assertEqual(author.group, "P3120")

        author.name = "Пётр Петров"
        author.group = "P3130"
        self.assertEqual(author.name, "Пётр Петров")
        self.assertEqual(author.group, "P3130")

    def test_author_invalid_name_raises(self) -> None:
        author = Author(name="OK", group="P3120")
        with self.assertRaises(ValueError):
            author.name = ""

    def test_author_invalid_group_raises(self) -> None:
        author = Author(name="OK", group="P3120")
        with self.assertRaises(ValueError):
            author.group = "P1"


class TestAppModel(unittest.TestCase):
    """Тесты для модели App."""

    def test_app_getters_setters_ok(self) -> None:
        author = Author(name="Автор", group="P3120")
        app = App(name="TestApp", version="1.0", author=author)

        self.assertEqual(app.name, "TestApp")
        self.assertEqual(app.version, "1.0")
        self.assertIs(app.author, author)

        app.name = "NewName"
        app.version = "2.0"
        self.assertEqual(app.name, "NewName")
        self.assertEqual(app.version, "2.0")

    def test_app_invalid_name_raises(self) -> None:
        author = Author(name="Автор", group="P3120")
        app = App(name="TestApp", version="1.0", author=author)
        with self.assertRaises(ValueError):
            app.name = "   "

    def test_app_invalid_author_type_raises(self) -> None:
        author = Author(name="Автор", group="P3120")
        app = App(name="TestApp", version="1.0", author=author)
        with self.assertRaises(TypeError):
            app.author = "не автор"


class TestUserModel(unittest.TestCase):
    """Тесты для модели User."""

    def test_user_ok(self) -> None:
        user = User(user_id=1, name="Алиса")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "Алиса")

        user.id = 10
        user.name = "Боб"
        self.assertEqual(user.id, 10)
        self.assertEqual(user.name, "Боб")

    def test_user_invalid_id_type(self) -> None:
        with self.assertRaises(TypeError):
            User(user_id="1", name="Имя")

    def test_user_invalid_name(self) -> None:
        with self.assertRaises(ValueError):
            User(user_id=1, name="   ")


class TestUserCurrencyModel(unittest.TestCase):
    """Тесты для модели UserCurrency."""

    def test_user_currency_ok(self) -> None:
        """
        Корректное создание объекта UserCurrency
        с целочисленными идентификаторами.
        """
        uc = UserCurrency(subscription_id=1, user_id=2, currency_id=10)

        # Проверяем, что объект создался
        self.assertIsInstance(uc, UserCurrency)

        self.assertEqual(uc.user_id, 2)
        self.assertEqual(uc.currency_id, 10)

    def test_user_currency_invalid_user_id_type_constructor(self) -> None:
        """
        Если в конструктор передать user_id неправильного типа,
        должно выбрасываться исключение (в твоей реализации — ValueError).
        """
        with self.assertRaises(ValueError):
            UserCurrency(subscription_id=1, user_id="1", currency_id=10)

    def test_user_currency_invalid_currency_id_type_constructor(self) -> None:
        """
        Если в конструктор передать currency_id неправильного типа,
        также ожидаем ValueError.
        """
        with self.assertRaises(ValueError):
            UserCurrency(subscription_id=1, user_id=1, currency_id="10")

    def test_user_currency_invalid_user_id_setter(self) -> None:
        """
        Если попытаться присвоить строку в user_id уже после создания объекта,
        сеттер тоже должен выбросить ValueError.
        """
        uc = UserCurrency(subscription_id=1, user_id=1, currency_id=10)
        with self.assertRaises(ValueError):
            uc.user_id = "2"

    def test_user_currency_invalid_currency_id_setter(self) -> None:
        """
        Аналогично для currency_id: неправильный тип -> ValueError.
        """
        uc = UserCurrency(subscription_id=1, user_id=1, currency_id=10)
        with self.assertRaises(ValueError):
            uc.currency_id = "20"



if __name__ == "__main__":
    unittest.main()
