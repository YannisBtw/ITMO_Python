def summ(nums, target):
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
