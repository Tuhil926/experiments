import pygame
import time
import numpy as np
time.sleep(.5)

screenWidth = 600
screenLength = 800

screen = pygame.display.set_mode((screenLength, screenWidth))


def wave(amplitude, k, w, t, x, phs_dif):
    return amplitude*np.sin(w*t - k*x + phs_dif)


def plot(x, y, color):
    global screenLength
    global screenWidth
    for i in range(len(x)-1):
        pygame.draw.line(screen, color, (x[i], y[i] + (screenWidth/2)), (x[i + 1], y[i + 1] + (screenWidth/2)))

#common variables
time1 = 0#time variable
vel = 500
dt = 0.01
phs_dif = 0#np.pi
n = 1
#variables for first wave
a1 = 60
wl1 = 2*screenLength/n
k1 = 2*np.pi/wl1
w1 = k1*vel
dir1 = 1
#variables for second wave
a2 = 60
wl2 = 2*screenLength/n
k2 = 2*np.pi/wl2
w2 = k2*vel
dir2 = 1

counter = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))

    x = np.linspace(0, screenLength, 101)

    y = wave(a1, dir1*k1, w1, time1, x, phs_dif) + wave(a2, dir2*k2, w2, time1, x, 0)
    plot(x, y, (255, 255, 255))

    counter += 1
    if counter > 500:
#        n += 1
        counter = 0
        if n > 5:
            n = 1
    time1 += dt

    # variables for first wave
    a1 = 60
    wl1 = 0.1* screenLength / n
    k1 = 2 * np.pi / wl1
    w1 = k1 * vel
    dir1 = 1
    # variables for second wave
    a2 = 60
    wl2 = 0.11 * screenLength / n
    k2 = 2 * np.pi / wl2
    w2 = k2 * vel
    dir2 = 1

    y = []
    time.sleep(dt)
    pygame.display.update()

