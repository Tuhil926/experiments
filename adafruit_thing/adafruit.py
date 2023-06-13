from Adafruit_IO import RequestError, Client, Feed
from datetime import date
from colorama import Fore


def print_data(data):
    print(Fore.CYAN + "\nStreak:", str(data[1]))
    print("Work done:", data[0])
    print(Fore.WHITE + "")


ADA_USERNAME = "Tuhil"
ADA_KEY = "aio_Vnba62v0VRwvEmx1LckJH9niwEsl"

aio = Client(ADA_USERNAME, ADA_KEY)
print(aio.base_url)

username = input("Enter your username: ").lower()
feed = None

def create_feed():
    feed = Feed(username, username)
    aio.create_feed(feed, feed.key)

    date_today = int(str(date.today()).replace("-", ""))
    data_to_send = "Created account" + "~" + "0~" + str(date_today)
    aio.send_data(feed.key, data_to_send)

    file = open("others.txt", "w")
    file.write(username + " ")
    file.close()

    print("created new feed")


try:
    # checking if the file
    file = open("others.txt", "a+")
    file.seek(0)
    data = file.read().split()
    print(data)
    file.close()
    if len(data) == 0:
        create_feed()
    elif data[0] != username:
        print(Fore.RED + "Wrong username! Only one user per device" + Fore.WHITE)
        quit()
    feed = aio.feeds(username)
    print("Opened feed")
except RequestError:
    create_feed()

details = aio.receive(feed.key).value.split("~")
print_data(details)
while True:
    choice = input(Fore.LIGHTGREEN_EX + "Enter choice:\n1) See others' data\n2) Update your data\n3) View your data\n4) exit\n" + Fore.WHITE + ">>> ")
    if "1" in choice:
        file = open("others.txt", "r")
        others = file.read().split()
        others.pop(0)
        file.close()
        for person in others:
            try:
                data = aio.receive(person).value.split("~")
            except RequestError:
                print(Fore.RED + person, "not found" + Fore.WHITE)
                continue
            print("\n" + person + ":")
            print_data(data)

        if len(others) != 0:
            choice2 = input("Do you want to see the data of someone else?(y/n): ")
            if choice2 != "y":
                continue

        people = list(input("Enter the name(s) of the person(s): ").split())

        file = open("others.txt", "a")
        for person in people:
            try:
                data = aio.receive(person).value.split("~")
            except RequestError:
                print(Fore.RED + person, "not found" + Fore.WHITE)
                continue
            print("\n" + person + ":")
            print_data(data)
            file.write(person + " ")
        file.close()

    elif "2" in choice:
        streak = int(details[1])
        date_prev = int(details[2])
        date_today = int(str(date.today()).replace("-", ""))

        if date_today - date_prev == 1:
            streak += 1
        elif date_today - date_prev > 1:
            streak = 0

        user_data = input("Enter the description of your work: ")
        data_to_send = user_data + "~" + str(streak) + "~" + str(date_today)

        aio.send_data(feed.key, data_to_send)

    elif "3" in choice:
        details = aio.receive(feed.key).value.split("~")
        print_data(details)

    elif "4" in choice:
        break
    else:
        print(Fore.RED + "\nDude there are literally 4 options how did you mess this up\n" + Fore.WHITE)

    choice = input("\nDo you want to contine?(y/n): ")
    if choice != "y":
        break
    print("")
