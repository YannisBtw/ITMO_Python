"""Итерация 5 - noGIL: замеры для 2, 4, 6 потоков и сравнение."""

from __future__ import annotations

import math
import timeit

from cython_mod import integrate_cy
from cython_mod import integrate_nogil
from iteration3_processes import integrate_async_processes


def main() -> None:
    n = 8_000_000
    print("Итерация 5 (noGIL). n_iter =", n)

    t_cy = timeit.timeit(lambda: integrate_cy.integrate_sin(0.0, math.pi, n),
                         number=3)
    print(f"cython sin (1 поток): {t_cy / 3:.6f} сек/запуск")

    for thr in (2, 4, 6):
        t = timeit.timeit(
            lambda: integrate_nogil.integrate_sin_nogil(0.0, math.pi, n, thr),
            number=3)
        print(f"cython noGIL threads={thr}: {t / 3:.6f} сек/запуск")

    for jobs in (2, 4, 6):
        t = timeit.timeit(
            lambda: integrate_async_processes(math.sin, 0.0, math.pi,
                                              n_jobs=jobs, n_iter=n), number=3)
        print(f"python processes jobs={jobs}: {t / 3:.6f} сек/запуск")


if __name__ == "__main__":
    main()
