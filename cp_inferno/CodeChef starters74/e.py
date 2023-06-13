T = int(input())
for i in range(T):
    N, M = [int(x) for x in input().split()]
    A = [int(x) for x in input().split()]
    C = [int(x) for x in input().split()]
    max_C = 0
    max_bonus = 0
    for j in range(M):
        number_of_candies = 0
        if C[j] > max_C and C[j] / (j + 1) >= max_C / (j + 1):
            max_C = C[j]
            for k in range(N):
                number_of_candies += (A[k] // (j + 1))
            if number_of_candies * C[j] > max_bonus:
                max_bonus = number_of_candies * C[j]
    print(max_bonus)
