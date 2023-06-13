import pygame
import time
import random
import math


def move_X(angle, distance):
    return math.sin(angle/57.5) * distance


def move_Y(angle, distance):
    return math.cos(angle/57.5) * distance


pygame.init()
window_width = 800
window_height = 600
tot_scrnX = -800
tot_scrnY = -600
screen = pygame.display.seqt_mode((800, 600))

screenX = -800
screenX_chng = 0
screenY = -600
screenY_chng = 0
screen_width = 2400
screen_height = 1800

player_posX = screenX - 400
player_posY = screenY - 300

bulletImg = pygame.image.load("circle.png")
bulletX = 400
bulletY = 300
bulletX_chng = 0
bulletY_chng = 15
bullet_state = "ready"
bullet_damage = 15
bullet_health = 100
b_angle = 0
bullet_timer = 0

ran_x = []
ran_y = []

imgX = 400
imgY = 300

img = pygame.image.load("monsters.png")
player = pygame.image.load("invader.png")
for i in range(50):
    ran_x.append(random.randint(0, screen_width - 64))
    ran_y.append(random.randint(0, screen_height - 64))

running = True
while running:
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), [screenX, screenY, screen_width, screen_height])
    for i in range(len(ran_x)):
        screen.blit(img, (screenX + ran_x[i], screenY + ran_y[i]))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_a:
                screenX_chng += 1
            if event.key == pygame.K_d:
                screenX_chng -= 1
            if event.key == pygame.K_w:
                screenY_chng += 1
            if event.key == pygame.K_s:
                screenY_chng -= 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                screenX_chng -= 1
            if event.key == pygame.K_d:
                screenX_chng += 1
            if event.key == pygame.K_w:
                screenY_chng -= 1
            if event.key == pygame.K_s:
                screenY_chng += 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if bullet_state == "ready":
                player_posX = screenX - 400
                player_posY = screenY - 300
                bullet_state = "fire"
                b_angle = (angle * 57.5) - 90
    angle = math.atan2(-mouseY + 300, mouseX - 400)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if bullet_state == "ready":
                player_posX = screenX - 400
                player_posY = screenY - 300
                bullet_state = "fire"
                b_angle = (angle * 57.5) - 90

    if bullet_state == "ready":
        player_posX = screenX - 400
        player_posY = screenY - 300
        rot_bullet = pygame.transform.rotate(bulletImg, (angle * 57.5) - 90)
        screen.blit(rot_bullet, (bulletX - int(rot_bullet.get_width()/2), bulletY - int(rot_bullet.get_width()/2)))
    if bullet_state == "fire":
        bullet_timer += 1
        if bullet_timer > 250:
            bullet_state = "ready"
            bullet_timer = 0
        bulletX_chng = 1
        rot_bullet = pygame.transform.rotate(bulletImg, b_angle)
        screen.blit(rot_bullet, (screenX - player_posX - int(rot_bullet.get_width()/2), screenY - player_posY - int(rot_bullet.get_width()/2)))
    player_posX += 2 * move_X(b_angle, bulletX_chng)
    player_posY += 2 * move_Y(b_angle, bulletX_chng)
    screenX += screenX_chng
    screenY += screenY_chng
    rot_img = pygame.transform.rotate(player, (angle * 57.5) - 90)
    screen.blit(rot_img, (imgX - int(rot_img.get_width() / 2), imgY - int(rot_img.get_width() / 2)))
    if screenX_chng > 1 or screenX_chng < -1:
        screenX_chng = 0
    if screenY_chng > 1 or screenY_chng < -1:
        screenY_chng = 0
    if screenX > window_width/2 - 20:
        screenX = window_width/2 - 20
    if screenX < -screen_width + 420:
        screenX = -screen_width + 420
    if screenY > window_height/2 - 20:
        screenY = window_height/2 - 20
    if screenY < -screen_height + 320:
        screenY = -screen_height + 320
    pygame.display.update()
print(screenX)
print(screenY)