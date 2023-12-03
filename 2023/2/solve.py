from io import StringIO


def test1():
    input = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
    return StringIO(input).read().splitlines()


def live():
    with open("2023/2/input.txt") as fd:
        return fd.read().splitlines()


def solve1(strings: list[str]) -> int:
    limits = {"red": 12, "blue": 14, "green": 13}
    sum = 0
    for s in strings:
        game, outcomes = s.split(":")
        game = int(game.replace("Game ", ""))
        outcomes = outcomes.replace(";", ",").split(",")
        within_limit = True
        for dice in outcomes:
            n, colour = dice.strip().split(" ")
            if int(n) > limits[colour]:
                within_limit = False
                break
        if within_limit:
            sum += game
    return sum


def solve2(strings: list[str]) -> list[int]:
    sum = 0
    for s in strings:
        game, outcomes = s.split(":")
        game = int(game.replace("Game ", ""))
        outcomes = outcomes.replace(";", ",").split(",")
        minima = dict(red=0, green=0, blue=0)
        for dice in outcomes:
            n, colour = dice.strip().split(" ")
            minima[colour] = max(minima[colour], int(n))
        sum += minima["red"] * minima["green"] * minima["blue"]
    return sum


if __name__ == "__main__":
    print(f"part 1 test = {solve1(test1())}")
    print(f"part 1 live = {solve1(live())}")
    print(f"part 2 test = {solve2(test1())}")
    print(f"part 2 live = {solve2(live())}")

# 2575 too high
