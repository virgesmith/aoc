
import numpy as np

def test() -> list[str]:
  data = """30373
25512
65332
33549
35390"""
  return data.splitlines()


def live() -> list[str]:
  with open("2022/8/input.txt") as fd:
    return fd.read().splitlines()


def visible(a: np.ndarray, axis: int, flip: bool) -> np.ndarray:
  if flip:
    x = np.flip(a + 1, axis=axis)
  else:
    x = a + 1
  m = np.diff(np.maximum.accumulate(x, axis), axis=axis, prepend=0)
  if flip:
    m = np.flip(m, axis)
  return m > 0


def solve1(a: list[str]) -> int:
  f = np.array([[int(x) for x in list(s)] for s in a ])

  left = visible(f, 1, False)
  right = visible(f, 1, True)
  top = visible(f, 0, False)
  bottom = visible(f, 0, True)

  return np.logical_or.reduce((left, right, top, bottom)).sum()


def distprod(yt: int, xt: int, f: np.ndarray) -> int:
  ny = f.shape[0]
  nx = f.shape[1]
  h = f[yt, xt]

  up = 1
  y = yt - 1
  while y > 0 and f[y, xt] < h:
    y -= 1
    up += 1

  down = 1
  y = yt + 1
  while y < ny - 1 and f[y, xt] < h:
    y += 1
    down += 1

  left = 1
  x = xt - 1
  while x > 0 and f[yt, x] < h:
    x -= 1
    left += 1

  right = 1
  x = xt + 1
  while x < nx - 1 and f[yt, x] < h:
    x += 1
    right += 1

  return up * left * right * down


def solve2(a: list[str]) -> int:
  f = np.array([[int(x) for x in list(s)] for s in a ])
  return max(distprod(y, x, f) for (y, x), _ in np.ndenumerate(f))


if __name__ == "__main__":
  print(f"part 1 test = {solve1(test())}")
  print(f"part 1 live = {solve1(live())}")
  print(f"part 2 test = {solve2(test())}")
  print(f"part 2 live = {solve2(live())}")


