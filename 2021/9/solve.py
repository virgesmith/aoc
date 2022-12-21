import numpy as np


def test() -> list[str]:
  data = """2199943210
3987894921
9856789892
8767896789
9899965678"""
  return np.array([[int(n) for n in [*line]] for line in data.splitlines()])


def live() -> list[str]:
  with open("2021/9/input.txt") as fd:
    return np.array([[int(n) for n in [*line]] for line in fd.read().splitlines()])


def local_minima(a: np.array) -> np.array:
  m = np.zeros(a.shape, dtype=bool)
  m[:-1,:] = (a[:-1, :] - a[1:, :]) >= 0
  m[1:,:] |= (a[1:, :] - a[:-1, :]) >= 0
  m[:,:-1] |= (a[:, :-1] - a[:, 1:]) >= 0
  m[:,1:] |= (a[:, 1:] - a[:, :-1]) >= 0
  return ~m


def solve1(a: np.array) -> int:
  m = local_minima(a)
  return m.sum() + (m * a).sum()


def neighbours(node: tuple[int, int], shape: tuple[int, int]) -> list[tuple[int, int]]:
  n = []
  if node[0] > 0:
    n.append((node[0] - 1, node[1]))
  if node[0] < shape[0] - 1:
    n.append((node[0] + 1, node[1]))
  if node[1] > 0:
    n.append((node[0], node[1] - 1))
  if node[1] < shape[1] - 1:
    n.append((node[0], node[1] + 1))
  return n


def basin_size(a: np.array, bottom: tuple[int, int]) -> int:
  res = np.zeros(a.shape, dtype=bool)
  queue = [bottom]
  res[bottom] = True
  while queue:
    node = queue.pop(0)
    for n in neighbours(node, a.shape):
      if a[n] != 9 and not res[n]:
        queue.append(n)
        res[n] = True
  return res.sum()


def solve2(a: list[str]) -> int:
  m = local_minima(a)
  return np.prod(sorted(basin_size(a, p) for p in zip(*np.where(m)))[-3:])


if __name__ == "__main__":
  assert solve1(test()) == 15
  print(f"part 1 live = {solve1(live())}")
  assert solve2(test()) == 1134
  print(f"part 2 live = {solve2(live())}")
