

def test() -> list[str]:
  data = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""
  return data.splitlines()


def live() -> list[str]:
  with open("2022/3/input.txt") as fd:
    return fd.read().splitlines()


def mapping(s: str) -> int:
  assert len(s) == 1
  s = list(s)[0]
  if s.islower():
    return ord(s) - ord("a") + 1
  else:
    return ord(s) - ord("A") + 27


def solve1(a: set[str]) -> int:
  return sum([mapping({*s[:len(s)//2]} & {*s[len(s)//2:]}) for s in a])


def solve2(a: list[str]) -> int:

  g = list(zip(a[::3], a[1::3], a[2::3]))

  return sum([mapping({*s[0]} & {*s[1]} & {*s[2]}) for s in g])


if __name__ == "__main__":
  print(f"part 1 test = {solve1(test())}")
  print(f"part 1 live = {solve1(live())}")
  print(f"part 2 test = {solve2(test())}")
  print(f"part 2 live = {solve2(live())}")
