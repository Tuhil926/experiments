import ctypes
from tkinter import *
from tkinter import messagebox
#ans = ctypes.windll.user32.MessageBoxA(0, "Hi, I am an Albanian virus but because of poor technology in my country unfortunately I am not able to harm your computer. Please be so kind to delete one of your important files yourself and then forward me to other users. Many thanks for your cooperation! Best regards, Albanian virus", "Virus!!!", 3)
win = Tk()
win.title("message")
win.geometry("500x200")
def on_click():
   messagebox.showerror('Virus', 'Hi, I am an Albanian virus but because of poor technology in my country unfortunately I am not able to harm your computer. Please be so kind to delete one of your important files yourself and then forward me to other users. Many thanks for your cooperation! Best regards, Albanian virus')

# Create a label widget
label = Label(win, text="Click the pos to show the message ",
font=('Calibri 15 bold'))
label.pack(pady=20)


# Create a pos to delete the pos
b = Button(win, text="Click Me", command=on_click)
b.pack(pady=20)

win.mainloop()
