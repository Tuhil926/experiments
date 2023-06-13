def get_arr_inp():
    arr = list(map(int, input().split()))
    return arr


T = int(input())
for i in range(T):
    a, b, c = [int(x) for x in input().split()]
    if a + b == c:
        print("+")
    elif a - b == c:
        print("-")
    else:
        print("a")