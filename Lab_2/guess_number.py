from typing import List, Optional


def seq_search(target: int, nums: List[int]) -> List[Optional[int] | int
                                                     | List[int]]:
    """
    Функция для поиска target с помощью последовательного поиска:
    Проверяет элементы по одному слева направо.

    Args:
        target: Искомое число
        nums: Список чисел, в котором ищем.

    Returns:
        [найденное число или None, количество попыток, список проверенных чисел]
    """
    attempts = 0
    checked = []
    for x in nums:
        attempts += 1
        checked.append(x)
        if x == target:
            return [target, attempts, checked]
    return [None, attempts, checked]


def bin_search(target: int, nums: List[int]) -> List[Optional[int] | int
                                                     | List[int]]:
    """
    Функция для поиска target с помощью бинарного поиска по отсортированной
    копии списка.

    Args:
        target: Искомое число
        nums: Список чисел (может быть неотсортирован).

    Returns:
        [найденное число или None, количество попыток, список проверенных чисел]
    """
    a = sorted(nums)
    left, right = 0, len(a) - 1
    attempts = 0
    checked = []

    while left <= right:
        mid = (left + right) // 2
        attempts += 1
        checked.append(a[mid])
        if a[mid] == target:
            return [target, attempts, checked]
        elif a[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return [None, attempts, checked]


def guess_number(target: int, nums: List[int], method: str = "seq") -> List[
    Optional[int] | int | List[int]]:
    """
    Угадывает число target в списке nums выбранным способом. Если выбор не был
    сделан, то будет использован последовательный поиск.

    Args:
        target: Искомое число
        nums: Список чисел
        method: "seq" для последовательного поиска или "bin" для бинарного.

    Returns:
        [найденное число или None, количество попыток, список проверенных чисел]
    """
    if method == "seq":
        return seq_search(target, nums)
    elif method == "bin":
        return bin_search(target, nums)
    else:
        raise ValueError(
            "Неизвестный метод поиска. Используйте 'seq' или 'bin'.")


def get_user_input() -> tuple[int, list[int], str]:
    """
    Ввод данных от пользователя и выбор метода поиска.
    """
    target = int(input("Введите число для поиска: "))
    start_range = int(input("Введите начало диапазона: "))
    end_range = int(input("Введите конец диапазона: "))
    method = input("Выберите метод (seq/bin): ").strip().lower()

    nums = list(range(start_range, end_range + 1))

    return target, nums, method


def main() -> None:
    """
    Основная функция: получает данные, вызывает поиск и выводит результат.
    """

    target, nums, method = get_user_input()
    result = guess_number(target, nums, method)

    found, attempts, checked = result
    print(f"Результат: {found}, попыток: {attempts}")
    print(f"Проверенные числа: {checked}")


if __name__ == "__main__":
    main()
