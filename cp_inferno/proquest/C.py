T = int(input())
for i in range(T):
    n = int(input())
    pots = dict()
    for j in range(n):
        xi, yi = [int(x) for x in input().split()]
        yi = min(yi, j)
        pots[xi] = yi
    distances = pots.keys()
    explosiveness = list(pots.values())
    min_diffuse_index = 1
    for j in range(n):
        if explosiveness[-j] > j:
            min_diffuse_index = n-j
    min_diff = n - min_diffuse_index
    for j in range(min_diffuse_index - 1, -1, -1):
        min_diff += explosiveness[j]
        for k in range(j, j - explosiveness[j] - 1, -1):
            explosiveness[k] = 0
    print(min_diff)

    #print(pots)