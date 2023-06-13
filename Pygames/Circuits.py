import pygame
import numpy as np
import time

pygame.init()

screenWidth = 600
screenLength = 800

screen = pygame.display.set_mode((screenLength, screenWidth))

unit = 20

heliimg = pygame.image.load('heli.png')
mCi = pygame.image.load('MicroController2.png')
rimg = pygame.transform.rotate(pygame.image.load('Resistor.png'), 0)
resistorimg = pygame.transform.scale(rimg, (unit*3, unit))
mC = pygame.transform.scale(mCi, (unit*4, unit*4))
icon = pygame.transform.scale(mC, (32, 32))
pygame.display.set_icon(icon)
pygame.display.set_caption("Circuits")
background = pygame.image.load('LinesBg.png')

#font = pygame.font.Font("freesansbold.ttf", 32)


class button():
    def __init__(self, color, colorWhenMouseOver, colorWhenClicked, x, y, width, height, onClick,text=''):
        self.color = color
        self.defaultColor = color
        self.colorWhenMouseOver = colorWhenMouseOver
        self.colorWhenClicked = colorWhenClicked
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onCLick = onClick
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the Button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render(self.text, 1, (100, 255, 100))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        if self.isOver(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.color = self.colorWhenClicked
                eval(self.onCLick)
            else:
                self.color = self.colorWhenMouseOver
        else:
            self.color = self.defaultColor


    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class Component:
    def __init__(self, img, connections, position):
        self.img = img
        self.connections = connections
        self.position = position
        self.clicked = False
        self.offsets = (0, 0)
        self.rotation = 0
        self.rot_image = self.img

    def draw(self):
        screen.blit(self.rot_image, (self.position[0], self.position[1]))

    def follow_pointer(self):
        if self.clicked:
            self.position = (pygame.mouse.get_pos()[0] + self.offsets[0], pygame.mouse.get_pos()[1] + self.offsets[1])

    def check_mouse_on_me(self):
        return self.position[0] + self.rot_image.get_width() > pygame.mouse.get_pos()[0] > self.position[0] and self.position[1] + self.rot_image.get_height() > pygame.mouse.get_pos()[1] > self.position[1]

    def update(self):
        self.draw()
        self.follow_pointer()
        self.snap()

    def set_offsets(self):
        self.offsets = (self.position[0] - pygame.mouse.get_pos()[0], self.position[1] - pygame.mouse.get_pos()[1])

    def check_actions(self):
        global selected
        if self.check_mouse_on_me():
            self.set_offsets()
            self.clicked = True
            selected = self

    def snap(self):
        self.position = (unit * (self.position[0] // unit), unit * (self.position[1] // unit))

    def rotate(self, direction):
        prev_rot = self.rotation
        self.rotation += 90*direction
        self.rot_image = pygame.transform.rotate(self.img, self.rotation)
        for i in range(len(self.connections)):
            self.connections[i] = round(self.connections[i][0]*np.cos((self.rotation - prev_rot)*np.pi/180) + self.connections[i][1]*np.sin((self.rotation - prev_rot)*np.pi/180) + (-direction + 1)*self.rot_image.get_width()/2), round(-self.connections[i][0]*np.sin((self.rotation - prev_rot)*np.pi/180) + self.connections[i][1]*np.cos((self.rotation - prev_rot)*np.pi/180) - (-direction - 1)*self.rot_image.get_height()/2)


class Connection:
    def __init__(self, component1, connection1, component2, connection2):
        self.component1 = component1
        self.component2 = component2
        self.connection1 = connection1
        self.connection2 = connection2

    def draw(self):
        pygame.draw.aaline(screen, (230, 30, 10), (self.component1.position[0] + self.component1.connections[self.connection1][0],
                                             self.component1.position[1] + self.component1.connections[self.connection1][1]),
                                            (self.component2.position[0] + self.component2.connections[self.connection2][0],
                                             self.component2.position[1] + self.component2.connections[self.connection2][1]))
        pygame.draw.circle(screen, (230, 30, 10), (int(self.component1.position[0]) +
                                                   int(self.component1.connections[self.connection1][0]),
                                                   int(self.component1.position[1]) +
                                                   int(self.component1.connections[self.connection1][1])), 2, 1)
        pygame.draw.circle(screen, (230, 30, 10), (int(self.component2.position[0]) +
                                                   int(self.component2.connections[self.connection2][0]),
                                                   int(self.component2.position[1]) +
                                                   int(self.component2.connections[self.connection2][1])), 2, 1)


class GameManager:
    def __init__(self, screen):
        self.screen = screen


running = True
# m = [(4, 6), (4, 18), (4, 30), (4, 42), (45, 42), (45, 30), (45, 18), (45, 6)]
microConnections = [(8 *unit/16, 8 *unit/16), (8 *unit/16, 24 *unit/16), (8 *unit/16, 40 *unit/16), (8 *unit/16, 56 *unit/16),
       (56 *unit/16, 56 *unit/16), (56 *unit/16, 40 *unit/16), (56 *unit/16, 24 *unit/16), (56 *unit/16, 8 *unit/16),]

microConnections2 = list(microConnections)

selected = None

components = []
Micro = Component(mC, microConnections, (700, 400))
Micro2 = Component(mC, microConnections2, (300, 400))
qwerty = Component(heliimg, [(20*unit/16, 20*unit/16)], (300, 300))
components.append(Micro)
components.append(Micro2)
components.append(qwerty)
components.append(Component(resistorimg, [(8 * unit/16, 8 * unit/16), (40 * unit/16, 8 * unit/16)], (100, 100)))
connections = []
connections.append(Connection(Micro, 2, qwerty, 0))
connections.append(Connection(Micro, 7, qwerty, 0))
connections.append(Connection(Micro, 4, Micro2, 3))
connections.append(Connection(Micro, 5, Micro2, 2))
connections.append(Connection(Micro, 6, Micro2, 1))
connections.append(Connection(Micro2, 7, components[3], 1))
connections.append(Connection(Micro, 7, components[3], 0))

lineColor = (100, 100, 100)


def save():
    circuits_data = open("circuits_data.txt", "w")
    circuits_data.write("This is just a test\n" + str(Micro.position[0]))
    circuits_data.close()
    print("saved")


saveButton = button((50, 200, 40), (70, 210, 60), (100, 220, 90), screenLength - 100, 10, 90, 40,"save()", 'Save')

while running:
    screen.fill((70, 70, 70))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for component in components:
                component.check_actions()
        if event.type == pygame.MOUSEBUTTONUP:
            for component in components:
                component.clicked = False
        if event.type == pygame.KEYDOWN:
            if selected is not None:
                if event.key == pygame.K_LEFT:
                    selected.rotate(1)
                if event.key == pygame.K_RIGHT:
                    selected.rotate(-1)
    for i in range(int(screenLength/unit)):
        pygame.draw.line(screen, lineColor, (unit * i, 0), (unit * i, screenWidth))
        for j in range(int(screenWidth / unit)):
            pygame.draw.circle(screen, lineColor, (int(unit * i + (unit/2)), int(unit * j + (unit/2))), int(unit/5))
    for i in range(int(screenWidth/unit)):
        pygame.draw.line(screen, lineColor, (0, unit*i), (screenLength, unit * i))
#        Micro2.position = (16 * (Micro2.position[0]//16), 16 * (Micro2.position[1]//16))

    for component in components:
        component.update()
    for i in range(len(connections)):
        connections[i].draw()

    saveButton.draw(screen)

    pygame.display.update()

