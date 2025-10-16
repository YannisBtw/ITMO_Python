from typing import Dict, List, Callable
import pprint


Tree = Dict[str, List["Tree"]]


def gen_bin_tree(
    height: int = 4,
    root: int = 8,
    left_branch: Callable[[int], int] = lambda x: x + x // 2,
    right_branch: Callable[[int], int] = lambda x: x ** 2,
) -> Tree:
    """
    Нерекурсивно строит бинарное дерево в виде словаря:
        {"значение": [левое_поддерево, правое_поддерево]}
    Лист: {"значение": []}

    Args:
        height: высота дерева (0 — только корень)
        root: значение корня
        left_branch: функция вычисления левого потомка по значению узла
        right_branch: функция вычисления правого потомка по значению узла

    Returns:
        Tree: вложенный словарь

    Raises:
        ValueError: если height < 0
    """
    if height < 0:
        raise ValueError("Высота должна быть >= 0")

    tree: Tree = {str(root): []}
    if height == 0:
        return tree

    level_nodes: List[tuple[Tree, int]] = [(tree, root)]

    for _ in range(height):
        next_level: List[tuple[Tree, int]] = []
        for node_dict, value in level_nodes:
            lv = left_branch(value)
            rv = right_branch(value)

            left_node: Tree = {str(lv): []}
            right_node: Tree = {str(rv): []}

            node_dict[str(value)].extend([left_node, right_node])
            next_level.extend([(left_node, lv), (right_node, rv)])
        level_nodes = next_level

    return tree


if __name__ == "__main__":
    bin_tree = gen_bin_tree(height=4, root=8)
    print("Бинарное дерево при root=8, height=4):")
    pprint.pprint(bin_tree)
