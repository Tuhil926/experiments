T = int(input())

for i in range(T):
    N = int(input())
    S = input()
    number_of_1s = 0
    number_of_0s = 0
    for j in range(2 * N):
        number_of_0s += S[j] == "0"
        number_of_1s += S[j] == "1"
    output_indices = []
    number_of_indices_added = 0
    if number_of_0s == 0 or number_of_1s == 0:
        print("-1")
        continue
    if number_of_0s > number_of_1s:
        for j in range(2 * N):
            if S[j] == "0" and number_of_indices_added < N:
                output_indices.append(j)
                number_of_indices_added += 1
    else:
        for j in range(2 * N):
            if S[j] == "1" and number_of_indices_added < N:
                output_indices.append(j)
                number_of_indices_added += 1
    for index in output_indices:
        print(index + 1, end=" ")
    print()
