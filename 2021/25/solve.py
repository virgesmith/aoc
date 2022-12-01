from io import StringIO
import numpy as np

def test():
  input = \
"""v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""
  return np.array([list(line) for line in input.split("\n")])


def live():
  with open("2021/25/input.txt") as fd:
    return np.array([list(line) for line in fd.read().splitlines()])


def move_r(a: np.ndarray) -> tuple[np.ndarray, int]:
  nc = a.shape[1]
  return move_impl(a, ">", 1, lambda r, c: (r, ((c + 1) % nc)))


def move_d(a: np.ndarray) -> tuple[np.ndarray, int]:
  nr = a.shape[0]
  return move_impl(a, "v", 0, lambda r, c: ((r + 1) % nr, c))


# @profile kernprof -lv 2021/25/solve.py
def move_impl(a: np.ndarray, animal: str, axis: int, mapper) -> tuple[np.ndarray, int]:
  nr = a.shape[axis]
  # work out who moves
  move = np.logical_and(a == animal, np.roll(a, -1, axis=axis) == ".")
  # do the move
  for r, c in np.argwhere(move):
    a[r, c] = "."
    a[mapper(r, c)] = animal
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
    # break
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
  # part1(test())
  part1(live())
