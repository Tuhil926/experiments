import pygame
import random
import math
import time

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('background.jpg')
bkgrnd = pygame.transform.scale(background, (800, 600))

pygame.display.set_caption("Space invaders")
img = pygame.image.load('invader.png')
icon = pygame.transform.scale(img, (32, 32))
pygame.display.set_icon(icon)

playerImg = pygame.image.load("invader.png")
playerX = 370
playerY = 480
plX_chng = 0
plY_chng = 0
player_health = 1000

enemyImg = []
enemyX = []
enemyY = []
enemyX_chng = []
enemyY_change = []
enemyY_chng = []
num_of_enemies = 6
enemy_health = []
tot_boss_health = 2048

for i in range(num_of_enemies - 1):
    enemyImg.append(pygame.image.load("spaceship.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(-random.randint(64, 150))
    enemyX_chng.append(3)
    enemyY_change.append(20)
    enemyY_chng.append(40)
    enemy_health.append(64)
enemyImg.append(pygame.image.load("boss.png"))
enemyX.append(random.randint(0, 672))
enemyY.append(-random.randint(128, 150))
enemyX_chng.append(2)
enemyY_chng.append(40)
enemy_health.append(tot_boss_health)
boss_no = 5

bombImg = pygame.image.load("bomb.png")
bombX = enemyX[5] + 55
bombY = enemyY[5] + 50
bombX_chng = 0
bombY_chng = 2
bomb_health = 100
bomb_damage = 100
bomb_state = "ready"

bulletImg1 = pygame.image.load("bullet.png")
bulletImg2 = pygame.image.load("bullet2.png")
bulletImg3 = pygame.image.load("bullet3.png")
bulletImg = bulletImg1
bulletX = playerX
bulletY = playerY
bulletX_chng = 0
bulletY_chng = 15
bullet_state = "ready"
bullet_damage = 15
bullet_health = 100

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10

# random variables
frame_counter = 0
bullet_timer = 0
frame_counter2 = 0
timer = 0
upgrade_timer = 0.01
hr_timer = 0
firing = False
reload_timer = 0
reload = 30


class projectile(object):
    def __init__(self, image, x, y, damage, health, vel):
        self.image = image
        self.x = x
        self.y = y
        self.damage = damage
        self.health = health
        self.vel = vel

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the Button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 50)
            text = font.render(self.text, 1, (100, 255, 100))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (225, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collosion(enemyx, enemyy, playerx, playery, d):
    distance = math.sqrt((math.pow((enemyx + 5) - playerx, 2)) + (math.pow((enemyy + 5) - playery, 2)))
    if distance < d:
        return True
    else:
        return False


bullets = []
play_button = button((0, 200, 0), 350, 400, 100, 40, "Play")
upgrade_button = button((0, 200, 0), 325, 50, 150, 40, "Upgrade")
running = True
game_running = False
while running:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            if play_button.isOver(pos):
                play_button.color = (0, 240, 0)
            else:
                play_button.color = (0, 200, 0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.isOver(pos):
                plX_chng = 0
                plY_chng = 0
                playerX = 370
                playerY = 480
                bullet_state = "ready"
                score_value = 0
                frame_counter = 0
                bomb_state = "ready"
                player_health = 1000
                enemy_health[5] = tot_boss_health
                bomb_state = "ready"
                bullet_damage = 15
                upgrade_timer = 0
                bulletImg = bulletImg1
                for i in range(num_of_enemies - 1):
                    enemyX[i] = random.randint(0, 735)
                    enemyY[i] = -random.randint(64, 150)
                    enemyY_chng[i] = 20
                enemyX[boss_no] = random.randint(0, 672)
                enemyY[boss_no] = -random.randint(128, 150)
                time.sleep(0.4)
                game_running = True

    screen.blit(bkgrnd, (0, 0))
    font2 = pygame.font.Font("freesansbold.ttf", 64)
    intro = font2.render("Space Invaders 2", True, (200, 0, 50))
    intro2 = font.render("Press S to start", True, (190, 0, 60))
    scr = font.render("Score: "+ str(score_value), True, (200, 0, 50))
    screen.blit(intro, (130, 250))
    screen.blit(scr, (250, 330))
    play_button.draw(screen, (0, 100, 0))

    while game_running:
        upgrade = False

        screen.fill((12, 0, 20))

        screen.blit(bkgrnd, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    time.sleep(1)
                    game_running = False
                if event.key == pygame.K_a:
                    plX_chng -= 5
                if event.key == pygame.K_d:
                    plX_chng += 5
                if event.key == pygame.K_w:
                    plY_chng -= 5
                if event.key == pygame.K_s:
                    plY_chng += 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletY = playerY
                        bulletX = playerX
                        bullet_state = "fire"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    plX_chng += 5
                if event.key == pygame.K_d:
                    plX_chng -= 5
                if event.key == pygame.K_w:
                    plY_chng += 5
                if event.key == pygame.K_s:
                    plY_chng -= 5
            if event.type == pygame.MOUSEBUTTONDOWN:
                if len(bullets) < 5:
                    bullets.append(projectile(bulletImg, playerX+16, playerY+16, 15, 100, -15))
                if bullet_state == "ready":
                    bulletY = playerY
                    bulletX = playerX
                    bullet_state = "fire"

        playerX += plX_chng
        playerY += plY_chng

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736
        if playerY <= 0:
            playerY = 0
        elif playerY >= 536:
            playerY = 536

        for i in range(num_of_enemies - 1):
            enemyX[i] += enemyX_chng[i]

            if enemyX[i] <= 0:
                enemyX_chng[i] = 3
                enemyY[i] += enemyY_chng[i]
            elif enemyX[i] >= 736:
                enemyX_chng[i] = -3
                enemyY[i] += enemyY_chng[i]

            for bullet in bullets:
                collision = is_collosion(enemyX[i], enemyY[i], bullet.x, bullet.y, 32)
                if bullet_state == "fire":
                    if collision:
                        bullet.health -= 4
                        if bullet.health <= 0:
                            bullet.health = 100
                            bullet.y = playerY
                            bullet_state = "ready"
                        enemy_health[i] -= bullet.damage
                        enemyY[i] -= 10
                        if enemy_health[i] <= 0:
                            enemyX[i] = random.randint(0, 735)
                            enemyY[i] = -random.randint(64, 150)
                            enemy_health[i] = 64
                            score_value += 300
            enemy(enemyX[i], enemyY[i], i)
            if enemy_health[i] < 64:
                pygame.draw.rect(screen, (255, 255, 255), [enemyX[i], enemyY[i] - 10, 64, 5], )
                pygame.draw.rect(screen, (0, 255, 0), [enemyX[i], enemyY[i]-10, enemy_health[i], 5],)
            if enemyY[i] > 550:
                game_running = False

        if frame_counter > 500:
            if bomb_state == "ready":
                bomb_health = 100
                bomb_state = "fire"
                bombX = enemyX[5] + 55
                bombY = enemyY[5] + 100
            if bomb_state == "fire":
                if bomb_health < 0:
                    bomb_state = "fire"
                bombY += 2*bombY_chng
                screen.blit(bombImg, (bombX, bombY))
                if bombY > 600:
                    bombY = enemyY[5] + 20
                    bomb_state = "ready"
            enemyX[boss_no] += enemyX_chng[boss_no]
            enemyY[boss_no] += enemyY_chng[boss_no]

            if playerX - enemyX[boss_no] > 32:
                enemyX_chng[boss_no] = 2
            elif playerX - enemyX[boss_no] < 32:
                enemyX_chng[boss_no] = -2
            else:
                enemyX_chng[boss_no] = 0

            if playerY - enemyY[boss_no] > 375:
                enemyY_chng[boss_no] = 1
            elif playerY - enemyY[boss_no] < 375:
                enemyY_chng[boss_no] = -1
            else:
                enemyY_chng[boss_no] = 0
            for bullet in bullets:
                collision = is_collosion(enemyX[5] + 40, enemyY[5], bullet.x, bullet.y, 64)
                if bullet_state == "fire":
                    if collision:
                        bullet.health -= 4
                        if bullet.health <= 0:
                            bullet.health = 100
                            bullet.y = playerY
                            bullet_state = "ready"
                        enemy_health[5] -= bullet.damage
                        enemyY[boss_no] -= 2
            if enemy_health[5] < 0:
                bomb_state = "ready"
                score_value += 5000
                enemy_health[5] = tot_boss_health
                enemyX[5] = random.randint(0, 672)
                enemyY[5] = -random.randint(128, 150)
                frame_counter = 0
            enemy(enemyX[boss_no], enemyY[boss_no], boss_no)
            pygame.draw.rect(screen, (255, 255, 255), [enemyX[5], enemyY[5] - 10, 128, 5], )
            pygame.draw.rect(screen, (0, 255, 0), [enemyX[5], enemyY[5] - 10, enemy_health[5]/tot_boss_health * 128, 5], )
            col = is_collosion(bombX + 12, bombY + 12, playerX + 32, playerY + 32, 32)
            if col:
                player_health -= bomb_damage
                bomb_health -= 10

        for bullet in bullets:
            bullet.draw()
            bullet.y += bullet.vel
            if bullet.y < -32:
                bullets.pop(bullets.index(bullet))

        if bulletY <= -32:
            bulletY = playerY
            bullet_state = "ready"

        if bullet_state == "fire":
            bulletY -= bulletY_chng
            fire_bullet(bulletX, bulletY)

        frame_counter += 1
        if frame_counter > 10000:
            frame_counter = 10000

        show_score(textX, textY)
        player(playerX, playerY)
        if player_health < 1000:
            pygame.draw.rect(screen, (255, 255, 255), [playerX, playerY - 10, 64, 5], )
            pygame.draw.rect(screen, (0, 255, 0), [playerX, playerY - 10, player_health/1000 * 64, 5], )
            hr_timer += 0.01
            if hr_timer > 4:
                hr_timer = 4.1
                player_health += 1
        if player_health >= 1000:
            hr_timer = 0
            player_health = 1000
        if player_health <= 0:
            player_health = 0
            game_over = font2.render("GAME OVER", True, (225, 0, 0))
            screen.blit(game_over, (210, 260))
            time.sleep(.3)
            game_running = False
        frame_counter2 += 1
        upgrade_timer += 0.01
        if score_value > 10000:
            bulletImg = bulletImg3
            bullet_damage = 25
            for bullet in bullets:
                bullet.damage = 25
            if score_value > 20000:
                tot_boss_health = 3000
                bulletImg = bulletImg2
                bullet_damage = 50
                for bullet in bullets:
                    bullet.damage = 50
                if score_value > 30000:
                    tot_boss_health = 5000
                    bullet_damage = 100
                    for bullet in bullets:
                        bullet.damage = 100
        if frame_counter2 > 2000:
            for i in range(num_of_enemies - 1):
                enemyY_chng[i] += timer
            frame_counter2 = 0
            timer += 1

        pygame.display.update()
        if player_health <= 0:
            time.sleep(1)
    pygame.display.update()
print("score: ", score_value)
