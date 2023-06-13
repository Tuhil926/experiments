T = int(input())
for i in range(T):
    N = int(input())
    B = [int(x) for x in input().split()]
    number_of_ones = B.count(1)
    if N%2 == number_of_ones%2:
        print("YES")
    else:
        print("NO")