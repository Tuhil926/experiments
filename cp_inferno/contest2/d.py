num = int(input())

for i in range(num):
    length = int(input())
    s = "dec"
    s_prev = "dec"
    list_of_nos = [int(x) for x in input().split()]
    if list_of_nos[0] < list_of_nos[1]:
        s = "inc"
        s_prev = "inc"

    if s == "dec":
        for j in range(1, length - 1):
            if list_of_nos[j] > list_of_nos[j + 1]:
                s = "dec"
            elif list_of_nos[j] < list_of_nos[j + 1]:
                s = "inc"