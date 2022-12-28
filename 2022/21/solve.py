from typing import Optional, Protocol


UNARY_OPS = {
  "-": lambda x: -x,
}

BINARY_OPS = {
  "+": lambda x, y: x + y,
  "-": lambda x, y: x - y,
  "*": lambda x, y: x * y,
  "/": lambda x, y: x / y,
}


class Expression(Protocol):
  def eval(self) -> int:
    ...

  def find(self, name: str) -> Optional["Expression"]:
    ...


class Scalar:
  def __init__(self, name: str, n: int):
    self.name = name
    self.n = n

  def eval(self) -> int:
    return self.n

  def find(self, name: str) -> Expression | None:
    if self.name == name:
      return self
    return None

  def __repr__(self) -> str:
    return f'{{"{self.name}": {self.n}}}'


class BinaryOp:
  def __init__(self, name: str, op: str, left: Expression, right: Expression):
    self.name = name
    self.op = op
    self.left = left
    self.right = right

  def eval(self)-> int:
    return BINARY_OPS[self.op](self.left.eval(), self.right.eval())

  def find(self, name: str) -> Expression | None:
    if self.name == name:
      return self
    left = self.left.find(name)
    if left:
      return left
    return self.right.find(name)

  def __repr__(self) -> str:
    return f'{{"{self.name}": {{"{self.op}": [{self.left}, {self.right}]}}}}'


class UnaryOp:
  def __init__(self, name: str, op: str, operand: Expression) -> None:
    self.name = name
    self.op = op
    self.operand = operand

  def eval(self) -> int:
    return UNARY_OPS[self.op](self.operand.eval())

  def find(self, name: str) -> Expression | None:
    if self.name == name:
      return self
    return self.operand.find(name)

  def __repr__(self) -> str:
    return f'{{"{self.name}": {{"{self.op}": {self.operand}}}}}'


def expression_factory(expression_id: str, all_expressions: dict[str, list[str]]) -> Expression:
  expression = all_expressions[expression_id]
  if len(expression) == 1:
    return Scalar(expression_id, int(expression[0]))
  if len(expression) == 2:
    return UnaryOp(expression_id, expression[0], expression_factory(expression[1], all_expressions))
  elif len(expression) == 3:
    return BinaryOp(expression_id,
                    expression[1],
                    expression_factory(expression[0], all_expressions),
                    expression_factory(expression[2], all_expressions))
  raise ValueError("expression not understood")



def test() -> dict[str, list[str]]:
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
  return {line.split(": ")[0]: line.split(": ")[1].split(" ") for line in data.splitlines()}


def live() -> dict[str, list[str]]:
  with open("2022/21/input.txt") as fd:
    return {line.split(": ")[0]: line.split(": ")[1].split(" ") for line in fd.read().splitlines()}


def solve1(expressions: dict[str, list[str]]) -> int:
  tree = expression_factory("root", expressions)
  return int(tree.eval())


def solve2(expressions: dict[str, list[str]]) -> int:
  expressions["root"] = [expressions["root"][0], "-", expressions["root"][2]]
  tree = expression_factory("root", expressions)
  humn = tree.find("humn")

  dx = 0.1
  f = tree.eval()
  while f != 0:
    x = humn.n
    # 1st deriv
    humn.n += dx
    df = (tree.eval() - f) / dx
    # Newton
    x -= f / df
    humn.n = x
    f = tree.eval()
  return int(x)


if __name__ == "__main__":
  assert solve1(test()) == 152
  print(f"part 1 = {solve1(live())}")
  assert solve2(test()) == 301
  print(f"part 2 = {solve2(live())}")
