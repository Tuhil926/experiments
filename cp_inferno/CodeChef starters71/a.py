T = int(input())

for i in range(T):
    X, Y = [int(x) for x in input().split()]
    if X > 10 * Y:
        print("YES")
    else:
        print("NO")