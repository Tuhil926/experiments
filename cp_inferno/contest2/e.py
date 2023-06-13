n = int(input())
for i in range(n):
    length = int(input())
    numbers = [int(x) for x in input().split()]
    prev = numbers[0]
    inversions = 0
    continuous = 0
    three_in_row = False
    for j in range(length):
        if numbers[j] != prev:
            inversions += 1
        else:
            continuous += 1
        if continuous >= 3 and three_in_row == False:
            inversions += 2
            three_in_row = True
        prev = numbers[j]
    print(inversions)
