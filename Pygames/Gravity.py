import pygame
import numpy as np
import time

screenWidth = 600
screenLength = 800

screen = pygame.display.set_mode((screenLength, screenWidth))

dt = 0
G = 1000000


class Planet:
    def __init__(self, mass, position, image, radius, color):
        self.mass = mass
        self.position = position
        self.image = image
        self.radius = radius
        self.width = self.radius
        self.color = color
        self.acceleration = [0, 0]
        self.velocity = [0, 0]
        self.collided = False
        self.line = []

    def draw(self):
        if self.image is not None:
            screen.blit(self.image, (self.position[0] - self.image.get_width()/2, self.position[1] - self.image.get_height()/2))
        else:
            pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius, self.width)
        if len(self.line) >= 2:
            for i in range(len(self.line) - 1):
                pygame.draw.line(screen, [255 * i / len(self.line), 255 * i / len(self.line), 255 * i / len(self.line)], self.line[i], self.line[i + 1])

    def update(self):
        self.velocity[0], self.velocity[1] = self.velocity[0] + self.acceleration[0]*dt, self.velocity[1] + self.acceleration[1]*dt
        self.position[0], self.position[1] = self.position[0] + self.velocity[0]*dt, self.position[1] + self.velocity[1]*dt
        self.line.append(self.position)


def componentof(vector1, vector2):
    magVector2 = (vector2[0]**2 + vector2[1]**2)**0.5
    mag = vector1[0]*vector2[0]/magVector2 + vector1[1]*vector2[1]/magVector2
    return mag


def magnitude(vector2):
    return (vector2[0] ** 2 + vector2[1] ** 2) ** 0.5

def mod(n):
    if n >= 0:
        return  n
    else:
        return -n

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
                force = G*planet1.mass*planet2.mass/(distance**2)
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
planet1 = Planet(100, [400, 300], None, 30, [255, 255, 200])
planet2 = Planet(5, [123, 300], None, 10, [255, 200, 200])
planet3 = Planet(0.05, [96, 300], None, 7, [0, 255, 255])
planet4 = Planet(5, [600, 300], None, 20, [0, 255, 255])
planets.append(planet4)
planet3.velocity[0] = 0
planet3.velocity[1] = 170
planet2.velocity[0] = 0
planet2.velocity[1] = 600
planet1.velocity[0] = 0
planet1.velocity[1] = -(planet2.velocity[1]*planet2.mass + planet3.velocity[1]*planet3.mass)/planet1.mass
planets.append(planet1)
planets.append(planet2)
planets.append(planet3)
tim = 0
time.sleep(2)
while running:
    tim = time.time_ns()
    if dt > 0.05:
        dt = 0.05
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for planet in planets:
        planet.draw()
        planet.update()
    gravity(planets)
#    print(planet1.acceleration)
    pygame.display.update()
    for planet in planets:
        planet.collided = False
    dt = 5*(time.time_ns() - tim)/10000000000

