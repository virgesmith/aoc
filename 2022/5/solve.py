from io import StringIO
import numpy as np
import pandas as pd

def test() -> list[str]:
  stacks = """
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3
"""

  moves = """move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
  df = pd.read_fwf(StringIO("\n".join(reversed(stacks.splitlines()))), delimiter=" ", header=0)

  stacks = {col: list(df[col].dropna().values) for col in df.columns}
  return stacks, moves.splitlines()


def live() -> list[str]:
  with open("2022/5/input1.txt") as fd:
    df = pd.read_fwf(StringIO("\n".join(reversed(fd.read().splitlines()))), delimiter=" ", header=0)
  stacks = {col: list(df[col].dropna().values) for col in df.columns}
  with open("2022/5/input2.txt") as fd:
    moves = fd.read().splitlines()
  return stacks, moves


def solve1(a: tuple) -> int:
  stacks, moves = a
  for move in moves:
    s = move.split(" ")
    n = int(s[1])
    src = s[3]
    dst = s[5]
    for _ in range(n):
      stacks[dst].append(stacks[src].pop())

  result = [stacks[s][-1][1] for s in stacks]
  return "".join(result)

def solve2(a: list[str]) -> int:
  stacks, moves = a
  for move in moves:
    s = move.split(" ")
    n = int(s[1])
    src = s[3]
    dst = s[5]
    stacks[dst].extend(stacks[src][-n:])
    for _ in range(n):
      stacks[src].pop()

  result = [stacks[s][-1][1] for s in stacks]
  return "".join(result)


if __name__ == "__main__":
  print(f"part 1 test = {solve1(test())}")
  print(f"part 1 live = {solve1(live())}")
  print(f"part 2 test = {solve2(test())}")
  print(f"part 2 live = {solve2(live())}")
