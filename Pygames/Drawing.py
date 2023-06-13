import pygame
pygame.init()
screen_width = 1100
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))


# variables
mouse_pos = (0, 0)
prev_mouse_pos = pygame.mouse.get_pos()
drawing = False
brush_color = [255, 255, 255]
bg_color = [0, 0, 0]
brush_size = 1

# colors
violet = [120, 50, 255]
indigo = [60, 50, 255]
blue = [60, 150, 255]
green = [90, 255, 60]
yellow = [255, 255, 70]
orange = [255, 140, 60]
red = [255, 60, 60]
white = [255, 255, 255]
custom = [255, 255, 255]


def change_color(color):
    global brush_color
    brush_color = color


def clear(screen):
    screen.fill(bg_color)


def distance(pos1, pos2):
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5


class Button:
    def __init__(self,fontSize, textColor, color, colorWhenMouseOver, colorWhenClicked, x, y, width, height, onClick,text=''):
        self.color = color
        self.fontSize = fontSize
        self.textColor = textColor
        self.defaultColor = color
        self.colorWhenMouseOver = colorWhenMouseOver
        self.colorWhenClicked = colorWhenClicked
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onCLick = onClick
        self.text = text
        self.clicked = False

    def draw(self, win, outline=None):
        # Call this method to draw the Button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (int(self.x), int(self.y), int(self.width), int(self.height)), 0)

        if self.text != '':
            font = pygame.font.Font('freesansbold.ttf', self.fontSize)
            text = font.render(self.text, 1, self.textColor)
            win.blit(text, (
            int(self.x + (self.width / 2 - text.get_width() / 2)), int(self.y + (self.height / 2 - text.get_height() / 2))))

        if self.onCLick != "pass":
            if self.isOver(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    if not self.clicked:
                        self.clicked = True
                        self.color = self.colorWhenClicked
                        eval(self.onCLick)
                else:
                    self.clicked = False
                    self.color = self.colorWhenMouseOver
            else:
                self.clicked = False
                self.color = self.defaultColor

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class ColorButton:
    def __init__(self, color, x, y, onClick):
        self.color = color
        self.x = x
        self.y = y
        self.onClick = onClick
        self.button = Button(10, [0, 0, 0], self.color, self.color, self.color, self.x, self.y, 30, 20, self.onClick)


class ColorSelector:
    def __init__(self, screen):
        self.visible = False
        self.screen = screen
        self.width = 300
        self.height = 200
        self.bg_color = [50, 50, 50]
        self.pos = [800, 0]
        self.slider_red = Slider(self.screen, [255, 100, 100], self.pos[0] + 30, self.pos[1] + 50, 240, 255)
        self.slider_green = Slider(self.screen, [100, 255, 100], self.pos[0] + 30, self.pos[1] + 100, 240, 255)
        self.slider_blue = Slider(self.screen, [100, 100, 255], self.pos[0] + 30, self.pos[1] + 150, 240, 255)

    def draw(self):
        if self.visible:
            pygame.draw.rect(screen, self.bg_color, [self.pos[0], self.pos[1], self.width, self.height])
            self.slider_red.draw()
            self.slider_green.draw()
            self.slider_blue.draw()

    def update(self):
        global custom
        self.slider_red.update()
        self.slider_green.update()
        self.slider_blue.update()
        custom[0] = self.slider_red.value
        custom[1] = self.slider_green.value
        custom[2] = self.slider_blue.value


class Slider:
    def __init__(self, screen, color, x, y, width, max_val, value=0):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.max_val = max_val
        self.value = value
        self.dragging = False

    def draw(self):
        pygame.draw.line(self.screen, self.color, [self.x, self.y], [self.x + self.width, self.y], 3)
        pygame.draw.circle(self.screen, self.color, [int(self.x) + int((self.value/self.max_val)*self.width), int(self.y)], 7)

    def update(self):
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.x <= pos[0] <= (self.x + self.width) and self.y - 10 <= pos[1] <= self.y + 10:
                self.dragging = True
        if self.dragging:
            if pygame.mouse.get_pressed()[0]:
                self.value = ((pos[0] - self.x)/self.width)*self.max_val
            else:
                self.dragging = False
        if self.value > self.max_val:
            self.value = self.max_val
        elif self.value < 0:
            self.value = 0


running = True
color_buttons = [ColorButton(violet, 40, 550, "change_color(violet)"),
                 ColorButton(indigo, 90, 550, "change_color(indigo)"),
                 ColorButton(blue, 140, 550, "change_color(blue)"),
                 ColorButton(green, 190, 550, "change_color(green)"),
                 ColorButton(yellow, 240, 550, "change_color(yellow)"),
                 ColorButton(orange, 290, 550, "change_color(orange)"),
                 ColorButton(red, 340, 550, "change_color(red)"),
                 ColorButton(white, 390, 550, "change_color(white)"),
                 ColorButton(custom, 440, 550, "change_color(custom)")]
clear_button = Button(9, [255, 255, 255], [60, 60, 60], [120, 120, 120], [200, 200, 200], 750, 550, 30, 20, "clear(screen)", text="clear")
color_selector = ColorSelector(screen)
brush_size_selector = Slider(screen, [255, 255, 255], 830, 220, 300, 255, value=26)
color_selector.visible = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    brush_size = int(brush_size_selector.value/10)
    pygame.draw.rect(screen, [20, 20, 20], [800, 0, 300, 300])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.mouse.get_pressed()[0]:
        drawing = True

    if drawing:
        pygame.draw.line(screen, brush_color, prev_mouse_pos, mouse_pos, brush_size)
        if brush_size > 7:
            pygame.draw.circle(screen, brush_color, mouse_pos, int(brush_size/2))
    for button in color_buttons:
        button.button.draw(screen)
    clear_button.draw(screen)
    color_selector.draw()
    brush_size_selector.draw()

    color_selector.update()
    brush_size_selector.update()
    pygame.draw.line(screen, (255, 255, 255), [800, 0], [800, screen_height], 3)

    pygame.display.update()
    drawing = False
    prev_mouse_pos = mouse_pos
