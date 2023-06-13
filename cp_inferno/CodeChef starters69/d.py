T = int(input())

for i in range(T):
    N, K = [int(x) for x in input().split()]
    A = [int(x) for x in input().split()]
    B = [int(x) for x in input().split()]
    exists = [1 for x in range(N)]
    is_possible = True
#    for category in A:
#        if category not in categories:
#            categories.append(category)
#    if K > len(categories):
#        print("-1")

    tot_time = 0
    for j in range(K):
        index = -1
        min_existed = False
        min_time = 10 ** 6
        for p in range(len(A)):
            if B[p] < min_time and exists[p]:
                min_time = B[p]
                index = p
                min_existed = True
        if not min_existed:
            is_possible = False
        tot_time += min_time
        category = A[index]
        k = 0
        while k < N:
            if category == A[k]:
                exists[k] = 0
            k += 1
    if is_possible:
        print(tot_time)
    else:
        print("-1")
