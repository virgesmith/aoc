
def test() -> list[str]:
  data = """
"""
  return data.splitlines()


def live() -> list[str]:
  with open("2022/?/input.txt") as fd:
    return fd.read().splitlines()


def solve1(a: set[str]) -> int:
  return


def solve2(a: list[str]) -> int:
  return


if __name__ == "__main__":
  print(f"part 1 test = {solve1(test())}")
  # print(f"part 1 live = {solve1(live())}")
  # print(f"part 2 test = {solve2(test())}")
  # print(f"part 2 live = {solve2(live())}")
