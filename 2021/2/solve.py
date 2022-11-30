import pandas as pd
from io import StringIO


def live() -> pd.DataFrame:
  return pd.read_csv("2021/2/input.txt", delimiter=" ", header=None)


def test() -> pd.DataFrame:

  test = """
    forward 5
    down 5
    forward 8
    up 3
    down 8
    forward 2
"""  # indent here causes an extra empty row, and changes the col 2 dtype to float
  return pd.read_csv(StringIO(test), delimiter=" ", header=None, skipinitialspace=True)


def part1(s: pd.DataFrame) -> int:
  s["dx"] = s.apply(lambda r: r[1] if r[0] == "forward" else 0, axis=1)
  s["dy"] = s.apply(lambda r: r[1] if r[0] == "down" else -r[1] if r[0] == "up" else 0, axis=1)
  return s.dx.sum() * s.dy.sum()


def part2(s: pd.DataFrame) -> int:
  # part 2
  s["da"] = s.apply(lambda r: r[1] if r[0] == "down" else -r[1] if r[0] == "up" else 0, axis=1)
  s["a"] = s.da.cumsum()

  def m(row):
    dx = dy = 0
    if row[0] == "forward":
      dx = row[1]
      dy = row[1] * row["a"]
    return dx, dy

  s[["dx", "dy"]] = s.apply(m, axis=1, result_type="expand")
  return s.dx.sum() * s.dy.sum()

if __name__ == "__main__":
  print(f"test part1: {part1(test())}")
  print(f"test part2: {part2(test())}")
  print(f"part1: {part1(live())}")
  print(f"part2: {part2(live())}")