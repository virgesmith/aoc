from io import StringIO
from collections import defaultdict


def test():
    input = """\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""
    return StringIO(input).read().splitlines()[0].split(",")


def live():
    with open("2023/15/input.txt") as fd:
        return fd.read().splitlines()[0].split(",")


def hash(string: str) -> int:
    hash = 0
    for c in string:
        hash = ((hash + ord(c)) * 17) % 256
    return hash


def solve1(seq: list[str]) -> int:
    return sum(hash(entry) for entry in seq)


def solve2(seq: list[str]) -> int:
    hashmap = defaultdict(lambda: {})
    for entry in seq:
        if "-" in entry:
            key = entry[:-1]
            if key in hashmap[hash(key)]:
                del hashmap[hash(key)][key]
        elif "=" in entry:
            key, value = entry.split("=")
            hashmap[hash(key)] |= {key: int(value)}

    return sum(
        (h + 1) * (i + 1) * hashmap[h][k]
        for h in range(256)
        for i, k in enumerate(hashmap[h])
    )


if __name__ == "__main__":
    print(f"part 1 test = {solve1(test())}")
    print(f"part 1 live = {solve1(live())}")
    print(f"part 2 test = {solve2(test())}")
    print(f"part 2 live = {solve2(live())}")
