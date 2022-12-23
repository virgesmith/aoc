import re
import numpy as np
import matplotlib.pyplot as plt

VOID = 0
PATH = 1
ROCK = 2
ROUTE = 3

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

Y = 0
X = 1

dir_str = ["R", "D", "L", "U"]

lookup = {
  " ": VOID,
  ".": PATH,
  "#": ROCK,
}


def parse(data: list[str]) -> tuple[np.ndarray, list]:
  map = [[lookup[c] for c in line] for line in data[:-2]]
  width = max(len(line) for line in map)
  for line in map:
    if len(line) < width:
      line.extend([VOID] * (width - len(line)))
  dir = re.split(r'(-?\d*\.?\d+)', data[-1])
  while "" in dir:
    dir.remove("")
  for i, d in enumerate(dir):
    if d.isdigit():
      dir[i] = int(d)

  return np.array(map, dtype=int), dir



def test() -> tuple[np.array, list[str | int]]:
  data = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5""".splitlines()
  return parse(data)


def live() -> list[str]:
  with open("2022/22/input.txt") as fd:
    data = fd.read().splitlines()
  return parse(data)



edge_map_test = {
  (( 0, 2), UP):    ((0, 0), DOWN), # A
  (( 1, 0), UP):    ((-1, 2), DOWN), # A
  (( 0, 2), LEFT):  ((0, 1), DOWN), # B
  (( 1, 1), UP):    ((0, 1), RIGHT), # B
  (( 0, 2), RIGHT): ((2, 4), LEFT), # C
  (( 2, 3), RIGHT): ((0, 3), LEFT), # C
  (( 1, 0), LEFT):  ((3, 3), UP), # D
  (( 2, 3), DOWN):  ((1, -1), RIGHT), # D
  (( 1, 2), RIGHT): ((1, 3), DOWN), # E
  (( 2, 3), UP):    ((1, 3), LEFT), # E
  (( 1, 0), DOWN):  ((3, 2), UP), # F
  (( 2, 2), DOWN):  ((2, 0), UP), # F
  (( 1, 1), DOWN):  ((2, 1), RIGHT), # G
  (( 2, 2), LEFT):  ((2, 1), UP), # G
}


edge_map_live = {
  (( 0, 1), UP):  ((3, -1), RIGHT), # A
  (( 3, 0), LEFT):  ((-1, 1), DOWN), # A
  (( 0, 2), UP):  ((4, 0), UP), # B
  (( 3, 0), DOWN):  ((-1, 2), DOWN), # B
  (( 0, 1), LEFT):  ((2, -1), RIGHT),
  (( 2, 0), LEFT):  ((0, 0), RIGHT), # C
  (( 0, 2), RIGHT):  ((2, 2), LEFT), # D
  (( 2, 1), RIGHT): ((0, 3), LEFT),
  (( 1, 1), LEFT):  ((1, 0), DOWN), # E
  (( 2, 0), UP):  ((1, 0), RIGHT),
  (( 0, 2), DOWN):  ((1, 2), LEFT), # F
  (( 1, 1), RIGHT):  ((1, 2), UP),
  (( 2, 1), DOWN):  ((3, 1), LEFT), # G
  (( 3, 0), RIGHT):  ((3, 1), UP),
}


def out_coord(face, dir, face_size):
  if dir == RIGHT:
    x = [(face[X] + 1) * face_size] * face_size
    y = [face[Y] * face_size + i for i in range(face_size)]
  elif dir == DOWN:
    x = [(face[X] + 1) * face_size - 1 - i for i in range(face_size)]
    y = [(face[Y] + 1) * face_size] * face_size
  elif dir == LEFT:
    x = [face[X] * face_size - 1] * face_size
    y = [(face[Y] + 1) * face_size - 1 - i for i in range(face_size)]
  elif dir == UP:
    x = [face[X] * face_size + i for i in range(face_size)]
    y = [face[Y] * face_size - 1] * face_size
  return list((yx, dir) for yx in zip(y, x))


def point_mappings(edge_map, face_size):
  mappings = {}
  for k in edge_map:
    from_edge, from_dir = k
    to_edge, to_dir = edge_map[k]
    from_points = out_coord(from_edge, from_dir, face_size)
    to_points = out_coord(to_edge, to_dir, face_size)
    mappings |= dict(zip(from_points, to_points))
  return mappings


def step(p, orient, bounds) -> tuple[int, int]:
  if orient == LEFT:
    return p[Y], (p[X] - 1) % bounds[X]
  elif orient == DOWN:
    return (p[Y] + 1) % bounds[Y], p[X]
  elif orient == RIGHT:
      return p[Y], (p[X] + 1) % bounds[X]
  elif orient == UP:
      return (p[Y] - 1) % bounds[Y], p[X]



def step_cube(p, orient, map, mappings) -> tuple[tuple[int, int], int]:
  if orient == LEFT:
    p_new = p[Y], p[X] - 1
  elif orient == DOWN:
    p_new = p[Y] + 1, p[X]
  elif orient == RIGHT:
    p_new = p[Y], p[X] + 1
  elif orient == UP:
    p_new = p[Y] - 1, p[X]
  else:
    raise ValueError("invalid orientation")

  if (p_new, orient) not in mappings:
    if map[p_new] == ROCK:
      return p, orient
    else:
      return p_new, orient

  else:
    p_newer, orient_new = mappings[(p_new, orient)]
    print(f"crossed edge {p_new} {dir_str[orient]} -> {p_newer} {dir_str[orient_new]}")
    if map[p_newer] == ROCK:
      return p, orient
    else:
      return p_newer, orient_new


def move(p, n, map, orient):
  for _ in range(n):
    p_new = step(p, orient, map.shape)
    while map[p_new] == VOID:
      p_new = step(p_new, orient, map.shape)
    if map[p_new] == ROCK:
      return p
    p = p_new
    map[p] = ROUTE
  return p


def move_cube(p, n, map, orient, mappings):
  face_size = int(np.sqrt(np.product(map.shape) / 12))
  for _ in range(n):
    p_new, orient = step_cube(p, orient, map, mappings)
    p = p_new
    map[p] = ROUTE
  return p, orient


def solve1(map: np.ndarray, directions: list[str | int]) -> int:
  # move to start
  p = (0, 0)
  while map[p] != PATH:
    p = (0, p[X]+1)
  orient = RIGHT

  map[p] = ROUTE

  print(directions)

  while directions:
    order = directions.pop(0)
    if order == "L":
      orient = (orient - 1) % 4
      print(f"Turned L, direction is {dir_str[orient]}")
    elif order == "R":
      orient = (orient + 1) % 4
      print(f"Turned R, direction is {dir_str[orient]}")
    else:
      p = move(p, order, map, orient)
      print(f"Moved to {p}")

  return 1000 * (p[Y] + 1) + 4 * (p[X] + 1) + orient


def solve2(map: np.ndarray, directions: list[str | int], edge_map: dict) -> int:
  # move to start
  p = (0, 0)
  while map[p] != PATH:
    p = (0, p[X]+1)
  orient = RIGHT

  map[p] = ROUTE

  face_size = int(np.sqrt(np.product(map.shape) // 12))

  mappings = point_mappings(edge_map, face_size)

  # for m in mappings:
  #   print(f"{m[0]} {dir_str[m[1]]} -> {mappings[m][0]} {dir_str[mappings[m][1]]}")
  # print(directions)

  while directions:
    order = directions.pop(0)
    if order == "L":
      orient = (orient - 1) % 4
      print(f"Turned L, direction is {dir_str[orient]}")
    elif order == "R":
      orient = (orient + 1) % 4
      print(f"Turned R, direction is {dir_str[orient]}")
    else:
      p, orient = move_cube(p, order, map, orient, mappings)
      print(f"Moved to {p}")

  plt.imshow(map)
  plt.show()
  return 1000 * (p[Y] + 1) + 4 * (p[X] + 1) + orient


if __name__ == "__main__":
  assert solve1(*test()) == 6032
  print(f"part 1 = {solve1(*live())}") # 146092
  assert solve2(*test(), edge_map_test) == 5031
  print(f"part 2 = {solve2(*live(), edge_map_live)}") # 110342
