import threading
import time
import unittest
from http.client import HTTPConnection

from myapp import run_server


class ServerThread(threading.Thread):
    """Фоновый поток для запуска тестового сервера."""

    def __init__(self, host: str = "localhost", port: int = 8081) -> None:
        super().__init__(daemon=True)
        self.host = host
        self.port = port

    def run(self) -> None:
        run_server(host=self.host, port=self.port)


class TestControllerRoutes(unittest.TestCase):
    """Интеграционные тесты контроллера и шаблонов."""

    @classmethod
    def setUpClass(cls) -> None:
        """Запуск сервера один раз перед всеми тестами."""
        cls.host = "localhost"
        cls.port = 8081
        cls.server_thread = ServerThread(host=cls.host, port=cls.port)
        cls.server_thread.start()
        # Дадим серверу чуть-чуть времени подняться
        time.sleep(0.5)

    def _get(self, path: str) -> tuple[int, str]:
        """Вспомогательный метод: сделать GET-запрос и вернуть (status, body)."""
        conn = HTTPConnection(self.host, self.port, timeout=5)
        conn.request("GET", path)
        resp = conn.getresponse()
        body = resp.read().decode("utf-8", errors="ignore")
        conn.close()
        return resp.status, body

    def test_index_route(self) -> None:
        """Маршрут '/' должен отдавать 200 и содержать название приложения."""
        status, body = self._get("/")
        self.assertEqual(status, 200)
        self.assertIn("CurrenciesListApp", body)

    def test_users_route(self) -> None:
        """Маршрут '/users' должен отдавать 200 и содержать заголовок 'Пользователи'."""
        status, body = self._get("/users")
        self.assertEqual(status, 200)
        self.assertIn("Пользователи", body)

    def test_currencies_route(self) -> None:
        """
        Маршрут '/currencies' должен отдавать 200
        (если API доступно) или 500 при ошибке.

        В любом случае маршрут должен корректно обрабатываться,
        а не падать с исключением.
        """
        status, body = self._get("/currencies")
        self.assertIn(status, (200, 500))
        if status == 200:
            # При успешном ответе проверим, что в HTML есть слово 'Курсы'
            self.assertIn("Курсы валют", body)
        else:
            # При ошибке должен быть текст про ошибку
            self.assertIn("Ошибка при получении курсов", body)

    def test_author_route(self) -> None:
        """Маршрут '/author' должен отдавать 200 и содержать ФИО автора или группу."""
        status, body = self._get("/author")
        self.assertEqual(status, 200)
        self.assertIn("Учебная группа", body)


if __name__ == "__main__":
    unittest.main()
