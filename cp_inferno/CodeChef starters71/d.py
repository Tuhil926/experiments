T = int(input())

for i in range(T):
    N = int(input())
    types = [int(x) for x in input().split()]

    types.sort()

    current_type = types[0]
    number_of_current_type = 1
    possible = "YES"

    for j in range(1, N):
        if types[j] == current_type:
            number_of_current_type += 1
        else:
            if number_of_current_type % 2 != 0:
                possible = "NO"
                break
            current_type = types[j]
            number_of_current_type = 1
    if number_of_current_type % 2 != 0:
        possible = "NO"
    print(possible)