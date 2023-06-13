n = int(input(""))

sum_tot = n*(n + 1)/2
sum = 0

ep = input("").split()

for e in ep:
    sum += int(e)

print(int(sum_tot - sum))