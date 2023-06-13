import pygame
import time
import random
import math
import win32api
import win32con
import win32gui

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)

fuchsia = (255, 0, 128)  # Transparency color

# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

invisibility_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
invisibility_screen.set_alpha(228)

mask = pygame.image.load("mask2.png")
masks = []
for i in range(25):
    masks.append(pygame.transform.scale(mask, (800 + i * 100, 800 + i * 100)))


class Vector:
    def __init__(self, *components):
        if isinstance(components[0], list) or isinstance(components[0], tuple):
            self.components = list(components[0])
        else:
            self.components = list(components)
        self.dimension = len(self.components)

    def __add__(self, other):
        v1 = self.components
        v2 = other.components
        if self.dimension >= other.dimension:
            for i in range(other.dimension):
                v1[i] += v2[i]
            return Vector(v1)
        else:
            for i in range(self.dimension):
                v2[i] += v1[i]
            return Vector(v2)

    def __sub__(self, other):
        v1 = self.components
        v2 = other.components
        if self.dimension >= other.dimension:
            for i in range(other.dimension):
                v1[i] -= v2[i]
            return Vector(v1)
        else:
            for i in range(self.dimension):
                v2[i] = v1[i] - v2[i]
            for j in range(self.dimension, other.dimension):
                v2[j] *= -1
            return Vector(v2)

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            v = self.components
            for i in range(self.dimension):
                v[i] *= other
            return Vector(v)

        elif isinstance(other, Vector):
            v1 = self.components
            v2 = other.components
            if self.dimension >= other.dimension:
                sum = 0
                for i in range(other.dimension):
                    sum += v1[i] * v2[i]
                return sum
            else:
                sum = 0
                for i in range(self.dimension):
                    sum += v1[i] * v2[i]
                return sum

    def __rmul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            v = self.components
            for i in range(self.dimension):
                v[i] *= other
            return Vector(v)

    def __mod__(self, other):
        if isinstance(other, Vector) and self.dimension <=3 and other.dimension <=3:
            res = [self[1]*other[2] - self[2]*other[1], self[2]*other[0] - self[0]*other[2], self[0]*other[1] - self[1]*other[0]]
            return Vector(res)
        else:
            raise TypeError("For cross product, two vectors of dimension less than 3 are required")

    def __getitem__(self, item):
        try:
            return self.components[item]
        except IndexError:
            return 0

    def __str__(self):
        return str(self.components)

    def __truediv__(self, other):
        return self*(1/other)

    def mag(self):
        sum = 0
        for component in self.components:
            sum += component**2
        return sum ** 0.5

    def unit(self):
        return Vector(((1/self.mag())*self).components)

    @staticmethod
    def mag_of_a_vector(components):
        sum = 0
        for component in components:
            sum += component ** 2
        return sum ** 0.5

    @staticmethod
    def unit_vector(components):
        magnitude = 0
        for component in components:
            magnitude += component ** 2
        magnitude = magnitude**0.5
        return [components[0]/magnitude, components[1]/magnitude]

    @staticmethod
    def distance(v1, v2):
        return (Vector(v1) - Vector(v2)).mag()

    @staticmethod
    def rotate(vector, angle):
        x = vector[0] * math.cos(angle) - vector[1] * math.sin(angle)
        y = vector[0] * math.sin(angle) + vector[1] * math.cos(angle)
        return [x, y]


class Map:
    def __init__(self, size):
        self.size = size
        self.color = [230, 230, 230]
        #self.color = fuchsia
        self.line_spacing = 30

    def draw(self, screen, player):
        map_pos = [SCREEN_WIDTH/2 - player.pos[0], SCREEN_HEIGHT/2 - player.pos[1], self.size[0], self.size[1]]
        pygame.draw.rect(screen, self.color, map_pos)
        for i in range(int(SCREEN_WIDTH/self.line_spacing) + 1):
            start_pos = [i * self.line_spacing + (SCREEN_WIDTH/2 - player.pos[0])%self.line_spacing, map_pos[1]]
            if map_pos[0] < start_pos[0] < map_pos[0] + self.size[0]:
                pygame.draw.line(screen, [200, 200, 200], start_pos, [start_pos[0], map_pos[1] + self.size[1]], width=2)
        for i in range(int(SCREEN_HEIGHT/self.line_spacing) + 1):
            start_pos = [map_pos[0], i * self.line_spacing + (SCREEN_HEIGHT/2 - player.pos[1])%self.line_spacing]
            if map_pos[1] < start_pos[1] < map_pos[1] + self.size[1]:
                pygame.draw.line(screen, [200, 200, 200], start_pos, [map_pos[0] + self.size[0], start_pos[1]], width=2)


class HealthBar:
    def __init__(self, player, health, offsets):
        self.player = player
        self.max_health = health
        self.health = health
        self.prev_health = health
        self.offsets = offsets
        self.width = 40
        self.height = 5
        self.bg_color = [255, 255, 255]
        self.health_color = [100, 235, 50]
        self.prev_health_color = [229, 70, 50]

    def draw(self, screen):
        if self.health < self.max_health:
            pygame.draw.rect(screen, self.bg_color, [self.player.pos_on_screen[0] - self.width/2 + self.offsets[0], self.player.pos_on_screen[1] + self.offsets[1], self.width, self.height])
            pygame.draw.rect(screen, self.prev_health_color,
                             [self.player.pos_on_screen[0] - self.width / 2 + self.offsets[0],
                              self.player.pos_on_screen[1] + self.offsets[1],
                              self.width * self.prev_health / self.max_health,
                              self.height])
            pygame.draw.rect(screen, self.health_color,
                             [self.player.pos_on_screen[0] - self.width / 2 + self.offsets[0], self.player.pos_on_screen[1] + self.offsets[1], self.width*self.health/self.max_health,
                              self.height])

    def update(self):
        if self.health > self.max_health:
            self.health = self.max_health
        elif self.health < 0:
            self.health = 0
            self.player.health_zero()
        if self.prev_health > self.health:
            self.prev_health -= (self.prev_health - self.height)*dt
        else:
            self.prev_health = self.health


class Player:
    def __init__(self, pos=(random.randint(0, 1000), random.randint(0, 1000)), acceleration=5000, type = "player", attack_cooldown = 0.3, color = (212, 194, 150), damaged_color = (247, 156, 130)):
        self.pos = list(pos)
        self.pos_on_screen = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
        self.direction_moving = [0, 0]
        self.direction_moving_unit = [0, 0]
        self.normal_color = color
        self.damaged_color = damaged_color
        self.color = self.normal_color
        self.border_color = [0, 0, 0]
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.drag_coeff = 10
        self.acceleration_magnitude = acceleration
        self.mask_no = 0
        self.invisible = False
        self.health_bar = HealthBar(self, 100, [0, 30])
        self.type = type
        self.attacked_last = 0
        self.damaged_last = 0
        self.attack_cooldown = attack_cooldown
        self.damage_cooldown = 0.5
        self.attacking = False
        self.ai_attack_anim = self.AiAttackAnim(self)
        self.taking_damage = False
        self.dead = False
        self.knockback = 1000
        self.prev_enemy_pos = [0, 0]

        self.stick_color = [77, 63, 51]
        self.weapon_color = [171, 171, 171]
        self.weapon_border = [94, 94, 94]
        self.lines = [[[19, -17], [19, 30], self.stick_color], [[20, -18], [20, 31], [200, 170, 160]], [[21, -17], [21, 30], self.stick_color],
                      [[21, 28], [35, 32], self.weapon_border], [[35, 32], [37, 28], self.weapon_border], [[37, 28], [37, 22], self.weapon_border], [[37, 22], [35, 18], self.weapon_border], [[35, 18], [21, 22], self.weapon_border]]
        self.weapon_points = [[21, 28], [35, 32], [37, 28], [37, 22], [35, 18], [21, 22]]
        self.angle = 0
        self.angle_offset = 0
        self.angular_speed = 20

        self.radius = 20

    def draw_lines(self, screen):
        for line in self.lines:
            pygame.draw.line(screen, line[2],
                             (Vector(Vector.rotate(line[0], self.angle + self.angle_offset)) + Vector(self.pos_on_screen)).components,
                             (Vector(Vector.rotate(line[1], self.angle + self.angle_offset)) + Vector(self.pos_on_screen)).components,
                             width=2)

    def transform_coordinates(self, list_of_points):
        out_points = []
        for point in list_of_points:
            out_points.append((Vector(Vector.rotate(point, self.angle + self.angle_offset)) + Vector(self.pos_on_screen)).components)
        return out_points

    def draw(self, screen):
        if not self.invisible:
            pygame.draw.polygon(screen, self.weapon_color, self.transform_coordinates(self.weapon_points))
            self.draw_lines(screen)

            pygame.draw.circle(screen, self.border_color, [SCREEN_WIDTH/2, SCREEN_HEIGHT/2], self.radius + 3)
            pygame.draw.circle(screen, self.color, [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2], self.radius)
            self.health_bar.draw(screen)

    def draw_other_player(self, screen, player):
        pygame.draw.polygon(screen, self.weapon_color, self.transform_coordinates(self.weapon_points))
        self.draw_lines(screen)
        pygame.draw.circle(screen, self.border_color, [SCREEN_WIDTH / 2 - player.pos[0] + self.pos[0],
                                                SCREEN_HEIGHT / 2 - player.pos[1] + self.pos[1]], 23)
        pygame.draw.circle(screen, self.color, [SCREEN_WIDTH / 2 - player.pos[0] + self.pos[0], SCREEN_HEIGHT / 2 - player.pos[1] + self.pos[1]], 20)
        self.health_bar.draw(screen)

    def update(self, map, keys):
        #keys = pygame.key.get_pressed()
        self.direction_moving = [0, 0]
        if keys[1]:
            self.direction_moving[0] -= 1
        if keys[3]:
            self.direction_moving[0] += 1
        if keys[0]:
            self.direction_moving[1] -= 1
        if keys[2]:
            self.direction_moving[1] += 1
        if self.direction_moving[0] != 0 or self.direction_moving[1] != 0:
            self.direction_moving_unit = Vector.unit_vector(self.direction_moving)
        else:
            self.direction_moving_unit = [0, 0]
        #print(self.direction_moving_unit)
        self.acceleration[0] = self.acceleration_magnitude * self.direction_moving_unit[0]
        self.acceleration[1] = self.acceleration_magnitude * self.direction_moving_unit[1]

        self.acceleration[0] -= self.velocity[0] * self.drag_coeff
        self.acceleration[1] -= self.velocity[1] * self.drag_coeff

        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt

        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt

        if self.pos[0] < 0:
            self.pos[0] = 0
            self.velocity[0] = 0
        elif self.pos[0] > map.size[0]:
            self.pos[0] = map.size[0]
            self.velocity[0] = 0

        if self.pos[1] < 0:
            self.pos[1] = 0
            self.velocity[1] = 0
        elif self.pos[1] > map.size[1]:
            self.pos[1] = map.size[1]
            self.velocity[1] = 0

        if self.mask_no > 24:
            self.mask_no = 24
        elif self.mask_no < 0:
            self.mask_no = 0

        self.health_bar.health += 5 * dt
        self.health_bar.update()

        if time.time_ns()/1000000000 - self.damaged_last > self.damage_cooldown:
            self.taking_damage = False

        if self.taking_damage:
            self.color = self.damaged_color
        else:
            self.color = self.normal_color

        if self.type == "player":
            rotation_vector = [pygame.mouse.get_pos()[0] - self.pos_on_screen[0], pygame.mouse.get_pos()[1] - self.pos_on_screen[1]]
            if rotation_vector[0] != 0 and rotation_vector[1] != 0:
                self.angle = math.acos(Vector(rotation_vector)*Vector(1, 0)/Vector.mag_of_a_vector(rotation_vector))
            if rotation_vector[1] < 0:
                self.angle = -self.angle
            #print(self.angle)

        if self.attacking:
            self.angle_offset -= self.angular_speed * dt
            if self.angle_offset < -2:
                self.angle_offset = -2
                self.angular_speed = -self.angular_speed
            elif self.angle_offset > 0:
                self.angle_offset = 0
                self.angular_speed = -self.angular_speed

        self.ai_attack_anim.update()

    def ai_update(self, player):
        if Vector.distance(player.pos, self.pos) < 100 + 400*(player.mask_no + 1)/26 or (player.invisible == False and Vector.distance(player.pos, self.pos) < 600):
            self.direction_moving_unit = (Vector(player.pos) - Vector(self.pos)).unit().components
            self.acceleration[0] = self.acceleration_magnitude * self.direction_moving_unit[0]
            self.acceleration[1] = self.acceleration_magnitude * self.direction_moving_unit[1]
            self.prev_enemy_pos = list(player.pos)
        elif 100 < Vector.distance(self.prev_enemy_pos, self.pos) < 500:
            self.direction_moving_unit = (Vector(self.prev_enemy_pos) - Vector(self.pos)).unit().components
            self.acceleration[0] = self.acceleration_magnitude * self.direction_moving_unit[0]
            self.acceleration[1] = self.acceleration_magnitude * self.direction_moving_unit[1]

        self.acceleration[0] -= self.velocity[0] * self.drag_coeff
        self.acceleration[1] -= self.velocity[1] * self.drag_coeff

        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt

        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt

        self.pos_on_screen = [SCREEN_WIDTH / 2 - player.pos[0] + self.pos[0], SCREEN_HEIGHT / 2 - player.pos[1] + self.pos[1]]

        if self.type == "ai":
            rotation_vector = [player.pos_on_screen[0] - self.pos_on_screen[0], player.pos_on_screen[1] - self.pos_on_screen[1]]
            if rotation_vector[0] != 0 and rotation_vector[1] != 0:
                self.angle = math.acos(Vector(rotation_vector)*Vector(1, 0)/Vector.mag_of_a_vector(rotation_vector))
            if rotation_vector[1] < 0:
                self.angle = -self.angle

    def ai_collision_update(self, player):
        if player.type == "player":
            if not player.taking_damage:
                if time.time_ns()/1000000000 - self.attacked_last > self.attack_cooldown:
                    player.health_bar.health -= 20
                    self.ai_attack_anim.play()
                    self.attacked_last = time.time_ns()/1000000000
                    player.damaged_last = time.time_ns()/1000000000
                    player.taking_damage = True

                    rel_pos = (Vector(player.pos_on_screen) - Vector(self.pos_on_screen)).unit()
                    player.velocity[0] += rel_pos.components[0] * self.knockback
                    player.velocity[1] += rel_pos.components[1] * self.knockback

    def collision_update(self, player):
        if player.type == "ai":
            if self.attacking:
                if not player.taking_damage:
                    rel_pos = (Vector(player.pos_on_screen) - Vector(self.pos_on_screen)).unit()
                    if ((Vector(pygame.mouse.get_pos()) - Vector(self.pos_on_screen)).unit()) * rel_pos > 0.5:
                        if time.time_ns()/1000000000 - self.attacked_last > self.attack_cooldown:
                            self.attacked_last = time.time_ns()/1000000000
                            player.health_bar.health -= 40
                            player.taking_damage = True
                            player.damaged_last = time.time_ns()/1000000000
                            player.velocity[0] += rel_pos.components[0] * self.knockback
                            player.velocity[1] += rel_pos.components[1] * self.knockback
                        self.attacking = False

    def health_zero(self):
        if self.type == "player":
            pygame.quit()
            exit()
        elif self.type == "ai":
            self.dead = True


    class AiAttackAnim:
        def __init__(self, entity):
            self.entity = entity
            self.playing = False
            self.reversing = False

        def update(self):
            if self.playing:
                if not self.reversing:
                    self.entity.angle_offset -= self.entity.angular_speed * dt
                    if self.entity.angle_offset < -1:
                        self.entity.angle_offset = -1
                        self.reversing = True
                else:
                    self.entity.angle_offset += self.entity.angular_speed * dt
                    if self.entity.angle_offset > 0:
                        self.entity.angle_offset = 0
                        self.reversing = False
                        self.playing = False

        def play(self):
            self.playing = True


class Barrier:
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = [150, 150, 150]
        self.type = "rect"

    def draw(self, screen, player):
        pygame.draw.rect(screen, self.color, [self.start_pos[0] + player.pos_on_screen[0] - player.pos[0], self.start_pos[1] + player.pos_on_screen[1] - player.pos[1], self.end_pos[0] - self.start_pos[0], self.end_pos[1] - self.start_pos[1]])


def do_entity_collisions(players):
    for player1 in players:
        for player2 in players:
            if player2 is not player1:
                dist = Vector.distance(player1.pos, player2.pos)
                if dist < 40:
                    net_repulsion = (Vector(player1.pos) - Vector(player2.pos)).unit().components
                    player2.velocity[0] -= net_repulsion[0]*2000*dt
                    player2.velocity[1] -= net_repulsion[1]*2000*dt
                if dist < 50:
                    player2.ai_collision_update(player1)
                if dist < 70:
                    player2.collision_update(player1)


def do_obstacle_collisions(obstacles, players):
    for obstacle in obstacles:
        if obstacle.type == "rect":
            for player in players:
                if obstacle.start_pos[0] - player.radius < player.pos[0] < obstacle.end_pos[0] + player.radius and obstacle.start_pos[1] - player.radius< player.pos[1] < obstacle.end_pos[1] + player.radius:
                    nearest = max(obstacle.start_pos[0] - player.pos[0] - player.radius, player.pos[0] - obstacle.end_pos[0] - player.radius, obstacle.start_pos[1] - player.pos[1] - player.radius, player.pos[1] - obstacle.end_pos[1] - player.radius)
                    if nearest == obstacle.start_pos[0] - player.pos[0] - player.radius:
                        player.pos[0] = obstacle.start_pos[0] - player.radius
                    elif nearest == player.pos[0] - obstacle.end_pos[0] - player.radius:
                        player.pos[0] = obstacle.end_pos[0] + player.radius
                    elif nearest == obstacle.start_pos[1] - player.pos[1] - player.radius:
                        player.pos[1] = obstacle.start_pos[1] - player.radius
                    elif nearest == player.pos[1] - obstacle.end_pos[1] - player.radius:
                        player.pos[1] = obstacle.end_pos[1] + player.radius


running = True

map = Map([3000, 3000])

players = []
player = Player()
players.append(player)
for i in range(4):
    players.append(Player(pos=[random.randint(0, 1000), random.randint(0, 1000)], acceleration=2000, type="ai", attack_cooldown=1, color=[75, 107, 73], damaged_color=[103, 107, 73]))
obstacles = []
obstacles.append(Barrier([400, 400], [500, 1000]))
obstacles.append(Barrier([500, 400], [1000, 500]))
obstacles.append(Barrier([500, 900], [1000, 1000]))
#obstacles.append(Barrier([]))

time_now = time.time_ns()
time_prev = time.time_ns()
while running:
    time_now = time.time_ns()
    dt = (time_now - time_prev)/1000000000
    time_prev = time_now

    keys = pygame.key.get_pressed()

    if random.random() < 0.1*dt:
        players.append(Player(pos=[random.randint(0, 1000), random.randint(0, 1000)], acceleration=2000, type="ai",
                              attack_cooldown=1, color=[75, 107, 73], damaged_color=[103, 107, 73]))

    screen.fill((200, 200, 200))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            player.mask_no += event.y*3

    map.draw(screen, player)

    for obstacle in obstacles:
        obstacle.draw(screen, player)

    player.draw(screen)
    player.update(map, [keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d]])

    do_entity_collisions(players)
    do_obstacle_collisions(obstacles, players)
    if pygame.mouse.get_pressed()[0] or keys[pygame.K_SPACE]:
        player.attacking = True
    else:
        player.attacking = False
        player.angle_offset = 0

    for i in range(1, len(players)):
        players[i].draw_other_player(screen, player)
        players[i].update(map, [0, 0, 0, 0])
        players[i].ai_update(player)
    for player1 in players:
        if player1.dead:
            #print("dead!")
            players.__delitem__(players.index(player1))

    if keys[pygame.K_LSHIFT]:
        #pygame.draw.circle(invisibility_screen, [0, 0, 0], [SCREEN_WIDTH/2, SCREEN_HEIGHT/2], 100, 1)
        screen.blit(masks[player.mask_no], [SCREEN_WIDTH/2 - masks[player.mask_no].get_width()/2, SCREEN_HEIGHT/2 - masks[player.mask_no].get_height()/2])
        player.invisible = True
    else:
        player.invisible = False

    pygame.display.update()
