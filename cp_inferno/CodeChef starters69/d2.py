T = int(input())

for i in range(T):
    N, K = [int(x) for x in input().split()]
    A = [int(x) for x in input().split()]
    B = [int(x) for x in input().split()]
    items = dict()
    for j in range(N):
        items[A[j]] = []
    for j in range(N):
        items[A[j]].append(B[j])
    if K > len(items):
        print("-1")
    else:
        tot_time = 0
        min_elements = []
        for key in items.keys():
            min_elements.append(min(items[key]))
        min_elements.sort()
        for j in range(K):
            tot_time += min_elements[j]
        print(tot_time)