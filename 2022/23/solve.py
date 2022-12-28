from collections import Counter
import numpy as np

GROUND = 0
ELF = 1

N = 0
S = 1
W = 2
E = 3

dir_str = ["N", "S", "W", "E"]

offsets = [
  [(-1, -1), (-1,  0), (-1,  1)],
  [( 1, -1), ( 1,  0), ( 1,  1)],
  [(-1, -1), ( 0, -1), ( 1, -1)],
  [(-1,  1), ( 0,  1), ( 1,  1)],
]


all_offsets = [(-1, -1), (-1,  0), (-1,  1),
               ( 0, -1),           ( 0,  1),
               ( 1, -1), ( 1,  0), ( 1,  1)]

ElfPositions_t = dict[tuple[int, int], tuple[int, int] | None]

def as_dict(elf_map: np.ndarray) -> ElfPositions_t:
  iter = np.nditer(elf_map, flags=['multi_index'])
  return {iter.multi_index: None for i in iter if i == ELF}  # type: ignore[misc]


def test() -> ElfPositions_t:
  data = """..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
.............."""
  elf_map = np.array([list(map(lambda p: ELF if p == "#" else GROUND, line)) for line in data.splitlines()])
  return as_dict(elf_map)


def live() -> ElfPositions_t:
  with open("2022/23/input.txt") as fd:
    elf_map = np.array([list(map(lambda p: ELF if p == "#" else GROUND, line)) for line in fd.read().splitlines()])
  return as_dict(elf_map)


class Elves:
  elves: ElfPositions_t

  def __init__(self, elves: ElfPositions_t) -> None:
    self.remap(elves)

  def propose_moves(self, turn: int) -> None:
    for dir in range(4):
      for elf in self.elves:
        if not self.elves[elf]:
          self.elves[elf] = _propose_move(elf, self.map, (turn + dir) % 4)
    self.elves = _remove_collisions(self.elves)

  def move(self) -> int:
    num_moves = sum(1 for elf in self.elves if self.elves[elf] and self.elves[elf] != elf)
    new_elves: ElfPositions_t = {}
    for elf in self.elves:
      new_elves[self.elves[elf] if self.elves[elf] else elf] = None  # type: ignore[index]
    self.remap(new_elves)
    return num_moves

  def remap(self, elves: ElfPositions_t) -> None:
    ymin = min(elf[0] for elf in elves) - 1
    ymax = max(elf[0] for elf in elves) + 1
    xmin = min(elf[1] for elf in elves) - 1
    xmax = max(elf[1] for elf in elves) + 1
    self.map = np.full((ymax - ymin + 1, xmax - xmin + 1), GROUND)
    self.elves = {}
    for elf in elves:
      new_pos = add(elf, (-ymin, -xmin))
      self.elves[new_pos] = None
      self.map[new_pos] = ELF

  def print(self) -> None:
    chars = [".", "#"]
    for y in range(self.map.shape[0]):
      print("".join([chars[x] for x in self.map[y, :]]))


def add(p: tuple[int, int], o: tuple[int, int]) -> tuple[int, int]:
  return (p[0] + o[0], p[1] + o[1])


def all_free(elf: tuple[int, int], elf_map: np.ndarray) -> bool:
  return all(elf_map[p] == GROUND for p in (add(elf, o) for o in all_offsets))


def free(elf: tuple[int, int], dir: int, elf_map: np.ndarray) -> bool:
  points = (add(elf, o) for o in offsets[dir])
  # all() is True if valid_points is empty!
  if not points:
    return False
  return all(elf_map[p] == GROUND for p in points)


def _propose_move(elf, map, dir) -> tuple[int, int] | None:
  if all_free(elf, map):
    return elf
  if free(elf, dir, map):
    return add(elf, offsets[dir][1])
  return None


def _remove_collisions(proposed: ElfPositions_t) -> ElfPositions_t:
  count = Counter(proposed.values())
  for k in count:
    if count[k] > 1:
      for i in proposed:
        if proposed[i] == k:
          proposed[i] = None
  return proposed


def solve1(elf_positions: ElfPositions_t) -> int:
  elves = Elves(elf_positions)
  for turn in range(10):
    elves.propose_moves(turn)
    elves.move()
  return (elves.map[1:-1, 1:-1] == GROUND).sum()


def solve2(elf_positions: ElfPositions_t) -> int:
  elves = Elves(elf_positions)
  turn = 0
  while True:
    elves.propose_moves(turn)
    num_moves = elves.move()
    print(turn + 1, num_moves, elves.map.shape)
    if num_moves == 0:
      break
    turn += 1

  # print_map(elf_map)
  return turn + 1


if __name__ == "__main__":
  assert solve1(test()) == 110
  print(f"part 1 = {solve1(live())}")  # 4218
  assert solve2(test()) == 20
  print(f"part 2 = {solve2(live())}") # 976

