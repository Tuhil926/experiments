def S1(n, r):
    sum = 0
    sum += (n * (n - 1) / 2) - ((n - r) * (n - r - 1) / 2)
    sum += r * (n - 2*r) + (r * (r - 1) / 2)
    return int(sum)


def S(n, k):
    return (2 * n * k) - (k * ((2 * k) + 1))


T = int(input())
for i in range(T):
    N, K = [int(x) for x in input().split()]
    if (N//2) > K:
        print(S(N, K))
    else:
        print(int(N * (N - 1) / 2))
