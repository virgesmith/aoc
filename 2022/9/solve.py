from functools import reduce
import numpy as np

def test() -> list[str]:
  data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""
  return data.splitlines()


def live() -> list[str]:
  with open("2022/9/input.txt") as fd:
    return fd.read().splitlines()


v = {
  "U": np.array([0, 1]),
  "D": np.array([0, -1]),
  "L": np.array([-1, 0]),
  "R": np.array([1, 0]),
}


def tail_move(h: np.ndarray, t: np.ndarray) -> np.ndarray:
  theta = h - t
  delta = theta @ theta

  if delta < 4.0:
    return np.array([0,0])
  elif delta == 4 or delta == 8:
    return theta // 2
  elif delta == 5:
    return np.clip(theta, -1, 1)
  else:
    raise RuntimeError(f"too far: {delta}")


def unroll(moves: list[str]) -> list[str]:
  return reduce(list.__add__, ([d[0]]*int(d[1]) for d in (m.split(" ") for m in moves)))


def solve1(moves: list[str]) -> int:

  h = np.array([0, 0])
  t = np.array([0, 0])

  tail_history = [(t[0], t[1])]
  for m in unroll(moves):
    h += v[m]
    t += tail_move(h, t)
    tail_history.append((t[0], t[1]))

  return len(set(tail_history))


def solve2(moves: list[str]) -> int:
  rope = [np.array([0, 0]) for _ in range(10)]

  tail_history = [(rope[-1][0], rope[-1][1])]
  for m in unroll(moves):
    rope[0] += v[m]
    for i in range(9):
      rope[i+1] += tail_move(rope[i], rope[i+1])
    tail_history.append((rope[-1][0], rope[-1][1]))
  return len(set(tail_history))


if __name__ == "__main__":
  print(f"part 1 test = {solve1(test())}")
  print(f"part 1 live = {solve1(live())}")
  print(f"part 2 test = {solve2(test())}")
  print(f"part 2 live = {solve2(live())}")

# part 1 test = 13
# part 1 live = 6745
# part 2 test = 1
# part 2 live = 2793