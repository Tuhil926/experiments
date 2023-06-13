def longest_common_subsequence(a, b):
    if len(a) > len(b):
        a, b = b, a
    max_len = 0
    for p in range(len(a)):
        for q in range(p, len(a)):
            if a[p:q + 1:] in b:
                if q - p + 1> max_len:
                    max_len = q - p + 1
    return max_len


T = int(input())
for i in range(T):
    N = int(input())
    S = input()
    max_len = 0
    for j in range(N + 1):
        length = longest_common_subsequence(S[:j], S[::-1][:N - j])
        #print(S[:j], S[::-1][:N - j], length)
        if length > max_len:
            max_len = length
    print(max_len)
