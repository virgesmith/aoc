from io import StringIO
from typing import Generator
import numpy as np


def test1() -> list[str]:
    input = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
    return StringIO(input).read().splitlines()


def chunk(all: list[str]) -> Generator[list[str], None, None]:
    chunk = []
    for line in all:
        if line == "":
            yield chunk
            chunk = []
        else:
            chunk.append(line)
    yield chunk


def live():
    with open("2023/13/input.txt") as fd:
        return fd.read().splitlines()


def find_hpivot(map: list[str]) -> int:
    for pivot in range(1, len(map)):
        length = min(pivot, len(map) - pivot)
        symmetric = True
        for i in range(1, length + 1):
            if map[pivot - i] != map[pivot + i - 1]:
                symmetric = False
                break
        if symmetric:
            return pivot
    return 0


def find_vpivot(map: list[str]) -> int:
    for pivot in range(1, len(map[0])):
        length = min(pivot, len(map[0]) - pivot)
        symmetric = True
        for line in map:
            if line[pivot - length : pivot] != line[pivot : pivot + length][::-1]:
                symmetric = False
                break
        if symmetric:
            return pivot
    return 0


def find_hsmudge(map: np.ndarray[int]) -> int:
    for pivot in range(1, map.shape[0]):
        length = min(pivot, map.shape[0] - pivot)
        diff = map[pivot - length : pivot, :] != np.flipud(
            map[pivot : pivot + length, :]
        )
        if diff.sum() == 1:
            return pivot
    return 0


def find_vsmudge(map: np.ndarray[int]) -> int:
    for pivot in range(1, map.shape[1]):
        length = min(pivot, map.shape[1] - pivot)
        diff = map[:, pivot - length : pivot] != np.fliplr(
            map[:, pivot : pivot + length]
        )
        if diff.sum() == 1:
            return pivot
    return 0


def solve1(maps: list[str]) -> int:
    sum = 0
    for map in chunk(maps):
        sum += 100 * find_hpivot(map) + find_vpivot(map)
    return sum


def solve2(maps: list[str]) -> int:
    sum = 0
    for map in chunk(maps):
        # for line in map:
        #     print(line)
        a = np.where(np.array([list(line) for line in map]) == "#", 1, 0)
        sum += 100 * find_hsmudge(a) + find_vsmudge(a)
    return sum


if __name__ == "__main__":
    print(f"part 1 test = {solve1(test1())}")
    print(f"part 1 live = {solve1(live())}")
    print(f"part 2 test = {solve2(test1())}")
    print(f"part 2 live = {solve2(live())}")
