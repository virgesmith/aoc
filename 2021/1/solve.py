
import pandas as pd

s = pd.read_csv("2021/1/input.txt", header=None)

print(f"Part 1: {(s.diff(1) > 0).sum()[0]}")
print(f"Part 2: {(s.rolling(window=3).sum().diff(1) > 0).sum()[0]}")