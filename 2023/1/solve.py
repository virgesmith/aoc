from io import StringIO


def test1():
    input = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
    return StringIO(input).read().splitlines()


def test2():
    input = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""
    return StringIO(input).read().splitlines()


def live():
    with open("2023/1/input.txt") as fd:
        return fd.read().splitlines()


def solve_impl(string: str, digits: dict[str, int], order: range) -> int:
    for i in order:
        for d in digits:
            if string[i:].startswith(d):
                return digits[d]
    raise ValueError(f"no digits in {string}")


def first(string: str, digits: dict[str, int]) -> int:
    return solve_impl(string, digits, range(len(string)))


def last(string: str, digits: dict[str, int]) -> int:
    return solve_impl(string, digits, range(len(string) - 1, -1, -1))


def solve1(strings: list[str]) -> int:
    digits = {str(d): d for d in range(1, 10)}
    return sum(first(s, digits) * 10 + last(s, digits) for s in strings)


def solve2(strings: list[str]) -> list[int]:
    digits = {str(d): d for d in range(1, 10)} | dict(
        one=1, two=2, three=3, four=4, five=5, six=6, seven=7, eight=8, nine=9
    )
    return sum(first(s, digits) * 10 + last(s, digits) for s in strings)


if __name__ == "__main__":
    print(f"part 1 test = {solve1(test1())}")
    print(f"part 1 live = {solve1(live())}")
    print(f"part 2 test = {solve2(test2())}")
    print(f"part 2 live = {solve2(live())}")
