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


