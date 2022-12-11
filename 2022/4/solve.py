
def test() -> list[str]:
  data = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
  return data.splitlines()


def live() -> list[str]:
  with open("2022/4/input.txt") as fd:
    return fd.read().splitlines()


def solve1(a: list[str]) -> int:
  split = ((s[0].split("-"), s[1].split("-")) for s in (s.split(",") for s in a))

  def is_subset(s: list[list[str]]) -> bool:
    s1 = set(range(int(s[0][0]), int(s[0][1])+1))
    s2 = set(range(int(s[1][0]), int(s[1][1])+1))
    return s1.issubset(s2) or s2.issubset(s1)

  return sum(1 for s in split if is_subset(s))


def solve2(a: list[str]) -> int:
  split = ((s[0].split("-"), s[1].split("-")) for s in (s.split(",") for s in a))

  def intersects(s: list[list[str]]) -> bool:
    s1 = set(range(int(s[0][0]), int(s[0][1])+1))
    s2 = set(range(int(s[1][0]), int(s[1][1])+1))
    return len(s1.intersection(s2))

  return sum(1 for s in split if intersects(s))


if __name__ == "__main__":
  print(f"part 1 test = {solve1(test())}")
  print(f"part 1 live = {solve1(live())}")
  print(f"part 2 test = {solve2(test())}")
  print(f"part 2 live = {solve2(live())}")
