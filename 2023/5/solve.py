from io import StringIO


def test1():
    input = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

"""
    return StringIO(input).read().splitlines()


def live():
    with open("2023/5/input.txt") as fd:
        return fd.read().splitlines()


def solve1(strings: list[str]) -> int:
    seeds = [int(n) for n in strings[0].split()[1:]]
    return solve_impl(strings, seeds)


def solve_impl(strings: list[str], seeds: list[int]):
    dsts, srcs, lengths = [], [], []
    for string in strings[2:]:
        if "map" in string:
            to, _, frm = string.split()[0].split("-")
            print(f"{to}->{frm}")
            dsts, srcs, lengths = [], [], []
            continue
        if string == "":
            for i, seed in enumerate(seeds):
                for j in range(len(dsts)):
                    if seed - srcs[j] >= 0 and seed - srcs[j] < lengths[j]:
                        seeds[i] += dsts[j] - srcs[j]
                        break
            continue
        dst, src, length = [int(s) for s in string.split()]
        dsts.append(dst)
        srcs.append(src)
        lengths.append(length)
    return min(seeds)


def solve2(strings: list[str]) -> int:
    seed_data = [int(n) for n in strings[0].split()[1:]]
    seeds = list(zip(seed_data[::2], seed_data[1::2]))

    print(seeds)
    maps = []
    for string in strings[2:6]:
        if "map" in string:
            to, _, frm = string.split()[0].split("-")
            print(f"{to}->{frm}")
            maps = []
            continue
        if string == "":
            print(maps)
            for i, seed in enumerate(seeds):
                new_seeds = []
                for j in range(len(maps)):
                    new_seeds.extend(intersect_split(maps[j], seed))
                    # if seed - srcs[j] >= 0 and seed - srcs[j] < lengths[j]:
                    #     seeds[i] += dsts[j] - srcs[j]
                    #     break
                print(new_seeds)
            seeds = new_seeds
            print(seeds)
            continue
        dst, src, length = [int(s) for s in string.split()]
        maps.append((src, length, dst - src))

    return 0


def intersect_split(
    a: tuple[int, int, int], b: tuple[int, int]
) -> list[tuple[int, int]]:
    if b[0] + b[1] < a[0] and b[0] > a[0] + a[1]:
        raise ValueError("b>a!")
    elif b[0] + b[1] < a[0] or b[0] > a[0] + a[1]:
        print("b outside a")
        return [b]
    elif b[0] >= a[0] and b[0] + b[1] <= a[0] + a[1]:
        print("b left intersects a")
        return [(b[0] + a[2], b[1])]
    elif b[0] < a[0]:
        print("b right intersects a")
        x = a[0] - b[0]
        return [(b[0], x), (a[0] + a[2], b[1] - x)]
    else:
        x = a[0] + a[1] - b[0]
        return [(b[0] + a[2], x), (a[0] + a[1], b[1] - x)]


if __name__ == "__main__":
    print(f"part 1 test = {solve1(test1())}")
    print(f"part 1 live = {solve1(live())}")
    print(f"part 2 test = {solve2(test1())}")
#    print(f"part 2 live = {solve2(live())}")

# print(intersect_split((25, 50, 100), (10, 10)))
# print(intersect_split((25, 50, 100), (80, 10)))
# print(intersect_split((25, 50, 100), (35, 10)))
# print(intersect_split((25, 50, 100), (20, 15)))
# print(intersect_split((25, 50, 100), (65, 15)))
