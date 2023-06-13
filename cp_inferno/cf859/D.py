def get_arr_inp():
    arr = list(map(int, input().split()))
    return arr


def print_out(rem):
    if rem:
        print("YES")
    else:
        print("NO")


T = int(input())
for i in range(T):
    n, q = get_arr_inp()
    a = get_arr_inp()

    sum = 0
    even_or_odd = [0]
    for number in a:
        sum += number
        even_or_odd.append(sum % 2)

    for j in range(q):
        l, r, k = get_arr_inp()
        l -= 1
        if even_or_odd[l] == even_or_odd[r]:
            if k % 2 == 0:
                print_out(sum % 2)
            elif (r - l) % 2 == 0:
                print_out(sum % 2)
            else:
                print_out((sum + 1) % 2)
        else:
            if k % 2 == 0:
                print_out((sum+ 1) % 2)
            elif (r - l) % 2 == 0:
                print_out((sum + 1) % 2)
            else:
                print_out((sum) % 2)
