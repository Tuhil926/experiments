def val(array, index):
    try:
        return int(array[index])
    except IndexError:
        return 0


T = int(input())
num_of_digits_max = 30

for i in range(T):
    N = int(input())
    A = [int(x) for x in input().split()]
    for j in range(N):
        A[j] = (str(bin(A[j]))[::-1])[:-2]
    ors = []
    for j in range(30):
        sum = 0
        for k in range(N):
            sum += val(A[k], j)
        ors.append(sum)
    #print(ors)
    min_from_starts = []
    min_from_ends = []
    for j in range(30):
        tot_or_for_digit = ors[j]
        if ors[j] == 0:
            min_from_starts.append(0)
            min_from_ends.append(N - 1)
            continue
        elif ors[j] == 1:
            index = 0
            for l in range(N):
                if val(A[l], j) == 1:
                    index = l
            min_from_starts.append(index + 1)
            min_from_ends.append(index)
            continue
        k = 0
        while val(A[k], j) != 1:
            k += 1
        k += 1
        min_from_starts.append(k)
        k = N - 1
        while val(A[k], j) != 1:
            k -= 1
        min_from_ends.append(k)
    print(max(min_from_starts) - min(min_from_ends))
