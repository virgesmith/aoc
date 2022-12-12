import numpy as np

def test() -> np.ndarray:
  data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
  return to_matrix(data)


def live() -> np.ndarray:
  with open("2022/12/input.txt") as fd:
    return to_matrix(fd.read())


def to_matrix(a: list[str]) -> np.ndarray:
  m = np.array([[ord(x) - ord("a") + 1 for x in list(s)] for s in a.splitlines()])
  m[m == -13] = 0
  m[m == -27] = 27
  return m


def to_graph(m):
  g = {}
  (ny, nx) = m.shape
  for (y, x), n in np.ndenumerate(m):
    g[(y, x)] = []
    for (dy, dx) in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
      yp = y + dy
      xp = x + dx
      if yp < 0 or yp >= ny or xp < 0 or xp >= nx:
        continue
      if m[yp, xp] - n < 2:
        g[(y,x)].append((yp, xp))
  return g


def bfs_sp(graph: dict, start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
  explored = []
  queue = [[start]]

  if start == goal:
    return [goal]

  while queue:
    path = queue.pop(0)
    node = path[-1]

    if node not in explored:
      neighbours = graph[node]

      for neighbour in neighbours:
        new_path = list(path)
        new_path.append(neighbour)
        queue.append(new_path)

        if neighbour == goal:
          return new_path
      explored.append(node)

  # nodes are not connected
  return []


def solve1(m: np.ndarray) -> int:
  g = to_graph(m)
  start = tuple(np.argwhere(m == 0)[0])
  finish = tuple(np.argwhere(m == 27)[0])

  # steps is no. nodes - 1
  return len(bfs_sp(g, start, finish)) - 1


def solve2(m: np.ndarray) -> int:
  g = to_graph(m)
  starts = np.argwhere(m == 1)
  finish = tuple(np.argwhere(m == 27)[0])

  lengths = [len(bfs_sp(g, tuple(start), finish)) - 1 for start in starts]
  return min(l for l in lengths if l >= 0)


if __name__ == "__main__":
  assert solve1(test()) == 31
  print(f"part 1 = {solve1(live())}")
  assert solve2(test()) == 29
  print(f"part 2 = {solve2(live())}")
