T = int(input())
for i in range(T):
    n, a, b = [int(x) for x in input().split()]
    if (a >= n and b >= n):
        print("Yes")
    else:
        print("No")