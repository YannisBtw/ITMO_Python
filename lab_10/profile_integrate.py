"""Профилирование integrate() (итерация 4).

Запуск:
    python profile_integrate.py

Сохраняет profile.pstats и печатает топ-20 функций по времени.
"""

from __future__ import annotations

import cProfile
import math
import pstats

from integrate_base import integrate


def main() -> None:
    profiler = cProfile.Profile()
    profiler.enable()
    integrate(math.sin, 0.0, math.pi, n_iter=2_000_000)
    profiler.disable()

    profiler.dump_stats("profile.pstats")
    stats = pstats.Stats("profile.pstats")
    stats.strip_dirs().sort_stats("tottime").print_stats(20)


if __name__ == "__main__":
    main()
