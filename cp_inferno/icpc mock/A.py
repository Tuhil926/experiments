T = int(input())
for i in range(T):
    N = int(input())
    S = input()
    D = [int(x) for x in input().split()]
    j = 0
    possible = S[0] == "R"
    number_of_steps = 0
    max_index = 0
    while possible and j != N - 1:
        while j < N and S[j] == "R":
            if D[j] + j > max_index:
                max_index = D[j] + j
            j += 1
        if j > max_index:
            if j != N:
                possible = False
                break
            else:
                break
        S = "R"*(max_index + 1) + S[max_index + 1::]
        #print(S)
        number_of_steps += 1
    if possible:
        print(number_of_steps)
    else:
        print(-1)
