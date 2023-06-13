from math import gcd
import math


def lcm(x, y):
    return int(x * y / gcd(x, y))


T = int(input())
for i in range(T):
    A, B = [int(x) for x in input().split()]
    min_val = A - 1
    X = B
    n = 1
    while n <= X:
        if X % n == 0:
            req_val = lcm(A, int(X/n)) - gcd(B, int(X/n))
            if req_val < min_val:
                min_val = req_val
        n += 1
    print(min_val)
