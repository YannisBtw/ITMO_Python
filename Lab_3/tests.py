import unittest
from binary_tree import gen_bin_tree


class TestGenBinTree(unittest.TestCase):
    def test_height_zero(self):
        self.assertEqual(gen_bin_tree(0, 5), {"5": []})

    def test_height_one(self):
        tree = gen_bin_tree(1, 5, l_b=lambda x: x + 1,
                            r_b=lambda x: x ** 2)
        self.assertEqual(tree, {"5": [{"6": []}, {"25": []}]})

    def test_height_two(self):
        tree = gen_bin_tree(2, 5, l_b=lambda x: x + 1,
                            r_b=lambda x: x ** 2)
        self.assertEqual(
            tree,
            {"5": [
                {"6": [{"7": []}, {"36": []}]},
                {"25": [{"26": []}, {"625": []}]}
            ]}
        )

    def test_custom_family(self):
        tree = gen_bin_tree(1, 10, l_b=lambda x: x ** 2,
                            r_b=lambda x: 2 * (x + 4))
        self.assertEqual(tree, {"10": [{"100": []}, {"28": []}]})

    def test_diff_rules_make_diff_trees(self):
        t1 = gen_bin_tree(2, 5)
        t2 = gen_bin_tree(2, 5, l_b=lambda x: x + 1,
                          r_b=lambda x: x ** 2)
        self.assertNotEqual(t1, t2)


if __name__ == "__main__":
    unittest.main()
