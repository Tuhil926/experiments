import pygame
import random
import time
import threading
import math
import numpy as np
import  concurrent.futures

screenWidth = 600
screenLength = 800

screen = pygame.display.set_mode((screenLength, screenWidth))

dt = 0
K = 30000000


class Planet:
    def __init__(self, mass, charge, position, radius, color, image=None):
        self.mass = mass
        self.charge = charge
        self.position = np.array(position)
        self.image = image
        self.radius = radius
        self.width = self.radius
        self.color = color
        self.acceleration = np.array([0, 0])
        self.velocity = np.array([0, 0])
        self.collided = False
        self.drag = 4

    def draw(self):
        if self.image is not None:
            screen.blit(self.image, (self.position[0] - self.image.get_width()/2, self.position[1] - self.image.get_height()/2))
        else:
            pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius, self.width)

    def update(self):
        self.velocity[0], self.velocity[1] = self.velocity[0]*(1 - self.drag*dt) + self.acceleration[0]*dt, self.velocity[1]*(1 - self.drag*dt) + self.acceleration[1]*dt
        self.position[0], self.position[1] = self.position[0] + self.velocity[0]*dt, self.position[1] + self.velocity[1]*dt
        if self.position[0] < 0:
            self.position[0] = 0
            self.velocity[0] = -self.velocity[0]
        if self.position[0] > screenLength:
            self.position[0] = screenLength
            self.velocity[0] = -self.velocity[0]
        if self.position[1] < 0:
            self.position[1] = 0
            self.velocity[1] = -self.velocity[1]
        if self.position[1] > screenWidth:
            self.position[1] = screenWidth
            self.velocity[1] = -self.velocity[1]


def componentof(vector1, vector2):
    return vector1.dot(vector2)/magnitude(vector2)



def magnitude(vector2):
    return np.sqrt(vector2.dot(vector2))


def mod(n):
    if n >= 0:
        return n
    else:
        return -n


def molecular_force(planets):
    for planet1 in planets:
        planet1.acceleration = np.array([0, 0])
        for planet2 in planets:
            if planet2 is not planet1:
                distance = magnitude(planet1.position - planet2.position)
                radius_difference = planet1.radius + planet2.radius
                if distance == 0:
                    distance = 0.01
                if distance < radius_difference:
                    force = -K * planet1.charge * planet2.charge / ((radius_difference) ** 2) -mod(K*planet1.charge * planet2.charge*(radius_difference - distance)/((distance + 100)**2)/30)
                else:
                    force = -K * planet1.charge * planet2.charge / (distance ** 2)
                cos = (planet2.position[0] - planet1.position[0]) / distance
                sin = (planet2.position[1] - planet1.position[1]) / distance
                planet1.acceleration[0] += force * cos / planet1.mass
                planet1.acceleration[1] += force * sin / planet1.mass


def gravity(planets):
    velocity_changes = []
    position_changes = []
    for planet1 in planets:
        velocity_changes.append([0, 0])
        position_changes.append([0, 0])
        planet1.acceleration = [0, 0]
        for planet2 in planets:
            if planet2 is not planet1:
                distance = ((planet1.position[0] - planet2.position[0])**2 + (planet1.position[1] - planet2.position[1])**2)**0.5
                if distance < planet1.radius + planet2.radius:
                    force = -K * planet1.charge * planet2.charge * distance / ((planet1.radius + planet2.radius) ** 3)
                else:
                    force = -K * planet1.charge * planet2.charge / (distance ** 2)
                cos = (planet2.position[0] - planet1.position[0]) / distance
                sin = (planet2.position[1] - planet1.position[1]) / distance
                planet1.acceleration[0] += force * cos/planet1.mass
                planet1.acceleration[1] += force * sin/planet1.mass

                x21 = [-planet1.position[0] + planet2.position[0], -planet1.position[1] + planet2.position[1]]
                if distance < planet1.radius + planet2.radius:
                    u1 = [componentof(planet1.velocity, x21)*cos, componentof(planet1.velocity, x21)*sin]
                    u2 = [componentof(planet2.velocity, x21)*cos, componentof(planet2.velocity, x21)*sin]
                    if mod(x21[0]*u1[0]) != 0:
                        mag_u1 = magnitude(u1)*x21[0]*u1[0]/mod(x21[0]*u1[0])
                        mag_u2 = magnitude(u2) * x21[0] * u2[0] / mod(x21[0] * u2[0])
                    else:
                        mag_u1 = magnitude(u1)
                        mag_u2 = magnitude(u2)
                    if mag_u1 > mag_u2:
                        v1 = (mag_u1*(planet1.mass - planet2.mass) + 2*planet2.mass*mag_u2)/(planet1.mass + planet2.mass)
                        velVector = [v1*cos, v1*sin]
                        velocity = [0, 0]
                        velocity[0] = - u1[0] + velVector[0]
                        velocity[1] = - u1[1] + velVector[1]
                        velocity_changes[planets.index(planet1)][0] += velocity[0]
                        velocity_changes[planets.index(planet1)][1] += velocity[1]
#                    position_changes[planets.index(planet1)][0] = -cos*(-distance + planet1.radius + planet2.radius)*planet2.mass/(planet1.mass + planet2.mass)
#                    position_changes[planets.index(planet1)][1] = -sin*(-distance + planet1.radius + planet2.radius)*planet2.mass/(planet1.mass + planet2.mass)
#                    planet1.velocity = [-planet1.velocity[0], -planet1.velocity[1]]
    for i in range(len(planets)):
        planets[i].velocity[0] += velocity_changes[i][0]
        planets[i].velocity[1] += velocity_changes[i][1]
        planets[i].position[0] += position_changes[i][0]
        planets[i].position[1] += position_changes[i][1]


running = True

planets = []
tim = 0
planets.append(Planet(1000, 0, [300, 500], 30, [150, 150, 200]))
#planets.append(Planet(1, -1, [300, 300], 30, [150, 150, 200]))
#planets.append(Planet(1, 1, [500, 400], 30, [200, 150, 150]))
#planets.append(Planet(1, -1, [500, 200], 30, [150, 150, 200]))
#planets.append(Planet(1, -1, [400, 200], 30, [150, 150, 200]))
#planets.append(Planet(1, -1, [500, 600], 30, [150, 150, 200]))
#planets.append(Planet(1, -1, [400, 600], 30, [150, 150, 200]))
#planets.append(Planet(1, -1, [300, 600], 30, [150, 150, 200]))
for i in range(10):
    planets.append(Planet(1, 2, [random.random()*800, random.random()*600], 30, [255, 180, 150]))
for i in range(10):
    planets.append(Planet(0.1, -2, [random.random()*800, random.random()*600], 10, [150, 170, 255]))
#for i in range(10):
#    planets.append(Planet(1, 1, [random.random()*800, random.random()*600], 30, [150, 150, 250]))
#for i in range(10):
#    planets.append(Planet(1, -1, [random.random()*800, random.random()*600], 30, [150, 150, 250]))

counter = 0
tim1 = time.time_ns()


def update_loop():
    global dt
    global counter
    global planets
    global running
    global tim1
    counter += 1
    if counter >= 100:
        counter = 0
        print(100000000000/(time.time_ns() - tim1))
        tim1 = time.time_ns()

        print(int(1 / dt))
    for i in range(len(planets) - 1):
        planets[i + 1].update()
    molecular_force(planets)
    for planet in planets:
        planet.collided = False



def render_loop2():
    global running
    global planets
    global screen
    pygame.init()
    screen = pygame.display.set_mode((screenLength, screenWidth))
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if pygame.mouse.get_pressed()[0]:
            planets[0].charge = 5
            planets[0].position = list(pygame.mouse.get_pos())
            planets[0].draw()
        else:
            planets[0].charge = 0
        for i in range(len(planets) - 1):
            planets[i + 1].draw()
        #    print(planet1.acceleration)
        pygame.display.update()


def render_loop():
    global running
    global planets
    global screen
    pygame.init()
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if pygame.mouse.get_pressed()[0]:
        planets[0].charge = 5
        planets[0].position = list(pygame.mouse.get_pos())
        planets[0].draw()
    else:
        planets[0].charge = 0
    for i in range(len(planets) - 1):
        planets[i + 1].draw()
    #    print(planet1.acceleration)
    pygame.display.update()


#with concurrent.futures.ProcessPoolExecutor() as executor:



while running:
    tim = time.time_ns()
    if dt > 0.05:
        dt = 0.05

    update_loop()
    render_loop()

    dt = (time.time_ns() - tim) / 10000000000


def main():
    while running:
        tim = time.time_ns()
        if dt > 0.05:
            dt = 0.05
        counter += 1
        if counter > 100:
            counter = 0
            print(int(1/dt))
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if pygame.mouse.get_pressed()[0]:
            planets[0].charge = 5
            planets[0].position = list(pygame.mouse.get_pos())
            planets[0].draw()
        else:
            planets[0].charge = 0
        for i in range(len(planets) - 1):
            planets[i + 1].draw()
            planets[i + 1].update()
        molecular_force(planets)
    #    print(planet1.acceleration)
        pygame.display.update()
        for planet in planets:
            planet.collided = False
        dt = 5*(time.time_ns() - tim)/10000000000

