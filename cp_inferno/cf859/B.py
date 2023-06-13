def get_arr_inp():
    arr = list(map(int, input().split()))
    return arr


T = int(input())
for i in range(T):
    n = int(input())
    a = get_arr_inp()
    mih = 0
    bin = 0
    for bag in a:
        if bag % 2 == 0:
            mih += bag
        else:
            bin += bag
    if mih > bin:
        print("YES")
    else:
        print("NO")