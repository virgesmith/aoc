from io import StringIO
from math import sqrt, floor, ceil

def test1():
    input = """\
Time:      7  15   30
Distance:  9  40  200
"""
    return StringIO(input).read().splitlines()


def live():
    with open("2023/6/input.txt") as fd:
        return fd.read().splitlines()

EPS = 1e-8 # deals with ineqality (> distance)

def bounds(time: int, record: int) -> tuple[int, int]:
    x = sqrt(time * time / 4 - record - EPS)
    lower = ceil(-x + time / 2)
    upper = floor(x + time / 2)
    return lower, upper


def solve1(strings: list[str]) -> int:
    times = (int(s) for s in strings[0].split()[1:])
    records = (int(s) for s in strings[1].split()[1:])
    sum = 1
    for time, record in zip(times, records):
        x = sqrt(time * time / 4 - record - EPS)
        lower, upper = bounds(time, record)
        sum *= (upper - lower) + 1
    return sum

def solve2(strings: list[str]) -> int:
    time = int(strings[0].split(":")[1].replace(" ", ""))
    record = int(strings[1].split(":")[1].replace(" ", ""))

    lower, upper = bounds(time, record)
    return upper - lower + 1


if __name__ == "__main__":
    print(f"part 1 test = {solve1(test1())}")
    print(f"part 1 live = {solve1(live())}")
    print(f"part 2 test = {solve2(test1())}")
    print(f"part 2 live = {solve2(live())}")
