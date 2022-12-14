
def test() -> list[str]:
  data = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""
  return ((line.split(" | ")[0].split(" "), line.split(" | ")[1].split(" ")) for line in data.splitlines())


def live() -> list[str]:
  with open("2021/8/input.txt") as fd:
    return ((line.split(" | ")[0].split(" "), line.split(" | ")[1].split(" ")) for line in fd.read().splitlines())


def solve1(a: list[str]) -> int:
  return sum(sum(len(n) in [2, 3, 4, 7] for n in line[1]) for line in a)


def solve2(a: list[str]) -> int:
  a = list(a)
  digits = []
  for i, line in enumerate(a):
    m = {}
    for n in line[0]:
      if len(n) == 2:
        m[1] = n
      elif len(n) == 3:
        m[7] = n
      elif len(n) == 4:
        m[4] = n
      elif len(n) == 7:
        m[8] = n
    d = [None, None, None, None]
    for j, n in enumerate(line[1]):
      if len(n) == 2:
        d[j] = "1"
      elif len(n) == 3:
        d[j] = "7"
      elif len(n) == 4:
        d[j] = "4"
      elif len(n) == 7:
        d[j] = "8"
      elif len(n) == 6:
        if set(m[4]).issubset(n):
          d[j] = "9"
        elif set(m[7]).issubset(n):
          d[j] = "0"
        else:
          d[j] = "6"
      elif len(n) == 5:
        if set(m[1]).issubset(n):
          d[j] = "3"
        elif len(set(n).difference(m[4])) == 2:
          d[j] = "5"
        else:
          d[j] = "2"

    digits.append(int("".join(d)))
  return sum(digits)


if __name__ == "__main__":
  assert solve1(test()) == 26
  print(f"part 1 live = {solve1(live())}")
  assert solve2(test()) == 61229
  print(f"part 2 live = {solve2(live())}")
