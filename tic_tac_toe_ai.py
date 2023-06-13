import pickle
import random
import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

GRID_COLOR = [252, 186, 3]
PLAYER1_COLOR = [3, 157, 252]
PLAYER2_COLOR = [252, 49, 3]


class Square:
    def __init__(self, pos, state=0, width=60):
        self.pos = pos
        self.state = state
        self.width = width
        self.colors = [PLAYER2_COLOR, PLAYER1_COLOR]
        self.pressed = False
        self.balck = [0, 0, 0]
        self.grey = [30, 30, 30]
        self.light_grey = [50, 50, 50]
        self.background_color = self.balck

        self.color = self.colors[self.state - 1]

    def draw(self):
        self.update()
        pygame.draw.rect(screen, self.background_color, [self.pos[0], self.pos[1], self.width, self.width])
        self.color = self.colors[self.state - 1]
        if self.state == 2:
            pygame.draw.circle(screen, self.color, [int(self.pos[0] + self.width / 2), int(self.pos[1] + self.width / 2)],
                               int(self.width * 0.8 / 2))
            pygame.draw.circle(screen, self.background_color, [int(self.pos[0] + self.width / 2), int(self.pos[1] + self.width / 2)],
                               int(self.width * 0.7 / 2))
        elif self.state == 1:
            pygame.draw.line(screen, self.color, [int(self.pos[0] + self.width * 0.1), int(self.pos[1] + self.width * 0.1)],
                             [int(self.pos[0] + self.width * 0.9), int(self.pos[1] + self.width * 0.9)], int(self.width * 0.05))
            pygame.draw.line(screen, self.color, [int(self.pos[0] + self.width * 0.1), int(self.pos[1] + self.width * 0.9)],
                             [int(self.pos[0] + self.width * 0.9), int(self.pos[1] + self.width * 0.1)], int(self.width * 0.05))
        else:
            pass
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_pos[0] < self.pos[0] + self.width and self.pos[1] < mouse_pos[1] < self.pos[1] + self.width:
            if pygame.mouse.get_pressed()[0]:
                self.background_color = self.light_grey
            else:
                self.background_color = self.grey
        else:
            self.background_color = self.balck


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
            font = pygame.font.Font('pygames/freesansbold.ttf', self.fontSize)
            text = font.render(self.text, True, self.textColor)
            win.blit(text, (
            int(self.x + (self.width / 2 - text.get_width() / 2)), int(self.y + (self.height / 2 - text.get_height() / 2))))

        if self.onCLick != "":
            if self.isOver(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    if not self.clicked:
                        self.clicked = True
                        self.color = self.colorWhenClicked
                        self.onCLick()
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


class Node:
    def __init__(self, turn, grid_str="000000000"):
        self.turn = turn
        self.grid_str = grid_str
        self.next_nodes = []
        self.score = 0
        self.can_win = False

    def make_grid(self):
        grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(3):
            for j in range(3):
                grid[i][j] = int(self.grid_str[3*i + j])
        return grid

    def check_won(self, grid):
        has_won = 0
        for i in range(3):
            if grid[i][0] == grid[i][1] == grid[i][2] and not has_won:
                has_won = grid[i][0]
            if grid[0][i] == grid[1][i] == grid[2][i] and not has_won:
                has_won = grid[0][i]
        if grid[0][0] == grid[1][1] == grid[2][2] and not has_won:
            has_won = grid[0][0]
        if grid[0][2] == grid[1][1] == grid[2][0] and not has_won:
            has_won = grid[0][2]
        return has_won

    def __str__(self):
        grid_str = self.grid_str
        grid_str = grid_str.replace("2", "O")
        grid_str = grid_str.replace("1", "X")
        grid_str = grid_str.replace("0", "*")
        return grid_str[0:3:] + "\n" + grid_str[3:6:] + "\n" + grid_str[6::] + "\n"


def make_grid_str(grid):
    grid_str = ""
    for i in range(3):
        for j in range(3):
            grid_str += str(grid[i][j])
    return grid_str


def make_tree(node):
    current_grid = node.make_grid()
    current_turn = node.turn
    won = node.check_won(current_grid)
    next_turn = (current_turn % 2) + 1
    if won == 0:
        for i in range(3):
            for j in range(3):
                if not current_grid[i][j]:
                    next_grid = node.make_grid()
                    next_grid[i][j] = next_turn
                    next_node = Node(next_turn, grid_str=make_grid_str(next_grid))
                    #print(next_node)
                    node.next_nodes.append(next_node)

    for next_node1 in node.next_nodes:
        make_tree(next_node1)
    if won == 2:
        node.score = 1
        node.can_win = True
    elif won == 1:
        node.score = -1
        node.can_win = True
    elif len(node.next_nodes) == 0:
        node.score = 0
    else:
        can_win = True
        for next_node2 in node.next_nodes:
            node.score += next_node2.score
        for next_node2 in node.next_nodes:
            if len(next_node2.next_nodes) == 0 or next_node2.can_win:
                can_win = False
                break
            has_a_win = False
            for next_next_node in next_node2.next_nodes:
                if next_next_node.can_win:
                    has_a_win = True
                    break
            if not has_a_win:
                can_win = False
                break
        node.can_win = can_win


root_node = Node(1)
#make_tree(root_node)


try:
    tree_file = open("treefile.bin", "rb")
    root_node = pickle.load(tree_file)
    tree_file.close()
except FileNotFoundError:
    make_tree(root_node)

    tree_file = open("treefile.bin", "wb")
    pickle.dump(root_node, tree_file)
    tree_file.close()

current_node = root_node

starts = random.choice([1, 2])
#starts = 1

print("Start!")
first_turn = True

class TicTacToe:
    def __init__(self):
        self.grid = []
        self.squares = []
        self.square_width = 100
        self.pos = [SCREEN_WIDTH / 2 - 1.5*self.square_width, SCREEN_HEIGHT / 2 - 1.5*self.square_width]
        self.color = GRID_COLOR
        self.mouse_pressed = 0
        self.won = False
        self.player = 2
        self.ai_player = starts
        self.won_time = 0
        self.winning_player = 0
        font = pygame.font.Font("pygames/freesansbold.ttf", 60)
        self.ai_won_text = font.render("I Won!!", True, (255, 255, 255))
        self.player_won_text = font.render("You Won!!", True, (255, 255, 255))
        self.draw_text = font.render("It's a draw!!", True, (255, 255, 255))
        self.retry_button = Button(30, (255, 255, 255), (50, 50, 50), (120, 120, 120), (230, 230, 230), [SCREEN_WIDTH / 2 - 100, 500], 200, 70, self.reset, text="Play again")
        for i in range(3):
            row = []
            val_row = []
            for j in range(3):
                row.append(Square([self.pos[0] + j*self.square_width, self.pos[1] + i*self.square_width], width=self.square_width))
                val_row.append(0)
            self.squares.append(row)
            self.grid.append(val_row)

    def draw(self):
        for row in self.squares:
            for square in row:
                square.draw()
        for i in range(1, 3):
            pygame.draw.line(screen, self.color,
                             [int(self.pos[0] + self.square_width * i), int(self.pos[1])],
                             [int(self.pos[0] + self.square_width * i), int(self.pos[1] + self.square_width * 3)],
                             int(self.square_width * 0.05))
        for i in range(1, 3):
            pygame.draw.line(screen, self.color,
                             [int(self.pos[0]), int(self.pos[1] + self.square_width * i)],
                             [int(self.pos[0] + self.square_width * 3), int(self.pos[1] + self.square_width * i)],
                             int(self.square_width * 0.05))

        if self.won:
            self.retry_button.draw(screen)
            if self.winning_player == 0:
                screen.blit(self.draw_text, [SCREEN_WIDTH/2 - self.draw_text.get_width()/2, 10])
            elif self.winning_player == self.ai_player:
                screen.blit(self.ai_won_text, [SCREEN_WIDTH/2 - self.ai_won_text.get_width()/2, 10])
            else:
                screen.blit(self.player_won_text, [SCREEN_WIDTH/2 - self.player_won_text.get_width()/2, 10])

    def update(self):
        global current_node
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if mouse_pressed - self.mouse_pressed == 1 and self.player != self.ai_player:
            self.mouse_pressed = 1
            if mouse_pressed:
                if self.pos[0] < mouse_pos[0] < self.pos[0] + self.square_width * 3 and self.pos[1] < \
                        mouse_pos[1] < self.pos[1] + self.square_width * 3:
                    column = int((mouse_pos[0] - self.pos[0]) / self.square_width)
                    row = int((mouse_pos[1] - self.pos[1]) / self.square_width)
                    if not self.squares[row][column].pressed and not self.won:
                        self.squares[row][column].pressed = True
                        self.grid[row][column] = self.player
                        self.player = self.ai_player

                        current_grid_str = make_grid_str(self.grid)

                        for node in current_node.next_nodes:
                            if node.grid_str == current_grid_str:
                                current_node = node
                                break
                        print(current_node)
                        won = current_node.check_won(self.grid)
                        self.winning_player = won
                        if won == 1:
                            print("You won!")
                            self.won = True
                        elif won == 2:
                            print("I won!")
                            self.won = True
                        if check_draw(self.grid):
                            print("It's a draw!")
                            self.won = True
        elif mouse_pressed - self.mouse_pressed == -1:
            self.mouse_pressed = 0

        for i in range(3):
            for j in range(3):
                self.squares[i][j].state = self.grid[i][j]
                self.squares[i][j].pressed = self.grid[i][j] != 0

        if self.player == self.ai_player and not self.won:
            self.won = self.update_ai()
            self.player = (self.ai_player % 2) + 1
        for i in range(3):
            for j in range(3):
                self.squares[i][j].state = self.grid[i][j]
                self.squares[i][j].pressed = self.grid[i][j] != 0

    def reset(self):
        global current_node
        global root_node
        global starts
        global first_turn
        first_turn = True
        self.grid = []
        self.squares = []
        for i in range(3):
            row = []
            val_row = []
            for j in range(3):
                row.append(Square([self.pos[0] + j*self.square_width, self.pos[1] + i*self.square_width], width=self.square_width))
                val_row.append(0)
            self.squares.append(row)
            self.grid.append(val_row)
        current_node = root_node
        starts = (starts % 2) + 1
        #starts = random.choice([1, 2])
        self.ai_player = starts
        self.player = 2
        self.won = False
        self.winning_player = 0

    def update_ai(self):
        global current_node
        global first_turn
        #current_grid = self.grid
        if starts == 2:
            max_score = -1000000
            max_score_node = current_node.next_nodes[0]

            possible_nodes = []
            for node in current_node.next_nodes:
                # if node.check_won(node.make_grid()):
                #     max_score_node = node
                #     break
                # print(node.score, node.can_win, end=" ")
                next_can_win = False
                for next_node in node.next_nodes:
                    # print(next_node.can_win)
                    if next_node.can_win:
                        next_can_win = True
                        break
                wins = False
                for next_node in node.next_nodes:
                    for next_next_node2 in next_node.next_nodes:
                        if next_next_node2.check_won(next_next_node2.make_grid()):
                            wins = True
                            break
                if not wins and not next_can_win:
                    possible_nodes.append(node)
                elif node.score > max_score and not next_can_win:
                    # print(max_score)
                    max_score = node.score
                    max_score_node = node
            if len(possible_nodes) != 0:
                max_score_node = random.choice(possible_nodes)
            for node in current_node.next_nodes:
                if node.can_win:
                    max_score_node = node
            if first_turn:
                max_score_node = current_node.next_nodes[4]
                if random.random() < 0.6:
                    max_score_node = random.choice(current_node.next_nodes)
                first_turn = False

            current_node = max_score_node
            print(current_node)
            self.grid = current_node.make_grid()

            won = current_node.check_won(self.grid)
            self.winning_player = won
            if won == 1:
                print("You won!")
                return True
            elif won == 2:
                print("I won!")
                return True
            if check_draw(self.grid):
                print("It's a draw!")
                return True
        else:
            min_score = 1000000
            min_score_node = current_node.next_nodes[0]
            possible_nodes = []
            for node in current_node.next_nodes:
                # if node.check_won(node.make_grid()):
                #     max_score_node = node
                #     break
                next_can_win = False
                for next_node in node.next_nodes:
                    # print(next_node.can_win)
                    if next_node.can_win:
                        next_can_win = True
                        break
                wins = False
                for next_node in node.next_nodes:
                    for next_next_node2 in next_node.next_nodes:
                        if next_next_node2.check_won(next_next_node2.make_grid()):
                            wins = True
                            break
                if not wins and not next_can_win:
                    possible_nodes.append(node)
                elif node.score < min_score and not next_can_win:
                    # print(max_score)
                    min_score = node.score
                    min_score_node = node
            if len(possible_nodes) != 0:
                min_score_node = random.choice(possible_nodes)
            for node in current_node.next_nodes:
                if node.can_win:
                    min_score_node = node

            current_node = min_score_node
            print(current_node)
            self.grid = current_node.make_grid()

            won = current_node.check_won(self.grid)
            self.winning_player = won
            if won == 2:
                print("You won!")
                return True
            elif won == 1:
                print("I won!")
                return True
            if check_draw(self.grid):
                print("It's a draw!")
                return True


def check_draw(grid):
    is_draw = True
    for i in range(3):
        for j in range(3):
            if not grid[i][j]:
                is_draw = False
                break
    return is_draw


game = TicTacToe()

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    game.draw()
    game.update()
    pygame.display.update()