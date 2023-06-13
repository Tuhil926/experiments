from tkinter import *
import random

root = Tk()

root.geometry("800x600")


def to_hex(number, digits):
    hex_num = str(hex(number)).replace("0x", "", 1)
    if not len(hex_num) > digits:
        while len(hex_num) < digits:
            hex_num = "0" + hex_num
    return hex_num


def generate_response():
    resonses = ["hi", "hello", "what's up", "how are you doing", "you clicked the Button", "*click*", "*clack*", "sup", "lol", "these are random colors", "this might look nice but the code is really messy", "you have decided to click the Button", "hmmmmmmm", "XD", ":P", "im here", "this is ridiculous"]
    return resonses[random.randint(0, len(resonses) - 1)]


def randomColor():
    return "#" + to_hex(int(random.random()*255), 2) + to_hex(int(random.random()*255), 2) + to_hex(int(random.random()*255), 2)


def click():
    label1 = Label(root, text=generate_response(), bg=randomColor())
    label1.place(relx=random.random()*(root.winfo_width() - label1.winfo_reqwidth())/root.winfo_width(), rely=random.random()*(root.winfo_height() - label1.winfo_reqheight())/root.winfo_height())


button1 = Button(root, text="click me", padx=50, pady=10, command=click)

button1.pack()

root.mainloop()

