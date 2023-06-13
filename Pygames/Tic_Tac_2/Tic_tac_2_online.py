import pygame
import threading
import time
import socket
import os
import pickle
import animations.animations as animations

row_count = 3
column_count = 3
req_to_win = 3

GRID_COLOR = [252, 186, 3]
PLAYER1_COLOR = [3, 157, 252]
PLAYER2_COLOR = [252, 49, 3]

game_state = "game_select"

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024*4

client_ip = None
host = None

score_file = open("data\\scores.txt", "r")
scores = score_file.read().split()
player1Score = int(scores[0])
player2Score = int(scores[1])
score_file.close()

clearButtonText = "Clear"


def send_file(filename, host, port):
    # get the file size
    filesize = os.path.getsize(filename)
    # create the client socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    #print("[+] Connected.")

    # send the filename and filesize
    #s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # start sending the file
    #progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transmission in
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            #progress.update(len(bytes_read))

    # close the socket
    s.close()
    #print("                                     message sent")


def receive_file(filename):
    global client_ip
    # device's IP address
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 5001
    # receive 4096 bytes each time
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    # create the server socket
    # TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to our local address
    s.bind((SERVER_HOST, SERVER_PORT))
    # enabling our server to accept connections
    # 5 here is the number of unaccepted connections that
    # the system will allow before refusing new connections
    s.listen(5)
    #print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    # accept connection if there is any
    client_socket, address = s.accept()
    # if below code is executed, that means the sender is connected
    #print(f"[+] {address} is connected.")

    # receive the file infos
    # receive using client socket, not server socket
    #received = client_socket.recv(BUFFER_SIZE)
    #print(received)
    #received = received.decode()
    #rec_filename, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    # convert to integer
    #filesize = int(filesize)
    # start receiving the file from the socket
    # and writing to the file stream
    # progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            # progress.update(len(bytes_read))

    # close the client socket
    client_socket.close()
    # close the server socket
    s.close()
    client_ip = address[0]


def go_to_game():
    global game_state
    game_state = "game"
    game.mouse_pressed = True


def go_to_menu():
    global game_state
    game_state = "menu"
    menu.button_anim.play(15)
    menu.scoreboard_anim.play(15)
    menu.playbutton_anim.play(15)
    menu.tic_tac_2_text_anim.play(15)


def go_to_settings():
    global game_state
    game_state = "settings"


def go_to_how_to_play():
    global game_state
    game_state = "how_to_play"
    how_to_play.back_button_anim.play(15)
    how_to_play.text1_anim.play(15)
    how_to_play.text2_anim.play(15)
    how_to_play.text3_anim.play(15)
    how_to_play.text4_anim.play(15)
    how_to_play.text5_anim.play(15)
    how_to_play.text6_anim.play(15)
    how_to_play.text7_anim.play(15)
    how_to_play.text8_anim.play(15)
    how_to_play.text9_anim.play(15)
    how_to_play.text10_anim.play(15)
    how_to_play.text11_anim.play(15)
    how_to_play.text12_anim.play(15)


def clearScores():
    global clearButtonText
    global player1Score, player2Score
    if clearButtonText == "Clear":
        clearButtonText = "Undo"
        score_file = open(r"data\scores.txt", "w")
        score_file.write(str(player1Score) + "\n" + str(player2Score))
        score_file.close()
        player1Score = 0
        player2Score = 0
    elif clearButtonText == "Undo":
        clearButtonText = "Clear"
        score_file = open(r"data\scores.txt", "r")
        scores = score_file.read().split()
        player1Score = int(scores[0])
        player2Score = int(scores[1])
        score_file.close()


screen_number = 0
def go_to_initial_menu():
    global screen_number
    screen_number = 0
    game_selector.offline_button_anim.play(15)
    game_selector.online_button_anim.play(15)


def set_game_mode_to_offline():
    global screen_number
    screen_number = 4


def set_game_mode_to_online():
    global screen_number
    screen_number = 1
    game_selector.backButton_anim.play(15)
    game_selector.join_button_anim.play(15)
    game_selector.create_button_anim.play(15)


def create_game():
    global screen_number
    screen_number = 2


def join_game():
    global screen_number
    screen_number = 3


def run_after_delay(function, time_to_start):
    time.sleep(time_to_start)
    function()


def invoke(function, time_to_start):
    thread = threading.Thread(target=run_after_delay, args=(function, time_to_start))
    thread.start()


class Square:
    def __init__(self, pos, state=0, width=60):
        self.pos = pos
        self.state = state
        self.width = width
        self.colors = [PLAYER1_COLOR, PLAYER2_COLOR]
        self.pressed = False

        self.color = self.colors[self.state - 1]

    def draw(self):
        self.color = self.colors[self.state - 1]
        if self.state == 1:
            pygame.draw.circle(screen, self.color, [int(self.pos[0] + self.width / 2), int(self.pos[1] + self.width / 2)],
                               int(self.width * 0.8 / 2))
            pygame.draw.circle(screen, [0, 0, 0], [int(self.pos[0] + self.width / 2), int(self.pos[1] + self.width / 2)],
                               int(self.width * 0.7 / 2))
        elif self.state == 2:
            pygame.draw.line(screen, self.color, [int(self.pos[0] + self.width * 0.1), int(self.pos[1] + self.width * 0.1)],
                             [int(self.pos[0] + self.width * 0.9), int(self.pos[1] + self.width * 0.9)], int(self.width * 0.05))
            pygame.draw.line(screen, self.color, [int(self.pos[0] + self.width * 0.1), int(self.pos[1] + self.width * 0.9)],
                             [int(self.pos[0] + self.width * 0.9), int(self.pos[1] + self.width * 0.1)], int(self.width * 0.05))
        else:
            pass


class Button:
    def __init__(self,fontSize, textColor, color, colorWhenMouseOver, colorWhenClicked, pos, width, height, onClick, text=''):
        self.color = color
        self.fontSize = fontSize
        self.textColor = textColor
        self.defaultColor = color
        self.colorWhenMouseOver = colorWhenMouseOver
        self.colorWhenClicked = colorWhenClicked
        self.pos = pos
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.width = width
        self.height = height
        self.onCLick = onClick
        self.text = text
        self.clicked = False

    def draw(self, win, outline=None):
        self.x = self.pos[0]
        self.y = self.pos[1]
        # Call this method to draw the Button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (int(self.x), int(self.y), int(self.width), int(self.height)), 0)

        if self.text != '':
            font = pygame.font.Font('data\\freesansbold.ttf', self.fontSize)
            text = font.render(self.text, True, self.textColor)
            win.blit(text, (
            int(self.x + (self.width / 2 - text.get_width() / 2)), int(self.y + (self.height / 2 - text.get_height() / 2))))

        if self.onCLick != "":
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


class TextBox:
    def __init__(self, text, pos, size=22, font="freesansbold.ttf", color=(255, 255, 255), align="middle"):
        self.font = pygame.font.Font(font, size)
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color
        self.rendered_text = self.font.render(self.text, True, self.color)
        self.align = align

    def draw_and_update(self):
        self.rendered_text = self.font.render(self.text, True, self.color)
        if self.align == "middle":
            screen.blit(self.rendered_text, [self.pos[0] - self.rendered_text.get_width()/2, self.pos[1] - self.rendered_text.get_height()/2])
        elif self.align == "left":
            screen.blit(self.rendered_text, [self.pos[0],
                                             self.pos[1] - self.rendered_text.get_height() / 2])


class Selection:
    def __init__(self,screen, fontSize, textColor, color, colorWhenMouseOver, colorWhenClicked, pos, width, height, selections, selected):
        self.color = color
        self.screen = screen
        self.fontSize = fontSize
        self.textColor = textColor
        self.defaultColor = color
        self.colorWhenMouseOver = colorWhenMouseOver
        self.colorWhenClicked = colorWhenClicked
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.height = height
        self.selections = selections
        self.selected = selected
        self.button = Button(self.fontSize, self.textColor, self.color, self.colorWhenMouseOver, self.colorWhenClicked, [self.x, self.y], self.width, self.height, "", text=self.selections[self.selected])
        self.right = Button(self.fontSize, self.textColor, self.color, self.colorWhenMouseOver, self.colorWhenClicked, [self.x + self.width, self.y], self.height, self.height, "", text=">")
        self.left = Button(self.fontSize, self.textColor, self.color, self.colorWhenMouseOver, self.colorWhenClicked,
                           [self.x -self.height, self.y], self.height, self.height, "", text="<")

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


class InputBox:
    def __init__(self, pos, width, height, color=(255, 255, 255), text_color=(50, 50, 50), default_text="enter pos"):
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color
        self.text_color = text_color
        self.text = default_text
        self.cursor = ""
        self.font = pygame.font.Font("data\\freesansbold.ttf", int(0.6 * self.height))
        self.clicked = False
        self.key_pressed = False
        self.start_time = time.time_ns()

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.pos[0], self.pos[1], self.width, self.height])
        text = self.font.render(self.text, True, self.text_color)
        cursor = self.font.render(self.cursor, True, self.text_color)
        screen.blit(text, [self.pos[0] + self.width/2 - text.get_width()/2, self.pos[1] + self.height/2 - text.get_height()/2])
        screen.blit(cursor, [self.pos[0] + self.width / 2 + text.get_width() / 2,
                           self.pos[1] + self.height / 2 - cursor.get_height() / 2])

    def update(self):
        global host
        if not self.clicked:
            self.cursor = ""
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]
            if mouse_pressed:
                if pygame.rect.Rect([self.pos[0], self.pos[1], self.width, self.height]).collidepoint(mouse_pos[0], mouse_pos[1]):
                    self.clicked = True
        else:
            time_now = time.time_ns()
            if int(2*(time_now - self.start_time)/1000000000)%2 == 1:
                self.cursor = "|"
            else:
                self.cursor = ""
            keys = pygame.key.get_pressed()
            try:
                key = keys.index(True)
                if not self.key_pressed:
                    self.key_pressed = True
                    if keys[pygame.K_BACKSPACE]:
                        if len(self.text) > 0:
                            self.text = self.text[0:len(self.text) - 1]
                    elif keys[pygame.K_RETURN]:
                        self.clicked = False
                        host = self.text
                    else:
                        if keys[pygame.K_0]:
                            self.text += "0"
                        elif keys[pygame.K_1]:
                            self.text += "1"
                        elif keys[pygame.K_2]:
                            self.text += "2"
                        elif keys[pygame.K_3]:
                            self.text += "3"
                        elif keys[pygame.K_4]:
                            self.text += "4"
                        elif keys[pygame.K_5]:
                            self.text += "5"
                        elif keys[pygame.K_6]:
                            self.text += "6"
                        elif keys[pygame.K_7]:
                            self.text += "7"
                        elif keys[pygame.K_8]:
                            self.text += "8"
                        elif keys[pygame.K_9]:
                            self.text += "9"
                        elif keys[pygame.K_PERIOD]:
                            self.text += "."
            except ValueError:
                self.key_pressed = False


class TicTac2:
    def __init__(self):
        self.mouse_pressed = True
        self.player = 1
        self.won = 0
        self.once_extended = False
        self.req_to_win = req_to_win
        self.row_added = False
        self.color = GRID_COLOR
        self.square_width = 60
        self.column_count = column_count
        self.row_count = row_count
        self.squares = []
        self.square_values = []
        self.pos = [screen_width/2 - self.column_count*self.square_width/2, screen_height/2 - self.row_count*self.square_width/2]
        for i in range(self.row_count):
            row = []
            val_row = []
            for j in range(self.column_count):
                row.append(Square([self.pos[0] + j*self.square_width, self.pos[1] + i*self.square_width], width=self.square_width))
                val_row.append(0)
            self.squares.append(row)
            self.square_values.append(val_row)
        self.starting_player = 1

    def draw(self):
        for i in range(1, self.column_count):
            pygame.draw.line(screen, self.color,
                             [int(self.pos[0] + self.square_width * i), int(self.pos[1])],
                             [int(self.pos[0] + self.square_width * i), int(self.pos[1] + self.square_width * self.row_count)],
                             int(self.square_width * 0.05))
        for i in range(1, self.row_count):
            pygame.draw.line(screen, self.color,
                             [int(self.pos[0]), int(self.pos[1] + self.square_width * i)],
                             [int(self.pos[0] + self.square_width * self.column_count), int(self.pos[1] + self.square_width * i)],
                             int(self.square_width * 0.05))
        for row in self.squares:
            for square in row:
                square.draw()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if mouse_pressed - self.mouse_pressed == 1:
            if mouse_pressed:
                if self.pos[0] < mouse_pos[0] < self.pos[0] + self.square_width * self.column_count and self.pos[1] < \
                        mouse_pos[1] < self.pos[1] + self.square_width * self.row_count:
                    column = int((mouse_pos[0] - self.pos[0]) / self.square_width)
                    row = int((mouse_pos[1] - self.pos[1]) / self.square_width)
                    if not self.squares[row][column].pressed and not self.won:
                        self.squares[row][column].pressed = True
                        self.square_values[row][column] = self.player
                        if self.player == 1:
                            self.player = 2
                        elif self.player == 2:
                            self.player = 1
                        self.row_added = False
                        filled_squares = 0
                        for i in range(self.row_count):
                            for j in range(self.column_count):
                                if self.square_values[i][j] != 0:
                                    filled_squares += 1
                        if filled_squares == self.column_count * self.row_count:
                            self.check_if_won()
                            if not self.won:
                                self.add_row()
                                self.add_row(up=True)
                                self.add_column()
                                self.add_column(left=True)
                                self.req_to_win += 1
                            #invoke(self.clear, 1)

                def add_row_if_consecutively_extended():
                    if not self.once_extended:
                        if self.row_added:
                            self.req_to_win += 1
                            self.row_added = False
                            self.once_extended = True
                        else:
                            self.row_added = True

                if self.pos[0] < mouse_pos[0] < self.pos[0] + self.square_width * self.column_count and mouse_pos[1] < self.pos[1]:
                    #print("up")
                    self.toggle_player()
                    self.add_row(up=True)
                    add_row_if_consecutively_extended()
                if self.pos[0] < mouse_pos[0] < self.pos[0] + self.square_width * self.column_count and mouse_pos[1] > self.pos[1] + self.square_width * self.row_count:
                    #print("down")
                    self.toggle_player()
                    self.add_row()
                    add_row_if_consecutively_extended()
                if self.pos[1] < mouse_pos[1] < self.pos[1] + self.square_width * self.row_count and mouse_pos[0] < self.pos[0]:
                    #print("left")
                    self.toggle_player()
                    self.add_column(left=True)
                    add_row_if_consecutively_extended()
                if self.pos[1] < mouse_pos[1] < self.pos[1] + self.square_width * self.row_count and mouse_pos[0] > self.pos[0] + self.square_width * self.column_count:
                    #print("right")
                    self.toggle_player()
                    self.add_column()
                    add_row_if_consecutively_extended()

        for i in range(self.row_count):
            for j in range(self.column_count):
                self.pos = [screen_width / 2 - self.column_count * self.square_width / 2,
                            screen_height / 2 - self.row_count * self.square_width / 2]
                self.squares[i][j].state = self.square_values[i][j]
                self.squares[i][j].pos = [self.pos[0] + j * self.square_width, self.pos[1] + i * self.square_width]
                self.squares[i][j].width = self.square_width

        for i in range(self.row_count):
            for j in range(self.column_count - self.req_to_win + 1):
                value = self.square_values[i][j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[i][j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [j, i], [j + self.req_to_win - 1, i])

        for i in range(self.column_count):
            for j in range(self.row_count - self.req_to_win + 1):
                value = self.square_values[j][i]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[j + k][i]:
                        break
                else:
                    if value != 0:
                        self.win(value, [i, j], [i, j + self.req_to_win - 1])

        for i in range(self.row_count):
            len_of_diagonal = min(self.row_count - i, self.column_count)
            for j in range(len_of_diagonal - self.req_to_win + 1):
                value = self.square_values[i + j][j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[i + j + k][j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [j, i + j], [j + self.req_to_win - 1, i + j + self.req_to_win - 1])
            len_of_diagonal = min(i + 1, self.column_count)
            for j in range(len_of_diagonal - self.req_to_win + 1):
                value = self.square_values[i - j][j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[i - j - k][j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [j, i - j], [j + self.req_to_win - 1, i - j - self.req_to_win + 1])

        for i in range(1, self.column_count):
            len_of_diagonal = min(self.row_count, self.column_count - i)
            for j in range(len_of_diagonal - self.req_to_win + 1):
                value = self.square_values[j][i + j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[j + k][i + j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [i + j, j], [i + j + self.req_to_win - 1, j + self.req_to_win - 1])
            len_of_diagonal = min(self.row_count, self.column_count - i)
            for j in range(len_of_diagonal - self.req_to_win + 1):
                value = self.square_values[self.row_count - j - 1][i + j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[self.row_count - j - 1 - k][i + j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [i + j, self.row_count - j - 1], [i + j + self.req_to_win - 1, self.row_count - j - 1 - self.req_to_win + 1])

        if self.row_count*self.square_width > screen_height - 10 or self.column_count * self.square_width > screen_width - 10:
            self.square_width *= 0.9

        self.mouse_pressed = mouse_pressed

    def check_if_won(self):
        for i in range(self.row_count):
            for j in range(self.column_count - self.req_to_win + 1):
                value = self.square_values[i][j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[i][j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [j, i], [j + self.req_to_win - 1, i])

        for i in range(self.column_count):
            for j in range(self.row_count - self.req_to_win + 1):
                value = self.square_values[j][i]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[j + k][i]:
                        break
                else:
                    if value != 0:
                        self.win(value, [i, j], [i, j + self.req_to_win - 1])

        for i in range(self.row_count):
            len_of_diagonal = min(self.row_count - i, self.column_count)
            for j in range(len_of_diagonal - self.req_to_win + 1):
                value = self.square_values[i + j][j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[i + j + k][j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [j, i + j], [j + self.req_to_win - 1, i + j + self.req_to_win - 1])
            len_of_diagonal = min(i + 1, self.column_count)
            for j in range(len_of_diagonal - self.req_to_win + 1):
                value = self.square_values[i - j][j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[i - j - k][j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [j, i - j], [j + self.req_to_win - 1, i - j - self.req_to_win + 1])

        for i in range(1, self.column_count):
            len_of_diagonal = min(self.row_count, self.column_count - i)
            for j in range(len_of_diagonal - self.req_to_win + 1):
                value = self.square_values[j][i + j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[j + k][i + j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [i + j, j], [i + j + self.req_to_win - 1, j + self.req_to_win - 1])
            len_of_diagonal = min(self.row_count, self.column_count - i)
            for j in range(len_of_diagonal - self.req_to_win + 1):
                value = self.square_values[self.row_count - j - 1][i + j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[self.row_count - j - 1 - k][i + j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [i + j, self.row_count - j - 1], [i + j + self.req_to_win - 1, self.row_count - j - 1 - self.req_to_win + 1])

    def clear(self):
        self.square_values = []
        self.squares = []
        self.row_count = row_count
        self.column_count = column_count
        self.req_to_win = req_to_win
        self.once_extended = False
        for i in range(self.row_count):
            row = []
            val_row = []
            for j in range(self.column_count):
                row.append(Square([self.pos[0] + j * self.square_width, self.pos[1] + i * self.square_width],
                                  width=self.square_width))
                val_row.append(0)
            self.squares.append(row)
            self.square_values.append(val_row)
        self.won = False
        #print("clearing")
        self.mouse_pressed = True
        self.square_width = 60
        go_to_menu()

    def win(self, player, start_pos_of_line, end_pos_of_line):
        global player1Score
        global player2Score
        if not self.won:
            self.won = True
            print(f"Player {player} Won!")
            if player == 1:
                player1Score += 1
            elif player == 2:
                player2Score += 1

            if self.starting_player == 1:
                self.starting_player = 2
            elif self.starting_player == 2:
                self.starting_player = 1
            self.player = self.starting_player

            invoke(self.clear, 1.6)
        pygame.draw.line(screen, [55, 255, 55], [int(start_pos_of_line[0] * self.square_width + self.square_width / 2 + self.pos[0]), int(start_pos_of_line[1] * self.square_width + self.square_width / 2 + self.pos[1])], [int(end_pos_of_line[0] * self.square_width + self.square_width / 2 + self.pos[0]), int(end_pos_of_line[1] * self.square_width + self.square_width / 2 + self.pos[1])], int(self.square_width * 0.05))

    def add_row(self, up=False):
        self.row_count += 1
        row = []
        squares = []
        if up:
            for i in range(self.column_count):
                row.append(0)
                squares.append(
                    Square([self.pos[0], self.pos[1] + i * self.square_width],
                           width=self.square_width))
            self.square_values.insert(0, row)
            self.squares.insert(0, squares)
        else:
            for i in range(self.column_count):
                row.append(0)
                squares.append(Square([self.pos[0] + self.row_count * self.square_width, self.pos[1] + i * self.square_width],
                                  width=self.square_width))
            self.square_values.append(row)
            self.squares.append(squares)

    def add_column(self, left=False):
        self.column_count += 1
        if left:
            for i in range(self.row_count):
                self.square_values[i].insert(0, 0)
                self.squares[i].insert(0, Square([self.pos[0] + self.row_count * i, self.pos[1] + i * self.square_width],
                                              width=self.square_width))
        else:
            for i in range(self.row_count):
                self.square_values[i].append(0)
                self.squares[i].append(Square([self.pos[0] + self.row_count * i, self.pos[1] + i * self.square_width],
                                  width=self.square_width))

    def toggle_player(self):
        if self.player == 1:
            self.player = 2
        elif self.player == 2:
            self.player = 1


class TicTac2_server:
    def __init__(self):
        self.mouse_pressed = True
        self.client_mouse_pressed = True
        self.player = 1
        self.won = 0
        self.once_extended = False
        self.req_to_win = req_to_win
        self.row_added = False
        self.color = GRID_COLOR
        self.square_width = 60
        self.column_count = column_count
        self.row_count = row_count
        self.squares = []
        self.square_values = []
        self.pos = [screen_width/2 - self.column_count*self.square_width/2, screen_height/2 - self.row_count*self.square_width/2]
        for i in range(self.row_count):
            row = []
            val_row = []
            for j in range(self.column_count):
                row.append(Square([self.pos[0] + j*self.square_width, self.pos[1] + i*self.square_width], width=self.square_width))
                val_row.append(0)
            self.squares.append(row)
            self.square_values.append(val_row)

        self.starting_player = 1

        #inp_file = open("server_data/received.bin", "wb")
        #inp_file.write(b"")
        #inp_file.close()

    def draw(self):
        for i in range(1, self.column_count):
            pygame.draw.line(screen, self.color,
                             [int(self.pos[0] + self.square_width * i), int(self.pos[1])],
                             [int(self.pos[0] + self.square_width * i), int(self.pos[1] + self.square_width * self.row_count)],
                             int(self.square_width * 0.05))
        for i in range(1, self.row_count):
            pygame.draw.line(screen, self.color,
                             [int(self.pos[0]), int(self.pos[1] + self.square_width * i)],
                             [int(self.pos[0] + self.square_width * self.column_count), int(self.pos[1] + self.square_width * i)],
                             int(self.square_width * 0.05))
        for row in self.squares:
            for square in row:
                square.draw()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        self.check_if_won()

        if self.player == 1:
            self.check_if_clicked(mouse_pressed, self.mouse_pressed, mouse_pos)
        else:
            try:
                inp_file = open(r"server_data\\received.bin", "rb")
                data = pickle.load(inp_file)
                #print(data)
                self.check_if_clicked(data[1], self.client_mouse_pressed, data[0])
                self.client_mouse_pressed = data[1]
                inp_file.close()

                data_file = open("server_data\\received.bin", "wb")
                data = [[0, 0], 0]
                pickle.dump(data, data_file)
                data_file.close()
                #inp_file = open("server_data/received.bin", "wb")
                #inp_file.write(b"")
                #inp_file.close()
            except EOFError:
                print("file empty")

        self.normalise_squares()

        if self.row_count*self.square_width > screen_height - 10 or self.column_count * self.square_width > screen_width - 10:
            self.square_width *= 0.9

        self.mouse_pressed = mouse_pressed

        if self.won:
            self.client_mouse_pressed = True

    def normalise_squares(self):
        for i in range(self.row_count):
            for j in range(self.column_count):
                self.pos = [screen_width / 2 - self.column_count * self.square_width / 2,
                            screen_height / 2 - self.row_count * self.square_width / 2]
                self.squares[i][j].state = self.square_values[i][j]
                self.squares[i][j].pos = [self.pos[0] + j * self.square_width, self.pos[1] + i * self.square_width]
                self.squares[i][j].width = self.square_width

    def check_if_won(self):
        for i in range(self.row_count):
            for j in range(self.column_count - self.req_to_win + 1):
                value = self.square_values[i][j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[i][j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [j, i], [j + self.req_to_win - 1, i])

        for i in range(self.column_count):
            for j in range(self.row_count - self.req_to_win + 1):
                value = self.square_values[j][i]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[j + k][i]:
                        break
                else:
                    if value != 0:
                        self.win(value, [i, j], [i, j + self.req_to_win - 1])

        for i in range(self.row_count):
            len_of_diagonal = min(self.row_count - i, self.column_count)
            for j in range(len_of_diagonal - self.req_to_win + 1):
                value = self.square_values[i + j][j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[i + j + k][j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [j, i + j], [j + self.req_to_win - 1, i + j + self.req_to_win - 1])
            len_of_diagonal = min(i + 1, self.column_count)
            for j in range(len_of_diagonal - self.req_to_win + 1):
                value = self.square_values[i - j][j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[i - j - k][j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [j, i - j], [j + self.req_to_win - 1, i - j - self.req_to_win + 1])

        for i in range(1, self.column_count):
            len_of_diagonal = min(self.row_count, self.column_count - i)
            for j in range(len_of_diagonal - self.req_to_win + 1):
                value = self.square_values[j][i + j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[j + k][i + j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [i + j, j], [i + j + self.req_to_win - 1, j + self.req_to_win - 1])
            len_of_diagonal = min(self.row_count, self.column_count - i)
            for j in range(len_of_diagonal - self.req_to_win + 1):
                value = self.square_values[self.row_count - j - 1][i + j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[self.row_count - j - 1 - k][i + j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [i + j, self.row_count - j - 1], [i + j + self.req_to_win - 1, self.row_count - j - 1 - self.req_to_win + 1])

    def clear(self):
        self.square_values = []
        self.squares = []
        self.row_count = row_count
        self.column_count = column_count
        self.req_to_win = req_to_win
        self.once_extended = False
        for i in range(self.row_count):
            row = []
            val_row = []
            for j in range(self.column_count):
                row.append(Square([self.pos[0] + j * self.square_width, self.pos[1] + i * self.square_width],
                                  width=self.square_width))
                val_row.append(0)
            self.squares.append(row)
            self.square_values.append(val_row)
        self.won = False
        self.mouse_pressed = True
        self.client_mouse_pressed = True
        self.square_width = 60
        go_to_menu()

        thread = threading.Thread(target=self.send_data)
        thread.start()

    def win(self, player, start_pos_of_line, end_pos_of_line):
        global player1Score
        global player2Score
        if not self.won:
            self.won = True
            print(f"Player {player} Won!")
            if player == 1:
                player1Score += 1
            elif player == 2:
                player2Score += 1

            if self.starting_player == 1:
                self.starting_player = 2
            elif self.starting_player == 2:
                self.starting_player = 1
            self.player = self.starting_player


            invoke(self.clear, 1.6)
        pygame.draw.line(screen, [55, 255, 55], [int(start_pos_of_line[0] * self.square_width + self.square_width / 2 + self.pos[0]), int(start_pos_of_line[1] * self.square_width + self.square_width / 2 + self.pos[1])], [int(end_pos_of_line[0] * self.square_width + self.square_width / 2 + self.pos[0]), int(end_pos_of_line[1] * self.square_width + self.square_width / 2 + self.pos[1])], int(self.square_width * 0.05))

    def add_row(self, up=False):
        self.row_count += 1
        row = []
        squares = []
        if up:
            for i in range(self.column_count):
                row.append(0)
                squares.append(
                    Square([self.pos[0], self.pos[1] + i * self.square_width],
                           width=self.square_width))
            self.square_values.insert(0, row)
            self.squares.insert(0, squares)
        else:
            for i in range(self.column_count):
                row.append(0)
                squares.append(Square([self.pos[0] + self.row_count * self.square_width, self.pos[1] + i * self.square_width],
                                  width=self.square_width))
            self.square_values.append(row)
            self.squares.append(squares)

    def add_column(self, left=False):
        self.column_count += 1
        if left:
            for i in range(self.row_count):
                self.square_values[i].insert(0, 0)
                self.squares[i].insert(0, Square([self.pos[0] + self.row_count * i, self.pos[1] + i * self.square_width],
                                              width=self.square_width))
        else:
            for i in range(self.row_count):
                self.square_values[i].append(0)
                self.squares[i].append(Square([self.pos[0] + self.row_count * i, self.pos[1] + i * self.square_width],
                                  width=self.square_width))

    def toggle_player(self):
        if self.player == 1:
            self.player = 2
        elif self.player == 2:
            self.player = 1

    def check_if_clicked(self, mouse_pressed, prev_mouse_pressed, mouse_pos):
        if mouse_pressed - prev_mouse_pressed == 1:
            print("mouse pressed")
            if mouse_pressed:
                if self.pos[0] < mouse_pos[0] < self.pos[0] + self.square_width * self.column_count and self.pos[1] < \
                        mouse_pos[1] < self.pos[1] + self.square_width * self.row_count:
                    column = int((mouse_pos[0] - self.pos[0]) / self.square_width)
                    row = int((mouse_pos[1] - self.pos[1]) / self.square_width)
                    if not self.squares[row][column].pressed and not self.won:
                        self.squares[row][column].pressed = True
                        self.square_values[row][column] = self.player
                        self.squares[row][column].state = self.square_values[row][column]
                        if self.player == 1:
                            self.player = 2
                        elif self.player == 2:
                            self.player = 1
                        self.row_added = False
                        filled_squares = 0
                        for i in range(self.row_count):
                            for j in range(self.column_count):
                                if self.square_values[i][j] != 0:
                                    filled_squares += 1
                        if filled_squares == self.column_count * self.row_count:
                            self.check_if_won()
                            if not self.won:
                                self.add_row()
                                self.add_row(up=True)
                                self.add_column()
                                self.add_column(left=True)
                                self.req_to_win += 1
                            # invoke(self.clear, 1)

                def add_row_if_consecutively_extended():
                    if not self.once_extended:
                        if self.row_added:
                            self.req_to_win += 1
                            self.row_added = False
                            self.once_extended = True
                        else:
                            self.row_added = True

                if self.pos[0] < mouse_pos[0] < self.pos[0] + self.square_width * self.column_count and mouse_pos[1] < self.pos[1]:
                    #print("up")
                    self.toggle_player()
                    self.add_row(up=True)
                    add_row_if_consecutively_extended()
                if self.pos[0] < mouse_pos[0] < self.pos[0] + self.square_width * self.column_count and mouse_pos[1] > self.pos[1] + self.square_width * self.row_count:
                    #print("down")
                    self.toggle_player()
                    self.add_row()
                    add_row_if_consecutively_extended()
                if self.pos[1] < mouse_pos[1] < self.pos[1] + self.square_width * self.row_count and mouse_pos[0] < self.pos[0]:
                    #print("left")
                    self.toggle_player()
                    self.add_column(left=True)
                    add_row_if_consecutively_extended()
                if self.pos[1] < mouse_pos[1] < self.pos[1] + self.square_width * self.row_count and mouse_pos[0] > self.pos[0] + self.square_width * self.column_count:
                    #print("right")
                    self.toggle_player()
                    self.add_column()
                    add_row_if_consecutively_extended()
            self.check_if_won()
            self.normalise_squares()
            thread = threading.Thread(target=self.send_data)
            thread.start()

    def send_data(self):
        data_file = open("server_data\\data_file.bin", "wb")
        data = [self.squares, self.square_values, self.req_to_win, player1Score, player2Score, self.player]
        pickle.dump(data, data_file)
        data_file.close()
        send_file("server_data\\data_file.bin", client_ip, 5001)
        print("sent")

    def look_for_messages(self):
        global running
        global client_ip
        global host
        while running:
            receive_file("server_data\\received.bin")
            host = client_ip


class TicTac2_client:
    def __init__(self):
        self.mouse_pressed = True
        self.player = 1
        self.color = GRID_COLOR
        self.won = False
        self.req_to_win = 3
        self.square_width = 60
        self.column_count = column_count
        self.row_count = row_count
        self.squares = []
        self.square_values = []
        self.pos = [screen_width / 2 - self.column_count * self.square_width / 2,
                    screen_height / 2 - self.row_count * self.square_width / 2]
        for i in range(self.row_count):
            row = []
            val_row = []
            for j in range(self.column_count):
                row.append(Square([self.pos[0] + j * self.square_width, self.pos[1] + i * self.square_width],
                                  width=self.square_width))
                val_row.append(0)
            self.squares.append(row)
            self.square_values.append(val_row)

        self.starting_player = 1

        inp_file = open("client_data/received.bin", "wb")
        dat = [self.squares, self.square_values, self.req_to_win, player1Score, player2Score, self.player]
        pickle.dump(dat, inp_file)
        inp_file.close()

    def draw(self):
        for i in range(1, self.column_count):
            pygame.draw.line(screen, self.color,
                             [int(self.pos[0] + self.square_width * i), int(self.pos[1])],
                             [int(self.pos[0] + self.square_width * i), int(self.pos[1] + self.square_width * self.row_count)],
                             int(self.square_width * 0.05))
        for i in range(1, self.row_count):
            pygame.draw.line(screen, self.color,
                             [int(self.pos[0]), int(self.pos[1] + self.square_width * i)],
                             [int(self.pos[0] + self.square_width * self.column_count), int(self.pos[1] + self.square_width * i)],
                             int(self.square_width * 0.05))
        for row in self.squares:
            for square in row:
                square.draw()

    def update(self):
        global player1Score
        global player2Score

        self.row_count = len(self.squares)
        self.column_count = len(self.squares[0])

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        self.check_if_won()

        if mouse_pressed - self.mouse_pressed == 1:
            if self.player == 2:
                data = [mouse_pos, mouse_pressed]
                thread = threading.Thread(target=self.send_data, args=(data,))
                thread.start()
                #invoke(self.send_data_auto, 0.5)

        for i in range(self.row_count):
            for j in range(self.column_count):
                self.pos = [screen_width / 2 - self.column_count * self.square_width / 2,
                            screen_height / 2 - self.row_count * self.square_width / 2]
                self.squares[i][j].state = self.square_values[i][j]
                self.squares[i][j].pos = [self.pos[0] + j * self.square_width, self.pos[1] + i * self.square_width]
                self.squares[i][j].width = self.square_width

        if self.row_count*self.square_width > screen_height - 10 or self.column_count * self.square_width > screen_width - 10:
            self.square_width *= 0.9

        try:
            recv_file = open(r"client_data\\received.bin", "rb")
            data = pickle.load(recv_file)
            #print(data)
            self.squares = data[0]
            self.square_values = data[1]
            self.req_to_win = data[2]
            player1Score = data[3]
            player2Score = data[4]
            self.player = data[5]
            recv_file.close()
        except EOFError:
            pass

        self.mouse_pressed = mouse_pressed

    def clear(self):
        self.square_values = []
        self.squares = []
        self.row_count = row_count
        self.column_count = column_count
        self.req_to_win = req_to_win
        for i in range(self.row_count):
            row = []
            val_row = []
            for j in range(self.column_count):
                row.append(Square([self.pos[0] + j * self.square_width, self.pos[1] + i * self.square_width],
                                  width=self.square_width))
                val_row.append(0)
            self.squares.append(row)
            self.square_values.append(val_row)
        self.won = False
        self.mouse_pressed = True
        self.square_width = 60
        go_to_menu()

        data = [[0, 0], 0]
        thread = threading.Thread(target=self.send_data, args=(data,))
        thread.start()

    def win(self, player, start_pos_of_line, end_pos_of_line):
        global player1Score
        global player2Score
        if not self.won:
            self.won = True
            print(f"Player {player} Won!")
            if player == 1:
                player1Score += 1
            elif player == 2:
                player2Score += 1

            if self.starting_player == 1:
                self.starting_player = 2
            elif self.starting_player == 2:
                self.starting_player = 1
            self.player = self.starting_player

            invoke(self.clear, 1.6)
        pygame.draw.line(screen, [55, 255, 55], [int(start_pos_of_line[0] * self.square_width + self.square_width / 2 + self.pos[0]), int(start_pos_of_line[1] * self.square_width + self.square_width / 2 + self.pos[1])], [int(end_pos_of_line[0] * self.square_width + self.square_width / 2 + self.pos[0]), int(end_pos_of_line[1] * self.square_width + self.square_width / 2 + self.pos[1])], int(self.square_width * 0.05))

    def check_if_won(self):
        for i in range(self.row_count):
            for j in range(self.column_count - self.req_to_win + 1):
                value = self.square_values[i][j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[i][j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [j, i], [j + self.req_to_win - 1, i])

        for i in range(self.column_count):
            for j in range(self.row_count - self.req_to_win + 1):
                value = self.square_values[j][i]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[j + k][i]:
                        break
                else:
                    if value != 0:
                        self.win(value, [i, j], [i, j + self.req_to_win - 1])

        for i in range(self.row_count):
            len_of_diagonal = min(self.row_count - i, self.column_count)
            for j in range(len_of_diagonal - self.req_to_win + 1):
                value = self.square_values[i + j][j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[i + j + k][j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [j, i + j], [j + self.req_to_win - 1, i + j + self.req_to_win - 1])
            len_of_diagonal = min(i + 1, self.column_count)
            for j in range(len_of_diagonal - self.req_to_win + 1):
                value = self.square_values[i - j][j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[i - j - k][j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [j, i - j], [j + self.req_to_win - 1, i - j - self.req_to_win + 1])

        for i in range(1, self.column_count):
            len_of_diagonal = min(self.row_count, self.column_count - i)
            for j in range(len_of_diagonal - self.req_to_win + 1):
                value = self.square_values[j][i + j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[j + k][i + j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [i + j, j], [i + j + self.req_to_win - 1, j + self.req_to_win - 1])
            len_of_diagonal = min(self.row_count, self.column_count - i)
            for j in range(len_of_diagonal - self.req_to_win + 1):
                value = self.square_values[self.row_count - j - 1][i + j]
                for k in range(1, self.req_to_win):
                    if value != self.square_values[self.row_count - j - 1 - k][i + j + k]:
                        break
                else:
                    if value != 0:
                        self.win(value, [i + j, self.row_count - j - 1], [i + j + self.req_to_win - 1, self.row_count - j - 1 - self.req_to_win + 1])

    def send_data(self, data):
        data_file = open("client_data\\data_file.bin", "wb")
        pickle.dump(data, data_file)
        data_file.close()
        send_file("client_data\\data_file.bin", host, 5001)

    def send_data_auto(self):
        data_file = open("client_data\\data_file.bin", "wb")
        data = [pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0]]
        pickle.dump(data, data_file)
        data_file.close()
        send_file("client_data\\data_file.bin", host, 5001)

    def look_for_messages(self):
        global running
        global client_ip
        global host
        while running:
            receive_file("client_data\\received.bin")
            print("receiver file")
            host = client_ip


class Menu:
    def __init__(self):
        self.screen = screen

        self.text_pos = (
            int(screen_width / 2),
            int(screen_height / 2))
        self.tic_tac_2_text = TextBox("Tic Tac 2.0", self.text_pos, 150, 'data\\freesansbold.ttf', [255, 50, 0])
        self.playButtonDimensions = [90, 50]
        self.settingsButtonDimensions = [160, 40]
        self.playbutton = Button(30, (125, 255, 100), (70, 200, 60), (90, 230, 80), (110, 255, 100),
                                 [self.screen.get_width() / 2 - self.playButtonDimensions[0] / 2,
                                 11 * self.screen.get_height() / 16], self.playButtonDimensions[0],
                                 self.playButtonDimensions[1], "go_to_game()", text="PLAY")
        self.how_to_play_button = Button(20, (50, 50, 50), (220, 220, 60), (250, 250, 100), (255, 255, 100),
                                         [self.screen.get_width() / 9 - self.settingsButtonDimensions[0] / 2,
                                     self.screen.get_height() / 10 - self.settingsButtonDimensions[1] / 2],
                                         self.settingsButtonDimensions[0],
                                         self.settingsButtonDimensions[1], "go_to_how_to_play()", text="How To Play")
        self.scoreboard = ScoreBoard(screen, [255, 255, 100], [0, 0, 0], [screen_width - 260, 20], 230, 100)

        self.button_anim = animations.ButtonSlideAnim(self.how_to_play_button, list(self.how_to_play_button.pos), list([-100, self.how_to_play_button.y]))
        self.scoreboard_anim = animations.ButtonSlideAnim(self.scoreboard, list(self.scoreboard.position), [self.scoreboard.position[0] + 200, self.scoreboard.position[1]])
        self.playbutton_anim = animations.ButtonSlideAnim(self.playbutton, list(self.playbutton.pos), [self.playbutton.pos[0] - 500, self.playbutton.pos[1]])
        self.tic_tac_2_text_anim = animations.ButtonSlideAnim(self.tic_tac_2_text, list(self.tic_tac_2_text.pos), [self.tic_tac_2_text.pos[0] + 1000, self.tic_tac_2_text.pos[1]])

    def draw(self):
        self.playbutton.draw(screen)
        self.how_to_play_button.draw(screen)
        self.scoreboard.update()
        self.scoreboard.draw()
        self.tic_tac_2_text.draw_and_update()

        self.button_anim.update()
        self.playbutton_anim.update()
        self.scoreboard_anim.update()
        self.tic_tac_2_text_anim.update()


class HowToPlay:
    def __init__(self):
        self.font = pygame.font.Font("data\\freesansbold.ttf", 22)
        self.backButtonDimensions = [70, 50]
        self.backButton = Button(25, (0, 0, 0), (200, 200, 30), (230, 230, 100), (255, 255, 100),
                                 [9 * screen.get_width() / 10 - self.backButtonDimensions[0] / 2,
                                  screen.get_height() / 10 - self.backButtonDimensions[1] / 2],
                                 self.backButtonDimensions[0],
                                 self.backButtonDimensions[1], "go_to_menu()", text="Back")

        self.back_button_anim = animations.ButtonSlideAnim(self.backButton, list(self.backButton.pos),
                                                          [self.backButton.pos[0] + 200, self.backButton.pos[1]])

        self.distance_from_left = 70

        self.text1 = TextBox("This is basically a game of tic tac toe, but the players can now",
                                 [self.distance_from_left, 100], align="left")
        self.text2 = TextBox("add rows and columns in their turn instead of a circle or cross.",
                                 [self.distance_from_left, 135], align="left")
        self.text3 = TextBox("If both the players add a row or column consecutively, the number",
                                 [self.distance_from_left, 170], align="left")
        self.text4 = TextBox("of circles or crosses in a line required to win increases by one.",
                                 [self.distance_from_left, 205], align="left")
        self.text5 = TextBox("This, however, can only happen once, and the next time rows or ",
                                 [self.distance_from_left, 240], align="left")
        self.text6 = TextBox("columns are added consecutively, it won't increase. If all the ",
                                 [self.distance_from_left, 275], align="left")
        self.text7 = TextBox("squares get filled and it's a draw, a row or column will be added",
                                 [self.distance_from_left, 310], align="left")
        self.text8 = TextBox("on each side, and the game will continue. In this case as well, ",
                                 [self.distance_from_left, 345], align="left")
        self.text9 = TextBox("the number of circles or crosses in a line required to win increases",
                                 [self.distance_from_left, 380], align="left")
        self.text10 = TextBox("by one. So, the game won't end until someone wins.", [self.distance_from_left, 415], align="left")

        self.text11 = TextBox("Game rules and concept developed by: Anand Srinivasan", [self.distance_from_left, 490], align="left")
        self.text12 = TextBox("Coded by: K V Tuhil", [self.distance_from_left, 530], align="left")

        self.text1_anim = animations.ButtonSlideAnim(self.text1, list(self.text1.pos),
                                                           [self.text1.pos[0] + 800, self.text1.pos[1]])
        self.text2_anim = animations.ButtonSlideAnim(self.text2, list(self.text2.pos),
                                                     [self.text2.pos[0] - 800, self.text2.pos[1]])
        self.text3_anim = animations.ButtonSlideAnim(self.text3, list(self.text3.pos),
                                                     [self.text3.pos[0] + 800, self.text3.pos[1]])
        self.text4_anim = animations.ButtonSlideAnim(self.text4, list(self.text4.pos),
                                                     [self.text4.pos[0] - 800, self.text4.pos[1]])
        self.text5_anim = animations.ButtonSlideAnim(self.text5, list(self.text5.pos),
                                                     [self.text5.pos[0] + 800, self.text5.pos[1]])
        self.text6_anim = animations.ButtonSlideAnim(self.text6, list(self.text6.pos),
                                                     [self.text6.pos[0] - 800, self.text6.pos[1]])
        self.text7_anim = animations.ButtonSlideAnim(self.text7, list(self.text7.pos),
                                                     [self.text7.pos[0] + 800, self.text7.pos[1]])
        self.text8_anim = animations.ButtonSlideAnim(self.text8, list(self.text8.pos),
                                                     [self.text8.pos[0] - 800, self.text8.pos[1]])
        self.text9_anim = animations.ButtonSlideAnim(self.text9, list(self.text9.pos),
                                                     [self.text9.pos[0] + 800, self.text9.pos[1]])
        self.text10_anim = animations.ButtonSlideAnim(self.text10, list(self.text10.pos),
                                                     [self.text10.pos[0] - 800, self.text10.pos[1]])
        self.text11_anim = animations.ButtonSlideAnim(self.text11, list(self.text11.pos),
                                                     [self.text11.pos[0] + 800, self.text11.pos[1]])
        self.text12_anim = animations.ButtonSlideAnim(self.text12, list(self.text12.pos),
                                                     [self.text12.pos[0] - 800, self.text12.pos[1]])

    def draw(self):
        self.backButton.draw(screen)
        self.text1.draw_and_update()
        self.text2.draw_and_update()
        self.text3.draw_and_update()
        self.text4.draw_and_update()
        self.text5.draw_and_update()
        self.text6.draw_and_update()
        self.text7.draw_and_update()
        self.text8.draw_and_update()
        self.text9.draw_and_update()
        self.text10.draw_and_update()
        self.text11.draw_and_update()
        self.text12.draw_and_update()

        self.text1_anim.update()
        self.text2_anim.update()
        self.text3_anim.update()
        self.text4_anim.update()
        self.text5_anim.update()
        self.text6_anim.update()
        self.text7_anim.update()
        self.text8_anim.update()
        self.text9_anim.update()
        self.text10_anim.update()
        self.text11_anim.update()
        self.text12_anim.update()

        self.back_button_anim.update()


game = None
class GameSelector:
    def __init__(self):
        self.font = pygame.font.Font("data\\freesansbold.ttf", 30)
        self.backButtonDimensions = [70, 50]
        self.offline_button = Button(20, [0, 0, 0], [200, 200, 50], [220, 220, 100], [255, 255, 150], [200, 320], 100, 50, "set_game_mode_to_offline()", text="offline")
        self.online_button = Button(20, [0, 0, 0], [200, 200, 50], [220, 220, 100], [255, 255, 150], [500, 320], 100,
                                     50, "set_game_mode_to_online()", text="online")
        self.join_button = Button(20, [0, 0, 0], [200, 200, 50], [220, 220, 100], [255, 255, 150], [350, 250], 100,
                                     50, "join_game()", text="Join")
        self.create_button = Button(20, [0, 0, 0], [200, 200, 50], [220, 220, 100], [255, 255, 150], [350, 320], 100,
                                  50, "create_game()", text="Create")
        self.backButton = Button(25, (0, 0, 0), (200, 200, 30), (230, 230, 100), (255, 255, 100),
                                 [9 * screen.get_width() / 10 - self.backButtonDimensions[0] / 2,
                                  screen.get_height() / 10 - self.backButtonDimensions[1] / 2],
                                 self.backButtonDimensions[0],
                                 self.backButtonDimensions[1], "go_to_initial_menu()", text="Back")
        self.screen_number = 0
        self.input_box = InputBox([300, 300], 200, 30, [255, 255, 255], default_text="192.168.1.")

        self.offline_button_anim = animations.ButtonSlideAnim(self.offline_button, list(self.offline_button.pos), [self.offline_button.pos[0] - 500, self.offline_button.pos[1]])
        self.online_button_anim = animations.ButtonSlideAnim(self.online_button, list(self.online_button.pos), [self.online_button.pos[0] + 500, self.online_button.pos[1]])
        self.join_button_anim = animations.ButtonSlideAnim(self.join_button, list(self.join_button.pos),
                                                          [self.join_button.pos[0] + 500, self.join_button.pos[1]])
        self.create_button_anim = animations.ButtonSlideAnim(self.create_button, list(self.create_button.pos),
                                                          [self.create_button.pos[0] - 500, self.create_button.pos[1]])
        self.backButton_anim = animations.ButtonSlideAnim(self.backButton, list(self.backButton.pos),
                                                          [self.
                                                          backButton.pos[0] + 200, self.backButton.pos[1]])

    def update_and_draw(self):
        global game_state
        global game
        global host
        global client_ip
        screen.fill((30, 30, 30))
        self.screen_number = screen_number
        if self.screen_number == 0:
            text = self.font.render("Would you like to play online or offline?", True, [255, 255, 255])
            screen.blit(text, [screen_width/2 - text.get_width()/2, 200])
            self.offline_button.draw(screen)
            self.online_button.draw(screen)

            self.offline_button_anim.update()
            self.online_button_anim.update()
        elif self.screen_number == 1:
            text = self.font.render("Would you like to join a game or create one?", True, [255, 255, 255])
            screen.blit(text, [screen_width / 2 - text.get_width() / 2, 200])
            self.create_button.draw(screen)
            self.join_button.draw(screen)
            self.backButton.draw(screen)

            self.create_button_anim.update()
            self.join_button_anim.update()
            self.backButton_anim.update()
        elif self.screen_number == 2:
            text1 = self.font.render("Creating game...", True, [255, 255, 255])
            text2 = self.font.render(f"The ipv4 address of this game is {socket.gethostbyname(socket.gethostname())}", True, [255, 255, 255])
            text3 = self.font.render("The other player must enter this address to join", True, [255, 255, 255])
            text4 = self.font.render("Waiting for player 2 to join..", True, [255, 255, 255])
            screen.blit(text1, [screen_width / 2 - text1.get_width() / 2, 100])
            screen.blit(text2, [screen_width / 2 - text2.get_width() / 2, 190])
            screen.blit(text3, [screen_width / 2 - text3.get_width() / 2, 280])
            screen.blit(text4, [screen_width / 2 - text4.get_width() / 2, 370])
            pygame.display.update()
            receive_file("server_data\\received.bin")
            host = client_ip
            game = TicTac2_server()
            thread = threading.Thread(target=game.look_for_messages)
            thread.start()
            go_to_menu()
        elif self.screen_number == 3:
            self.backButton.draw(screen)
            self.backButton_anim.update()
            text = self.font.render("Enter the IpV4 address of the game and press enter", True, [255, 255, 255])
            text2 = self.font.render("Joining..", True, [255, 255, 255])
            screen.blit(text, [screen_width / 2 - text.get_width() / 2, 200])
            self.input_box.draw()
            self.input_box.update()
            if host is not None:
                data_file = open("client_data\\data_file.bin", "wb")
                data = [[0, 0], 0]
                pickle.dump(data, data_file)
                data_file.close()

                screen.blit(text2, [screen_width / 2 - text.get_width() / 2, 400])
                send_file("client_data\\data_file.bin", host, 5001)
                go_to_menu()
                game = TicTac2_client()
                thread = threading.Thread(target=game.look_for_messages)
                thread.start()
        elif screen_number == 4:
            game = TicTac2()
            go_to_menu()


class ScoreBoard:
    def __init__(self, screen, bkColor, textColor, position, width, height):
        self.height = height
        self.width = width
        self.position = position
        self.pos = self.position
        self.textColor = textColor
        self.screen = screen
        self.bkColor = bkColor
        self.font = pygame.font.Font('data\\freesansbold.ttf', 20)
        self.scoreBoardText = self.font.render("Score Board", True, self.textColor)
        self.player1 = self.font.render("Player 1:", True, self.textColor)
        self.player2 = self.font.render("Player 2:", True, self.textColor)
        self.score1 = self.font.render(str(player1Score), True, self.textColor)
        self.score2 = self.font.render(str(player2Score), True, self.textColor)
        self.clearButton = Button(10, (255, 100, 90), (230, 230, 50), (250, 250, 70), (255, 255, 110), [self.position[0] + self.width - 50, self.position[1] + 5], 40, 20, "clearScores()", text=clearButtonText)

    def draw(self):
        self.clearButton.pos = [self.position[0] + self.width - 50, self.position[1] + 5]
        self.position = self.pos
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
        self.clearButton.draw(self.screen)

    def update(self):
        global clearButtonText
        global player1Score
        global player2Score
        self.score1 = self.font.render(str(player1Score), True, self.textColor)
        self.score2 = self.font.render(str(player2Score), True, self.textColor)
        self.clearButton.text = clearButtonText


screen_width = 800
screen_height = 600

pygame.init()

icon = pygame.image.load("data\\Tic_tac_2_icon2.png")
pygame.display.set_caption("Tic Tac 2.0")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((screen_width, screen_height))

menu = Menu()
game_selector = GameSelector()
how_to_play = HowToPlay()

go_to_initial_menu()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == "how_to_play":
        screen.fill((30, 30, 30))
        how_to_play.draw()

    if game_state == "game_select":
        game_selector.update_and_draw()

    if game_state == "menu":
        screen.fill((30, 30, 30))
        menu.draw()

    if game_state == "game":
        if game.player == 1:
            screen.fill(PLAYER1_COLOR)
        elif game.player == 2:
            screen.fill(PLAYER2_COLOR)
        pygame.draw.rect(screen, (10, 10, 10), [7, 7, screen_width - 14, screen_height - 14])
        game.draw()
        game.update()

    pygame.display.update()
pygame.quit()

score_file = open("data\\scores.txt", "w")
score_file.write(str(player1Score) + "\n" + str(player2Score))
score_file.close()

exit()
