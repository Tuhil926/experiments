inp = input().split()
n, k = int(inp[0]), int(inp[1])
for i in range(k):
    if n % 10 != 0:
        n -= 1
    else:
        n /= 10
print(int(n))