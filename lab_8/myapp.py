from __future__ import annotations

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from jinja2 import Environment, PackageLoader, select_autoescape

from models import Author, App, User, Currency
from utils.currencies_api import file_logged_get_currencies


main_author = Author(name="Ломаченко Ян", group="P3120")
app_info = App(name="CurrenciesListApp", version="1.0", author=main_author)

users: list[User] = [
    User(user_id=1, name="Субо"),
    User(user_id=2, name="Магомед"),
    User(user_id=3, name="Чарли"),
    User(user_id=4, name="Шовхал"),
    User(user_id=5, name="Александра"),
    User(user_id=6, name="Монтгомери")

]

CURRENCY_CODES: list[str] = ["USD", "EUR", "GBP", "AUD", "THB", "VND", "CNY",
                             "IDR", "UAH", "AED", "CAD", "JPY"]


env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape(["html", "xml"]),
)


def render_template(template_name: str, context: dict) -> str:
    """
    Отрендерить HTML-шаблон с переданными данными.

    Parameters:
        template_name: имя файла шаблона (например, "index.html").
        context: словарь с данными, которые передаются в шаблон.
    """
    template = env.get_template(template_name)
    return template.render(**context)



class MyRequestHandler(BaseHTTPRequestHandler):
    """
    Обработчик HTTP-запросов.

    Реализует маршруты:
      /           — главная страница
      /users      — список пользователей
      /currencies — курсы валют
      /author     — страница об авторе
    """

    def do_GET(self) -> None:
        """Обработка всех GET-запросов."""
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path == "/":
            self.handle_index()
        elif path == "/users":
            self.handle_users()
        elif path == "/currencies":
            self.handle_currencies()
        elif path == "/author":
            self.handle_author()
        else:
            self.send_error(404, "Страница не найдена")


    def handle_index(self) -> None:
        """Главная страница '/'."""
        html = render_template(
            "index.html",
            {
                "myapp": app_info.name,
                "author_name": main_author.name,
                "group": main_author.group,
            },
        )
        self._send_html_response(html)

    def handle_users(self) -> None:
        """Страница со списком пользователей '/users'."""
        html = render_template(
            "users.html",
            {
                "myapp": app_info.name,
                "users": users,
            },
        )
        self._send_html_response(html)

    def handle_currencies(self) -> None:
        """Страница с курсами валют '/currencies'."""
        try:
            rates = file_logged_get_currencies(CURRENCY_CODES)
        except Exception as e:
            error_html = f"<h1>Ошибка при получении курсов валют</h1><p>{e}</p>"
            self._send_html_response(error_html, status_code=500)
            return

        currencies: list[Currency] = []
        for idx, (code, value) in enumerate(rates.items(), start=1):
            c = Currency(
                currency_id=idx,
                num_code=None,
                char_code=code,
                name=None,
                value=value,
                nominal=1,
            )
            currencies.append(c)

        html = render_template(
            "currencies.html",
            {
                "myapp": app_info.name,
                "currencies": currencies,
            },
        )
        self._send_html_response(html)

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
        self._send_html_response(html)


    def _send_html_response(self, html: str, status_code: int = 200) -> None:
        """Отправить HTML-ответ клиенту."""
        self.send_response(status_code)
        self.send_header(
            "Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


def run_server(host: str = "localhost", port: int = 8080) -> None:
    """Запустить HTTP-сервер."""
    httpd = HTTPServer((host, port), MyRequestHandler)
    print(f"Сервер запущен: http://{host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    run_server()
