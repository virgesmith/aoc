import re
from collections import Counter
import numpy as np

import matplotlib.pyplot as plt

SENSOR = 0
BEACON = 1
COL = 0
ROW = 1


def test() -> list[tuple[tuple[int, int], tuple[int, int]]]:
  data = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

  split = (re.split(r'=|,|:', x) for x in data.splitlines())
  return [((int(line[1]), int(line[3])), (int(line[5]), int(line[7]))) for line in split]


def live() -> list[str]:
  with open("2022/15/input.txt") as fd:
    split = (re.split(r'=|,|:', x) for x in fd.read().splitlines())
    return [((int(line[1]), int(line[3])), (int(line[5]), int(line[7]))) for line in split]


def extent(sensors):
  return ((min(p[SENSOR][COL] - manhattan(p) for p in sensors),
           max(p[SENSOR][COL] + manhattan(p) for p in sensors)),
          (min(p[SENSOR][ROW] - manhattan(p) for p in sensors),
           max(p[SENSOR][ROW] + manhattan(p) for p in sensors)))


def manhattan(pair: tuple[tuple[int, int], tuple[int, int]]) -> int:
  return abs(pair[SENSOR][COL] - pair[BEACON][COL]) + abs(pair[SENSOR][ROW] - pair[BEACON][ROW])


def solve_graph(sensors: list) -> int:
  (xmin, xmax), (ymin, ymax) = extent(sensors)

  free = np.zeros((ymax - ymin + 1, xmax - xmin + 1), dtype=int)
  for y in range(ymin, ymax + 1):
    for sensor in sensors:
      overlap = max(0, manhattan(sensor) - abs(y - sensor[SENSOR][ROW]) + 1)
      if overlap:
        x0 = max(0, sensor[SENSOR][COL] - overlap + 1 - xmin)
        x1 = min(xmax - xmin + 1, sensor[SENSOR][COL] + overlap - xmin)
        free[y - ymin, x0:x1] = 1

  for sensor in sensors:
    free[sensor[SENSOR][ROW] - ymin, sensor[SENSOR][COL] - xmin] = 2
    free[sensor[BEACON][ROW] - ymin, sensor[BEACON][COL] - xmin] = 3
  plt.imshow(free)
  return 0


def solve1(sensors: list, row: int) -> int:
  (xmin, xmax), _ = extent(sensors)

  free = np.zeros(xmax - xmin + 1, dtype=int)
  for sensor in sensors:
    overlap = max(0, manhattan(sensor) - abs(row - sensor[SENSOR][ROW]) + 1)
    if overlap:
      x0 = max(xmin, sensor[SENSOR][COL] - overlap + 1) - xmin
      x1 = min(xmax - xmin + 1, sensor[SENSOR][COL] + overlap) - xmin
      free[x0:x1] = 1

  for sensor in sensors:
    if sensor[SENSOR][ROW] == row:
      free[sensor[SENSOR][COL] - xmin] = 2
    if sensor[BEACON][ROW] == row:
      free[sensor[BEACON][COL] - xmin] = 3
  return sum(free == 1)


def bounds(sensor):
  n = manhattan(sensor) + 1
  b = [(sensor[SENSOR][COL] + i, sensor[SENSOR][ROW] + (n - i)) for i in range(n + 1)] \
    + [(sensor[SENSOR][COL] - i, sensor[SENSOR][ROW] + (n - i)) for i in range(n + 1)] \
    + [(sensor[SENSOR][COL] + i, sensor[SENSOR][ROW] - (n - i)) for i in range(n + 1)] \
    + [(sensor[SENSOR][COL] - i, sensor[SENSOR][ROW] - (n - i)) for i in range(n + 1)]
  return set(b)


def solve2(sensors: list, _extent: tuple[int, int]) -> int:
  boundaries = [bounds(s) for s in sensors]

  inter = []

  for i, p0 in enumerate(boundaries):
    for p1 in boundaries[:i]:
      inter.extend(p0.intersection(p1))

  counts = Counter(inter)

  filtered = [k for k in counts if counts[k] % 2 == 0]

  for p in filtered:
    in_range = False
    for s in sensors:
      if manhattan(s) >= abs(s[SENSOR][COL] - p[COL]) + abs(s[SENSOR][ROW] - p[ROW]):
        in_range = True
        break
    if not in_range:
      return p[COL] * 4_000_000 + p[ROW]


if __name__ == "__main__":
  assert solve1(test(), 10) == 26
  print(f"part 1 live = {solve1(live(), 2000000)}") # 5176944
  assert solve2(test(), (0, 20)) == 56000011
  print(f"part 2 live = {solve2(live(), (0, 4000000))}")
  plt.show()
