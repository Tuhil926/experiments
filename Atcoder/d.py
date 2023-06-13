A, B = [int(x) for x in input().split()]

g = int((A/B/2)**(2/3))
if g == 0:
    g += 1
s1 = (A/(g**0.5) + (g - 1)*B)
s2 = (A/((g + 1)**0.5) + (g)*B)

if s2 > s1:
    print(s1)
else:
    print(s2)