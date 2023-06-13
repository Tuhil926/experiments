import time
limit = 10000000
result = []
length = []
square = []
number = 3
stringNumber = ""
digits = ""
pi = "31415926535"
tim = time.time_ns()
for i in range(limit):
    number = (i + 1)**(1/1.5)
    stringNumber = str(number)
    digits = stringNumber.replace('.', '')
    for j in range(7):
        if pi[0:j+5] in digits:
#            print(digits, end = "   ")
#            print(i + 5)
            result.append(digits)
            length.append(j + 5)
            square.append(i + 1)
n = length.index(max(length))
for i in range(len(length)):
    if length[i] == length[n]:
        print(result[i], "  ", length[i], "   ", square[i])
for i in range(len(length)):
    if length[i] == length[n] - 1:
        print(result[i], "  ", length[i], "   ", square[i])
print((time.time_ns() - tim)/1000000000)
