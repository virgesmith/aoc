from typing import Callable, Protocol


BINARY_OPS = {
  "+": lambda x, y: x + y,
  "-": lambda x, y: x - y,
  "*": lambda x, y: x * y,
  "/": lambda x, y: x / y,
}


class Expression(Protocol):
  def eval(self, lookup: dict[str, "Expression"]) -> int:
    ...


class Value:
  def __init__(self, n: int):
    self.n = n

  def eval(self, _: dict[str, Expression]) -> int:
    return self.n


class BinaryOp:
  def __init__(self, op: Callable[[int, int], int], left: str, right: str):
    self.op = op
    self.left = left
    self.right = right

  def eval(self, lookup: dict[str, Expression]):
    return self.op(lookup[self.left].eval(lookup), lookup[self.right].eval(lookup))


def expression_factory(a: list[str]) -> Expression:
  if len(a) == 1:
    return Value(int(a[0]))
  elif len(a) == 3:
    return BinaryOp(BINARY_OPS[a[1]], a[0], a[2])
  raise ValueError("expression not understood")


def test() -> dict[str, Expression]:
  data = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""
  return {line.split(": ")[0]: expression_factory(line.split(": ")[1].split(" ")) for line in data.splitlines()}


def live() -> dict[str, Expression]:
  with open("2022/21/input.txt") as fd:
    return {line.split(": ")[0]: expression_factory(line.split(": ")[1].split(" ")) for line in fd.read().splitlines()}


def solve1(expressions: dict[str, Expression]) -> int:
  return int(expressions["root"].eval(expressions))


def solve2(expressions: dict[str, Expression]) -> int:
  expressions["root"] = BinaryOp(BINARY_OPS["-"], expressions["root"].left, expressions["root"].right)

  dx = 0.1
  f = expressions["root"].eval(expressions)
  while f != 0:
    x = expressions["humn"].n
    # 1st deriv
    expressions["humn"].n += dx
    df = (expressions["root"].eval(expressions) - f) / dx
    # Newton
    x -= f / df
    expressions["humn"].n = x
    f = expressions["root"].eval(expressions)
  return int(x)


if __name__ == "__main__":
  assert solve1(test()) == 152
  print(f"part 1 = {solve1(live())}")
  assert solve2(test()) == 301
  print(f"part 2 = {solve2(live())}")
