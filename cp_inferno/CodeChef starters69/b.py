T = int(input())

for i in range(T):
    A, B, C = [int(x) for x in input().split()]
    if A != B and B != C and A != C:
        print("YES")
    else:
        print("NO")