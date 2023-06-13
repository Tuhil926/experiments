try:
    weight = float(input("Weight: "))
except ValueError:
    print("Error")
    exit()

choice = input('Kg or Lbs: ').lower()
if choice == 'l':
    print('Weight in kg: ', weight * 0.453592)
elif choice == 'k':
    print('Weight in lbs: ', weight / 0.453592)
