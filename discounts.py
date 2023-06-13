price = float(input("Price :"))
x = price - (price * 30 / 100)
y = (price - (price * 20 / 100)) - ((price - (price * 20 / 100)) / 10)
print(f"price by 1st shopkeeper :{x}")
print(f"price by 2st shopkeeper :{y}")

if x > y:
    print("shopkeeper 2 has the better offer")
else:
    print("shopkeeper 1 has the better offer")