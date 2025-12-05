"""Инструменты для работы с API курсов валют ЦБ РФ."""

from __future__ import annotations

import functools
import logging
import sys
from typing import Any, Callable, Iterable, TextIO

import requests

LoggerOrStream = logging.Logger | TextIO
FuncType = Callable[..., Any]


def logger(func: FuncType | None = None, *,
           handle: LoggerOrStream = sys.stdout) -> FuncType:
    """
    Декоратор для логирования вызовов функций.

    Поддерживает три варианта аргумента ``handle``:

    1. Обычный поток вывода (по умолчанию): ``sys.stdout``.
    2. Любой файловый поток (например, ``io.StringIO()``).
    3. Объект ``logging.Logger``.

    Вариант выбирается автоматически:

    * если ``handle`` является экземпляром ``logging.Logger``,
      то используются методы ``info()`` и ``error()``;
    * иначе предполагается, что это файловый поток с методом ``write()``.

    При вызове функции логируются:

    * INFO: старт вызова + аргументы;
    * INFO: успешное завершение + результат.

    При возникновении исключения:

    * ERROR: тип и текст исключения;
    * исключение пробрасывается дальше без изменения типа.

    Параметризуемый декоратор: может использоваться как
    ``@logger`` и как ``@logger(handle=...)``.
    """

    def _decorate(fn: FuncType) -> FuncType:
        if isinstance(handle, logging.Logger):
            info = handle.info
            error = handle.error
        else:

            def info(message: str) -> None:
                handle.write(f"INFO: {message}\n")

            def error(message: str) -> None:
                handle.write(f"ERROR: {message}\n")

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            info(f"Вызов {fn.__name__} с args={args}, kwargs={kwargs}")
            try:
                result = fn(*args, **kwargs)
            except Exception as e:
                error(
                    f"Функция {fn.__name__} завершилась с исключением"
                    f" {type(e).__name__}: {e}")
                raise
            else:
                info(f"{fn.__name__} вернула {result!r}")
                return result

        return wrapper

    if func is None:
        return _decorate
    return _decorate(func)


def get_currencies(
        currency_codes: Iterable[str],
        url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
        timeout: float = 5.0,
) -> dict[str, float]:
    """
    Получить курсы указанных валют с API ЦБ РФ.

    Параметры
    ---------
    currency_codes:
        Итерируемый объект с символьными кодами валют
        (например, ['USD', 'EUR']).
    url:
        URL API ЦБ РФ или тестовый URL.
    timeout:
        Таймаут HTTP-запроса в секундах.

    Возвращает
    ----------
    dict[str, float]
        Словарь вида {"USD": 93.25, "EUR": 101.7}.

    Исключения
    ----------
    ConnectionError
        Если API недоступен или произошла сетевая ошибка.
    ValueError
        Если ответ не удаётся распарсить как корректный JSON.
    KeyError
        Если отсутствует ключ "Valute" или указанная валюта.
    TypeError
        Если курс валюты имеет некорректный тип (не число).
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ошибка при запросе к API: {e}") from e

    try:
        data = response.json()
    except ValueError as e:
        raise ValueError("Некорректный JSON в ответе API") from e

    try:
        valute_dict = data["Valute"]
    except KeyError as e:
        raise KeyError('В ответе JSON отсутствует ключ "Valute"') from e

    result: dict[str, float] = {}
    for code in currency_codes:
        try:
            currency_info = valute_dict[code]
        except KeyError as e:
            raise KeyError(f"Валюта {code!r} отсутствует в данных API") from e

        value = currency_info.get("Value")
        if not isinstance(value, (int, float)):
            raise TypeError(f"Курс валюты {code!r} имеет неверный тип:"
                            f" {type(value).__name__}"
            )

        result[code] = float(value)

    return result


@logger
def logged_get_currencies(
        currency_codes: Iterable[str],
        url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
        timeout: float = 5.0,
) -> dict[str, float]:
    """
    Обёртка над get_currencies с логированием через декоратор в stdout.

    Логика получения курсов остаётся в get_currencies, здесь только логирование.
    """
    return get_currencies(currency_codes, url=url, timeout=timeout)


def setup_currency_file_logger(
        filename: str = "currency.log") -> logging.Logger:
    """
    Создать логгер для записи логов работы с валютами в файл.

    Параметры
    ---------
    filename:
        Имя файла лога.

    Возвращает
    ----------
    logging.Logger
        Настроенный логгер.
    """
    logger_obj = logging.getLogger("currency_file")
    logger_obj.setLevel(logging.INFO)

    if not logger_obj.handlers:
        file_handler = logging.FileHandler(filename, encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger_obj.addHandler(file_handler)

    return logger_obj


file_logger = setup_currency_file_logger("currency.log")


@logger(handle=file_logger)
def file_logged_get_currencies(
        currency_codes: Iterable[str],
        url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
        timeout: float = 5.0,
) -> dict[str, float]:
    """
    Обёртка над get_currencies с логированием в файл currency.log.
    """
    return get_currencies(currency_codes, url=url, timeout=timeout)
