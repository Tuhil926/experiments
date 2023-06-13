from time import sleep


def tri_check_sides(q, r, e):
    s = [1, 2, 3, 4, 5, 6]
    s[0] = q  # int(input("Side 1 :") or 1)
    s[1] = r  # int(input("Side 2 :") or 1)
    s[2] = e  # int(input("Side 3 :") or 1)
    s[3] = s[0]
    s[4] = s[1]
    s[5] = s[2]
    p = True
    typ = "ac"
    for a in range(3):
        if s[a] + s[a + 1] <= s[a + 2]:
            p = False
    if p == False:
        print("not possible")
    else:
        print("possible")
    if p == True:
        for a in range(3):
            if s[a] * s[a] > (s[a + 1] * s[a + 1]) + (s[a + 2] * s[a + 2]):
                typ = "ob"
            elif s[a] * s[a] == (s[a + 1] * s[a + 1]) + (s[a + 2] * s[a + 2]):
                typ = "rt"
        if typ == "ob":
            print("it's an obtuse angled triangle")
        if typ == "rt":
            print("it's a right angled triangle")
        if typ == "ac":
            print("it's an acute angled triangle")


def tri_checker():
    while True:
        print("Input the lengths of the sides of your triangle")
        a = input("side 1: ")
        if a == "exit":
            break
        if len(a) == 0:
            print("error: no value entered", end="")
            for q in range(5):
                sleep(0.5)
                print(".", end="")
            sleep(2)
            print(".")
            break
        b = input("side 2: ")
        if len(b) == 0:
            print("error: no value entered", end="")
            for q in range(5):
                sleep(0.5)
                print(".", end="")
            sleep(2)
            print(".")
            break
        c = input("side 3: ")
        if len(c) == 0:
            print("error: no value entered", end="")
            for q in range(5):
                sleep(0.5)
                print(".", end="")
            sleep(2)
            print(".")
            break
        tri_check_sides(int(a), int(b), int(c))
