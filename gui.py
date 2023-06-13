import tkinter
import csv

with open("names.csv", "a") as names:
    top = tkinter.Tk()
    name = tkinter.Entry(top)
    button1 = tkinter.Button(top, text="enter")
    name.pack()
    button1.place(relx=.5, rely=.54)
    top.mainloop()
