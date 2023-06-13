from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np


def wave(amplitude, k, w, t, x, phs_dif):
    return amplitude*np.sin(w*t - k*x + phs_dif)


style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
divisions = 101
counter = 0
rngePi = 4.0
time = 0.0
phase_d = 0
vel = 1
n = 4
k1 = 0.25
k2 = 0.25
a1 = 1
a2 = 1
w1 = k1*vel
w2 = k2*vel
direction1 = 1
direction2 = -1


def animate(i):
    global counter
    global divisions
    global rngePi
    global time
    global k1
    global k2
    global a1
    global a2
    global w1
    global w2
    global n
    xs = np.linspace(0, rngePi*np.pi, divisions)
#    ys = a1*np.sin(k1*xs + phase) + a2*np.sin(k2*xs + phase + phase_d)
    ys = wave(a1, direction1*n*k1, n*w1, time, xs, phase_d) + wave(a2, direction2*n*k2, n*w2, time, xs, 0.0)
    ax1.clear()
    time += 0.1
    counter += 1
    if counter > 100:
        counter = 0
#        n += 1
    ax1.plot(xs, ys)
    ax1.scatter([0, 0], [2*(a1+a2), -2*(a1+a2)])


ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()
a = np.linspace(0, 4*np.pi, 101)
b = np.sin(a)
