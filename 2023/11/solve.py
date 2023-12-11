from io import StringIO

import numpy as np

def test1():
    input = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
    return StringIO(input).read().splitlines()


def test2():
    input = """\
"""
    return StringIO(input).read().splitlines()


def live():
    with open("2023/11/input.txt") as fd:
        return fd.read().splitlines()


def expand(a: np.ndarray) -> np.ndarray:
    row = 0
    while row < a.shape[1]:
        if a[row, :].sum() == 0:
            a = np.insert(a, row, a[row, :], 0)
            row += 1
        row += 1
    col = 0
    while col < a.shape[0]:
        if a[:, col].sum() == 0:
            a = np.insert(a, col, a[:, col], 1)
            col += 1
        col += 1
    return a


def solve1(map: list[str]) -> int:
    a = np.array([[point == '#' for point in line] for line in map], dtype=int)
    print(a)
    a = expand(a)
    print(a)
    return 0


def solve2(map: list[str]) -> int:

    return 0

if __name__ == "__main__":
    print(f"part 1 test = {solve1(test1())}")
    # print(f"part 1 live = {solve1(live())}")
    # print(f"part 2 test = {solve2(test2())}")
    # print(f"part 2 live = {solve2(live())}")
