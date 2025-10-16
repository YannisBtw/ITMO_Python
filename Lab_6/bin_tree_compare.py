from typing import Dict, List, Callable
import timeit
import pprint

from matplotlib import pyplot as plt

Tree = Dict[str, List["Tree"]]


def left_leaf(root: int) -> int:
    """Формула для левого потомка: root + root // 2"""
    return root + root // 2


def right_leaf(root: int) -> int:
    """Формула для правого потомка: root ** 2"""
    return root ** 2


def build_tree_recursive(
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

    left_subtree = build_tree_recursive(height - 1, left_value, l_b, r_b)
    right_subtree = build_tree_recursive(height - 1, right_value, l_b, r_b)

    return {str(root): [left_subtree, right_subtree]}


from typing import Dict, List, Callable

Tree = Dict[str, List["Tree"]]


def build_tree_iterative(
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


Tree = Dict[str, List["Tree"]]


def benchmark(
        func: Callable[
            [int, int, Callable[[int], int], Callable[[int], int]], Tree],
        *,
        height: int,
        root: int,
        left: Callable[[int], int],
        right: Callable[[int], int],
        repeat: int = 10,
        number: int = 1
) -> float:
    """Измеряет время выполнения функции, строящей дерево."""
    stmt = lambda: func(height, root, left, right)
    times = timeit.repeat(stmt, repeat=repeat, number=number)
    return min(times)


def main():
    root = 8
    left = left_leaf
    right = right_leaf

    heights = list(range(0, 9))  # 0..8

    rec_times = []
    itr_times = []

    print("Таблица времени (минимум из повторов):")
    print(f"{'height':>6} | {'recursive, ms':>13} | {'iterative, ms':>13}")
    print("-" * 40)

    for h in heights:
        t_rec = benchmark(build_tree_recursive,
                          height=h, root=root, left=left, right=right,
                          repeat=20, number=1) * 10000.0
        t_itr = benchmark(build_tree_iterative,
                          height=h, root=root, left=left, right=right,
                          repeat=20, number=1) * 10000.0

        rec_times.append(t_rec)
        itr_times.append(t_itr)

        print(f"{h:6d} | {t_rec:13.3f} | {t_itr:13.3f}")

    plt.plot(heights, rec_times, marker="o", label="Рекурсивная")
    plt.plot(heights, itr_times, marker="o", label="Нерекурсивная")
    plt.xlabel("Высота дерева")
    plt.ylabel("Время, мс")
    plt.title("Сравнение времени построения: рекурсивно vs нерекурсивно")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
