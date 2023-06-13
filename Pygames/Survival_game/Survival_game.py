import pygame
import time

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Map:
    def __init__(self, size):
        self.size = size

    def draw(self, player_pos, screen):
        pygame.draw.rect(screen, (255, 255, 255), [-player_pos[0] + SCREEN_WIDTH/2, -player_pos[1] + SCREEN_HEIGHT/2, self.size[0], self.size[1]])


class Player:
    def __init__(self):
        self.color = (100, 180, 255)
        self.border_color = (80, 140, 200)
        self.pos = [0, 0]
        self.map_dimensions = [0, 0]
        self.speed = 200

    def draw(self, screen):
        pygame.draw.circle(screen, self.border_color, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), 22)
        pygame.draw.circle(screen, self.color, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 20)

    def update(self, w, a, s, d, mouse_pos, mouse_clicked, dt):
        if w:
            self.pos[1] -= self.speed*dt
        if a:
            self.pos[0] -= self.speed*dt
        if s:
            self.pos[1] += self.speed*dt
        if d:
            self.pos[0] += self.speed*dt

        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[0] > self.map_dimensions[0]:
            self.pos[0] = self.map_dimensions[0]
        if self.pos[1] < 0:
            self.pos[1] = 0
        if self.pos[1] > self.map_dimensions[1]:
            self.pos[1] = self.map_dimensions[1]

    def check_for_movement(self, dt):
        keys = pygame.key.get_pressed()
        w = keys[pygame.K_w]
        a = keys[pygame.K_a]
        s = keys[pygame.K_s]
        d = keys[pygame.K_d]
        self.update(w, a, s, d, 0, 0, dt)


map = Map([1000, 1000])
player = Player()
player.map_dimensions = map.size

dt = 0
time_prev = time.time_ns()

running = True
while running:
    dt = (time.time_ns() - time_prev)/1000000000
    time_prev = time.time_ns()
    main_screen.fill((200, 200, 200))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.check_for_movement(dt)

    map.draw(player.pos, main_screen)
    player.draw(main_screen)

    pygame.display.update()


