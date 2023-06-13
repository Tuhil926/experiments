def root(x):
    # g = 1
    # while round(g, ndigits=15) != round(x/g, ndigits=15):
    #    g = (g + x/g)/2
    # return round(g, ndigits=15)
    return x**0.5


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




