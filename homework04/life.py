import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        grid = [[random.randint(0, int(randomize)) for _ in range(self.cols)] for _ in range(self.rows)]
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        neighbours = []
        row, col = cell
        neigh_index_shifts = [(-1, -1), (-1, 0), (0, -1), (1, 1), (1, 0), (0, 1), (-1, 1), (1, -1)]

        for position in neigh_index_shifts:
            new_row, new_col = row + position[0], col + position[1]
            if new_row < 0 or new_row >= self.rows or new_col < 0 or new_col >= self.cols:
                continue
            neighbours.append(self.curr_generation[new_row][new_col])

        return neighbours

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        next_gen = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i, row in enumerate(self.curr_generation):
            for j, _ in enumerate(row):
                neighbours = sum(self.get_neighbours((i, j)))

                if 2 <= neighbours <= 3:
                    if neighbours == 3 and self.curr_generation[i][j] == 0:
                        next_gen[i][j] = 1
                        continue
                    next_gen[i][j] = self.curr_generation[i][j]
                    continue

                next_gen[i][j] = 0

        return next_gen

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation.copy()
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations  # type: ignore

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return not self.prev_generation == self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as f:
            grid = [list(map(int, row.strip("\n").split())) for row in f.readlines()]
        game = GameOfLife((len(grid), len(grid[0])))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            for row in self.curr_generation:
                f.write(" ".join(map(str, row)) + "\n")
