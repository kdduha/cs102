from copy import deepcopy
from random import choice, randint
from typing import Any, List, Optional, Tuple, Union

import pandas as pd  # type: ignore


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    row, col = coord
    vector = choice(["up", "right"])
    if row - 1 and col + 1 < len(grid[0]) - 1:
        if vector == "up":
            row -= 1
        else:
            col += 1
    elif row == 1 and col + 1 < len(grid[0]) - 1:
        col += 1
    elif col + 1 == len(grid[0]) - 1 and row - 1:
        row -= 1
    grid[row][col] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for cell in empty_cells:
        grid = remove_wall(grid, cell)

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    coord_exits = []
    for row, elem_1 in enumerate(grid):
        for col, elem_2 in enumerate(elem_1):
            if elem_2 == "X":
                coord_exits.append((row, col))

    return coord_exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    for row, element_1 in enumerate(grid):
        for col, element_2 in enumerate(element_1):
            if grid[row][col] == k:
                if row != 0 and not grid[row - 1][col]:
                    grid[row - 1][col] = k + 1
                if row != len(grid) - 1 and not grid[row + 1][col]:
                    grid[row + 1][col] = k + 1
                if col != 0 and not grid[row][col - 1]:
                    grid[row][col - 1] = k + 1
                if col != len(grid[0]) - 1 and not grid[row][col + 1]:
                    grid[row][col + 1] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[Any, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid_cp:
    :param exit_coord:
    :return:
    """
    grid_cp = deepcopy(grid)
    row, col = exit_coord
    end = grid_cp[row][col]
    k = end
    path = [exit_coord]

    while k > 0:
        if row != 0 and grid_cp[row - 1][col] == k - 1:
            row -= 1
            path.append((row, col))
        elif row != len(grid_cp) - 1 and grid_cp[row + 1][col] == k - 1:
            row += 1
            path.append((row, col))
        elif col != 0 and grid_cp[row][col - 1] == k - 1:
            col -= 1
            path.append((row, col))
        elif col != len(grid_cp[0]) - 1 and grid_cp[row][col + 1] == k - 1:
            col += 1
            path.append((row, col))
        k -= 1

    if len(path) != end:
        last_row, last_col = path[-1]
        grid_cp[last_row][last_col] = " "
        return shortest_path(grid, exit_coord)

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    row, col = coord
    if row in [0, len(grid) - 1] and col in [0, len(grid[0]) - 1]:
        return True
    if (
        row in [0, len(grid) - 1]
        and grid[abs(row - 1)][col] != " "
        or col in [0, len(grid) - 1]
        and grid[row][abs(col - 1)] != " "
    ):
        return True

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    exits = get_exits(grid)
    if len(exits) == 1:
        return grid, exits[0]

    start, finish = exits[0], exits[1]
    if encircled_exit(grid, start) or encircled_exit(grid, finish):
        return grid, None

    for row, element_1 in enumerate(grid):
        for col, element_2 in enumerate(element_1):
            if grid[row][col] == " ":
                grid[row][col] = 0

    grid[start[0]][start[1]] = 1
    grid[finish[0]][finish[1]] = 0
    k = 0

    while grid[finish[0]][finish[1]] == 0:
        k += 1
        grid = make_step(grid, k)

    return grid, shortest_path(grid, finish)


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
