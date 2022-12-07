
def test() -> list[str]:
  data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""
  return data.splitlines()


def live() -> list[str]:
  with open("2022/7/input.txt") as fd:
    return fd.read().splitlines()


def dir(cwd: list[str]) -> str:
  return f'/{"/".join(cwd)}'


def solve1(a: list[str]) -> int:
  lines = [line.split(" ") for line in a]
  cwd = []
  tree = { dir(cwd): 0 }
  for line in lines:
    if line[0] == "$":
      if line[1] == "cd":
        if line[2] == "..":
          cwd.pop()
        elif line[2] != "/":
          cwd.append(line[2])
      elif line[1] == "ls":
        pass
    elif line[0] == "dir":
      tree[dir(cwd + [line[1]])] = 0
    else:
      tree[dir(cwd)] += int(line[0])

  totals = {}
  for d in tree:
    totals[d] = sum(tree[d2] for d2 in tree if d in d2)

  total = sum(totals[d] for d in totals if totals[d] <= 100000)

  return total, totals

def solve2(a: list[str]) -> int:
  _, totals = solve1(a)
  unused = 70000000 - totals["/"]
  to_free = 30000000 - unused

  return sorted(totals[d] for d in totals if totals[d] >= to_free)[0]

if __name__ == "__main__":
  print(f"part 1 test = {solve1(test())[0]}")
  print(f"part 1 live = {solve1(live())[0]}")
  print(f"part 2 test = {solve2(test())}")
  print(f"part 2 live = {solve2(live())}")
