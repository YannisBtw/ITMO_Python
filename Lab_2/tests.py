import unittest
from guess_number import (
    seq_search,
    bin_search,
    guess_number,
)


class TestSeqSearch(unittest.TestCase):
    def test_seq_found_middle(self):
        res = seq_search(2, [1, 2, 3])
        self.assertEqual(res[0], 2)
        self.assertEqual(res[1], 2)
        self.assertEqual(res[2], [1, 2])

    def test_seq_found_first(self):
        res = seq_search(1, [1, 2, 3])
        self.assertEqual(res[0], 1)
        self.assertEqual(res[1], 1)
        self.assertEqual(res[2], [1])

    def test_seq_not_found(self):
        res = seq_search(10, [1, 2, 3])
        self.assertIsNone(res[0])
        self.assertEqual(res[1], 3)
        self.assertEqual(res[2], [1, 2, 3])


    def test_seq_empty(self):
        res = seq_search(5, [])
        self.assertIsNone(res[0])
        self.assertEqual(res[1], 0)
        self.assertEqual(res[2], [])


class TestBinSearch(unittest.TestCase):
    def test_bin_found_unsorted(self):
        res = bin_search(7, [9, 1, 7, 2, 5])
        self.assertEqual(res[0], 7)
        self.assertIn(7, res[2])
        self.assertEqual(res[1], 2)

    def test_bin_found_edges(self):
        a = [1, 2, 3, 4, 5]
        self.assertEqual(bin_search(1, a)[1], 2)
        self.assertEqual(bin_search(5, a)[1], 3)

    def test_bin_not_found(self):
        res = bin_search(6, [1, 2, 3, 4, 5])
        self.assertIsNone(res[0])
        self.assertEqual(res[1], 3)
        self.assertTrue(all(x in [1, 2, 3, 4, 5] for x in res[2]))

    def test_bin_single_element(self):
        self.assertEqual(bin_search(7, [7]), [7, 1, [7]])
        self.assertEqual(bin_search(8, [7]), [None, 1, [7]])

    def test_bin_empty(self):
        self.assertEqual(bin_search(1, []), [None, 0, []])


class TestGuessNumber(unittest.TestCase):
    def test_default_method_is_seq(self):
        res = guess_number(2, [1, 2, 3])
        self.assertEqual(res[0], 2)
        self.assertEqual(res[1], 2)
        self.assertEqual(res[2], [1, 2])

    def test_guess_seq_and_bin(self):
        seq_res = guess_number(4, [1, 4, 7], method="seq")
        bin_res = guess_number(4, [7, 1, 4], method="bin")
        self.assertEqual(seq_res[0], 4)
        self.assertEqual(bin_res[0], 4)

    def test_guess_invalid_method(self):
        with self.assertRaises(ValueError):
            guess_number(4, [1, 4, 7], method="unknown")


if __name__ == "__main__":
    unittest.main()
