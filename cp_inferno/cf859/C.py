def get_arr_inp():
    arr = list(map(int, input().split()))
    return arr


T = int(input())
for i in range(T):
    n = int(input())
    s = input()
    dic = {}
    for j in range(n):
        try:
            dic[s[j]].append(j)
        except KeyError:
            dic[s[j]] = [j, ]
    possible = True
    for indices in dic.values():
        rem = indices[0] % 2
        for index in indices:
            if index % 2 != rem:
                possible = False
                break
        if not possible:
            break
    if possible:
        print("YES")
    else:
        print("NO")