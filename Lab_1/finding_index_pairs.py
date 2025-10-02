from typing import List, Optional, Tuple


def summ(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
        Находит пару индексов в списке чисел, сумма которых равна заданному числу.

        Функция перебирает все возможные пары элементов в списке `nums` и возвращает
        минимальную пару индексов `(j, i)`, таких что:
            nums[j] + nums[i] == target

        Минимальная пара означает:
        - сначала выбирается минимальный индекс j,
        - при равенстве j выбирается минимальный индекс i.

        Параметры:
            nums (List[int]): список целых чисел.
            target (int): число, которому должна быть равна сумма двух элементов.

        Возвращает:
            Optional[Tuple[int, int]]:
                - (j, i) — индексы пары, если решение найдено,
                - None — если подходящей пары нет или список слишком короткий.

        Исключения:
            TypeError: если список содержит элементы, которые нельзя складывать с int.

        Примеры:
            >>> summ([2, 7, 11, 15], 9)
            (0, 1)

            >>> summ([3, 2, 4], 6)
            (1, 2)

            >>> summ([3, 3], 6)
            (0, 1)

            >>> summ([1, 2, 3], 7) is None
            True
        """

    ans = []

    if len(nums) < 2:
        return None

    for j in range(len(nums) - 1):
        for i in range(j + 1, len(nums)):
            if nums[j] + nums[i] == target:
                ans.append((j, i))

    if not ans:
        return None

    return min(ans)


try:
    data_1 = list(
        map(int, input('Введите массив чисел через пробел: ').split()))
    data_2 = int(input('Введите число для поиска: '))
    print(summ(data_1, data_2))

except ValueError:
    print("Ошибка: вводите только целые числа через пробел!")
