"""Итерация 4 - Cython: замеры и сравнение."""

from __future__ import annotations

import math
import timeit

from cython_mod import integrate_cy
from integrate_base import integrate as integrate_py


def main() -> None:
    n = 2_000_000
    print("Итерация 4 (Cython). n_iter =", n)

    t_py = timeit.timeit(lambda: integrate_py(math.sin, 0.0, math.pi, n_iter=n),
                         number=3)
    print(f"pure python sin: {t_py / 3:.6f} сек/запуск")

    t_cy = timeit.timeit(lambda: integrate_cy.integrate_sin(0.0, math.pi, n),
                         number=3)
    print(f"cython C-level sin: {t_cy / 3:.6f} сек/запуск")

    t_pycall = timeit.timeit(
        lambda: integrate_cy.integrate_pycall(math.sin, 0.0, math.pi, n),
        number=3)
    print(f"cython loop + py-call sin: {t_pycall / 3:.6f} сек/запуск")

    print("\nКонтроль (sin должен быть около 2.0):")
    print("python:", integrate_py(math.sin, 0.0, math.pi, n_iter=200_000))
    print("cython:", integrate_cy.integrate_sin(0.0, math.pi, 200_000))


if __name__ == "__main__":
    main()
