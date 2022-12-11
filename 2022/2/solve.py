
def test():
  return ["A Y", "B X", "C Z"]


def live():
  with open("2022/2/input.txt") as fd:
    return fd.read().splitlines()


def gen_lookup() -> dict[str, int]:
  return { "A X": 1 + 3, "A Y": 2 + 6, "A Z": 3 + 0,
           "B X": 1 + 0, "B Y": 2 + 3, "B Z": 3 + 6,
           "C X": 1 + 6, "C Y": 2 + 0, "C Z": 3 + 3}


def gen_lookup2() -> dict[str, int]:
  return { "A X": 3 + 0, "A Y": 1 + 3, "A Z": 2 + 6,
           "B X": 1 + 0, "B Y": 2 + 3, "B Z": 3 + 6,
           "C X": 2 + 0, "C Y": 3 + 3, "C Z": 1 + 6}


def solve1(strategy: list[str]) -> int:
  lookup = gen_lookup()
  return sum(lookup[s] for s in strategy)


def solve2(strategy: list[str]):
  lookup = gen_lookup2()
  return sum(lookup[s] for s in strategy)


if __name__ == "__main__":
  print(f"part 1 test = {solve1(test())}")
  print(f"part 1 live = {solve1(live())}")
  print(f"part 2 test = {solve2(test())}")
  print(f"part 2 live = {solve2(live())}")
