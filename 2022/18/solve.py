import numpy as np


bounds_t = tuple[tuple[int, int], tuple[int, int], tuple[int, int]]
point_t = tuple[int, int, int]


def test() -> list[point_t]:
  data = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""
  return [tuple(int(n) for n in line.split(",")) for line in data.splitlines()]


def live() -> list[point_t]:
  with open("2022/18/input.txt") as fd:
    return [tuple(int(n) for n in line.split(",")) for line in fd.read().splitlines()]


def extent(a: list[point_t]) -> bounds_t:
  return ((min(x[0] for x in a) - 1, max(x[0] for x in a) + 2),
          (min(x[1] for x in a) - 1, max(x[1] for x in a) + 2),
          (min(x[2] for x in a) - 1, max(x[2] for x in a) + 2))


def make_lava(a: list[point_t], extent: bounds_t) -> np.ndarray:
  (xmin, xmax), (ymin, ymax), (zmin, zmax) = extent
  lava = np.zeros((xmax - xmin, ymax - ymin, zmax - zmin), dtype=int)
  for i in a:
    lava[i[0] - xmin, i[1] - ymin, i[2] - zmin] = 1
  return lava


def count_faces(lava: np.ndarray, extent: bounds_t) -> int:
  (xmin, xmax), (ymin, ymax), (zmin, zmax) = extent
  faces = 0
  for y in range(ymax - ymin):
    for z in range(zmax - zmin):
      faces += abs(lava[1:, y, z] - lava[:-1, y, z]).sum()
  for x in range(xmax - xmin):
    for z in range(zmax - zmin):
      faces += abs(lava[x, 1:, z] - lava[x, :-1, z]).sum()
  for x in range(xmax - xmin):
    for y in range(ymax - ymin):
      faces += abs(lava[x, y, 1:] - lava[x, y, :-1]).sum()
  return faces


def neighbours(array: np.ndarray, point: point_t) -> set[point_t]:
  x, y, z = point
  xmax, ymax, zmax = array.shape
  return set((
    (max(0, x - 1), y, z),
    (min(x + 1, xmax - 1), y, z),
    (x, max(0, y - 1), z),
    (x, min(y + 1, ymax - 1), z),
    (x, y, max(0, z - 1)),
    (x, y, min(z + 1, zmax - 1))
  ))


def flood_face_count(array: np.ndarray, point: point_t) -> int:
  xmax, ymax, zmax = array.shape
  visited = np.zeros(array.shape, dtype=bool)
  queue = [point]
  current = array[point]
  count = 0
  while queue:
    node = queue.pop(0)
    if array[node] == current and visited[node]:
      continue
    if array[node] == current:
      queue.extend(neighbours(array, node))
    else:
      count += 1
    visited[node] = True

  return count


def solve1(a: list[point_t]) -> int:
  ext = extent(a)
  lava = make_lava(a, ext)
  return count_faces(lava, ext)


def solve2(a: list[point_t]) -> int:
  ext = extent(a)
  lava = make_lava(a, ext)
  return flood_face_count(lava, (0, 0, 0))


if __name__ == "__main__":
  assert solve1(test()) == 64
  print(f"part 1 = {solve2(test())}")
  assert solve2(test()) == 58
  print(f"part 2 = {solve2(live())}")

