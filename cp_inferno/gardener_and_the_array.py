T = int(input())
for i in range(T):
    n = int(input())
    c = []
    numbers = {}
    for j in range(n):
        inp = [int(x) for x in input().split()]
        del inp[0]
        for num in inp:
            try:
                numbers[num] += 1
            except KeyError:
                numbers[num] = 1
        c.append(inp)
    yes = False
    for element in c:
        for num in element:
            if numbers[num] == 1:
                break
        else:
            yes = True
            print("Yes")
            break
    if not yes:
        print("NO")

