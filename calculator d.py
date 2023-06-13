while True:
    num1 = input("Number 1:")
    if num1 == "exit":
        break
    operation = input("Operation:")
    if operation == "exit":
        break
    num2 = input("Number 2:")
    if operation in ["addition", "add", "+", "plus", "a"]:
        print(f"The answer is:{float(num1) + float(num2)}")
    if operation in ["subtraction", "-", "minus", "subtract", "s"]:
        print(f"The answer is:{float(num1) - float(num2)}")
    if operation in ["multiplication", "*", "into", "multiply", "m"]:
        print(f"The answer is:{float(num1) * float(num2)}")
    if operation in ["division", "/", "by", "divide", "hate divide", "d"]:
        print(f"The answer is:{float(num1) / float(num2)}")
