import pygame
import time
import random
import math

pygame.init()

dt = 0

screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Bouncy Ball")
pygame.display.set_icon(pygame.image.load("data/BouncyBallIcon.png"))

plankAcceleratoin_actual = 4000
plankDrag_actual = 4
ballSpeed_actual = 500
plankAcceleratoin = plankAcceleratoin_actual
plankDrag = plankDrag_actual
ballSpeed = ballSpeed_actual

file = open("data/scores.csv", "r")
scores = file.read().split()
file.close()

player1Score = int(scores[0])
player2Score = int(scores[1])
highScoreInSinglePlayer = int(scores[2])
timeStarted = 0

currentScreen = "pos"
gameMode = 'single'

clearButtonText = "clear"


def clearScores():
    global player1Score
    global player2Score
    global highScoreInSinglePlayer
    global clearButtonText
    global menu
    if clearButtonText == "clear":
        file = open("data/scores.csv", "w")
        file.write(str(player1Score) + "\n")
        file.write(str(player2Score) + "\n")
        file.write(str(highScoreInSinglePlayer))
        file.close()
        player1Score = 0
        player2Score = 0
        highScoreInSinglePlayer = 0
        clearButtonText = "undo"
    elif clearButtonText == "undo":
        file = open("data/scores.csv", "r")
        scores = file.read().split()
        file.close()

        player1Score = int(scores[0])
        player2Score = int(scores[1])
        highScoreInSinglePlayer = int(scores[2])
        clearButtonText = "clear"
    menu.scoreBoard.update()


def goToSettings():
    global currentScreen
    currentScreen = "settings"


def goToHowToPlay():
    global currentScreen
    currentScreen = 'howToPlay'


def goToMenu():
    global currentScreen
    global gameMode
    global menu
    global highScoreInSinglePlayer
    global timeStarted
    global clearButtonText
    if currentScreen == 'game':
        if gameMode == 'single':
            ScoreInSinglePlayer = int((time.time_ns() - timeStarted) / 1000000000)
            if ScoreInSinglePlayer > highScoreInSinglePlayer:
                highScoreInSinglePlayer = ScoreInSinglePlayer
    clearButtonText = "clear"
    menu.scoreBoard.update()
    currentScreen = 'pos'


def goToGame():
    global currentScreen
    global game
    global singlePlayerGame
    global ballSpeed
    global plankAcceleratoin
    global plankDrag
    global timeStarted
    currentScreen = 'game'
    ballSpeed = ballSpeed_actual
    plankAcceleratoin = plankAcceleratoin_actual
    plankDrag = plankDrag_actual
    if gameMode == 'single':
        timeStarted = time.time_ns()
        singlePlayerGame = GameSinglePlayer(screen)
    if gameMode == 'multi':
        game = Game(screen)


class button:
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
            font = pygame.font.Font('data/freesansbold.ttf', self.fontSize)
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


class Selection:
    def __init__(self,screen, fontSize, textColor, color, colorWhenMouseOver, colorWhenClicked, x, y, width, height, selections, selected):
        self.color = color
        self.screen = screen
        self.fontSize = fontSize
        self.textColor = textColor
        self.defaultColor = color
        self.colorWhenMouseOver = colorWhenMouseOver
        self.colorWhenClicked = colorWhenClicked
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selections = selections
        self.selected = selected
        self.button = button(self.fontSize, self.textColor, self.color, self.colorWhenMouseOver, self.colorWhenClicked, self.x, self.y, self.width, self.height, "pass", text=self.selections[self.selected])
        self.right = button(self.fontSize, self.textColor, self.color, self.colorWhenMouseOver, self.colorWhenClicked, self.x + self.width, self.y, self.height, self.height, "pass", text=">")
        self.left = button(self.fontSize, self.textColor, self.color, self.colorWhenMouseOver, self.colorWhenClicked,
                            self.x -self.height, self.y, self.height, self.height, "pass", text="<")

    def draw(self):
        self.button.draw(self.screen)
        self.right.draw(self.screen)
        self.left.draw(self.screen)

    def update(self):
        if self.right.isOver(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                if not self.right.clicked:
                    self.right.clicked = True
                    self.right.color = self.right.colorWhenClicked
                    self.next_selection()
            else:
                self.right.clicked = False
                self.right.color = self.right.colorWhenMouseOver
        else:
            self.right.clicked = False
            self.right.color = self.right.defaultColor

        if self.left.isOver(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                if not self.left.clicked:
                    self.left.clicked = True
                    self.left.color = self.left.colorWhenClicked
                    self.previous_selection()
            else:
                self.left.clicked = False
                self.left.color = self.left.colorWhenMouseOver
        else:
            self.left.clicked = False
            self.left.color = self.left.defaultColor

    def next_selection(self):
        self.selected += 1
        if self.selected > len(self.selections) - 1:
            self.selected = 0
        self.button.text = self.selections[self.selected]

    def previous_selection(self):
        self.selected -= 1
        if self.selected < 0:
            self.selected = len(self.selections) - 1
        self.button.text = self.selections[self.selected]


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.playButtonDimensions = [90, 50]
        self.settingsButtonDimensions = [100, 40]
        self.playButton = button(30, (125, 255, 100), (70, 200, 60), (90, 230, 80), (110, 255, 100), self.screen.get_width()/2 - self.playButtonDimensions[0]/2, 3*self.screen.get_height()/5, self.playButtonDimensions[0], self.playButtonDimensions[1], "goToGame()", text="PLAY")
        self.settingsButton = button(20, (50, 50, 50), (220, 220, 60), (250, 250, 100), (255, 255, 100),
                                 self.screen.get_width() / 10 - self.settingsButtonDimensions[0] / 2,
                                 self.screen.get_height() / 10 - self.settingsButtonDimensions[1] / 2, self.settingsButtonDimensions[0],
                                 self.settingsButtonDimensions[1], "goToSettings()", text="Settings")
        font = pygame.font.Font('data/freesansbold.ttf', 120)
        self.heading = font.render("Bouncy Ball", 1, (255, 60, 40))
        self.howToPlayButtonDimensions = [120, 40]
        self.howToPlayButton = button(15, (50, 50, 50), (220, 220, 60), (250, 250, 100), (255, 255, 100), self.screen.get_width()/10 - self.howToPlayButtonDimensions[0]/2, self.screen.get_height()/5, self.howToPlayButtonDimensions[0], self.howToPlayButtonDimensions[1], "goToHowToPlay()", text="How To Play")
        self.scoreBoardDimensions = [250, 130]
        self.scoreBoard = ScoreBoard(self.screen, (255, 255, 60), (50, 50, 50), [540, 30], self.scoreBoardDimensions[0], self.scoreBoardDimensions[1])

    def render(self):
        self.playButton.draw(self.screen)
        self.settingsButton.draw(self.screen)
        self.howToPlayButton.draw(self.screen)
        self.scoreBoard.draw()
        self.screen.blit(self.heading, (
            int(self.screen.get_width()/2- self.heading.get_width() / 2), int(self.screen.get_height()/2- self.heading.get_height()/1.5)))
        if pygame.key.get_pressed()[13]:
            goToGame()


class Settings:
    def __init__(self, screen):
        self.screen = screen
        self.backButtonDimensions = [70, 50]
        self.backButton = button(25, (255, 255, 255), (230, 230, 50), (240, 240, 70), (255, 255, 100), 9*self.screen.get_width() / 10 - self.backButtonDimensions[0] / 2,
                                 self.screen.get_height() / 10 - self.backButtonDimensions[1] / 2, self.backButtonDimensions[0],
                                 self.backButtonDimensions[1], "goToMenu()", text="Back")
        self.gameModeSelector = Selection(self.screen, 20, (50, 50, 50), (230, 230, 50), (250, 250, 60), (255, 255, 110), self.screen.get_width()/2 - 70, self.screen.get_height()/3, 140, 50, ["Single Player", "Multiplayer"], 0)
        self.plankAccelerationSelector = Selection(self.screen, 20, (50, 50, 50), (230, 230, 50), (250, 250, 60), (255, 255, 110),
                                                   self.screen.get_width()/2 - 95, self.screen.get_height()/2, 190, 50,
                                                   ["Plank Speed: 1000", "Plank Speed: 1500", "Plank Speed: 2000",
                                                    "Plank Speed: 2500", "Plank Speed: 3000", "Plank Speed: 3500",
                                                    "Plank Speed: 4000", "Plank Speed: 4500", "Plank Speed: 5000",
                                                    "Plank Speed: 6000", "Plank Speed: 7000", "Plank Speed: 8000",
                                                    "Plank Speed: 10000", "Plank Speed: 20000"], 6)

    def render(self):
        self.backButton.draw(self.screen)
        self.gameModeSelector.draw()
        self.plankAccelerationSelector.draw()

    def update(self):
        global gameMode
        self.gameModeSelector.update()
        self.plankAccelerationSelector.update()
        if self.gameModeSelector.selected == 0:
            gameMode = 'single'
        elif self.gameModeSelector.selected == 1:
            gameMode = 'multi'
        self.setPlankAcceleration()

    def setPlankAcceleration(self):
        global plankAcceleratoin_actual
        if self.plankAccelerationSelector.selected == 0:
            plankAcceleratoin_actual = 1000
        if self.plankAccelerationSelector.selected == 1:
            plankAcceleratoin_actual = 1500
        if self.plankAccelerationSelector.selected == 2:
            plankAcceleratoin_actual = 2000
        if self.plankAccelerationSelector.selected == 3:
            plankAcceleratoin_actual = 2500
        if self.plankAccelerationSelector.selected == 4:
            plankAcceleratoin_actual = 3000
        if self.plankAccelerationSelector.selected == 5:
            plankAcceleratoin_actual = 3500
        if self.plankAccelerationSelector.selected == 6:
            plankAcceleratoin_actual = 4000
        if self.plankAccelerationSelector.selected == 7:
            plankAcceleratoin_actual = 4500
        if self.plankAccelerationSelector.selected == 8:
            plankAcceleratoin_actual = 5000
        if self.plankAccelerationSelector.selected == 9:
            plankAcceleratoin_actual = 6000
        if self.plankAccelerationSelector.selected == 10:
            plankAcceleratoin_actual = 7000
        if self.plankAccelerationSelector.selected == 11:
            plankAcceleratoin_actual = 8000
        if self.plankAccelerationSelector.selected == 12:
            plankAcceleratoin_actual = 10000
        if self.plankAccelerationSelector.selected == 13:
            plankAcceleratoin_actual = 20000


class HowToPlay:
    def __init__(self, screen):
        self.screen = screen
        font = pygame.font.Font("data/freesansbold.ttf", 20)
        font2 = pygame.font.Font("data/freesansbold.ttf", 40)
        self.backButtonDimensions = [70, 50]
        self.backButton = button(25, (255, 255, 255), (230, 230, 50), (240, 240, 70), (255, 255, 100),
                                 9 * self.screen.get_width() / 10 - self.backButtonDimensions[0] / 2,
                                 self.screen.get_height() / 10 - self.backButtonDimensions[1] / 2,
                                 self.backButtonDimensions[0],
                                 self.backButtonDimensions[1], "goToMenu()", text="Back")
        self.text = font.render("In this game, you can win by making the ball cross your", 1, (255, 255, 255))
        self.text1 = font.render("opponent's side. In single player mode you should stop the", 1, (255, 255, 255))
        self.text2 = font.render("ball from crossing your side for as long as possible.", 1, (255, 255, 255))
        self.text3 = font2.render("Controls:", 1, (255, 255, 255))
        self.text4 = font.render("For player 1(Left), Press W and S to move up and down.", 1, (255, 255, 255))
        self.text5 = font.render("For player 2(Right), Press Up Arrow and Down Arrow to move up and down.", 1, (255, 255, 255))
        self.text6 = font.render("For single player mode, you can use Up and Down arrows to move.", 1, (255, 255, 255))

    def draw(self):
        self.backButton.draw(self.screen)
        self.screen.blit(self.text, (50, 50))
        self.screen.blit(self.text1, (50, 90))
        self.screen.blit(self.text2, (50, 130))
        self.screen.blit(self.text3, (250, 190))
        self.screen.blit(self.text4, (50, 260))
        self.screen.blit(self.text5, (50, 300))
        self.screen.blit(self.text6, (50, 340))


class ScoreBoard:
    def __init__(self, screen, bkColor, textColor, position, width, height):
        self.height = height
        self.width = width
        self.position = position
        self.textColor = textColor
        self.screen = screen
        self.bkColor = bkColor
        self.font = pygame.font.Font('data/freesansbold.ttf', 20)
        self.scoreBoardText = self.font.render("Score Board", 1, self.textColor)
        self.player1 = self.font.render("Player 1:", 1, self.textColor)
        self.player2 = self.font.render("Player 2:", 1, self.textColor)
        self.score1 = self.font.render(str(player1Score), 1, self.textColor)
        self.score2 = self.font.render(str(player2Score), 1, self.textColor)
        self.singlePlayer = self.font.render("SinglePlayer :", 1, self.textColor)
        self.singlePlayerScore = self.font.render(str(highScoreInSinglePlayer) + " s", 1, self.textColor)
        self.clearButton = button(10, (255, 100, 90), (230, 230, 50), (250, 250, 70), (255, 255, 110), self.position[0] + self.width - 50, self.position[1] + 5, 40, 20, "clearScores()", text=clearButtonText)

    def draw(self):
        pygame.draw.rect(self.screen, self.bkColor, [self.position[0], self.position[1], self.width, self.height])
        self.screen.blit(self.scoreBoardText, (self.position[0] + self.width/2 - self.scoreBoardText.get_width()/2, self.position[1] + 10))
        self.screen.blit(self.player1,
                         (self.position[0] + 10, self.position[1] + 20 + self.scoreBoardText.get_height()))
        self.screen.blit(self.score1,
                         (self.position[0] + self.width/2 + 10, self.position[1] + 20 + self.scoreBoardText.get_height()))
        self.screen.blit(self.score2,
                         (self.position[0] + self.width/2 + 10, self.position[1] + 30 + self.scoreBoardText.get_height() + self.player1.get_height()))
        self.screen.blit(self.player2,
                         (self.position[0] + 10, self.position[1] + 30 + self.scoreBoardText.get_height() + self.player1.get_height()))
        self.screen.blit(self.singlePlayer,
                         (self.position[0] + 10,
                          self.position[1] + 40 + self.scoreBoardText.get_height() + self.player1.get_height() + self.player2.get_height()))
        self.screen.blit(self.singlePlayerScore,
                         (self.position[0] + 10 + self.width/1.5,
                          self.position[
                              1] + 40 + self.scoreBoardText.get_height() + self.player1.get_height() + self.player2.get_height()))
        self.clearButton.draw(self.screen)

    def update(self):
        global clearButtonText
        global player1Score
        global player2Score
        global highScoreInSinglePlayer
        self.score1 = self.font.render(str(player1Score), 1, self.textColor)
        self.score2 = self.font.render(str(player2Score), 1, self.textColor)
        self.singlePlayerScore = self.font.render(str(highScoreInSinglePlayer) + " s", 1, self.textColor)
        self.clearButton.text = clearButtonText


class Ball:
    def __init__(self, screen,  color, radius):
        self.screen = screen
        self.color = color
        self.radius = radius
        self.velocity = [0, 0]
        self.position = [self.screen.get_width()/2, self.screen.get_height()/2]

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius, self.radius)

    def update(self):
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        if self.position[1] < self.radius:
            self.velocity[1] = -self.velocity[1]
            self.position[1] += -self.position[1] + self.radius
        if self.position[1] > self.screen.get_height() - self.radius:
            self.velocity[1] = -self.velocity[1]
            self.position[1] += self.screen.get_height() - self.position[1] - self.radius


class Plank:
    def __init__(self, screen, color, width, length, position, keys):
        self.screen = screen
        self.color = color
        self.width = width
        self.length = length
        self.velocity = [0, 0]
        self.position = position
        self.keys = keys

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (int(self.position[0]), int(self.position[1]), self.width, self.length), self.width)

        self.position[0] += self.velocity[0]*dt
        self.position[1] += self.velocity[1]*dt

    def update(self):
        if pygame.key.get_pressed()[self.keys[0]]:
            self.velocity[1] -= plankAcceleratoin*dt
        if pygame.key.get_pressed()[self.keys[1]]:
            self.velocity[1] += plankAcceleratoin*dt
        if self.position[1] < 0 and self.velocity[1] < 0:
            self.velocity[1] = -self.velocity[1]
        if self.position[1] > self.screen.get_height() - self.length and self.velocity[1] > 0:
            self.velocity[1] = -self.velocity[1]
        self.velocity[1] -= self.velocity[1]*plankDrag*dt

    def ifTouching(self, object, radius):
        if object.position[0] > self.position[0] and self.position[1]<object.position[1]< self.position[1] + self.length:
            if object.position[0] - self.position[0] - self.width - radius < 0:
                if object.velocity[0] < 0:
                    object.velocity[0] = -object.velocity[0]
                    object.velocity[1] += (self.velocity[1] - object.velocity[1])/2
        if object.position[0] < self.position[0] and self.position[1]<object.position[1]< self.position[1] + self.length:
            if -object.position[0] + self.position[0] - radius < 0:
                if object.velocity[0] > 0:
                    object.velocity[0] = -object.velocity[0]
                    object.velocity[1] += (self.velocity[1] - object.velocity[1])/2


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.ball = Ball(self.screen, (255, 255, 255), 12)
        self.plankLenth = 130
        self.plank1 = Plank(self.screen, [255, 55, 55], 5, self.plankLenth, [0, self.screen.get_height()/2 - self.plankLenth/2], [119, 115])
        self.plank2 = Plank(self.screen, [55, 255, 55], 5, self.plankLenth, [self.screen.get_width() - 5, self.screen.get_height()/2 - self.plankLenth/2], [273, 274])
        self.backButtonDimensions = [70, 50]
        self.backButton = button(25, (30, 30, 30), (230, 230, 50), (250, 250, 60), (255, 255, 90),
                                 9 * self.screen.get_width() / 10 - self.backButtonDimensions[0] / 2,
                                 self.screen.get_height() / 10 - self.backButtonDimensions[1] / 2,
                                 self.backButtonDimensions[0],
                                 self.backButtonDimensions[1], "goToMenu()", text="Back")
        self.ballSpeed = ballSpeed
        angle = random.random()*2*math.pi
        self.ball.velocity = [self.ballSpeed*math.cos(angle), 0]
        font = pygame.font.Font('data/freesansbold.ttf', 100)
        font2 = pygame.font.Font('data/freesansbold.ttf', 100)

        self.gameOver = font.render("Game Over", 1, (255, 50, 40))
        self.player2wins = font2.render("Player 2 Wins!", 1, (60, 255, 30))
        self.player1wins = font2.render("Player 1 Wins!", 1, (255, 10, 10))

    def render(self):
        self.backButton.draw(self.screen)
        self.ball.draw()
        self.plank1.draw()
        self.plank2.draw()

    def update(self):
        global ballSpeed
        global plankAcceleratoin
        global plankDrag
        global player1Score
        global player2Score
        ballSpeed += 2*dt
        plankAcceleratoin += 16*dt
        plankDrag += 0.016*dt
        self.ballSpeed = ballSpeed

        self.ball.update()
        self.plank1.update()
        self.plank2.update()
        self.plank1.ifTouching(self.ball, self.ball.radius)
        self.plank2.ifTouching(self.ball, self.ball.radius)
        if self.ball.velocity[0]**2 + self.ball.velocity[1]**2 != self.ballSpeed**2:
            r = self.ballSpeed/(self.ball.velocity[0]**2 + self.ball.velocity[1]**2)**(0.5)
            self.ball.velocity[0] = r * self.ball.velocity[0]
            self.ball.velocity[1] = r * self.ball.velocity[1]
        if pygame.key.get_pressed()[98]:
            goToMenu()
        if self.ball.position[0] < 0:
            time.sleep(0.3)
            self.screen.blit(self.player2wins, (int(self.screen.get_width()/2 - self.player2wins.get_width()/2), int(self.screen.get_height()/2.5)))
#            self.screen.blit(self.gameOver, (int(self.screen.get_width()/2 - self.gameOver.get_width()/2), int(self.screen.get_height()/2.5)))
            pygame.display.update()
            time.sleep(1)
            player2Score += 1
            goToMenu()
        if self.ball.position[0] > self.screen.get_width():
            time.sleep(0.3)
            self.screen.blit(self.player1wins, (
            int(self.screen.get_width() / 2 - self.player1wins.get_width() / 2), int(self.screen.get_height() / 2.5)))
#            self.screen.blit(self.gameOver, (int(self.screen.get_width()/2 - self.gameOver.get_width()/2), int(self.screen.get_height()/2.5)))
            pygame.display.update()
            time.sleep(1)
            player1Score += 1
            goToMenu()


class GameSinglePlayer:
    def __init__(self, screen):
        self.screen = screen
        self.ball = Ball(self.screen, (255, 255, 255), 12)
        self.plankLenth = 130
#        self.plank1 = Plank(self.screen, [255, 255, 255], 5, self.plankLenth, [0, self.screen.get_height()/2 - self.plankLenth/2], [119, 115])
        self.plank2 = Plank(self.screen, [255, 255, 255], 5, self.plankLenth, [self.screen.get_width() - 5, self.screen.get_height()/2 - self.plankLenth/2], [273, 274])
        self.backButtonDimensions = [70, 50]
        self.backButton = button(25, (30, 30, 30), (230, 230, 50), (250, 250, 60), (255, 255, 90),
                                 9 * self.screen.get_width() / 10 - self.backButtonDimensions[0] / 2,
                                 self.screen.get_height() / 10 - self.backButtonDimensions[1] / 2,
                                 self.backButtonDimensions[0],
                                 self.backButtonDimensions[1], "goToMenu()", text="Back")
        self.ballSpeed = ballSpeed
        angle = random.random()*2*math.pi
        self.ball.velocity = [self.ballSpeed*math.cos(angle), 0]
        font = pygame.font.Font('data/freesansbold.ttf', 120)
        self.gameOver = font.render("Game Over", 1, (255, 50, 40))

    def render(self):
        self.backButton.draw(self.screen)
        self.ball.draw()
#        self.plank1.draw()
        self.plank2.draw()

    def update(self):
        global ballSpeed
        global plankAcceleratoin
        global plankDrag
        global timeStarted
        global highScoreInSinglePlayer
        ballSpeed += 2*dt
        plankAcceleratoin += 16 * dt
        plankDrag += 0.016 * dt
        self.ballSpeed = ballSpeed
        self.ball.update()
#        self.plank1.update()
        self.plank2.update()
#        self.plank1.ifTouching(self.ball, self.ball.radius)
        self.plank2.ifTouching(self.ball, self.ball.radius)
        if self.ball.velocity[0]**2 + self.ball.velocity[1]**2 != self.ballSpeed**2:
            r = self.ballSpeed/(self.ball.velocity[0]**2 + self.ball.velocity[1]**2)**(0.5)
            self.ball.velocity[0] = r * self.ball.velocity[0]
            self.ball.velocity[1] = r * self.ball.velocity[1]
        if self.ball.position[0] < self.ball.radius:
            if self.ball.velocity[0] < 0:
                self.ball.velocity[0] = - self.ball.velocity[0]
        if pygame.key.get_pressed()[98]:
            goToMenu()
        if self.ball.position[0] > self.screen.get_width():
            ScoreInSinglePlayer = int((time.time_ns() - timeStarted) / 1000000000)
            if ScoreInSinglePlayer > highScoreInSinglePlayer:
                highScoreInSinglePlayer = ScoreInSinglePlayer
            time.sleep(0.3)
            self.screen.blit(self.gameOver, (int(self.screen.get_width()/2 - self.gameOver.get_width()/2), int(self.screen.get_height()/2.5)))
            pygame.display.update()
            time.sleep(0.6)
            goToMenu()


menu = Menu(screen)
settings = Settings(screen)
howToPlay = HowToPlay(screen)
game = Game(screen)
singlePlayerGame = GameSinglePlayer(screen)
running = True

#Tests:
counter = 0
counter2 = time.time_ns()
while running:
    timee = time.time_ns()
    counter += 1

    if currentScreen == 'pos':
        screen.fill((70, 70, 70))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                currentScreen = "none"
                running = False
        menu.render()

        pygame.display.update()

    if currentScreen == "settings":
        screen.fill((70, 70, 70))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                currentScreen = "pos"
        settings.render()
        settings.update()

        pygame.display.update()

    if currentScreen == "howToPlay":
        screen.fill((70, 70, 70))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                currentScreen = "pos"
        howToPlay.draw()

        pygame.display.update()

    if currentScreen == 'game':
        if gameMode == 'multi':
            screen.fill((30, 30, 30))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu.scoreBoard.update()
                    currentScreen = "pos"
            game.update()
            game.render()

        elif gameMode == 'single':
            screen.fill((30, 30, 30))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu.scoreBoard.update()
                    currentScreen = "pos"
            singlePlayerGame.update()
            singlePlayerGame.render()
    pygame.display.update()

    if counter > 1000:
        counter = 0
        print("Frame Rate: ", 1000*1000000000/(time.time_ns() - counter2))
        counter2 = time.time_ns()

    dt = (time.time_ns() - timee)/1000000000
    if dt > 1/16:
        dt = 1/16


file = open("data/scores.csv", "w")
file.write(str(player1Score) + "\n")
file.write(str(player2Score) + "\n")
file.write(str(highScoreInSinglePlayer))
file.close()
