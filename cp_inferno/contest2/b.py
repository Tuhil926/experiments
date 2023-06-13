n = int(input())

for i in range(n):
    max_char = 0
    len_str = int(input())
    string = input()
    for j in range(len_str):
        if max_char < ord(string[j]):
            max_char = ord(string[j])
    print(max_char - 96)