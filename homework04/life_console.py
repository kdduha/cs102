import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.subwin(self.life.rows + 2, self.life.cols + 2, 0, 0).box("|", "=")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j]:
                    screen.addstr(1 + i, 1 + j, "█")
                else:
                    screen.addstr(1 + i, 1 + j, " ")

    def run(self) -> None:
        screen = curses.initscr()
        curses.noecho()
        self.draw_borders(screen)
        self.draw_grid(screen)
        screen.refresh()
        UI.run(self)

        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            self.life.step()
            self.draw_grid(screen)
            screen.refresh()
            UI.run(self)

        curses.endwin()
