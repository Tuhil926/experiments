import pygame
import time
import random

screen_width = 800
screen_height = 600

pygame.init()

screen = pygame.display.set_mode([screen_width, screen_height])
dt = 0
timeconstant = 1
game_over = False
obstacle_speed = 500


class Car:
    def __init__(self):
        self.width = 30
        self.length = 50
        self.color = [200, 100, 100]
        self.pos = [screen_width/2 - self.width/2, screen_height/2 - self.length/2]
        self.speed = 500

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.pos[0], self.pos[1], self.width, self.length])

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.pos[0] -= self.speed*dt
        if keys[pygame.K_d]:
            self.pos[0] += self.speed*dt
        if keys[pygame.K_w]:
            self.pos[1] -= self.speed*dt
        if keys[pygame.K_s]:
            self.pos[1] += self.speed*dt


class Obstacle:
    def __init__(self):
        self.width = 50
        self.length = 50
        self.color = [100, 100, 100]
        self.pos = [random.random()*screen_width - self.width/2, -100]
        self.speed = obstacle_speed

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.pos[0], self.pos[1], self.width, self.length])

    def update(self):
        global timeconstant
        self.speed = obstacle_speed
        self.pos[1] += self.speed*dt
        if self.pos[1] > screen_height:
            obstacles.pop(obstacles.index(self))
        if self.pos[0] + self.width > car.pos[0] > self.pos[0] - car.width:
            if self.pos[1] + self.length > car.pos[1] > self.pos[1] - car.width:
                if (time_now - time_init)/1000000000 > 3:
                    game_over = True


obstacles = []


def spawn_obstacle():
    chance = random.random()
    if chance < 0.008:
        obstacles.append(Obstacle())


car = Car()
running = True
time1 = time.time_ns()
time_init = time1
time_now = 0
while running:
    screen.fill([0, 0, 0])
    spawn_obstacle()
    obstacle_speed += dt*10

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    car.update()
    car.draw()
    for obstacle in obstacles:
        obstacle.update()
        obstacle.draw()

    pygame.display.update()
    time_now = time.time_ns()
    dt = timeconstant*(time_now - time1) / 1000000000
    if dt > 0.05:
        dt = 0.05
    time1 = time.time_ns()
