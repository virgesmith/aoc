
def test() -> list[str]:
  data = """mjqjpqmgbljsphdztnvjfqwrcgsmlb
bvwbjplbgvbhsrlpgdmjqwftvncz
nppdvjthqldpwncqszvftbrmjlhg
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
"""
  return data.splitlines()


def live() -> str:
  with open("2022/6/input.txt") as fd:
    return fd.read()


def solve_impl(a: str, length: int) -> int:
  s = set()
  i = 0
  while len(s) < length - 1:
    s.add(a[i])
    i += 1
  while i < len(a):
    c = a[i]
    s.add(c)
    if len(s) >= length and len({*a[i-length:i]}) == length:
      return i
    i += 1
  return -1


def solve1(a: list[str]) -> int:
  return solve_impl(a, 4)


def solve2(a: list[str]) -> int:
  return solve_impl(a, 14)


if __name__ == "__main__":
  assert solve1(test()[0]) == 7
  assert solve1(test()[1]) == 5
  assert solve1(test()[2]) == 6
  assert solve1(test()[3]) == 10
  assert solve1(test()[4]) == 11
  print(f"part 1 = {solve1(live())}")
  assert solve2(test()[0]) == 19
  assert solve2(test()[1]) == 23
  assert solve2(test()[2]) == 23
  assert solve2(test()[3]) == 29
  assert solve2(test()[4]) == 26
  print(f"part 2 = {solve2(live())}")
