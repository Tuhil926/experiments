T = int(input())
for i in range(T):
    N = int(input())
    A = [int(x) for x in input().split()]
    B = [0 for x in range(N)]
    for a in range(N)[::-1]:
        B[a] = A[:a:].count(A[a] + 1) - A[a + 1::].count(A[a] - 1)
    sum_ = 0
    C = []
    max_ = 0
    for a in range(N)[::-1]:
        sum_ += B[a]
        if sum_ > max_:
            max_ = sum_
    print(max_)
