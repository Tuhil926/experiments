size = 32

weights = []

with open("Ai_weights.txt", "r") as weight_file:
    data = weight_file.read()
    rows = data.split()
    for row in rows:
        row1 = []
        for i in range(len(row)):
            row1.append(int(row[i]))
        weights.append(row1)

inp = []
input_file = open("Ai_input.txt", "r")
data = input_file.read()
rows = data.split()
for row in rows:
    row1 = []
    for i in range(len(row)):
        row1.append(int(row[i]))
    inp.append(row1)
input_file.close()

while True:
    result = 0
    for i in range(size):
        for j in range(size):
            result += inp[i][j]*weights[i][j]

    if result > 10:
        print("rect")
    else:
        print("circle")

    correct_or_not = input("Is it correct?")
    rect_or_not = input("is it actually a rect?")
    if rect_or_not == "y":
        if correct_or_not == "y":
            pass
        else:
            for i in range(size):
                for j in range(size):
                    weights[i][j] += inp[i][j]
    else:
        if not correct_or_not == "y":
            for i in range(size):
                for j in range(size):
                    weights[i][j] -= inp[i][j]

    with open("Ai_weights.txt", "w") as weight_file:
        for i in range(size):
            for j in range(size):
                weight_file.write(str(weights[i][j]))
            weight_file.write("\n")
