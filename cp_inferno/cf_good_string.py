for i in range(int(input())):
    s = [int(x) for x in input()]
    matr = []
    for j in range(10):
        temp = []
        for k in range(10):
            temp.append(0)
        matr.append(temp)

    for num in s:
        matr[num][num] += 1
        for j in range(10):
            if j != num and matr[j][j]:
                if matr[j][num] % 2 == 0:
                    matr[j][num] += 1
                if matr[num][j] % 2 == 1:
                    matr[num][j] += 1
    max = 0
    for j in range(10):
        for k in range(10):
            if j == k:
                if matr[j][k] > max:
                    max = matr[j][k]
            elif matr[j][k] % 2 != 0:
                if matr[j][k] + 1 > max:
                    max = matr[j][k] + 1

    #for j in range(10):
    #    print(matr[j])
    print(len(s) - max)