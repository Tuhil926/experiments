import pygame
import threading
import time
import socket
import os
import pickle


row_count = 3
column_count = 3
req_to_win = 3

GRID_COLOR = [252, 186, 3]
PLAYER1_COLOR = [3, 157, 252]
PLAYER2_COLOR = [252, 49, 3]

game_state = "pos"

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024*4

client_ip = None
host = None


def send_file(filename, host, port):
    # get the file size
    filesize = os.path.getsize(filename)
    # create the client socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    #print("[+] Connected.")

    # send the filename and filesize
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

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
    received = client_socket.recv(BUFFER_SIZE).decode()
    rec_filename, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    # convert to integer
    filesize = int(filesize)
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


def go_to_menu():
    global game_state
    game_state = "pos"


def go_to_settings():
    global game_state
    game_state = "settings"


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


class button:
    def __init__(self,fontSize, textColor, color, colorWhenMouseOver, colorWhenClicked, pos, width, height, onClick, text=''):
        self.color = color
        self.fontSize = fontSize
        self.textColor = textColor
        self.defaultColor = color
        self.colorWhenMouseOver = colorWhenMouseOver
        self.colorWhenClicked = colorWhenClicked
        self.x = pos[0]
        self.y = pos[1]
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
        self.button = button(self.fontSize, self.textColor, self.color, self.colorWhenMouseOver, self.colorWhenClicked, [self.x, self.y], self.width, self.height, "", text=self.selections[self.selected])
        self.right = button(self.fontSize, self.textColor, self.color, self.colorWhenMouseOver, self.colorWhenClicked, [self.x + self.width, self.y], self.height, self.height, "", text=">")
        self.left = button(self.fontSize, self.textColor, self.color, self.colorWhenMouseOver, self.colorWhenClicked,
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


class TicTac2_server:
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

        inp_file = open("server_data/received.bin", "wb")
        inp_file.write(b"")
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
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        self.check_if_won()

        if self.player == 1:
            self.check_if_clicked(mouse_pressed, mouse_pos)
        else:
            try:
                inp_file = open("server_data/received.bin", "rb")
                data = pickle.load(inp_file)
                print(data)
                self.check_if_clicked(data[1], data[0])
                inp_file.close()
                #inp_file = open("server_data/received.bin", "wb")
                #inp_file.write(b"")
                #inp_file.close()
            except EOFError:
                print("file empty")

        for i in range(self.row_count):
            for j in range(self.column_count):
                self.pos = [screen_width / 2 - self.column_count * self.square_width / 2,
                            screen_height / 2 - self.row_count * self.square_width / 2]
                self.squares[i][j].state = self.square_values[i][j]
                self.squares[i][j].pos = [self.pos[0] + j * self.square_width, self.pos[1] + i * self.square_width]

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
        self.mouse_pressed = True
        go_to_menu()

    def win(self, player, start_pos_of_line, end_pos_of_line):
        if not self.won:
            self.won = True
            print(f"Player {player} Won!")
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

    def check_if_clicked(self, mouse_pressed, mouse_pos):
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
            #thread = threading.Thread(target=self.send_data)
            #thread.start()

    def send_data(self):
        data_file = open("server_data/data_file.bin", "wb")
        data = [self.squares, self.square_values]
        pickle.dump(data, data_file)
        data_file.close()
        send_file("server_data/data_file.bin", client_ip, 5001)

    def look_for_messages(self):
        global running
        global client_ip
        global host
        while running:
            receive_file("server_data/received.bin")
            host = client_ip


class TicTac2_client:
    def __init__(self):
        self.mouse_pressed = True
        self.player = 1
        self.color = GRID_COLOR
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
        inp_file = open("server_data/received.bin", "wb")
        inp_file.write(b"")
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
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if mouse_pressed - self.mouse_pressed == 1:
            data = [mouse_pos, mouse_pressed]
            thread = threading.Thread(target=self.send_data, args=(data,))
            thread.start()

        for i in range(self.row_count):
            for j in range(self.column_count):
                self.pos = [screen_width / 2 - self.column_count * self.square_width / 2,
                            screen_height / 2 - self.row_count * self.square_width / 2]
                self.squares[i][j].state = self.square_values[i][j]
                self.squares[i][j].pos = [self.pos[0] + j * self.square_width, self.pos[1] + i * self.square_width]

        if self.row_count*self.square_width > screen_height - 10 or self.column_count * self.square_width > screen_width - 10:
            self.square_width *= 0.9

        try:
            recv_file = open("client_data/received.bin", "rb")
            data = pickle.load(recv_file)
            self.squares = data[0]
            self.square_values = data[1]
            recv_file.close()
        except EOFError:
            pass

        self.mouse_pressed = mouse_pressed

    def send_data(self, data):
        data_file = open("client_data/data_file.bin", "wb")
        pickle.dump(data, data_file)
        data_file.close()
        send_file("client_data/data_file.bin", host, 5001)

    def look_for_messages(self):
        global running
        global client_ip
        global host
        while running:
            receive_file("client_data/received.bin")
            host = client_ip


class Menu:
    def __init__(self):
        self.screen = screen
        self.font = pygame.font.Font('data/freesansbold.ttf', 150)
        self.playButtonDimensions = [90, 50]
        self.settingsButtonDimensions = [100, 40]
        self.playbutton = button(30, (125, 255, 100), (70, 200, 60), (90, 230, 80), (110, 255, 100),
                                 [self.screen.get_width() / 2 - self.playButtonDimensions[0] / 2,
                                 2 * self.screen.get_height() / 3], self.playButtonDimensions[0],
                                 self.playButtonDimensions[1], "go_to_game()", text="PLAY")
        self.settingsButton = button(20, (50, 50, 50), (220, 220, 60), (250, 250, 100), (255, 255, 100),
                                     [self.screen.get_width() / 10 - self.settingsButtonDimensions[0] / 2,
                                     self.screen.get_height() / 10 - self.settingsButtonDimensions[1] / 2],
                                     self.settingsButtonDimensions[0],
                                     self.settingsButtonDimensions[1], "go_to_settings()", text="Settings")

    def draw(self):
        self.playbutton.draw(screen)
        self.settingsButton.draw(screen)
        text = self.font.render("Tic Tac 2.0", True, [255, 50, 0])
        screen.blit(text, (
            int(screen_width / 2 - text.get_width() / 2),
            int(screen_height / 2 - text.get_height() / 2)))


class Settings:
    def __init__(self):
        self.screen = screen
        self.backButtonDimensions = [70, 50]
        self.backButton = button(25, (255, 255, 255), (230, 230, 50), (240, 240, 70), (255, 255, 100),
                                 [9 * self.screen.get_width() / 10 - self.backButtonDimensions[0] / 2,
                                 self.screen.get_height() / 10 - self.backButtonDimensions[1] / 2],
                                 self.backButtonDimensions[0],
                                 self.backButtonDimensions[1], "go_to_menu()", text="Back")
        self.gameModeSelector = Selection(self.screen, 20, (50, 50, 50), (230, 230, 50), (250, 250, 60),
                                          (255, 255, 110), [self.screen.get_width() / 2 - 70,
                                          self.screen.get_height() / 3], 140, 50, ["Offline", "LAN game"], 0)

    def draw(self):
        self.backButton.draw(screen)
        self.gameModeSelector.draw()

    def update(self):
        self.gameModeSelector.update()


mode = input("Would you like to join a game or create one?(j/c): ")
if mode == "j":
    host = input("enter the ipv4 of the server: ")
else:
    print(f"Creating Game... \nThe ipv4 address of this game is {socket.gethostbyname(socket.gethostname())}. The other player must enter this address to join\nWaiting For Player 2 to join...")
    receive_file("/server_data/received.bin")

    host = client_ip


screen_width = 800
screen_height = 600

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))

game = None
menu = Menu()
settings = Settings()

running = True

if mode == "c":
    game = TicTac2_server()

elif mode == "j":
    game = TicTac2_client()

thread = threading.Thread(target=game.look_for_messages)
thread.start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == "pos":
        screen.fill((30, 30, 30))
        menu.draw()

    if game_state == "settings":
        screen.fill((30, 30, 30))
        settings.draw()
        settings.update()

    if game_state == "game":
        screen.fill((0, 0, 0))
        game.draw()
        game.update()

    pygame.display.update()
print(running)
pygame.quit()
thread.join()
