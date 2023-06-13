from time import sleep


from random import random


def ci():
    def CI(sum, rate, time):
        if time == 0:
            return sum
        if time == 1:
            return float(sum) + (float(sum) * float(rate) / 100)
        else:
            return CI(sum, rate, (time - 1)) + (CI(sum, rate, (time - 1)) * rate / 100)

    print("enter the values to calculate compound interest:")
    sm = float(input("sum : "))
    rt = float(input("Rate : "))
    tm = float(input("Time : "))
    if tm < 23:
        for s in range(int(tm)):
            if s == 0:
                print(f"Interest for {s + 1}st year: {(CI(sm, rt, s + 1) - CI(sm, rt, s))}")
                sleep(.5)
            elif s == 1:
                print(f"Interest for {s + 1}nd year: {(CI(sm, rt, s + 1) - CI(sm, rt, s))}")
                sleep(.5)
            elif s == 2:
                print(f"Interest for {s + 1}rd year: {(CI(sm, rt, s + 1) - CI(sm, rt, s))}")
                sleep(.5)
            else:
                print(f"Interest for {s+1}th year: {(CI(sm, rt, s+1) - CI(sm, rt, s))}")
                sleep(.5)
    else:
        print("Can't calculate the interest for more than 22 years")
    print(f"total amount:{CI(sm, rt, tm)}")
    sleep(1)


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


def random_string(strings):
    return strings[int(random() * strings.__len__())]


def greet():
    greetings = ["hi!", "hello!", "welcome!", "greetings!"]
    return random_string(greetings)


def ask_q_help():
    questions = ["how can I help you?", "what can I do for you?", "what do you need?"]
    return random_string(questions)


def sorry():
    apologies = ["I don't think i can do that...", "Sorry, I can't do that..", "I don't know how to do that...", "I'm sorry but I won't be able to do that", "I don't think I can help you"]
    return random_string(apologies)


def become_impatient():
    response = ["LOOK, WILL YOU PLEASE TELL ME TO DO SOMETHING I CAN??", "STOP ASKING ME TO DO THINGS I CAN'T!!", "LOOK, I CAN'T DO THAT, OK???", "WHY DO YOU ASK ME TO DO THINGS I CAN'T???"]
    return random_string(response)


def calculator():
    while True:
        num1 = input("number 1:")
        if num1 == "exit":
            break
        operation = input("operation:")
        if operation == "exit":
            break
        num2 = input("number 2:")
        if operation in ["addition", "add", "+"]:
            print(f"The answer is:{float(num1) + float(num2)}")
        if operation in ["subtraction", "-", "minus"]:
            print(f"The answer is:{float(num1) - float(num2)}")
        if operation in ["multiplication", "*"]:
            print(f"The answer is:{float(num1) * float(num2)}")
        if operation in ["division", "/"]:
            print(f"The answer is:{float(num1) / float(num2)}")
        if operation in ["^", "power"]:
            print(f"The answer is:{float(num1) ** float(num2)}")
        if operation in ["root", "_/"]:
            print(f"The answer is:{float(num1) ** (1/float(num2))}")


print(greet())
sleep(.75)
error_counter = 0

while True:
    sleep(.75)
    words = input(ask_q_help() + "\n")
    if "calculator" in words.lower():
        sleep(.4)
        print("Here is the calculator:")
        sleep(.5)
        calculator()

    elif "compound interest" in words.lower():
        sleep(.4)
        print("here is the program to calculate compound interest:")
        sleep(.5)
        ci()

    elif "exit" in words.lower():
        sleep(.4)
        break

    elif "thank you" in words.lower():
        sleep(.4)
        print("You,re welcome")

    elif "hi" in words.lower():
        sleep(.4)
        print("hi")

    elif "bye" in words.lower():
        print("bye")
        sleep(.8)
        break

    elif "because" in words.lower():
        sleep(.4)
        print("ok.")
        error_counter = 0

    elif "ok" in words.lower():
        sleep(.4)
        print("GOOD!")
        error_counter = 0

    elif "no" in words.lower():
        sleep(.4)
        print("WELL, BYE THEN!")
        sleep(.4)
        break

    elif "triangle" in words.lower():
        sleep(.4)
        print("here is the triangle checker:")
        sleep(.5)
        tri_checker()

    else:
        error_counter += 1
        if error_counter > 3:
            sleep(.4)
            print(become_impatient())
        else:
            sleep(.4)
            print(sorry())

