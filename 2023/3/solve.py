from io import StringIO

from collections import defaultdict


def test1():
    input = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..\
    """
    return StringIO(input).read().splitlines()


def live():
    with open("2023/3/input.txt") as fd:
        return fd.read().splitlines()


def pad(strings: list[str]) -> list[str]:
    n = len(strings[0]) + 2
    return ["." * n] + [f".{s}." for s in strings] + ["." * n]


def solve1(strings: list[str]) -> int:
    strings = pad(strings)
    sum = 0
    for y in range(1, len(strings) - 1):
        x = 1
        while x < len(strings[y]) - 1:
            if strings[y][x].isdigit():
                xr = x + 1
                while strings[y][xr].isdigit() and x < len(strings[y]):
                    xr += 1
                ndots = (
                    strings[y - 1][x - 1 : xr + 1].count(".")
                    + strings[y][x - 1 : xr + 1].count(".")
                    + strings[y + 1][x - 1 : xr + 1].count(".")
                )
                if ndots < (xr - x + 2) * 2 + 2:
                    sum += int(strings[y][x:xr])
                x = xr
            x += 1
    return sum


def solve2(strings: list[str]) -> list[int]:
    strings = pad(strings)
    sum = 0
    stars = defaultdict(lambda: [])
    for y in range(1, len(strings) - 1):
        x = 1
        while x < len(strings[y]) - 1:
            if strings[y][x].isdigit():
                xr = x + 1
                while strings[y][xr].isdigit() and x < len(strings[y]):
                    xr += 1
                if (px := strings[y - 1][x - 1 : xr + 1].find("*")) != -1:
                    stars[(x + px - 1, y - 1)].append(int(strings[y][x:xr]))
                elif (px := strings[y][x - 1 : xr + 1].find("*")) != -1:
                    stars[(x + px - 1, y)].append(int(strings[y][x:xr]))
                elif (px := strings[y + 1][x - 1 : xr + 1].find("*")) != -1:
                    stars[(x + px - 1, y + 1)].append(int(strings[y][x:xr]))
                x = xr
            x += 1
    for v in stars.values():
        if len(v) == 2:
            sum += v[0] * v[1]
    return sum


if __name__ == "__main__":
    print(f"part 1 test = {solve1(test1())}")
    print(f"part 1 live = {solve1(live())}")
    print(f"part 2 test = {solve2(test1())}")
    print(f"part 2 live = {solve2(live())}")
