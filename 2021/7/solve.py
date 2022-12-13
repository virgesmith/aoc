from typing import Callable
import numpy as np

def test() -> list[int]:
  data = """16,1,2,0,4,2,7,1,2,14"""
  return [int(i) for i in data.split(",")]


def live() -> list[str]:
  with open("2021/7/input.txt") as fd:
    return [int(i) for i in fd.read().split(",")]


def f1(a: int, i: int) -> int:
  return abs(a - i)


def f2(a: int, i: int) -> int:
  x = abs(a - i)
  return x * (x + 1) // 2


def solve_impl(positions: list[int], cost_func: Callable[[int, int], int]) -> int:
  costs = []
  for i in range(min(positions), max(positions)+1):
    costs.append(sum(cost_func(a, i) for a in positions))
  return min(positions) + np.argmin(costs), min(costs)


def solve1(positions: list[int]) -> int:
  return solve_impl(positions, f1)


def solve2(positions: list[str]) -> int:
  return solve_impl(positions, f2)


if __name__ == "__main__":
  assert solve1(test()) == (2, 37)
  print(f"part 1 = {solve1(live())}")
  assert solve2(test()) == (5, 168)
  print(f"part 2 = {solve2(live())}")
