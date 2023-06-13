import pygame
import time

screenWidth = 600
screenLength = 800

screen = pygame.display.set_mode((screenLength, screenWidth))

heliimg = pygame.image.load('heli.png')
backgroundimg = pygame.image.load('marsBackground.jpg')
background = pygame.transform.scale(backgroundimg, (screenLength, screenWidth))

class heli():
    def __init__(self, x, y, rot, image):
        self.x = x
        self.y = y
        self.rot = rot
        self.image = image

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


x, y = 0, 0
helicopter = heli(x, y, 0, heliimg)

running = True

fps = 60
timePerTick = 1000000000 / fps
delta = 0
now = 0
lastTime = time.time_ns()
timer = 0
ticks = 0
while running:
    now = time.time_ns()
    delta += (now - lastTime) / timePerTick
    timer += now - lastTime
    lastTime = now

    if delta >= 1:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[100] == 1:
            helicopter.x += 5
        if keys[97] == 1:
            helicopter.x -= 5
        if keys[119] == 1:
            helicopter.y -= 5
        if keys[115] == 1:
            helicopter.y += 5
        helicopter.draw()

        pygame.display.update()
        ticks += 1
        delta -= 1

    if timer >= 1000000000:
        print("Ticks and Frames: ", ticks)
        for i in range(len(keys)):
            if keys[i] == 1:
                print(i)
        ticks = 0
        timer = 0

