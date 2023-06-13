import random
n = 1000000
q = 0
p = 0
x = 96
y = 0
z = 0
for i in range(n):
    q = random.randint(0, 128)
    p = random.randint(0, 128)
    if ((p - q)**2)**0.5 < x - 64:
        y += 1
print(y/n)