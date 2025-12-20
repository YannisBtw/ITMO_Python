import math
import unittest
from integrate_base import integrate

class TestIntegrate(unittest.TestCase):
    def test_known_integral_cos(self):
        res = integrate(math.cos, 0.0, math.pi, n_iter=400_000)
        self.assertAlmostEqual(res, 0.0, places=4)

    def test_stability(self):
        low = integrate(math.sin, 0.0, math.pi, n_iter=20_000)
        high = integrate(math.sin, 0.0, math.pi, n_iter=400_000)
        self.assertLess(abs(high - 2.0), abs(low - 2.0))

if __name__ == "__main__":
    unittest.main()
