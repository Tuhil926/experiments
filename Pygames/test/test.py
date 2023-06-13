import pygame

pygame.init()

screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))

currentScreen = "pos"


def goToSettings():
    global currentScreen
    currentScreen = "settings"


def goToMenu():
    global currentScreen
    currentScreen = 'pos'

def goToGame():
    global currentScreen
    currentScreen = 'game'

class button():
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
            font = pygame.font.SysFont('comicsans', self.fontSize)
            text = font.render(self.text, 1, self.textColor)
            win.blit(text, (
            int(self.x + (self.width / 2 - text.get_width() / 2)), int(self.y + (self.height / 2 - text.get_height() / 2))))

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




font = pygame.font.Font('freesansbold.ttf', 30)
text = font.render("Hurray it works", 1, (0, 0, 0))

x = 0



running = True
button1 = button(40, (125, 255, 100), (70, 200, 60), (80, 210, 70), (100, 220, 90), 100, 100, 50, 60, "goToGame()", text="PLAY")
while running:
    screen.fill((x, 255-x, int((x + 128)%256)))
    screen.blit(text, (50, 50))
#    button1.draw(screen)
    pygame.draw.rect(screen, (255, 255, 255), (200, 300, 570, 200), 2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    x += 1
    if x > 254:
        x = 0
    pygame.display.update()