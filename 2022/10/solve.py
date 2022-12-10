from typing import Generator

def test() -> list[str]:
  data = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""
  return data.splitlines()


def live() -> list[str]:
  with open("2022/10/input.txt") as fd:
    return fd.read().splitlines()


def decode(s: str) -> int | None:
  if len(s) == 4:
    return None
  else:
    return int(s.split(" ")[1])


def run(code: list[int|None]) -> list[int]:
  state = [1]
  for instr in code:
    state.append(state[-1])
    if instr:
      state.append(state[-1] + instr)
  return state


def solve1(a: list[str]) -> int:
  code = [decode(s) for s in a]
  state = run(code)

  cycles = [20, 60, 100, 140, 180, 220]
  return sum(c * state[c-1] for c in cycles)


def render(screen: Generator[str, None, None]) -> None:
  for y in range(6):
    print("".join([next(screen) for _ in range(40)]))


def solve2(a: list[str]) -> int:
  code = [decode(s) for s in a]
  state = run(code)

  screen = ("#" if abs(state[i] - i % 40) < 2 else "." for i in range(240))
  render(screen)
  return 0


if __name__ == "__main__":
  print(f"part 1 test = {solve1(test())}")
  print(f"part 1 live = {solve1(live())}")
  print(f"part 2 test = {solve2(test())}")
  print(f"part 2 live = {solve2(live())}")
