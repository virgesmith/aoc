import numpy as np

def test() -> list[tuple[tuple[int, int], tuple[int, int]]]:
  data = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""
  a = (s.split(" -> ") for s in data.splitlines())
  return [(tuple(int(c) for c in b[0].split(",")), tuple(int(c) for c in b[1].split(","))) for b in a]


def live() -> list[tuple[tuple[int, int], tuple[int, int]]]:
  with open("2021/5/input.txt") as fd:
    a = (s.split(" -> ") for s in fd.read().splitlines())
  return [(tuple(int(c) for c in b[0].split(",")), tuple(int(c) for c in b[1].split(","))) for b in a]


def extent(endpoints):
  return 1 + max(max(p[0][0], p[1][0]) for p in endpoints), 1 + max(max(p[0][1], p[1][1]) for p in endpoints)


def path(p):
  x = (p[1][0] - p[0][0], p[1][1] - p[0][1])
  m = abs(x[0]) if x[0] != 0 else abs(x[1])
  assert x[0] == 0 or x[1] == 0 or abs(x[0]) == abs(x[1])
  d = (x[0] // m, x[1] // m)
  return ((p[0][0] + i * d[0], p[0][1] + i * d[1]) for i in range(abs(m)+1))


def is_hv(p):
  return p[0][0] == p[1][0] or p[0][1] == p[1][1]


def solve1(endpoints) -> int:
  vents = np.zeros(extent(endpoints), dtype=int)
  for endpoint_pair in endpoints:
    if is_hv(endpoint_pair):
      for p in path(endpoint_pair):
        vents[p] += 1
  return (vents > 1).sum()


def solve2(endpoints) -> int:
  vents = np.zeros(extent(endpoints), dtype=int)
  for endpoint_pair in endpoints:
    for p in path(endpoint_pair):
      vents[p] += 1
  return (vents > 1).sum()



if __name__ == "__main__":
  assert solve1(test()) == 5
  print(f"part 1 = {solve1(live())}")
  assert solve2(test()) == 12
  print(f"part 2 = {solve2(live())}")
