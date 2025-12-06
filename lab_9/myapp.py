from __future__ import annotations

import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from jinja2 import Environment, PackageLoader, select_autoescape, TemplateError

from controllers.currencycontroller import CurrencyController
from controllers.databasecontroller import CurrencyRatesCRUD
from models import Author, App, User, Currency
from utils.currencies_api import file_logged_get_currencies

main_author = Author(name="Ломаченко Ян", group="P3120")
app_info = App(name="CurrenciesListApp", version="1.0", author=main_author)

users: list[User] = [
    User(user_id=1, name="Субо"),
    User(user_id=2, name="LEBROOOON"),
    User(user_id=3, name="Чарли"),
    User(user_id=4, name="Шовхал"),
    User(user_id=5, name="Triple T big Sahur"),
    User(user_id=6, name="Монтгомери"),
]

CURRENCY_CODES: list[str] = [
    "USD", "EUR", "GBP", "AUD", "THB", "VND",
    "CNY", "IDR", "UAH", "AED", "CAD", "JPY",
]

env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape(["html", "xml"]),
)


def render_template(template_name: str, context: dict) -> str:
    """
    Отрендерить HTML-шаблон с переданными данными.

    Parameters
    ----------
    template_name : str
        Имя файла шаблона (например, "index.html").
    context : dict
        Данные, которые передаются в шаблон.
    """
    template = env.get_template(template_name)
    return template.render(**context)


conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row

db = CurrencyRatesCRUD(conn)
currency_controller = CurrencyController(db)


def init_db_with_currencies() -> None:
    """
    Загрузить курсы валют из API и заполнить таблицу currency.

    Вызывается один раз при старте приложения.
    """
    try:
        rates = file_logged_get_currencies(CURRENCY_CODES)
    except Exception as exc:
        print(f"[INIT] Ошибка доступа к API: {exc}")
        return

    cursor = conn.cursor()
    cursor.execute("DELETE FROM currency")
    conn.commit()

    currencies: list[Currency] = []
    for code, info in rates.items():
        c = Currency(
            currency_id=None,
            char_code=str(info["char_code"]),
            value=float(info["value"]),
            nominal=int(info["nominal"]),
            num_code=str(info["num_code"]),
            name=str(info["name"]),
        )
        currencies.append(c)

    if currencies:
        currency_controller.add_many(currencies)
        print(f"[INIT] Добавлено валют: {len(currencies)}")


def init_db_with_users_and_subscriptions() -> None:
    """
    Заполнить таблицы user и user_currency начальными данными.

    Пользователи берутся из списка `users`,
    подписки задаются в словаре subscriptions.
    """
    cursor = conn.cursor()

    cursor.execute("DELETE FROM user")
    cursor.execute("DELETE FROM user_currency")
    conn.commit()

    user_rows = [(u.id, u.name) for u in users]
    cursor.executemany("INSERT INTO user(id, name) VALUES (?, ?)", user_rows)

    cursor.execute("SELECT id, char_code FROM currency")
    code_to_id: dict[str, int] = {
        row["char_code"]: row["id"] for row in cursor.fetchall()
    }

    if not code_to_id:
        print("[INIT] Таблица currency пуста, подписки не созданы.")
        return

    subscriptions: dict[int, list[str]] = {
        1: ["USD", "EUR"],
        2: ["USD", "GBP"],
        3: ["EUR", "JPY"],
        4: ["THB"],
        5: ["AUD", "CAD"],
        6: ["CNY", "VND"],
    }

    user_currency_rows: list[tuple[int, int]] = []
    for user_id, codes in subscriptions.items():
        for code in codes:
            currency_id = code_to_id.get(code)
            if currency_id is not None:
                user_currency_rows.append((user_id, currency_id))

    if user_currency_rows:
        cursor.executemany(
            "INSERT INTO user_currency(user_id, currency_id) VALUES (?, ?)",
            user_currency_rows,
        )
        conn.commit()

    print(
        f"[INIT] Users: {len(user_rows)}, "
        f"subscriptions: {len(user_currency_rows)}",
    )


def get_user_with_currencies(user_id: int) -> tuple[dict | None, list[dict]]:
    """
    Вернуть пользователя и список валют, на которые он подписан.

    Returns
    -------
    (user, currencies)
        user : dict | None
            Пользователь из таблицы user или None, если не найден.
        currencies : list[dict]
            Список валют из таблицы currency.
    """
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
    user_row = cursor.fetchone()
    if user_row is None:
        return None, []

    cursor.execute(
        """
        SELECT c.*
        FROM currency AS c
        JOIN user_currency AS uc ON uc.currency_id = c.id
        WHERE uc.user_id = ?
        """,
        (user_id,),
    )
    rows = cursor.fetchall()

    return dict(user_row), [dict(r) for r in rows]


init_db_with_currencies()
init_db_with_users_and_subscriptions()


class MyRequestHandler(BaseHTTPRequestHandler):
    """
    Обработчик HTTP-запросов.

    Реализованы маршруты:

      /                       — главная страница (index.html)
      /author                 — страница об авторе (author.html)
      /users                  — список пользователей (users.html)
      /user?id=...            — профиль пользователя (user.html)
      /currencies             — список валют (currencies.html)
      /currency/delete?id=... — удалить валюту по id
      /currency/update?USD=...— обновить курс валюты
      /currency/show          — вывести список валют в консоль
    """

    def do_GET(self) -> None:
        """Обработка всех GET-запросов."""
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        try:
            if path == "/":
                self.handle_index()
            elif path == "/author":
                self.handle_author()
            elif path == "/users":
                self.handle_users()
            elif path == "/user":
                self.handle_user()
            elif path == "/currencies":
                self.handle_currencies()
            elif path == "/currency/delete":
                self.handle_currency_delete()
            elif path == "/currency/update":
                self.handle_currency_update()
            elif path == "/currency/show":
                self.handle_currency_show()
            elif path == "/subscription/delete":
                self.handle_subscription_delete()
            elif path == "/subscription/add":
                self.handle_subscription_add()
            else:
                self.send_error(404, "Not Found")
        except TemplateError as exc:
            print("[TEMPLATE ERROR]", exc)
            self.send_error(500, "Template error")
        except Exception as exc:  # noqa: BLE001
            print("[UNHANDLED ERROR]", exc)
            self.send_error(500, "Internal Server Error")

    def handle_index(self) -> None:
        """
        Главная страница '/'.

        Требование задания:
        - вывести информацию об авторе;
        - вывести список валют (можно кратко).
        """
        currencies = currency_controller.list_currencies()

        html = render_template(
            "index.html",
            {
                "myapp": app_info.name,
                "author_name": main_author.name,
                "group": main_author.group,
                "currencies": currencies,
            },
        )
        self._send_html(html)

    def handle_author(self) -> None:
        """Страница об авторе '/author'."""
        html = render_template(
            "author.html",
            {
                "myapp": app_info.name,
                "author_name": main_author.name,
                "group": main_author.group,
            },
        )
        self._send_html(html)

    def handle_users(self) -> None:
        """Страница со списком пользователей '/users'."""
        html = render_template(
            "users.html",
            {"myapp": app_info.name, "users": users},
        )
        self._send_html(html)

    def handle_user(self) -> None:
        """
        Страница одного пользователя '/user?id=...'.

        Показывает данные пользователя и список валют,
        на которые он подписан.
        """
        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)

        user_id_str = params.get("id", [None])[0]
        try:
            user_id = int(user_id_str)
        except (TypeError, ValueError):
            self.send_error(400, "Bad Request")
            return

        user, currencies = get_user_with_currencies(user_id)
        if user is None:
            self.send_error(404, "Not Found")
            return

        all_currencies = currency_controller.list_currencies()

        html = render_template(
            "user.html",
            {
                "myapp": app_info.name,
                "user": user,
                "currencies": currencies,
                "all_currencies": all_currencies,
            },
        )
        self._send_html(html)

    def handle_currencies(self) -> None:
        """
        Страница со списком валют '/currencies'.

        Данные берутся из базы данных SQLite через CurrencyController.
        """
        currencies = currency_controller.list_currencies()
        html = render_template(
            "currencies.html",
            {"myapp": app_info.name, "currencies": currencies},
        )
        self._send_html(html)

    def handle_currency_delete(self) -> None:
        """
        Маршрут '/currency/delete?id=...'.

        Удаляет валюту по её идентификатору и делает редирект на /currencies.
        """
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        raw_id = params.get("id", [None])[0]
        try:
            currency_id = int(raw_id)
        except (TypeError, ValueError):
            self.send_error(400, "Bad Request")
            return

        currency_controller.delete_currency(currency_id)
        self._redirect("/currencies")

    def handle_currency_update(self) -> None:
        """
        Маршрут '/currency/update?USD=95.5'.

        Ожидается, что в строке запроса будет один параметр:
        имя параметра — символьный код валюты (например, USD),
        значение параметра — новый курс (float).
        """
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if not params:
            self.send_error(400, "Bad Request")
            return

        (code, values), = params.items()
        try:
            value = float(values[0])
        except (TypeError, ValueError):
            self.send_error(400, "Bad Request")
            return

        currency_controller.update_currency(code, value)
        self._redirect("/currencies")

    def handle_currency_show(self) -> None:
        """
        Маршрут '/currency/show'.

        Выводит список валют в консоль (для отладки)
        и отдаёт простую HTML-страницу.
        """
        currencies = currency_controller.list_currencies()

        print("\n=== ТЕКУЩИЕ ВАЛЮТЫ ===")
        for c in currencies:
            print(
                f"{c['id']} | {c['char_code']} | "
                f"{c['name']} | {c['value']}",
            )

        html = (
            "<h1>Список валют выведен в консоль сервера.</h1>"
            "<p><a href='/currencies'>Вернуться к списку валют</a></p>"
        )
        self._send_html(html)

    def handle_subscription_delete(self) -> None:
        """Удалить подписку пользователя на валюту."""
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        try:
            user_id = int(params.get("user_id", [None])[0])
            currency_id = int(params.get("currency_id", [None])[0])
        except (TypeError, ValueError):
            self.send_error(400, "Bad Request")
            return

        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM user_currency WHERE user_id = ? AND currency_id = ?",
            (user_id, currency_id),
        )
        conn.commit()

        self._redirect(f"/user?id={user_id}")

    def handle_subscription_add(self) -> None:
        """Добавить подписку пользователя на валюту по CharCode."""
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        try:
            user_id = int(params.get("user_id", [None])[0])
            char_code = params.get("char_code", [None])[0]
        except (TypeError, ValueError):
            self.send_error(400, "Bad Request")
            return

        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM currency WHERE char_code = ?",
            (char_code,),
        )
        row = cursor.fetchone()
        if row is None:
            self.send_error(404, "Not Found")
            return

        currency_id = row["id"]
        cursor.execute(
            "INSERT OR IGNORE INTO user_currency(user_id, currency_id) VALUES (?, ?)",
            (user_id, currency_id),
        )
        conn.commit()

        self._redirect(f"/user?id={user_id}")

    def _send_html(self, html: str, status: int = 200) -> None:
        """Отправить готовый HTML-код клиенту."""
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _redirect(self, location: str) -> None:
        """Сделать HTTP-редирект на указанный путь."""
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()


def run_server(host: str = "localhost", port: int = 8080) -> None:
    """Запустить HTTP-сервер."""
    httpd = HTTPServer((host, port), MyRequestHandler)
    print(f"Сервер запущен: http://{host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nВыключение сервера…")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    run_server()
