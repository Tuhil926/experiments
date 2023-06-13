n, k = [int(x) for x in input().split()]
a = [int(x) for x in input().split()]
a.sort()
tot = sum(a)
for i in range(n):
    if tot/(n - i) < n:
        print("this doesn't work")
sum = 0
for i in range(k):
    sum += a[i]*a[i]
print(sum)
#print(a)