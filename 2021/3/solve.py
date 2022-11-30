from io import StringIO
import pandas as pd

def test():
  test = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""
  return pd.read_fwf(StringIO(test), widths=[1] * 5, header=None)

def live():
  return pd.read_fwf("2021/3/input.txt", widths=[1] * 12, header=None)

def part1(s: pd.DataFrame) -> int:
  bin = round(s.mean()).astype(int).to_list()
  gamma = int("".join([str(b) for b in bin]), 2)
  epsilon = int("".join([str(1-b) for b in bin]), 2)
  return gamma * epsilon

def part2(s: pd.DataFrame) -> int:
  s1 = s.copy()
  for col in s1.columns:
    s1 = s1[s1[col] == round(s1[col].mean()+0.00001)]
  bin = s1.iloc[0].to_list()
  oxygen = int("".join([str(b) for b in bin]), 2)
  for col in s.columns:
    s = s[s[col] == round(1 - s[col].mean())]
    if len(s) == 1:
      break
  bin = s.iloc[0].to_list()
  co2 = int("".join([str(b) for b in bin]), 2)
  return oxygen * co2


print(f"test part1: {part1(test())}")
print(f"part1: {part1(live())}")

print(f"test part2: {part2(test())}")
print(f"part2: {part2(live())}")

