familyName = input("What is the name of your family? ")
numberOfFamilyMembers = int(input("How many members in your family? "))
familyMembers = []
for i in range(numberOfFamilyMembers):
    print("family member" + str(i + 1))
    name = input("enter name of family member: ")
    age = input("enter his/her age: ")
    phone = input("enter his/her phone number: ")
    familyMembers.append([name, age, phone])

adress = input("what is your adress? :")

print('\n\n')
print("The Family name is: ", familyName)
print("The members of the family are:")
for i in range(numberOfFamilyMembers):
    print(str(i + 1), ". ", familyMembers[i][0], ", age: ", familyMembers[i][1], ", phone No. : ", familyMembers[i][2])
print("The adress is: ", adress)

details = open("details.txt", "w")
details.write("The Family name is: "+ familyName + "\n")
for i in range(numberOfFamilyMembers):
    details.write(str(i + 1)+ ". "+ familyMembers[i][0]+ ", age: "+ familyMembers[i][1]+ ", phone No. : "+ familyMembers[i][2] + "\n")
details.write("The adress is: "+ adress + "\n")
details.close()

