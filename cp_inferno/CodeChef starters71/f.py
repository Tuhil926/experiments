T = int(input())

for i in range(T):
    N, K = [int(x) for x in input().split()]
    S = input()
    inversions = []
    current_elem = S[0]
    number_of_inversions = 0
    inversions.append(number_of_inversions)
    for j in range(1, N):
        if S[j] != current_elem:
            number_of_inversions += 1
            current_elem = S[j]
        inversions.append(number_of_inversions)
    min_inversions = 2*N
    for j in range(N - K + 1):
        number_of_inversions = inversions[j + K - 1] - inversions[j]
        if S[j] == "0":
            if number_of_inversions % 2 == 0:
                number_of_inversions += 1
        else:
            if number_of_inversions % 2 == 0:
                pass
            else:
                number_of_inversions += 1
        if number_of_inversions < min_inversions:
            min_inversions = number_of_inversions
    print(min_inversions)
