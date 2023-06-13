import turtle
import time


def hexagon():
    global t
    for i in range(70):
        t.color(col[i % 6])
        t.forward(i * 1 + 20)
        t.left(58 + i / 50)
        t.width(2)


def polygon(n, scale, steps = 70):
    global t
    for i in range(steps):
        t.color(col[i % n])
        t.forward((i + 20)*scale)
        t.left((360/n - 2) + i / 50)
        t.width(2)


def star(n, scale):
    t.color(col[4])
    for i in range(n):
        t.forward(100*scale)
        t.left(180 - 360/(2*n))


col = ("violet", "navy", "skyblue", "green", "yellow", "orange", "red", "violet", "navy", "skyblue", "green", "yellow", "orange", "red")
t = turtle.Turtle()
screen = turtle.Screen()
screen.bgcolor("black")
t.speed(30)

polygon(7, 1)

time.sleep(5)