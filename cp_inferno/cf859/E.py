import sys


def get_arr_inp():
    arr = list(map(int, input().split()))
    return arr


T = int(input())
for i in range(T):
    n = int(input())
    a = get_arr_inp()
    sums = [0]
    run_sum = 0
    for j in range(n):
        run_sum += a[j]
        sums.append(run_sum)
    left = 0
    mid = n - n // 2
    right = n
    for j in range(30):
        query = "? "
        query += str(mid - left) + " "
        for k in range(left, mid, 1):
            query += str(k + 1) + " "
        print(query)
        sys.stdout.flush()
        x1 = int(input())

        if x1 > sums[mid] - sums[left]:
            right = mid
        else:
            left = mid
        mid = (right + left) // 2

        if right == left + 1:
            break
    print("! " + str(mid + 1))
    sys.stdout.flush()
