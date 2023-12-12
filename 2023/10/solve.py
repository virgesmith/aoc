from io import StringIO

N = 0
E = 1
S = 2
W = 3


def test1():
    input = """\
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""
    return StringIO(input).read().splitlines()


def test2():
    input = """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""
    return StringIO(input).read().splitlines()


def live():
    with open("2023/10/input.txt") as fd:
        return fd.read().splitlines()


def start(map: list[str]) -> tuple[int, int, list[int]]:
    for y, line in enumerate(map):
        if "S" in line:
            break
    x = map[y].find("S")

    exits = []
    if y > 0 and map[y-1][x] in "|F7":
        exits.append(N)
    if x < len(map[0]) - 1 and map[y][x + 1] in "-J7":
        exits.append(E)
    if y < len(map) - 1 and map[y+1][x] in "|JL":
        exits.append(S)
    if x > 0 and map[y][x - 1] in "-FL":
        exits.append(W)

    return x, y, exits

def move(map: list[str], x: int, y: int, dir: int) -> tuple[int, int, int]:
    match dir:
        case 0: # N
            y -= 1
            if map[y][x] == "F": dir = E
            elif map[y][x] == "7": dir = W
        case 1: # E
            x += 1
            if map[y][x] == "J": dir = N
            elif map[y][x] == "7": dir = S
        case 2: # S
            y += 1
            if map[y][x] == "L": dir = E
            elif map[y][x] == "J": dir = W
        case 3: # W
            x -= 1
            if map[y][x] == "L": dir = N
            elif map[y][x] == "F": dir = S
    return x, y, dir


def solve1(map: list[str]) -> int:
    start_x, start_y, dirs = start(map)
    i = 0
    x, y, dir = start_x, start_y, dirs[0]
    while True:
        x, y, dir = move(map, x, y, dir)
        if x == start_x and y == start_y:
            break
        i += 1
    return (i + 1) // 2

def solve2(map: list[str]) -> int:
    route = [["."] * len(map[0]) for _ in range(len(map))]

    start_x, start_y, start_dirs = start(map)
    x, y, dir = start_x, start_y, start_dirs[0]
    while True:
        route[y][x] = "*"
        x, y, dir = move(map, x, y, dir)
        if x == start_x and y == start_y:
            break

    # correct S
    if N in start_dirs:
        if E in start_dirs:
            map[start_y] = map[start_y].replace("S", "L")
        elif W in start_dirs:
            map[start_y] = map[start_y].replace("S", "J")
        else:
            map[start_y] = map[start_y].replace("S", "|")
    elif S in start_dirs:
        if E in start_dirs:
            map[start_y] = map[start_y].replace("S", "F")
        elif W in start_dirs:
            map[start_y] = map[start_y].replace("S", "7")
    else:
        map[start_y] = map[start_y].replace("S", "-")

    # count contained points
    count = 0
    for y, line in enumerate(route):
        inside = False
        for x, point in enumerate(line):
            if point == "*" and map[y][x] in ["F", "L"]:
                entry = map[y][x]
            elif point == "*" and map[y][x] in ["7", "J"]:
                if (entry == "F" and map[y][x] == "J") or (entry == "L" and map[y][x] == "7"):
                    inside = not inside
                # print(f"exit at {x=}, {y=}")
            elif point == "*" and map[y][x] == "|":
                # print(f"crossing at {x=}, {y=}")
                inside = not inside
            elif point == "." and inside:
                count += 1
                route[y][x] = "X"

    for line in map:
        print("".join(line))
    for line in route:
        print("".join(line))
    return count

if __name__ == "__main__":
    print(f"part 1 test = {solve1(test1())}")
    print(f"part 1 live = {solve1(live())}")
    print(f"part 2 test = {solve2(test2())}")
    print(f"part 2 live = {solve2(live())}")
