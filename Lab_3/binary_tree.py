from typing import Dict, List, Callable
import pprint

Tree = Dict[str, List["Tree"]]


def left_leaf(root: int) -> int:
    """Формула для левого потомка: root + root // 2"""
    return root + root // 2


def right_leaf(root: int) -> int:
    """Формула для правого потомка: root ** 2"""
    return root ** 2


def gen_bin_tree(
        height: int = 4,
        root: int = 8,
        l_b: Callable[[int], int] = left_leaf,
        r_b: Callable[[int], int] = right_leaf
) -> Tree:
    """
    Рекурсивно строит бинарное дерево в виде словаря.

    Args:
        height: высота дерева (0 = только корень)
        root: значение корневого узла
        l_b: функция для вычисления левого потомка
        r_b: функция для вычисления правого потомка

    Returns:
        Дерево в виде словаря {"значение": [левое_поддерево, правое_поддерево]}
    """
    if height < 0:
        raise ValueError("Высота должна быть >= 0")

    if height == 0:
        return {str(root): []}

    left_value = l_b(root)
    right_value = r_b(root)

    left_subtree = gen_bin_tree(height - 1, left_value, l_b, r_b)
    right_subtree = gen_bin_tree(height - 1, right_value, l_b, r_b)

    return {str(root): [left_subtree, right_subtree]}


# --- Демонстрация ---
if __name__ == "__main__":
    tree = gen_bin_tree(height=4, root=8)
    print("Бинарное дерево при root=8, height=4):")
    pprint.pprint(tree)
