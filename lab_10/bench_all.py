"""Сквозной прогон замеров и формирование таблицы результатов."""

from __future__ import annotations

import math
import timeit
from importlib import import_module

import pandas as pd

from integrate_base import integrate as integrate_py
from iteration2_threads import integrate_async as integrate_threads
from iteration3_processes import \
    integrate_async_processes as integrate_processes


def _try_import(name: str):
    try:
        return import_module(name)
    except Exception:
        return None


def main() -> None:
    n_iter = 2_000_000
    rows = []

    t = timeit.timeit(
        lambda: integrate_py(math.sin, 0.0, math.pi, n_iter=n_iter),
        number=3) / 3
    rows.append(
        dict(iteration=1, method="python", detail="baseline sin", n_jobs=1,
             n_iter=n_iter, sec=t))

    for jobs in (2, 4, 6, 8):
        t = timeit.timeit(
            lambda: integrate_threads(math.sin, 0.0, math.pi, n_jobs=jobs,
                                      n_iter=n_iter), number=3) / 3
        rows.append(
            dict(iteration=2, method="threads", detail="ThreadPoolExecutor",
                 n_jobs=jobs, n_iter=n_iter, sec=t))

    for jobs in (2, 4, 6, 8):
        t = timeit.timeit(
            lambda: integrate_processes(math.sin, 0.0, math.pi, n_jobs=jobs,
                                        n_iter=n_iter), number=3) / 3
        rows.append(
            dict(iteration=3, method="processes", detail="ProcessPoolExecutor",
                 n_jobs=jobs, n_iter=n_iter, sec=t))

    cy = _try_import("cython_mod.integrate_cy")
    if cy:
        t = timeit.timeit(lambda: cy.integrate_sin(0.0, math.pi, n_iter),
                          number=3) / 3
        rows.append(
            dict(iteration=4, method="cython", detail="C-level sin", n_jobs=1,
                 n_iter=n_iter, sec=t))

        t = timeit.timeit(
            lambda: cy.integrate_pycall(math.sin, 0.0, math.pi, n_iter),
            number=3) / 3
        rows.append(
            dict(iteration=4, method="cython", detail="loop + py-call sin",
                 n_jobs=1, n_iter=n_iter, sec=t))

    nogil = _try_import("cython_mod.integrate_nogil")
    if nogil:
        for thr in (2, 4, 6):
            t = timeit.timeit(
                lambda: nogil.integrate_sin_nogil(0.0, math.pi, n_iter, thr),
                number=3) / 3
            rows.append(dict(iteration=5, method="cython_nogil",
                             detail="OpenMP prange sin", n_jobs=thr,
                             n_iter=n_iter, sec=t))

    df = pd.DataFrame(rows).sort_values(["iteration", "method", "n_jobs"])
    df.to_csv("results.csv", index=False)

    md = df.to_markdown(index=False)
    with open("results.md", "w", encoding="utf-8") as f:
        f.write("# Результаты замеров\n\n")
        f.write(f"n_iter = {n_iter}\n\n")
        f.write(md + "\n")

    print(df)
    print("\nСохранено: results.csv, results.md")


if __name__ == "__main__":
    main()
