from random import random
a = []
b = []
c = []
d = []
e = []
f = []
g = []
h = []
i = []
j = []
while True:
    if len(a) > 10000:
        break
    x = int(random()*10 + 1)
    if x == 1:
        a.append(x)
    elif x == 2:
        b.append(x)
    elif x == 3:
        c.append(x)
    elif x == 4:
        d.append(x)
    elif x == 5:
        e.append(x)
    elif x == 6:
        f.append(x)
    elif x == 7:
        g.append(x)
    elif x == 8:
        h.append(x)
    elif x == 9:
        i.append(x)
    elif x == 10:
        j.append(x)
for q in [a, b, c, d, e, f, g, h, i, j]:
    print(len(q)/1000)


