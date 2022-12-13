from functools import cmp_to_key
import numpy as np


def test() -> list[str]:
  data = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""
  return data.splitlines()


def live() -> list[str]:
  with open("2022/13/input.txt") as fd:
    return fd.read().splitlines()


def compare(left: int | list, right: int | list) -> int:
  match left, right:
    case int(), int():
      return np.sign(left - right)
    case list(), int():
      return compare(left, [right])
    case int(), list():
      return compare([left], right)
    case [], []:
      return 0
    case _, []:
      return 1
    case [], _:
      return -1
    case _:
      return compare(left[0], right[0]) or compare(left[1:], right[1:])


def solve1(a: list[str]) -> int:
  left = []
  right = []
  for i in range(0, len(a), 3):
    left.append(eval(a[i]))
    right.append(eval(a[i+1]))

  return sum(max(-compare(left[i], right[i]), 0) * (i + 1) for i in range(len(left)))


def solve2(a: list[str]) -> int:
  packets = []
  for i in range(0, len(a), 3):
    packets.append(eval(a[i]))
    packets.append(eval(a[i+1]))
  packets.append([[2]])
  packets.append([[6]])

  packets = sorted(packets, key=cmp_to_key(compare))
  return (1 + packets.index([[2]])) * (1 + packets.index([[6]]))


if __name__ == "__main__":
  assert solve1(test()) == 13
  print(f"part 1 live = {solve1(live())}")
  assert solve2(test()) == 140
  print(f"part 2 live = {solve2(live())}")
