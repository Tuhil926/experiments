T = int(input())
for i in range(T):
    n, k = [int(x) for x in input().split()]
    s = [int(x) for x in input()]
    a = [int(x) for x in input().split()]
    number_of_wiz = [0 for x in range(n)]
    for j in range(n):
        if s[j] == 1:
            continue
        min_dist = 100000
        ind_1 = 0
        ind_2 = -1
        for p in range(n):
            if s[p] == 0:
                continue
            if abs(a[p] - a[j]) < min_dist:
                min_dist = abs(a[p] - a[j])
                ind_1 = p
            elif abs(a[p] - a[j]) == min_dist:
                ind_2 = p
        if ind_2 == -1:
            number_of_wiz[ind_1] += 1
        else:
            if a[ind_1] < a[ind_2]:
                number_of_wiz[ind_1] += 1
            else:
                number_of_wiz[ind_2] += 1
    for j in range(n):
        if s[j] == 1:
            print(number_of_wiz[j], end=" ")
    print()