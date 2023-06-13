"""def inversion_number_2(binary_list, length):
    count = 0
    for i in range(length):
        if binary_list[i] == 1:
            for j in range(i + 1, length):
                if binary_list[j] == 0:
                    count += 1
    return count
"""


def inversion_number(binary_list, length):
    number_of_ones = 0
    count = 0
    for a in range(length):
        if binary_list[a] == 1:
            number_of_ones += 1
        else:
            count += number_of_ones
    return count


def number_of_elements_with_value_before(binary_list, length, element_index, value):
    counter = 0
    for a in range(element_index):
        if binary_list[a] == value:
            counter += 1
    return counter


def number_of_elements_with_value_after(binary_list, length, element_index, value):
    counter = 0
    for a in range(element_index + 1, length):
        if binary_list[a] == value:
            counter += 1
    return counter


n = int(input())
for i in range(n):
    length = int(input())
    numbers = [int(x) for x in input().split()]
    max_inversion_number = inversion_number(numbers, length)
    max_increase = 0


    #if numbers[0] == 0:
    #    max_increase = number_of_elements_with_value_after(numbers, length, 0, 0)
    #    print(max_inversion_number + max_increase)
    #    continue
    #elif numbers[length - 1] == 1:
    #    max_increase = number_of_elements_with_value_before(numbers, length, length - 1, 1)
    #    print(max_inversion_number + max_increase, max_increase)
    #    continue


    number_of_ones = 0
    for p in range(length):
        if numbers[p] == 1:
            number_of_ones += 1
    number_of_zeroes = length - number_of_ones

    n_after = number_of_zeroes
    n_before = 0


    for j in range(length):
        #n_after = number_of_elements_with_value_after(numbers, length, j, 0)
        #n_before = number_of_elements_with_value_before(numbers, length, j, 1)
        if numbers[j] == 0:
            n_after -= 1
            if n_after > n_before:
                if n_after - n_before > max_increase:
                    max_increase = n_after - n_before
                    #print(j)
        if numbers[j] == 1:
            if n_after < n_before:
                if n_before - n_after > max_increase:
                    max_increase = n_before - n_after
                    #print(j)
            n_before += 1
    print(max_inversion_number + max_increase)
