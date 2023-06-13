T = int(input())
for i in range(T):
    n = int(input())
    a = [int(x) for x in input().split()]
    a.sort(reverse=True)
    second_min = a[0]
    for j in range(n):
        if a[j] < second_min and a[j] != a[n - 1]:
            second_min = a[j]
    maximum_score = 2*a[0] - a[1] - a[n - 1]
    for j in range(n - 2):
        score = 2*a[j] - a[n - 1] - a[j + 1]
        if score > maximum_score:
            maximum_score = score
    for j in range(n - 2):
        score = a[0] + a[n - j - 2] - 2*a[n - j - 1]
        if score > maximum_score:
            maximum_score = score
    print(maximum_score)