from io import StringIO
from itertools import combinations
import numpy as np


def test():
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


def distances(a: np.ndarray, delta: int) -> tuple[list[int], list[int]]:
    x, y = a.shape
    x = [1 + delta * (a[:, i].sum() == 0) for i in range(x)]
    y = [1 + delta * (a[i, :].sum() == 0) for i in range(y)]
    return x, y


def distance(x0: int, x1: int, dx: list[int]) -> int:
    return sum(dx[x0:x1]) if x0 < x1 else sum(dx[x1:x0])


def solve_impl(map: list[str], delta: int) -> int:
    a = np.array([[point == "#" for point in line] for line in map], dtype=int)

    dx, dy = distances(a, delta - 1)
    locations = list(zip(*np.where(a == 1)))
    sum = 0
    for path in combinations(locations, 2):
        sum += distance(path[0][0], path[1][0], dy) + distance(
            path[0][1], path[1][1], dx
        )
    return sum


def solve1(map: list[str]) -> int:
    return solve_impl(map, 2)


def solve2(map: list[str], delta: int) -> int:
    return solve_impl(map, delta)


if __name__ == "__main__":
    print(f"part 1 test = {solve1(test())}")  # 374
    print(f"part 1 live = {solve1(live())}")  # 9681886
    print(f"part 2 test = {solve2(test(), 10)}")
    print(f"part 2 test = {solve2(test(), 100)}")
    print(f"part 2 live = {solve2(live(), 1000000)}")
