from math import *


def reduce_fraction(x, y):
    d = gcd(x, y)

    x = x // d
    y = y // d

    return [x, y]


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


T = int(input())
for i in range(T):
    A, B = [int(x) for x in input().split()]
    if (A + B) % 2 == 0:
        P_by_Q = [A, 2]
    else:
        P_by_Q = [A, 2]
        #P_by_Q = [A * (A + B + 1) / 2, A + B))]
    P_by_Q = reduce_fraction(P_by_Q[0], P_by_Q[1])
    print(P_by_Q[0] * modinv(P_by_Q[1], 998244353))
