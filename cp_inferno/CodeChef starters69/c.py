T = int(input())

for i in range(T):
    N = int(input())
    A = [int(x) for x in input().split()]
    A.sort()
    is_possible = True
    for i in range(N):
        if A[i] > i + 1:
            is_possible = False
            print("-1")
            break
    if is_possible:
        print(int(N * (N + 1) / 2 - sum(A)))
