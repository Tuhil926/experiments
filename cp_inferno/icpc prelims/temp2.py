#ethOS - Tuhil
def get_arr_inp():
    arr = [int(x) for x in input().split()]
    return arr

def fact(n):
    res = 1
    for b in range(n):
        res *= b + 1
    print("fheiw")
    return res

def decimalToBinary(n):
    return [int(x) for x in bin(n).replace("0b", "")]


def get_freq(inp_arr):
    freq = {}
    for j in range(len(inp_arr)):
        for k in range(len(inp_arr[j]), -1, -1):
            try:
                freq[k] += 1
            except IndexError:
                freq[k] = 1
    return freq

def x_or(arr):
    sum = 0
    for num in arr:
        sum = sum | num
    return sum

T = int(input())
for i in range(T):
    n, k= get_arr_inp()
    inp_arr = get_arr_inp()
    #inp_arr = [decimalToBinary(x) for x in inp_arr]
    sum_or = x_or(inp_arr)
    #print("fjds: ", sum_or)
    bin_sum_or_rev = decimalToBinary(sum_or)[::-1]
    bin_k_rev = decimalToBinary(k)[::-1]
    removed = []
    for j in range(len(bin_sum_or_rev), -1, -1):
        try:
            if bin_sum_or_rev[j] > bin_k_rev[j]:
                for z in range(len(inp_arr)):
                    if (inp_arr[z] | 2**j) == inp_arr[z]:
                        removed.append(z)
                #remove_at_j()
            elif bin_sum_or_rev[j] == bin_k_rev[j]:
                continue
            else:
                break
        except IndexError:
            continue
    print("fjds: ", bin_sum_or_rev, bin_k_rev, removed, k, sum_or)

    if k > sum_or:
        print("hfueiw", fact(n))
        continue

    if len(removed) == 0:
        print(fact(n))
        continue
    print((min(removed) + 1) * (n - max(removed)))

