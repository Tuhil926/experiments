import pygame
import random
from time import sleep
import math

pygame.init()


def move_X(angle, distance):
    return math.sin(angle/57.5) * distance


def move_Y(angle, distance):
    return math.cos(angle/57.5) * distance


class player(object):
    def __init__(self, x, y, tank, color, speed, movex, movey, body_damage, max_health, health_regen):
        self.x = x
        self.y = y
        self.tank = tank
        self.color = color
        self.speed = speed
        self.movex = movex
        self.movey = movey
        self.body_damage = body_damage
        self.max_health = max_health
        self.health_regen = health_regen

    def move(self):
        self.x += self.speed * self.movex
        self.y += self.speed * self.movey

    def draw(self):
        # pygame.draw.circle(screen, self.color, [750, 395], 20, 20)
        # pygame.draw.circle(screen, (150, 150, 200), [750, 395], 22, 2)
        screen.blit(player_img, (730, 375))


class bullet(object):
    def __init__(self, x, y, color, image, screen, penetration, damage, life, angle, rad):
        self.x = x
        self.y = y
        self.color = color
        self.image = image
        self.screen = screen
        self.penetration = penetration
        self.damage = damage
        self.life = life
        self.angle = angle
        self.rad = rad

    def move(self, angle, distance):
        self.x += math.sin(angle/57.5) * distance
        self.y += math.cos(angle/57.5) * distance

    def draw(self, x, y):
        self.screen.blit(self.image, (x, y))


class square(object):
    def __init__(self, x, y, color, rotation, image, screen, rad, health):
        self.x = x
        self.y = y
        self.color = color
        self.rotation = rotation
        self.image = image
        self.screen = screen
        self.rad = rad
        self.health = health

    def draw(self, x, y):
        pygame.draw.rect(self.screen, self.color, [x, y, 20, 20])
        #self.screen.blit(self.image, (int(x), int(y)))


def is_collision(object1, object2, mapx, mapy):
    dist = math.sqrt(math.pow((object2.x - object1.x - mapx), 2) + math.pow((object2.y - object1.y - mapy), 2))
    if dist < object1.rad + object2.rad:
        return True


screen = pygame.display.set_mode((1500, 790))

player_img = pygame.image.load("circle.png")
square_im = pygame.image.load("square.png")
barrl = pygame.image.load("tnk.png")
barrel = pygame.transform.scale(barrl, (50, 50))
square_ig = pygame.transform.scale(square_im, (20, 20))

# Colours
screen_color = (225, 225, 225)
map_color = (255, 255, 255)

# Coordinates
mapx = -random.randint(0, 9000)
mapy = -random.randint(0, 9000)
map_width = 9000
map_height = 9000

# random variables
speedmax = 2.5
max_speed = speedmax
bullet_speed = 5
acc = 0.1
r2 = 1.4142
no_sqr = 2000

playerxchng = 0
playerychng = 0
playerxa = 0
playerya = 0

ran_x = []
ran_y = []
ran_rot = []
squares = []
bullets = []
for i in range(no_sqr):
    ran_x.append(random.randint(0, map_width - 64))
    ran_y.append(random.randint(0, map_height - 64))
    ran_rot.append(random.randint(0, 0))
    squares.append(square(mapx + ran_x[i], mapy + ran_y[i], (255, 255, 50), ran_rot[i], pygame.transform.rotate(square_ig, ran_rot[i]), screen, 10, 10))

player = player(mapx, mapy, "basic", (0, 200, 255), 1, 1, 1, 10, 10, 10)
reload_counter = 0
running = True
while running:
    mouseX, mouseY = pygame.mouse.get_pos()
#    for event in pygame.event.get():
#        if event.type == pygame.MOUSEMOTION:
#            mouseX, mouseY = event.pos
    angle = math.atan2(-mouseY + 395, mouseX - 750)
    screen.fill(screen_color)
    keys = pygame.key.get_pressed()
    reload_counter += 1
    if keys[32] == 0:
        if reload_counter > 5:
            num = random.randint(0, 7)
            b_angle = (angle * 57.5) + 90 + num - 3.5
            bullets.append(bullet(-mapx + 745, -mapy + 390, (100, 200, 255), pygame.transform.scale(player_img, (10, 10)), screen, 10, 5, 150, b_angle, 4))
            playerxchng += move_X(b_angle, 0.5)
            playerychng += move_Y(b_angle, 0.5)
            reload_counter = 0
    pygame.draw.rect(screen, map_color, [mapx, mapy, map_width, map_height])
    # for i in range(int(map_width/10)):
    #     pygame.draw.line(screen, (225, 225, 225), (mapx + i*10, mapy), (mapx + i*10, mapy + map_height))
    # for i in range(int(map_height/10)):
    #     pygame.draw.line(screen, (225, 225, 225), (mapx, mapy + i*10), (mapx + map_width, mapy + i*10))
    for i in range(no_sqr):
        squares[i].x = mapx + ran_x[i]
        squares[i].y = mapy + ran_y[i]
    for bulle in bullets:
        bulle.move(bulle.angle, bullet_speed)
        bulle.draw(bulle.x + mapx, mapy + bulle.y)
        bulle.life -= 1
        if bulle.life < 1:
            bullets.pop(bullets.index(bulle))
    rot_img = pygame.transform.rotate(barrel, (angle * 57.5)- 90)
    screen.blit(rot_img, (750 - int(rot_img.get_width() / 2), 395 - int(rot_img.get_width() / 2)))
    # player.draw()
    if playerxchng >= max_speed:
        playerxchng -= 2*acc
        if playerxchng >= max_speed + 5:
            playerxchng = max_speed + 5
    if playerxchng <= -max_speed:
        playerxchng -= -2*acc
        if playerxchng <= -(max_speed + 5):
            playerxchng = -(max_speed + 5)
    if playerychng >= max_speed:
        playerychng -= 2*acc
        if playerychng >= max_speed + 5:
            playerychng = max_speed + 5
    if playerychng <= -max_speed:
        playerychng -= -2*acc
        if playerychng <= -(max_speed + 5):
            playerychng = -(max_speed + 5)
    playerxchng += playerxa
    playerychng += playerya
    mapx += playerxchng
    mapy += playerychng
    if mapx > 800:
        mapx = 800
    if mapy > 445:
        mapy = 445
    if mapx < -(map_width - 695):
        mapx = -(map_width - 695)
    if mapy < -(map_height - 340):
        mapy = -(map_height - 340)

    for bulle in bullets:
        for squar in squares:
            if 1540 > squar.x > -40 and 830 > squar.y > -40:
                if is_collision(bulle, squar, mapx, mapy):
                    squar.health -= bulle.damage
                    squar.x += move_X(angle, 5)
                    squar.y += move_Y(angle, 5)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    if keys[97] == 1:
        playerxa = acc
        playerxchng += acc
        if keys[119] == 1 or keys[115] == 1:
            max_speed = speedmax/r2
        else:
            max_speed = speedmax
    elif keys[100] == 1:
        playerxa = -acc
        playerxchng -= acc
        if keys[119] == 1 or keys[115] == 1:
            max_speed = speedmax/r2
        else:
            max_speed = speedmax
    elif playerxchng > 0:
        playerxa = -((acc/5) * playerxchng + 0.1)
    elif playerxchng < 0:
        playerxa = (acc/5) * -playerxchng + 0.1
    else:
        playerxa = 0

    if keys[119] == 1:
        playerya = acc
        playerychng += acc
    elif keys[115] == 1:
        playerya = -acc
        playerychng -= acc
    elif playerychng > 0:
        playerya = -((acc/5) * playerychng + 0.1)
    elif playerychng < 0:
        playerya = (acc/5) * -playerychng + 0.1
    else:
        playerya = 0

    for squar in squares:
        if 1540 > squar.x > -40 and 830 > squar.y > -40:
            if squar.health > 0:
                squar.draw(squar.x, squar.y)

    pygame.display.update()
    sleep(0.000)
for i in range(len(keys)):
    if keys[i] == 1:
        print(i)
