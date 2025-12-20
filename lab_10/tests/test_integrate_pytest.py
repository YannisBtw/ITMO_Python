import math
from integrate_base import integrate

def test_known_integral_sin():
    res = integrate(math.sin, 0.0, math.pi, n_iter=400_000)
    assert abs(res - 2.0) < 1e-4

def test_stability_more_iterations_better():
    low = integrate(math.sin, 0.0, math.pi, n_iter=20_000)
    high = integrate(math.sin, 0.0, math.pi, n_iter=400_000)
    assert abs(high - 2.0) < abs(low - 2.0)
