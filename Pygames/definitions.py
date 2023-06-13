import math
import pygame

def move_X(angle, distance):
    return math.sin(angle) * distance


def move_Y(angle, distance):
    return math.cos(angle) * distance

#def project(self, point):
#     rel_pos = [point[0] - self.pos[0], point[1] - self.pos[1], point[2] - self.pos[2]]
#     unit_rel_pos = unit_vector(add(unit_vector(rel_pos), self.direction_moving))
#    cos = dot(unit_rel_pos, self.direction_moving)
#    screen_projection = divide(multiply(unit_rel_pos, self.distance), cos)
#    screen_projection_with_centre_at_origin = subtract(screen_projection, self.direction_moving)
#    x = dot(screen_projection_with_centre_at_origin, self.right)
#    y = -dot(screen_projection_with_centre_at_origin, self.rel_up)
#    return [x, y]


"""
        for i in range(3):
            if self.square_values[i][0] == self.square_values[i][1] == self.square_values[i][2] != 0:
                print(f"Player {self.square_values[i][0]} Won!")
                self.won = self.square_values[i][0]
                invoke(self.clear, 1)
            if self.square_values[0][i] == self.square_values[1][i] == self.square_values[2][i] != 0:
                print(f"Player {self.square_values[0][i]} Won!")
                self.won = self.square_values[0][i]
                invoke(self.clear, 1)
        if self.square_values[0][0] == self.square_values[1][1] == self.square_values[2][2] != 0:
            print(f"Player {self.square_values[0][0]} Won!")
            self.won = self.square_values[0][0]
            invoke(self.clear, 1)
        if self.square_values[0][2] == self.square_values[1][1] == self.square_values[2][0] != 0:
            print(f"Player {self.square_values[0][2]} Won!")
            self.won = self.square_values[0][2]
            invoke(self.clear, 1)
"""

class Settings:
    def __init__(self):
        self.screen = screen
        self.backButtonDimensions = [70, 50]
        self.backButton = Button(25, (255, 255, 255), (230, 230, 50), (240, 240, 70), (255, 255, 100),
                                 [9 * self.screen.get_width() / 10 - self.backButtonDimensions[0] / 2,
                                 self.screen.get_height() / 10 - self.backButtonDimensions[1] / 2],
                                 self.backButtonDimensions[0],
                                 self.backButtonDimensions[1], "go_to_menu()", text="Back")
        self.gameModeSelector = Selection(self.screen, 20, (50, 50, 50), (230, 230, 50), (250, 250, 60),
                                          (255, 255, 110), [self.screen.get_width() / 2 - 70,
                                          self.screen.get_height() / 3], 140, 50, ["Offline", "LAN game"], 0)
        self.input_box = InputBox([300, 300], 200, 30, [255, 255, 255], default_text="192.168.1._")

    def draw(self):
        if self.gameModeSelector.selected == 1:
            self.input_box.draw()
        self.backButton.draw(screen)
        self.gameModeSelector.draw()

    def update(self):
        if self.gameModeSelector.selected == 1:
            self.input_box.update()
        self.gameModeSelector.update()


#offline_or_online = input("Would you like to play offline or online?(of/on): ")
#if offline_or_online == "of":
#    game = TicTac2()
#elif offline_or_online == "on":
#    mode = input("Would you like to join a game or create one?(j/c): ")
#    if mode == "j":
#        host = input("enter the ipv4 of the server: ")
#        print("Joining..")
#        send_file("client_data/data_file.bin", host, 5001)
#    else:
#        print(f"Creating Game... \nThe ipv4 address of this game is {socket.gethostbyname(socket.gethostname())}. The other player must enter this address to join\nWaiting For Player 2 to join...")
#        receive_file("/server_data/received.bin")
#        host = client_ip
#    if mode == "c":
#        game = TicTac2_server()

#    elif mode == "j":
#        game = TicTac2_client()

#    thread = threading.Thread(target=game.look_for_messages)
#    thread.start()


pygame.init()
screen = pygame.display.set_mode((800, 600))
img = pygame.image.load("invader.png")
imgX = 400
imgY = 300
angle = 0
angle_chng = 0
# angle = acos(v1•v2), Ax * Bx + Ay * By
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_a:
                angle_chng += 1
            if event.key == pygame.K_d:
                angle_chng -= 1
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
    angle = math.atan2(-mouseY + 300, mouseX - 400)

    rot_img = pygame.transform.rotate(img, (angle * 57.5) - 90)
    screen.blit(rot_img, (imgX - int(rot_img.get_width()/2), imgY - int(rot_img.get_width()/2)))
    pygame.display.update()
print(angle)