"""Итерация 3 - оптимизация с помощью процессов (ProcessPoolExecutor)."""

from __future__ import annotations

import concurrent.futures as ftres
import math
import timeit
from functools import partial
from typing import Callable

from integrate_base import integrate


def integrate_async_processes(
        f: Callable[[float], float],
        a: float,
        b: float,
        *,
        n_jobs: int = 2,
        n_iter: int = 100_000,
        verbose: bool = False
) -> float:
    """Параллельное интегрирование с процессами."""
    if not isinstance(n_jobs, int) or n_jobs <= 0:
        raise ValueError("n_jobs должно быть положительным целым числом")
    if not isinstance(n_iter, int) or n_iter <= 0:
        raise ValueError("n_iter должно быть положительным целым числом")

    executor = ftres.ProcessPoolExecutor(max_workers=n_jobs)
    spawn = partial(executor.submit, integrate, f,
                    n_iter=max(1, n_iter // n_jobs))

    step = (b - a) / n_jobs
    if verbose:
        for i in range(n_jobs):
            print(f"Процесс {i}, границы: {a + i * step}, {a + (i + 1) * step}")

    futures = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]

    try:
        return sum(f.result() for f in ftres.as_completed(futures))
    finally:
        executor.shutdown(wait=True)


def benchmark() -> None:
    n = 1_000_000
    print("Итерация 3: processes")
    for jobs in (2, 4, 6, 8):
        t = timeit.timeit(
            lambda: integrate_async_processes(math.sin, 0.0, math.pi,
                                              n_jobs=jobs, n_iter=n), number=3)
        print(f"jobs={jobs}: {t / 3:.6f} сек/запуск")


if __name__ == "__main__":
    print(integrate_async_processes(math.sin, 0.0, math.pi, n_jobs=2,
                                    n_iter=200_000, verbose=True))
    benchmark()
