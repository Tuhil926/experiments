T = int(input())
for i in range(T):
    n = int(input())
    s = input()
    number_of_returnable = 0
    for j in range(n):
        if s[j] == "-" or s[(j - 1) % n] == "-":
            number_of_returnable += 1
    if ">" not in s or "<" not in s:
        print(n)
    else:
        print(number_of_returnable)
