string = input()
count = 0
for letter in string:
    if letter == "w":
        count += 2
    else:
        count += 1
print(count)