from io import StringIO
import numpy as np
import pandas as pd

def test():
  input="""
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""
  return pd.read_fwf(StringIO(input), widths=[1] * 10, header=None).values


def live():
  return pd.read_fwf("2021/25/input.txt", widths=[1] * 139, header=None).values


def move_r(a: np.ndarray) -> tuple[np.ndarray, int]:
  nr = a.shape[0]
  nc = a.shape[1]
  move = np.zeros(a.shape, dtype=bool)
  # flag
  for r in range(a.shape[0]):
    for c in range(a.shape[1]):
      if a[r, c] == ">" and a[r, (c + 1) % nc] == ".":
        move[r, c] = True
  # move
  for r in range(a.shape[0]):
    for c in range(a.shape[1]):
      if move[r, c]:
        a[r, c] = "."
        a[r, (c + 1) % nc] = ">"
  return a, move.sum()


def move_d(a: np.ndarray) -> tuple[np.ndarray, int]:
  nr = a.shape[0]
  nc = a.shape[1]
  move = np.zeros(a.shape, dtype=bool)
  # flag
  for r in range(a.shape[0]):
    for c in range(a.shape[1]):
      if a[r, c] == "v" and a[(r + 1) % nr, c] == ".":
        move[r, c] = True
  # move
  for r in range(a.shape[0]):
    for c in range(a.shape[1]):
      if move[r, c]:
        a[r, c] = "."
        a[(r + 1) % nr, c] = "v"
  return a, move.sum()


def move(a: np.ndarray) -> tuple[np.ndarray, int]:
  a, n_r = move_r(a)
  a, n_d = move_d(a)
  return a, n_r + n_d


def loop(a: np.ndarray) -> tuple[np.ndarray, int]:
  i = 0
  while True:
    a, n = move(a)
    i += 1
    if not n:
      break
  return a, i


def display(a: np.ndarray) -> None:
  for r in range(a.shape[0]):
    for c in range(a.shape[1]):
      print(a[r, c], end="")
    print()
  print()


def part1(a: np.ndarray) -> None:
  display(a)
  a, n = loop(a)
  display(a)
  print(f"{n} iterations")

if __name__ == "__main__":
  part1(test())
  part1(live())
