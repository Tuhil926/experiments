import pygame
import random
import time
import mysql.connector as sqltor
mycon = sqltor.connect(host="127.0.0.1", user="root", password="sql@123456", database="Tuhil")
scores = open("scores.txt", "a")
name = input("Enter your name: ")
print("Enjoy The game!")
cursor = mycon.cursor()
pygame.init()
screen = pygame.display.set_mode((800, 600))
pos = pygame.mouse.get_pos()
dt = 0
obstacle_speed = 500
score = 0
myfont = pygame.font.SysFont('Comic Sans MS', 30)

car_img1 = pygame.image.load("car.png")
car_img = pygame. transform. scale(car_img1, [30, 50])
tree_img1 = pygame.image.load("tree3.png")
tree_img = pygame. transform. scale(tree_img1, [50, 50])
colour2 = (70, 50, 0)

game_mode = "pos"

class car:
    def __init__(self, pos):
        self.pos = pos
        self.speed = 500

    def draw(self):
        #pygame.draw.rect(screen, [200, 100, 100], (self.pos[0], self.pos[1], 30, 50))
        screen.blit(car_img, self.pos)

    def update(self):
        self.speed = obstacle_speed
        keys = pygame.key.get_pressed()
        if keys[97]:
            self.pos[0] -= self.speed*dt
        if keys[100]:
            self.pos[0] += self.speed*dt
        if keys[pygame.K_w]:
            self.pos[1] -= self.speed*dt
        if keys[pygame.K_s]:
            self.pos[1] += self.speed*dt
        if self.pos[0] > 785:
            self.pos[0] = 785
        if self.pos[0] < -15:
            self.pos[0] = -15
        if self.pos[1] > 585:
            self.pos[1] = 585
        if self.pos[1] < -15:
            self.pos[1] = -15


class obstacle:
    def __init__(self, pos):
        self.pos = [random.random()*800, -100]
        self.speed = obstacle_speed

    def update(self):
        global running
        global score
        global game_mode
        global obstacles
        global obstacle_speed
        self.pos[1] += self.speed*dt
        self.speed = obstacle_speed
        if self.pos[0] + 50 > car1.pos[0] > self.pos[0] - 30:
            if self.pos[1] + 50 > car1.pos[1] > self.pos[1] - 50:
                game_mode = "pos"
                cursor.execute("INSERT INTO scores VALUES('" + name + "', " + str(score) + ");")
                score = 0
                obstacle_speed = 500
                obstacles = []


    def draw(self):
        #pygame.draw.rect(screen, [100, 100, 100], (self.pos[0], self.pos[1], 50, 50))
        screen.blit(tree_img, self.pos)


def menu():
    global game_mode
    text = myfont.render("Press s to start", False, (300, 250, 200))
    if pygame.key.get_pressed()[pygame.K_s]:
        game_mode = "game"
    screen.blit(text, (100, 100))


def check():
    keys = pygame.key.get_pressed()
    for i in range(len(pygame.key.get_pressed())):
        if keys[i] == 1:
            print(i)
obstacles = []
def make_obstacle():
    ran = random.random()
    if ran < 0.005:
        obstacles.append(obstacle([0, 0]))

car1 = car([385, 300])

time1 = time.time_ns()
time2 = time1
running = True
while running:
    if game_mode == "pos":
        screen.fill((0, 0, 0))
        text = myfont.render("Press s to start", False, (200, 200, 200))
        if pygame.key.get_pressed()[pygame.K_s]:
            print("s")
            game_mode = "game"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(text, (400 - text.get_width()/2, 300 - text.get_height()/2))
        pygame.display.update()
    if game_mode == "game":
        score += dt
        time1 = time.time_ns()
        make_obstacle()
        pos = pygame.mouse.get_pos()
        obstacle_speed += 20*dt
        if 10 < score < 11:
            colour2 = (0, 0, 30)
        if 20 < score < 21:
            colour2 = (0, 50, 0)
        if 30 < score < 31:
            colour2 = (60, 0, 30)
        #check()

        score_text = myfont.render(str(round(score, 2)), False, (200, 200, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(colour2)
        car1.draw()
        car1.update()
        for obstacle1 in obstacles:
            obstacle1.draw()
            obstacle1.update()
        
        screen.blit(score_text, (5, 5))
        pygame.display.update()
        
        time2 = time.time_ns()
        dt = (time2 - time1)/1000000000
print("score:",  score, "seconds")
mycon.commit()
mycon.close()
scores.write(name +" "+ str(score) + "\n")
scores.close()
pygame.quit()
