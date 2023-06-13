n_i = int(input(""))
n = int(n_i)
s = 0
s += (int(n/3)) * 2
n = n % 3

if n == 1 or n == 2:
    s += 1

print(s)