n = int(input(""))
for i in range(n + 1):
    if n == 0:
        print("YES")
        break
    elif n < 0:
        print("NO")
        break
    n -= i + 1