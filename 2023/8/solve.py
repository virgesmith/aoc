from io import StringIO


def test1():
    input = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""
    return StringIO(input).read().splitlines()


def test2():
    input = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""
    return StringIO(input).read().splitlines()


def live():
    with open("2023/8/input.txt") as fd:
        return fd.read().splitlines()


def read(strings: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    path = strings[0]
    g = {}
    for s in strings[2:]:
        s = s.replace("(", "").replace(")", "").split("=")
        g[s[0].strip()] = tuple(t.strip() for t in s[1].split(","))
    return path, g


def solve1(strings: list[str]) -> int:
    path, g = read(strings)
    loc = "AAA"
    i = 0
    while loc != "ZZZ":
        for move in path:
            loc = g[loc][0] if move == "L" else g[loc][1]
            if loc != "ZZZ" and g[loc][0] == loc and g[loc][1] == loc:
                raise StopIteration("stuck")
        i += 1
    return i * len(path)


def solve2(strings: list[str]) -> int:
    path, g = read(strings)

    locs = [k for k in g if k.endswith("A")]

    print(locs)
    total = len(path)
    for loc in locs:
        count = 0
        while not loc.endswith("Z"):
            for move in path:
                loc = g[loc][0] if move == "L" else g[loc][1]
                if not loc.endswith("Z") and g[loc][0] == loc and g[loc][1] == loc:
                    raise StopIteration("stuck")
            count += 1

        # print(count, locs)
        total *= count

    return total


if __name__ == "__main__":
    print(f"part 1 test = {solve1(test1())}")
    print(f"part 1 live = {solve1(live())}")
    print(f"part 2 test = {solve2(test2())}")
    print(f"part 2 live = {solve2(live())}")
