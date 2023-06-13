import pickle
import os
import time


def encode(string, key):
    ascii_chars = []
    for i in range(128):
        ascii_chars.append(chr(i))
    duplicate = list(ascii_chars)
    codes = []
    for i in range(128):
        codes.append(duplicate.pop(key * i % len(duplicate)))
    out = ""
    for letter in string:
        out += codes[ascii_chars.index(letter)]
    return out


def decode(string, key):
    ascii_chars = []
    for i in range(128):
        ascii_chars.append(chr(i))
    duplicate = list(ascii_chars)
    codes = []
    for i in range(128):
        codes.append(duplicate.pop(key * i % len(duplicate)))
    out = ""
    for letter in string:
        out += ascii_chars[codes.index(letter)]
    return out


choice = input("What do you want to do? (Login or sign in?): ")
if "l" in choice.lower():
    username = input("Enter you username: ")
    if not os.path.isfile("users/" + username + ".txt"):
        print("You need to sign in!")
    else:
        password = input("Enter your password: ")
        if password.isnumeric():
            password = int(password)
            file = open("users/" + username + ".txt", "rb")
            data = pickle.load(file)
            file.close()
            data = decode(data, password)
            if data[0:len(username)] == username:
                choice2 = input("Select an option: \n1)Read the file \n2)Add data to file\n3)rewrite the file \n4)Change Password\n").lower()
                if "read" in choice2 or "1" in choice2:
                    file = open("users/" + username + ".txt", "rb")
                    data = pickle.load(file)
                    data = decode(data, password)
                    print(data[len(username):])
                    file.close()
                    time.sleep(10)
                if "add" in choice2 or "2" in choice2:
                    file = open("users/" + username + ".txt", "rb")
                    data = pickle.load(file)
                    data = decode(data, password)
                    data = data[len(username):]
                    file.close()
                    file = open("users/" + username + ".txt", "wb")
                    info = encode(username + data + input("Enter the data you want to store: "), password)
                    pickle.dump(info, file)
                    file.flush()
                    file.close()
                    time.sleep(10)
                if "write" in choice2 or "3" in choice2:
                    file = open("users/" + username + ".txt", "wb")
                    info = encode(username + input("Enter the data you want to store: "), password)
                    pickle.dump(info, file)
                    file.flush()
                    file.close()
                    time.sleep(10)
                if "password" in choice2 or "4" in choice2:
                    password = input("Enter your new password: ")
                    password1 = input("Enter your new password again: ")
                    if password1 != password:
                        print("passwords don't match!")
                    elif not password.isnumeric():
                        print("password needs to be a number!")
                    else:
                        password = int(password)
                        file = open("users/" + username + ".txt", "wb")
                        data = encode(data, password)
                        pickle.dump(data, file)
                        file.close()
                    time.sleep(10)
            else:
                print("Wrong password!")
        else:
            print("Password needs to be a number!")


elif "s" in choice.lower():
    username = input("Enter you username: ")
    if os.path.isfile("users/" + username + ".txt"):
        print("Username already exists!")
    elif len(username) < 5:
        print("Username needs to be longer!")
    else:
        password = input("Enter your password: ")
        password1 = input("Enter your password again: ")
        if password1 != password:
            print("passwords don't match!")
        elif not password.isnumeric():
            print("password needs to be a number!")
        else:
            password = int(password)
            file = open("users/" + username + ".txt", "wb")
            data = encode(username, password)
            pickle.dump(data, file)
            file.close()


