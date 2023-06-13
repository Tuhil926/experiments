import pygame
import time
import math

pygame.init()

screen_width = 800
screen_height = 600

dt = 0


def component_of(vector1, vector2):
    magVector2 = (vector2[0]**2 + vector2[1]**2+ vector2[2]**2)**0.5
    mag = vector1[0]*vector2[0]/magVector2 + vector1[1]*vector2[1]/magVector2 + vector1[2]*vector2[2]/magVector2
    return mag


def dot(vector1, vector2):
    return vector1[0]*vector2[0] + vector1[1]*vector2[1] + vector1[2]*vector2[2]


def cross(vector1, vector2):
    return [vector1[1]*vector2[2] - vector1[2]*vector2[1], vector1[2]*vector2[0] - vector1[0]*vector2[2], vector1[0]*vector2[1] - vector1[1]*vector2[0]]


def magnitude(vector2):
    return (vector2[0]**2 + vector2[1]**2+ vector2[2]**2)**0.5


def mod(n):
    if n >= 0:
        return n
    else:
        return -n


def unit_vector(vector):
    mag = magnitude(vector)
    if mag == 0:
        mag = 0.0000001
    return vector[0]/mag, vector[1]/mag, vector[2]/mag


def subtract(vector1, vector2):
    return [vector1[0] - vector2[0], vector1[1] - vector2[1], vector1[2] - vector2[2]]


def add(vector1, vector2):
    return [vector1[0] + vector2[0], vector1[1] + vector2[1], vector1[2] + vector2[2]]


def divide(vector, number):
    return [vector[0]/number, vector[1]/number, vector[2]/number]


def multiply(vector, number):
    return [vector[0]*number, vector[1]*number, vector[2]*number]


def draw_line(screen, color, point1, point2):
    # if one of the points in behind the camera while trying to draw a line, it won't work properly, so this fixes that
    if point1.is_front and point2.is_front:
        pygame.draw.line(screen, color, point1.pos, point2.pos)
    elif point1.is_front and not point2.is_front:
        rel_pos = [point1.pos[0] - point2.pos[0], point1.pos[1] - point2.pos[1], 0]
        rel_pos = unit_vector(rel_pos)
        rel_pos = multiply(rel_pos, 100000)
        pos2 = [point1.pos[0] + rel_pos[0], point1.pos[1] + rel_pos[1]]
        pygame.draw.line(screen, color, point1.pos, pos2)
    elif not point1.is_front and point2.is_front:
        rel_pos = [point2.pos[0] - point1.pos[0], point2.pos[1] - point1.pos[1], 0]
        rel_pos = unit_vector(rel_pos)
        rel_pos = multiply(rel_pos, 100000)
        pos2 = [point2.pos[0] + rel_pos[0], point2.pos[1] + rel_pos[1]]
        pygame.draw.line(screen, color, point2.pos, pos2)
    else:
        pass


class Camera:
    def __init__(self, pos, angle):
        self.pos = pos
        self.speed = 1
        self.angle = angle
        self.z_angle = 0.5
        self.direction = unit_vector(
            [math.cos(self.angle) * math.cos(self.z_angle), math.sin(self.angle) * math.cos(self.z_angle),
             -math.sin(self.z_angle)])
        self.distance = 400
        self.up = [0, 0, 1]
        self.right = unit_vector(cross(self.direction, self.up))
        self.rel_up = unit_vector(cross(self.right, self.direction))
        self.cube_points = [[1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1], [1, -1, -1]]

    def project(self, point):
        unit_rel_pos = unit_vector([point[0] - self.pos[0], point[1] - self.pos[1], point[2] - self.pos[2]])  # gets the unit vector of the relative position of the point wrt camera
        cos = dot(unit_rel_pos, self.direction)  # cos of the angle between unit_rel_pos and the direction_moving the camera is pointing in
        if 0 < cos < 0.000001:  # if cos is too small, the distance of projection becomes too large
            cos = 0.000001
        if -0.000001 < cos < 0:
            cos = -0.000001
        screen_projection = divide(multiply(unit_rel_pos, self.distance), cos)
        screen_projection_with_centre_at_origin = subtract(screen_projection, self.direction)  # the coordinates of the point projected onto a plane passing through origin, with the camera's direction_moving as normal vector
        x = dot(screen_projection_with_centre_at_origin, self.right)
        y = -dot(screen_projection_with_centre_at_origin, self.rel_up)
        return D2_Point([x + screen_width/2, y + screen_height/2], cos > 0)

    def update(self):
        xy_comp = cross(self.up, self.right)
        keys = pygame.key.get_pressed()
        self.direction = unit_vector(
            [math.cos(self.angle) * math.cos(self.z_angle), math.sin(self.angle) * math.cos(self.z_angle),
             -math.sin(self.z_angle)])
        self.right = unit_vector(cross(self.direction, self.up))
        self.rel_up = unit_vector(cross(self.right, self.direction))
        if keys[pygame.K_d]:
            self.pos[0] += self.speed*dt * dot(self.right, [1, 0, 0])
            self.pos[1] += self.speed*dt * dot(self.right, [0, 1, 0])
        if keys[pygame.K_a]:
            self.pos[0] -= self.speed*dt * dot(self.right, [1, 0, 0])
            self.pos[1] -= self.speed*dt * dot(self.right, [0, 1, 0])
        if keys[pygame.K_w]:
            self.pos[0] += self.speed*dt*dot(xy_comp, [1, 0, 0])
            self.pos[1] += self.speed*dt*dot(xy_comp, [0, 1, 0])
        if keys[pygame.K_s]:
            self.pos[0] -= self.speed*dt * dot(xy_comp, [1, 0, 0])
            self.pos[1] -= self.speed*dt * dot(xy_comp, [0, 1, 0])
        if keys[pygame.K_SPACE]:
            self.pos[2] += self.speed*dt
        if keys[pygame.K_LSHIFT]:
            self.pos[2] -= self.speed*dt
        if keys[pygame.K_h]:
            self.angle -= dt
        if keys[pygame.K_f]:
            self.angle += dt
        if keys[pygame.K_t]:
            self.z_angle -= dt
        if keys[pygame.K_g]:
            self.z_angle += dt
        if keys[pygame.K_LCTRL]:
            self.speed = 1.7
            self.distance += 0.05*(300 - self.distance)
        else:
            self.speed = 1
            self.distance += 0.05*(400 - self.distance)

    def draw_cube(self, screen):
        projected_points = []
        for point in self.cube_points:
            p = self.project(point)
            projected_points.append(p)
        draw_line(screen, [100, 255, 50], projected_points[0], projected_points[1])
        draw_line(screen, [100, 255, 50], projected_points[1], projected_points[2])
        draw_line(screen, [100, 255, 50], projected_points[2], projected_points[3])
        draw_line(screen, [100, 255, 50], projected_points[3], projected_points[0])
        draw_line(screen, [100, 255, 50], projected_points[4], projected_points[5])
        draw_line(screen, [100, 255, 50], projected_points[5], projected_points[6])
        draw_line(screen, [100, 255, 50], projected_points[6], projected_points[7])
        draw_line(screen, [100, 255, 50], projected_points[7], projected_points[4])
        draw_line(screen, [100, 255, 50], projected_points[0], projected_points[4])
        draw_line(screen, [100, 255, 50], projected_points[1], projected_points[5])
        draw_line(screen, [100, 255, 50], projected_points[2], projected_points[6])
        draw_line(screen, [100, 255, 50], projected_points[3], projected_points[7])

    def draw_point(self, screen, color, point, radius):
        d = magnitude(subtract(point, self.pos))
        r = radius*self.distance/d
        screen_pos = self.project(point)
        if screen_pos.is_front:
            pygame.draw.circle(screen, color, [int(screen_pos.pos[0]), int(screen_pos.pos[1])], int(r))


class D2_Point:
    # Just a 2D point, but function names can't start with a number, so D2
    def __init__(self, pos, is_front):
        self.pos = pos
        self.is_front = is_front


def main():
    global dt
    screen = pygame.display.set_mode((screen_width, screen_height))  # create the screen
    running = True

    camera1 = Camera([2.1, 2, 1.2], 4)  # create the camera object

    # create the grid of points
    points = []
    for i in range(11):
        for j in range(11):
            points.append([(i - 5)/3, (j - 5)/3, 0])

    t1 = time.time_ns()
    t2 = t1
    while running:
        # This just calculates dt(time between frames) as well as the time since the start
        t_now = time.time_ns()
        dt = (t_now - t2)/1000000000
        t = (t_now - t1) / 1000000000

        if dt > 1/60:
            t2 = time.time_ns()
            # check if the window is closed by the user
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # makes the point move in a circle
            point = [math.cos(t), math.sin(t), 0]

            # make the screen black
            screen.fill((0, 0, 0))

            # draw the point that is moving in a circle
            camera1.draw_point(screen, [255, 255, 255], point, 0.06)

            # draw the grid of points
            for point1 in points:
                camera1.draw_point(screen, [150, 150, 150], point1, 0.02)

            # draw the cube
            camera1.draw_cube(screen)

            camera1.update()

            pygame.display.update()


main()
