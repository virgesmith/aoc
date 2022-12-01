
from io import StringIO

def test():
  input = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""
  return StringIO(input).read().splitlines()

def live():
  with open("2022/1/input.txt") as fd:
    return fd.read().splitlines()


def solve_impl(a: list[str]) -> list[int]:
  splits = [i for i in range(len(a)) if a[i] == ""]
  brackets = [[int(n) for n in a[i + 1:j]] for i, j in zip([-1]+splits, splits+[len(a)])]
  return [sum(elf) for elf in brackets]


def solve1(a: list[str]) -> int:
  return max(solve_impl(a))

def solve2(a: list[str]) -> list[int]:
  return sum(sorted(solve_impl(a))[-3:])

if __name__ == "__main__":
  print(solve1(test()))
  print(solve1(live()))
  print(solve2(test()))
  print(solve2(live()))

# 24000
# 67027
# 45000
# 197291
