T = int(input())

for i in range(T):
    A, B, C = [int(x) for x in input().split()]
    if A + B == C or B + C == A or A + C == B:
        print("YES")
    else:
        print("NO")