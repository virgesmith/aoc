from io import StringIO


def test1():
    input = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
    return StringIO(input).read().splitlines()


def live():
    with open("2023/4/input.txt") as fd:
        return fd.read().splitlines()


def solve1(strings: list[str]) -> int:
    sum = 0
    for s in strings:
        theirs, held = s.split(":")[1].split("|")
        theirs = set(int(w) for w in theirs.strip().split())
        held = set(int(h) for h in held.strip().split())
        if (wins := len(theirs & held)) > 0:
            sum += 2 ** (wins - 1)
    return sum


def solve2(strings: list[str]) -> int:
    # sum = 0
    multiplier = [1] * len(strings)
    for i, s in enumerate(strings):
        theirs, held = s.split(":")[1].split("|")
        theirs = set(int(w) for w in theirs.strip().split())
        held = set(int(h) for h in held.strip().split())
        wins = len(theirs & held)
        for j in range(i + 1, i + 1 + wins):
            multiplier[j] += multiplier[i]
    return sum(multiplier)


if __name__ == "__main__":
    print(f"part 1 test = {solve1(test1())}")
    print(f"part 1 live = {solve1(live())}")
    print(f"part 2 test = {solve2(test1())}")
    print(f"part 2 live = {solve2(live())}")
