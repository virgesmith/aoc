from io import StringIO
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def test():
    input = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
    return StringIO(input).read().splitlines()


def live():
    with open("2023/14/input.txt") as fd:
        return fd.read().splitlines()


# direction, axis
N = (1, 0)
E = (-1, 1)
S = (-1, 0)
W = (1, 1)


def roll_n(a: np.ndarray) -> np.ndarray:
    while True:
        d = np.roll(a, 1, axis=0)
        movable = list(zip(*np.where(np.logical_and(a[1:, :] == "O", d[1:, :] == "."))))
        if len(movable) == 0:
            break
        for y, x in movable:
            a[y + 1][x] = "."
            a[y][x] = "O"
    return a


def roll_e(a: np.ndarray) -> np.ndarray:
    while True:
        d = np.roll(a, -1, axis=1)
        movable = list(
            zip(*np.where(np.logical_and(a[:, :-1] == "O", d[:, :-1] == ".")))
        )
        if len(movable) == 0:
            break
        for y, x in movable:
            a[y][x] = "."
            a[y][x + 1] = "O"
    return a


def roll_s(a: np.ndarray) -> np.ndarray:
    while True:
        d = np.roll(a, -1, axis=0)
        movable = list(
            zip(*np.where(np.logical_and(a[:-1, :] == "O", d[:-1, :] == ".")))
        )
        if len(movable) == 0:
            break
        for y, x in movable:
            a[y][x] = "."
            a[y + 1][x] = "O"
    return a


def roll_w(a: np.ndarray) -> np.ndarray:
    while True:
        d = np.roll(a, 1, axis=1)
        movable = list(zip(*np.where(np.logical_and(a[:, 1:] == "O", d[:, 1:] == "."))))
        if len(movable) == 0:
            break
        for y, x in movable:
            a[y][x + 1] = "."
            a[y][x] = "O"
    return a


def solve1(map: list[str]) -> int:
    a = np.array([list(line) for line in map])
    a = roll_n(a)

    sum = 0
    positions = list(zip(*np.where(a == "O")))
    for y, _ in positions:
        sum += a.shape[0] - y

    return sum


def solve2(map: list[str]) -> int:
    a = np.array([list(line) for line in map])
    loads = pd.Series()
    # eventually converges to a cycle with period 13
    for i in range(220):
        a = roll_n(a)
        a = roll_w(a)
        a = roll_s(a)
        a = roll_e(a)

        positions = list(zip(*np.where(a == "O")))
        load = 0
        for y, _ in positions:
            load += a.shape[0] - y

        if i > 200:
            loads.loc[(i + 1) % 13] = load

    return loads.loc[1_000_000_000 % 13]


if __name__ == "__main__":
    print(f"part 1 test = {solve1(test())}")
    print(f"part 1 live = {solve1(live())}")
    # print(f"part 2 test = {solve2(test())}")
    print(f"part 2 live = {solve2(live())}")
