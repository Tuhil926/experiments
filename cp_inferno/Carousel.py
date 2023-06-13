q = int(input())
for i in range(q):
    n = int(input())
    t = [int(x) for x in input().split()]
    one_color = True
    prev_animal = None
    number = 0
    num_animals = 0
    max_animals = 1
    for animal in t:
        if animal != prev_animal:
            number += 1
            num_animals = 1
        else:
            num_animals += 1
            if num_animals > max_animals:
                max_animals = num_animals
        prev_animal = animal
    number_of_colors = 1
    if number == 1:
        print(1)
        print("1 "*n)
        continue

    output = []
    prev_animal = None
    color = 2
    for animal in t:
        if animal != prev_animal:
            if color == 1:
                color = 2
            else:
                color = 1
        output.append(color)
        prev_animal = animal
    #print(number_of_colors)
    #print(output)

    if number % 2 == 1:
        if output[0] == output[1]:
            output[0] = 2
            print(2)
        elif output[n - 1] == output[n - 2]:
            output[n - 1] = 2
            print(2)
        elif t[0] != t[n - 1] and max_animals == 1:
            output[n - 1] = 3
            print(3)
        else:
            prev_out = None
            for k in range(n):
                if output[k] != prev_out:
                    prev_out = output[k]
                    if output[k] ==1:
                        output[k] = 2
                    else:
                        output[k] = 1
                else:
                    break
            print(2)
    else:
        print(2)
    for color in output:
        print(color, end=" ")
    print()
