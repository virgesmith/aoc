import numpy as np
import matplotlib.pyplot as plt

AIR = 0
ROCK = 1
SAND = 2


def test() -> list[list[tuple[int, int]]]:
  data = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
  parsed = [[tuple(int(y) for y in x.split(",")) for x in r2] for r2 in (r.split(" -> ") for r in data.splitlines())]
  return parsed


def live() -> list[list[tuple[int, int]]]:
  with open("2022/14/input.txt") as fd:
    parsed = [[tuple(int(y) for y in x.split(",")) for x in r2] for r2 in (r.split(" -> ") for r in fd.read().splitlines())]
    return parsed


def extent(rock: list[list[tuple[int, int]]]) -> tuple[int, int, int, int]:
  xmin = min(min(c[0] for c in b) for b in rock)
  xmax = max(max(c[0] for c in b) for b in rock)
  ymax = max(max(c[1] for c in b) for b in rock)
  return xmin, xmax, 0, ymax


def draw(rock: list[list[tuple[int, int]]], shape: tuple[int, int], xoffset: int) -> np.ndarray:
  cave = np.zeros(shape, dtype=int)
  for r in rock:
    for i in range(1, len(r)):
      x = sorted((r[i-1][0] - xoffset, r[i][0] - xoffset))
      y = sorted((r[i-1][1], r[i][1]))
      cave[y[0]:y[1]+1, x[0]:x[1]+1] = ROCK
  return cave

def solve1(rocks: list[list[tuple[int, int]]]) -> int:
  xmin, xmax, _, ny = extent(rocks)
  nx = xmax - xmin

  cave = draw(rocks, (ny+1, nx+1), xmin)

  sand_point = (0, 500 - xmin)
  i = 0
  while cave[sand_point] == AIR:
    y, x = sand_point
    while True:
      if cave[y + 1, x] != AIR:
        if x == 0:
          # plt.imshow(cave)
          return i
        elif cave[y + 1, x - 1] != AIR:
          if x == nx:
            # plt.imshow(cave)
            return i
          elif cave[y + 1, x + 1] != AIR:
            cave[y, x] = SAND
            break
          else:
            x += 1
        else:
          x -= 1
      y += 1
    i += 1
  raise RuntimeError("blocked")


def solve2(rocks: list[list[tuple[int, int]]]) -> int:
  # determine extent
  xmin, xmax, _, ny = extent(rocks)
  # add floor
  rocks.append([(500 - ny - 2, ny + 2), (500 + ny + 2, ny + 2)])
  # redetermine extent
  xmin, xmax, _, ny = extent(rocks)
  nx = xmax - xmin
  cave = draw(rocks, (ny+1, nx+1), xmin)

  sand_point = (0, 500 - xmin)
  i = 0

  while cave[sand_point] == AIR:
    y, x = sand_point
    while True:
      if cave[y + 1, x] != AIR:
        if cave[y + 1, x - 1] != AIR:
          if cave[y + 1, x + 1] != AIR:
            cave[y, x] = SAND
            break
          else:
            x += 1
        else:
          x -= 1
      y += 1
    i += 1
  plt.imshow(cave)
  return i

if __name__ == "__main__":
  assert solve1(test()) == 24
  print(f"part 1 live = {solve1(live())}")
  assert solve2(test()) == 93
  print(f"part 2 live = {solve2(live())}")
  # plt.show()
