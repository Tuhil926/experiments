cost_price = float(input("Cost price:"))
selling_price = float(input("Selling price:"))
x = (selling_price - cost_price)/cost_price * 100
if x < 0:
    print(f"There was a loss of {-x}% .")
elif x > 0:
    print(f"There was a profit of {x}%.")
else:
    print("There was no profit or loss.")