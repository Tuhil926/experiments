T = int(input())
for i in range(T):
    N = int(input())
    A = [int(x) for x in input().split()]
    max_neg = -10**10
    min_pos = 10**10

    for j in range(N):
        if A[j] > 0:
            if A[j] < min_pos:
                min_pos = A[j]
        else:
            if A[j] > max_neg:
                max_neg = A[j]

    max_neg *= -1
    X = min(max_neg, min_pos) - 1
    if X >= 0:
        print(X)
    else:
        print(-1)