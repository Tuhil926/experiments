import pygame
import time

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class ConwayGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grids = []
        grid = []
        for i in range(self.height):
            grid.append([0 for x in range(self.width)])
        self.grids.append(grid)
        self.current_grid = 0
        self.new_grid = []
        for i in range(self.height):
            self.new_grid.append([0 for x in range(self.width)])
        self.SURVIVES = (2, )
        self.GETS_CREATED = (3, )
        self.DIES = (1, 4, 5, 6, 7, 8)

        self.running_speed = 50
        self.prev_time = time.time_ns()

        self.mouse_pressed = 0
        self.step_key_pressed = 0
        self.prev_step_key_pressed = 0
        self.run_key_pressed = 0
        self.clear_key_pressed = 0

        self.undo_limit = 100

    def update(self):
        new_grid = []
        grid_is_empty = True
        for i in range(self.height):
            new_grid.append([0 for x in range(self.width)])
        for i in range(self.height):
            down = i + 1
            if down >= self.height:
                down -= self.height
            up = i - 1
            for j in range(self.width):
                left = j - 1
                right = j + 1
                if right >= self.width:
                    right -= self.width

                number_of_surrounding_cells = 0

                if self.grids[self.current_grid][up][left]:
                    number_of_surrounding_cells += 1
                if self.grids[self.current_grid][i][left]:
                    number_of_surrounding_cells += 1
                if self.grids[self.current_grid][down][left]:
                    number_of_surrounding_cells += 1
                if self.grids[self.current_grid][down][j]:
                    number_of_surrounding_cells += 1
                if self.grids[self.current_grid][down][right]:
                    number_of_surrounding_cells += 1
                if self.grids[self.current_grid][i][right]:
                    number_of_surrounding_cells += 1
                if self.grids[self.current_grid][up][right]:
                    number_of_surrounding_cells += 1
                if self.grids[self.current_grid][up][j]:
                    number_of_surrounding_cells += 1

                if number_of_surrounding_cells in self.SURVIVES:
                    new_grid[i][j] = self.grids[self.current_grid][i][j]
                elif number_of_surrounding_cells in self.GETS_CREATED:
                    new_grid[i][j] = 1
                elif number_of_surrounding_cells in self.DIES:
                    new_grid[i][j] = 0

                if number_of_surrounding_cells != 0:
                    grid_is_empty = False
        if not grid_is_empty:
            self.grids.append(new_grid)
            self.current_grid += 1

            if len(self.grids) >= self.undo_limit:
                del self.grids[0]
                self.current_grid -= 1
        #for i in range(self.height):
        #    for j in range(self.width):
        #        self.grid[i][j] = self.new_grid[i][j]

    def render(self, screen):
        cell_width = SCREEN_WIDTH/self.width
        cell_height = SCREEN_HEIGHT/self.height
        for i in range(self.height):
            for j in range(self.width):
                if self.grids[self.current_grid][i][j]:
                    pygame.draw.rect(screen, (255, 255, 255), (j * cell_width + 1, i * cell_height + 1, cell_width - 2, cell_height - 2))
                else:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (j * cell_width + 1, i * cell_height + 1, cell_width - 2, cell_height - 2))

    def mouse_input(self):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[2]:
            self.grids[self.current_grid][int(mouse_pos[1] * self.height/SCREEN_HEIGHT)][int(mouse_pos[0] * self.width/SCREEN_WIDTH)] = 1
        elif pygame.mouse.get_pressed()[0]:
            self.grids[self.current_grid][int(mouse_pos[1] * self.height / SCREEN_HEIGHT)][
                int(mouse_pos[0] * self.width / SCREEN_WIDTH)] = 0
    
    def keyboard_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] and not self.step_key_pressed:
            self.update()
            self.step_key_pressed = 1
        if not keys[pygame.K_s]:
            self.step_key_pressed = 0

        if keys[pygame.K_z] and not self.prev_step_key_pressed:
            if self.current_grid > 0:
                del self.grids[-1]
                self.current_grid -= 1
            self.prev_step_key_pressed = 1
        if not keys[pygame.K_z]:
            self.prev_step_key_pressed = 0

        if keys[pygame.K_c] and not self.clear_key_pressed:
            new_grid = []
            for i in range(self.height):
                new_grid.append([0 for x in range(self.width)])
            self.grids.append(new_grid)
            self.current_grid += 1
            self.clear_key_pressed = 1
        if not keys[pygame.K_c]:
            self.clear_key_pressed = 0

        if keys[pygame.K_r]:
            if (time.time_ns() - self.prev_time) / 1000000000 > (1 / self.running_speed):
                self.update()
                self.prev_time = time.time_ns()


def update_conway_grid(current_grid):
    SURVIVES = (2,)
    GETS_CREATED = (3,)
    DIES = (1, 4, 5, 6, 7, 8)
    height = len(current_grid)
    width = len(current_grid[0])
    new_grid = []
    for i in range(height):
        new_grid.append([0 for x in range(width)])
    for i in range(height):
        down = i + 1
        if down >= height:
            down -= height
        up = i - 1
        for j in range(width):
            left = j - 1
            right = j + 1
            if right >= width:
                right -= width

            number_of_surrounding_cells = 0

            if current_grid[up][left]:
                number_of_surrounding_cells += 1
            if current_grid[i][left]:
                number_of_surrounding_cells += 1
            if current_grid[down][left]:
                number_of_surrounding_cells += 1
            if current_grid[down][j]:
                number_of_surrounding_cells += 1
            if current_grid[down][right]:
                number_of_surrounding_cells += 1
            if current_grid[i][right]:
                number_of_surrounding_cells += 1
            if current_grid[up][right]:
                number_of_surrounding_cells += 1
            if current_grid[up][j]:
                number_of_surrounding_cells += 1

            if number_of_surrounding_cells in SURVIVES:
                new_grid[i][j] = current_grid[i][j]
            elif number_of_surrounding_cells in GETS_CREATED:
                new_grid[i][j] = 1
            elif number_of_surrounding_cells in DIES:
                new_grid[i][j] = 0

    return new_grid


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Conway's Game Of Life")

conway_grid = ConwayGrid(32, 24)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((50, 50, 50))

    conway_grid.mouse_input()
    conway_grid.keyboard_input()
    conway_grid.render(screen)

    pygame.display.update()
