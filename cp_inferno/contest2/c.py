n = int(input())

for i in range(n):
    arr_len = int(input())
    arr = input().split()
    arr_ints = [int(x) for x in arr]

    list_of_str_diff = [0 for a in arr]

    dupe = list(arr_ints)
    arr_ints.sort(reverse=True)

    #print(dupe)
    #print(arr_ints)

    list_of_str_diff[dupe.index(arr_ints[0])] = arr_ints[0] - arr_ints[1]

    for i in range(1, len(arr_ints)):
        ind = dupe.index(arr_ints[i])
        list_of_str_diff[ind] = arr_ints[i] - arr_ints[0]
        dupe[ind] = -1
        #print(i)

    for dif in list_of_str_diff:
        print(str(dif) + " ", end="")
    print()