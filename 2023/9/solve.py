from io import StringIO

def test():
    input = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
    return StringIO(input).read().splitlines()

def diff(x: list[int]) -> list[int]:
    return [xi - x[i] for i, xi in enumerate(x[1:])]


def integrate(x: list[int]) -> list[int]:
    return [sum(x[:i]) for i in range(1, len(x) + 1)]


def live():
    with open("2023/9/input.txt") as fd:
        return fd.read().splitlines()


def solve1(strings: list[str]) -> int:
    sum = 0
    for string in strings:
        seqs = [[int(s) for s in string.split()]]
        while not all(s==seqs[-1][0] for s in seqs[-1]):
            seqs.append(diff(seqs[-1]))
        for i in reversed(range(len(seqs) - 1)):
            extrap = seqs[i][-1] + seqs[i+1][-1]
            seqs[i].append(extrap)
        sum += seqs[0][-1]
    return sum

def solve2(strings: list[str]) -> int:
    sum = 0
    for string in strings:
        seqs = [[int(s) for s in string.split()]]
        while not all(s==seqs[-1][0] for s in seqs[-1]):
            seqs.append(diff(seqs[-1]))
        for i in reversed(range(len(seqs) - 1)):
            extrap = seqs[i][0] - seqs[i+1][0]
            seqs[i] = [extrap] + seqs[i] 
        sum += seqs[0][0]
    return sum


if __name__ == "__main__":
    print(f"part 1 test = {solve1(test())}")
    print(f"part 1 live = {solve1(live())}")
    print(f"part 2 test = {solve2(test())}")
    print(f"part 2 live = {solve2(live())}")
