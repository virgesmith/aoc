from typing import Generator
import numpy as np

def test() -> tuple[Generator[int, None, None], list[np.ndarray]]:
  data = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""
  a = data.splitlines()

  numbers = (int(i) for i in a[0].split(","))
  boards = [np.array([[int(i) for i in line.split()] for line in a[j:j+5]]) for j in range(2, len(a), 6)]
  return numbers, boards


def live() -> tuple[Generator[int, None, None], list[np.ndarray]]:
  with open("2021/4/input.txt") as fd:
    a = fd.read().splitlines()

  numbers = (int(i) for i in a[0].split(","))
  boards = [np.array([[int(i) for i in line.split()] for line in a[j:j+5]]) for j in range(2, len(a), 6)]
  return numbers, boards



def solve1(numbers: Generator[int, None, None], boards: list[np.ndarray]) -> int:
  scores = [np.zeros(b.shape, dtype=bool) for b in boards]

  for n in numbers:
    for i, b in enumerate(boards):
      scores[i] = np.logical_or(scores[i], b == n)
      if 5 in scores[i].sum(axis=1) or 5 in scores[i].sum(axis=0):
        return b[~scores[i]].sum() * n
  raise ValueError("numbers incomplete")


def solve2(numbers: Generator[int, None, None], boards: list[np.ndarray]) -> int:
  scores = [np.zeros(b.shape, dtype=bool) for b in boards]

  v = set()
  s = []

  for n in numbers:
    for i, b in enumerate(boards):
      scores[i] = np.logical_or(scores[i], b == n)
      if i not in v and (5 in scores[i].sum(axis=1) or 5 in scores[i].sum(axis=0)):
        v.add(i)
        s.append(b[~scores[i]].sum() * n)
  return s[-1]


if __name__ == "__main__":
  assert solve1(*test()) == 4512
  print(f"part 1 = {solve1(*live())}")
  assert solve2(*test()) == 1924
  print(f"part 2 = {solve2(*live())}")
