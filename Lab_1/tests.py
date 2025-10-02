import unittest
from finding_index_pairs import summ


class TestSumm(unittest.TestCase):
    def test_example_1(self):
        self.assertEqual(summ([2, 7, 11, 15], 9), (0, 1))

    def test_example_2(self):
        self.assertEqual(summ([3, 2, 4], 6), (1, 2))

    def test_example_3(self):
        self.assertEqual(summ([3, 3], 6), (0, 1))

    def test_no_solution(self):
        self.assertIsNone(summ([1, 2, 3], 7))

    def test_single_element(self):
        self.assertIsNone(summ([5], 5))

    def test_many_pairs_minimal(self):
        self.assertEqual(summ([1, 1, 1, 1], 2), (0, 1))

    def test_negatives(self):
        self.assertEqual(summ([-3, 1, 2, -1, 4], 1), (0, 4))

    def test_empty_list(self):
        self.assertIsNone(summ([], 10))


if __name__ == "__main__":
    unittest.main()
