import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.height = self.life.rows * self.cell_size
        self.width = self.life.cols * self.cell_size

        # Устанавливаем размер окна
        self.screen_size = self.width, self.height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                color = "green" if self.life.curr_generation[i][j] == 1 else "white"
                coords = (j * self.cell_size + 1, i * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1)
                pygame.draw.rect(self.screen, color, coords)

    def run(self) -> None:
        # Copy from previous assignment

        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        self.draw_lines()

        running = True
        pause = True
        press_mouse = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN and event.key == K_SPACE:
                    pause = not pause

                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    button_j, button_i = event.pos
                    i, j = (button_i - 1) // self.cell_size, (button_j - 1) // self.cell_size
                    self.life.curr_generation = self.life.prev_generation
                    self.life.curr_generation[i][j] = 1 if press_mouse else 0
                    self.draw_grid()
                    self.life.step()

            if not pause and self.life.is_changing and not self.life.is_max_generations_exceeded:
                self.draw_grid()
                self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


life = GameOfLife((24, 80))
GUI(life).run()
