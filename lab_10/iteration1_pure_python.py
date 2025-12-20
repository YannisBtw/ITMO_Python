"""Итерация 1 - базовая версия на чистом Python.

Требования:
- docstring + type hints + doctest: integrate_base.py
- unit-тесты: tests/
- замеры времени: этот файл и/или bench_all.py
"""

from __future__ import annotations

import math
import timeit

from integrate_base import integrate


def benchmark() -> None:
    print("Итерация 1: pure python")
    for n in (10_000, 50_000, 100_000, 300_000, 1_000_000):
        t = timeit.timeit(lambda: integrate(math.sin, 0.0, math.pi, n_iter=n),
                          number=5)
        print(f"n_iter={n:>8}: {t / 5:.6f} сек/запуск")


if __name__ == "__main__":
    print("Проверка sin:", integrate(math.sin, 0.0, math.pi, n_iter=200_000))
    print("Проверка cos:", integrate(math.cos, 0.0, math.pi, n_iter=200_000))
    benchmark()
