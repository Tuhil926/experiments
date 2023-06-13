T = int(input())
for i in range(T):
    N = int(input())
    A = [int(x) for x in input().split()]
    tot_sum = sum(A)
    if tot_sum % 2 == 1:
        print("NO")
    else:
        for a in A:
            if a % 2 == 1:
                print("YES")
                break
        else:
            print("NO")