from typing import Callable
from functools import reduce
import operator

class Monkey:
  def __init__(self, items: list[int], op: Callable[[int], int], modulus: int, dests: tuple[int, int]) -> None:
    self.items = items
    self.op = op
    self.modulus = modulus
    self.dests = dests
    self.inspections = 0


def inspect(monkeys: list[Monkey], worry: int, common_modulus: int) -> None:
  for m in monkeys:
    m.inspections += len(m.items)
    new = [(m.op(i) // worry) % common_modulus for i in m.items]
    monkeys[m.dests[True]].items.extend([i for i in new if i % m.modulus == 0])
    monkeys[m.dests[False]].items.extend([i for i in new if i % m.modulus != 0])
    m.items = []


def test() -> list[Monkey]:
  return [
# Monkey0:
#   Starting_items: [79, 98]
#   Operation: "new = old * 19"
#   Test: "divisible by 23"
#     - "If true: throw to monkey 2"
#     - "If false: throw to monkey 3"
    Monkey([79, 98], lambda i: i * 19, 23, (3, 2)),

# Monkey 1:
#   Starting items: 54, 65, 75, 74
#   Operation: new = old + 6
#   Test: divisible by 19
#     If true: throw to monkey 2
#     If false: throw to monkey 0
    Monkey([54, 65, 75, 74], lambda i: i + 6, 19, (0, 2)),

# Monkey 2:
#   Starting items: 79, 60, 97
#   Operation: new = old * old
#   Test: divisible by 13
#     If true: throw to monkey 1
#     If false: throw to monkey 3
    Monkey([79, 60, 97], lambda i: i * i, 13, (3, 1)),

# Monkey 3:
#   Starting items: 74
#   Operation: new = old + 3
#   Test: divisible by 17
#     If true: throw to monkey 0
#     If false: throw to monkey 1
    Monkey([74], lambda i: i + 3, 17, (1, 0))
  ]

def live() -> list[Monkey]:
  return [
# Monkey 0:
#   Starting items: 98, 70, 75, 80, 84, 89, 55, 98
#   Operation: new = old * 2
#   Test: divisible by 11
#     If true: throw to monkey 1
#     If false: throw to monkey 4
    Monkey([98, 70, 75, 80, 84, 89, 55, 98], lambda i: i * 2, 11, (4, 1)),

# Monkey 1:
#   Starting items: 59
#   Operation: new = old * old
#   Test: divisible by 19
#     If true: throw to monkey 7
#     If false: throw to monkey 3
    Monkey([59], lambda i: i * i, 19, (3, 7)),

# Monkey 2:
#   Starting items: 77, 95, 54, 65, 89
#   Operation: new = old + 6
#   Test: divisible by 7
#     If true: throw to monkey 0
#     If false: throw to monkey 5
    Monkey([77, 95, 54, 65, 89], lambda i: i + 6, 7, (5, 0)),

# Monkey 3:
#   Starting items: 71, 64, 75
#   Operation: new = old + 2
#   Test: divisible by 17
#     If true: throw to monkey 6
#     If false: throw to monkey 2
    Monkey([71, 64, 75], lambda i: i + 2, 17, (2, 6)),

# Monkey 4:
#   Starting items: 74, 55, 87, 98
#   Operation: new = old * 11
#   Test: divisible by 3
#     If true: throw to monkey 1
#     If false: throw to monkey 7
    Monkey([74, 55, 87, 98], lambda i: i * 11, 3, (7, 1)),

# Monkey 5:
#   Starting items: 90, 98, 85, 52, 91, 60
#   Operation: new = old + 7
#   Test: divisible by 5
#     If true: throw to monkey 0
#     If false: throw to monkey 4
    Monkey([90, 98, 85, 52, 91, 60], lambda i: i + 7, 5, (4, 0)),

# Monkey 6:
#   Starting items: 99, 51
#   Operation: new = old + 1
#   Test: divisible by 13
#     If true: throw to monkey 5
#     If false: throw to monkey 2
    Monkey([99, 51], lambda i: i + 1, 13, (2, 5)),

# Monkey 7:
#   Starting items: 98, 94, 59, 76, 51, 65, 75
#   Operation: new = old + 5
#   Test: divisible by 2
#     If true: throw to monkey 3
#     If false: throw to monkey 6
    Monkey([98, 94, 59, 76, 51, 65, 75], lambda i: i + 5, 2, (6, 3))
  ]


def solve_impl(monkeys: list[Monkey], gens: int, worry: int) -> int:
  common_modulus = reduce(operator.mul, (m.modulus for m in monkeys))
  for _ in range(gens):
    inspect(monkeys, worry, common_modulus)
  top2 = sorted(m.inspections for m in monkeys)[-2:]
  return top2[0] * top2[1]


def solve1(monkeys: list[Monkey]) -> int:
  return solve_impl(monkeys, 20, 3)


def solve2(monkeys: list[Monkey]) -> int:
  return solve_impl(monkeys, 10000, 1)


if __name__ == "__main__":
  print(f"part 1 test = {solve1(test())}")
  print(f"part 1 live = {solve1(live())}")
  print(f"part 2 test = {solve2(test())}")
  print(f"part 2 live = {solve2(live())}")
