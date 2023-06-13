N, M = [int(x) for x in input().split()]
A = [int(x) for x in input().split()]
B = [x for x in range(1, N+1)]
#print(B)

for i in range(1, M + 1):
    dupe_of_B = list(B)
    #print(i)
    for k in range(1, i):
        dupe_of_B[A[k - 1] - 1], dupe_of_B[A[k - 1]] = dupe_of_B[A[k - 1]], dupe_of_B[A[k - 1] - 1]
        #print(k)
    for k in range(i + 1, M + 1):
        dupe_of_B[A[k - 1] - 1], dupe_of_B[A[k - 1]] = dupe_of_B[A[k - 1]], dupe_of_B[A[k - 1] - 1]
        #print(k)
    print(dupe_of_B.index(1) + 1)
