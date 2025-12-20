"""Итерация 2 - оптимизация с помощью потоков (ThreadPoolExecutor).

Смысл:
- делим [a, b] на n_jobs частей
- каждый поток считает свой кусок
- складываем результаты

Важно:
Для CPU-bound кода на чистом Python потоки обычно не дают ускорения из-за GIL.
"""

from __future__ import annotations

import concurrent.futures as ftres
import math
import timeit
from functools import partial
from typing import Callable

from integrate_base import integrate


def integrate_async(
        f: Callable[[float], float],
        a: float,
        b: float,
        *,
        n_jobs: int = 2,
        n_iter: int = 100_000,
        verbose: bool = False
) -> float:
    """Параллельное интегрирование с потоками."""
    if not isinstance(n_jobs, int) or n_jobs <= 0:
        raise ValueError("n_jobs должно быть положительным целым числом")
    if not isinstance(n_iter, int) or n_iter <= 0:
        raise ValueError("n_iter должно быть положительным целым числом")

    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)
    spawn = partial(executor.submit, integrate, f,
                    n_iter=max(1, n_iter // n_jobs))

    step = (b - a) / n_jobs
    if verbose:
        for i in range(n_jobs):
            print(
                f"Работник {i}, границы: {a + i * step}, {a + (i + 1) * step}")

    futures = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]

    try:
        return sum(f.result() for f in ftres.as_completed(futures))
    finally:
        executor.shutdown(wait=True)


def benchmark() -> None:
    n = 1_000_000
    print("Итерация 2: threads")
    for jobs in (2, 4, 6, 8):
        t = timeit.timeit(
            lambda: integrate_async(math.sin, 0.0, math.pi, n_jobs=jobs,
                                    n_iter=n), number=3)
        print(f"jobs={jobs}: {t / 3:.6f} сек/запуск")


if __name__ == "__main__":
    print(integrate_async(math.sin, 0.0, math.pi, n_jobs=2, n_iter=200_000,
                          verbose=True))
    benchmark()
