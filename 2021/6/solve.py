
import numpy as np

def test() -> list[int]:
  data = """3,4,3,1,2"""
  return [int(i) for i in data.split(",")]


def live() -> list[int]:
  with open("2021/6/input.txt") as fd:
    a = fd.read().split(",")
  return [int(i) for i in a]



def evolve_naive(pop: list[int], days: int) -> list[int]:
  for i in range(days):
    new = sum(i == 0 for i in pop)
    pop = [i - 1 if i != 0 else 6 for i in pop]
    pop.extend([8] * new)
  return pop


def count(pop: list[int]) -> list[int]:
  counts = [0] * 9
  for p in pop:
    counts[p] += 1
  return counts


def evolve_counts(pop: list[int], days: int) -> list[int]:
  counts = count(pop)

  for i in range(days):
    new = counts[0]
    counts = counts[1:] + [new]
    counts[6] += new
  return counts


def solve1(input) -> int:
  return len(evolve_naive(input, 80))


def solve2(input) -> int:
  return sum(evolve_counts(input, 256))


if __name__ == "__main__":
  assert solve1(test()) == 5934
  print(f"part 1 = {solve1(live())}")
  assert solve2(test()) == 26984457539
  print(f"part 2 = {solve2(live())}")
