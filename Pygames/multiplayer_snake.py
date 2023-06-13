import pygame
import random
import time
import win32api
import win32con
import win32gui

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
fuchsia = (0, 0, 0)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)

hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)


class Map:
    def __init__(self):
        self.size_of_a_cell = 20
        self.grid = []
        for i in range(SCREEN_HEIGHT//self.size_of_a_cell):
            row = []
            for j in range(SCREEN_WIDTH//self.size_of_a_cell):
                row.append(0)
            self.grid.append(row)
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        self.game_over = False

    def draw_player(self, player):
        for point in player.points[:-1:]:
            pygame.draw.rect(screen, player.color, (point[0]*self.size_of_a_cell, point[1]*self.size_of_a_cell, self.size_of_a_cell, self.size_of_a_cell))


class Player:
    def __init__(self, map, inputs=(0, 1, 2, 3, 4), pos = (1, 0)):
        self.map = map
        self.pos = [pos[0], pos[1]]
        self.pos_on_screen = [self.pos[0]*self.map.size_of_a_cell, self.pos[1]*self.map.size_of_a_cell]
        self.points = [(self.pos[0] - 1, self.pos[1]), (self.pos[0], self.pos[1])]
        self.direction = 0  # 0 is right, 1 is up, 2 is left, 3 is down
        self.id = random.randint(0, 100000)
        self.color = (255, 60, 0)
        self.sprite_color = (255, 150, 100)
        self.last_updated = time.time_ns()/1000000000
        self.last_removed = time.time_ns()/1000000000
        self.last_dead_removed = time.time_ns()/1000000000
        self.wasd = [0, 0, 0, 0]
        self.input_buffer = []
        self.speed = 10
        self.remove_speed = 35
        self.die_speed = 60
        self.is_dead = False
        self.inputs = inputs
        self.dead_size = self.map.size_of_a_cell
        self.rotation = 0

    def update(self):
        now = time.time_ns()/1000000000

        if self.is_dead:
            if now - self.last_dead_removed > 1/self.die_speed:
                self.points.pop(-1)
                self.last_dead_removed = now
                self.dead_size *= 0.7
            return

        if self.speed and now - self.last_updated >= 1/self.speed:
            if len(self.input_buffer):
                direction = self.input_buffer.pop(0)
                if abs(self.direction - direction) != 2:
                    self.direction = direction
            if self.direction == 0:
                self.pos[0] += 1
            elif self.direction == 1:
                self.pos[1] -= 1
            elif self.direction == 2:
                self.pos[0] -= 1
            elif self.direction == 3:
                self.pos[1] += 1
            self.last_updated = now

            if self.pos[0] < 0 or self.pos[1] < 0 or self.pos[0] >= self.map.width or self.pos[1] >= self.map.height or tuple(self.pos) in self.points:
                self.is_dead = True

            self.points.append((self.pos[0], self.pos[1]))

        self.pos_on_screen[0] = self.points[-2][0]*self.map.size_of_a_cell
        self.pos_on_screen[1] = self.points[-2][1] * self.map.size_of_a_cell

        if self.direction == 0:
            self.pos_on_screen[0] += (now - self.last_updated) * self.speed * self.map.size_of_a_cell
        if self.direction == 1:
            self.pos_on_screen[1] -= (now - self.last_updated) * self.speed * self.map.size_of_a_cell
        if self.direction == 2:
            self.pos_on_screen[0] -= (now - self.last_updated) * self.speed * self.map.size_of_a_cell
        if self.direction == 3:
            self.pos_on_screen[1] += (now - self.last_updated) * self.speed * self.map.size_of_a_cell

        #keys = pygame.key.get_pressed()
        #print(self.wasd)

    def take_input(self, keys):
        now = time.time_ns() / 1000000000
        if len(self.input_buffer) <= 2:
            if keys[self.inputs[0]] - self.wasd[0] == 1:
                self.input_buffer.append(1)
            if keys[self.inputs[1]] - self.wasd[1] == 1:
                self.input_buffer.append(2)
            if keys[self.inputs[2]] - self.wasd[2] == 1:
                self.input_buffer.append(3)
            if keys[self.inputs[3]] - self.wasd[3] == 1:
                self.input_buffer.append(0)

        if keys[self.inputs[0]]:
            self.wasd[0] = 1
        else:
            self.wasd[0] = 0
        if keys[self.inputs[1]]:
            self.wasd[1] = 1
        else:
            self.wasd[1] = 0
        if keys[self.inputs[2]]:
            self.wasd[2] = 1
        else:
            self.wasd[2] = 0
        if keys[self.inputs[3]]:
            self.wasd[3] = 1
        else:
            self.wasd[3] = 0

        if keys[self.inputs[4]]:
            self.go_fast()
        else:
            self.speed = 10

    def go_fast(self):
        now = time.time_ns() / 1000000000
        if len(self.points) > 2 and not self.map.game_over:
            if now - self.last_removed > 1 / self.remove_speed:
                self.speed = 20
                self.points.pop(0)
                self.last_removed = now
        else:
            self.speed = 10

    def draw(self):
        if not self.is_dead:
            pygame.draw.rect(screen, self.sprite_color, (self.pos_on_screen[0], self.pos_on_screen[1], self.map.size_of_a_cell, self.map.size_of_a_cell))
        else:
            pygame.draw.rect(screen, self.sprite_color, (
                self.pos_on_screen[0] + self.map.size_of_a_cell/2 - self.dead_size/2, self.pos_on_screen[1] + self.map.size_of_a_cell/2 - self.dead_size/2, self.dead_size, self.dead_size))

    def next_pos(self):
        if self.direction == 0:
            return self.pos[0] + 1, self.pos[1]
        elif self.direction == 1:
            return self.pos[0], self.pos[1] - 1
        elif self.direction == 2:
            return self.pos[0] - 1, self.pos[1]
        elif self.direction == 3:
            return self.pos[0], self.pos[1] + 1


bot_going_fast = False


def update_bots(bots, players):
    global bot_going_fast
    for bot in bots:
        for player in players:
            org_dir = bot.direction
            colliding = False
            dir_to_turn = random.choice((-1, 1))
            for i in range(5):
                if bot.next_pos() in player.points or bot.next_pos()[0] < 0 or bot.next_pos()[1] < 0 or bot.next_pos()[0] >= bot.map.width or bot.next_pos()[1] >= bot.map.height or tuple(bot.next_pos()) in bot.points or random.random() < 0.0001:
                    colliding = True
                    #print("coll")
                    bot.direction += dir_to_turn
                    if bot.direction < 0:
                        bot.direction = 3
                    elif bot.direction > 3:
                        bot.direction = 0
                else:
                    break
            if len(bot.input_buffer) < 2 and colliding and (not len(bot.input_buffer) or bot.input_buffer[-1] != bot.direction):
                bot.input_buffer.append(bot.direction)
                #print(bot.input_buffer)
            bot.direction = org_dir

        bot.update()

        if random.random() < 0.001:
            bot_going_fast = True
        if random.random() < 0.001 or len(bot.points) < 5:
            bot_going_fast = False

        bot.take_input((0, 0, 0, 0, bot_going_fast))


map = Map()
player1 = Player(map, pos=(0, 0))
player2 = Player(map, pos=(map.width - 2, map.height - 1), inputs=(0, 1, 2, 3, 4))
player2.direction = 2
player2.color = (20, 60, 255)
player2.sprite_color = (100, 150, 255)
player2.points = [(map.width - 1, map.height - 1), (map.width - 2, map.height - 1)]

players = [player1, player2]

running = True
while running:
    keys = pygame.key.get_pressed()
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player1.update()
    player1.take_input((keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d], keys[pygame.K_SPACE]))
    player2.update()
    player2.take_input((keys[pygame.K_UP], keys[pygame.K_LEFT], keys[pygame.K_DOWN], keys[pygame.K_RIGHT], keys[pygame.K_RSHIFT]))
    #update_bots((player2,), players)
    for player in players:
        map.draw_player(player)
        player.draw()
        for other_player in players:
            if other_player is not player:
                if tuple(player.pos) in other_player.points:
                    player.is_dead = True
        if player.is_dead:
            map.game_over = True

    for player in players:
        if player.is_dead:
            for player_ in players:
                player_.speed = 0
            if not len(player.points):
                running = False

    pygame.display.update()
