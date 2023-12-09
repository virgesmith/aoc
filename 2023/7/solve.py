from io import StringIO
from collections import defaultdict

def test1():
    input = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
    return StringIO(input).read().splitlines()


cards1 = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
card_ranks1 = {card: i for i, card in enumerate(cards1)}

cards2 = ("J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A")
card_ranks2 = {card: i for i, card in enumerate(cards2)}


def count(hand: str):
    counts = defaultdict(lambda: 0)
    for card in hand:
        counts[card] += 1
    return counts


def hand_rank(hand: str, *, wildcards: bool=False) -> int:
    c = count(hand)
    if wildcards and "J" in c:
        nwild = c["J"]
        if nwild == 5:
            return 10
        del c["J"]
        # add nwild to higest value of c
        k = max(c, key=c.get)
        c[k] += nwild
    if 2 in c.values() and 3 in c.values():
        return 7
    elif len([ci for ci in c.values() if ci == 2]) == 2:
        return 5
    return max(c.values()) * 2


def card_rank(hand: str, *, wildcards: bool=False) -> float:
    rank = 0.0
    card_ranks = card_ranks1 if not wildcards else card_ranks2
    for card in hand:
        rank += card_ranks[card]
        rank *= 13
    return rank / 13 ** (len(hand) + 1)


def live():
    with open("2023/7/input.txt") as fd:
        return fd.read().splitlines()


def solve1(strings: list[str]) -> int:
    hands = dict(s.split() for s in strings)
    ranks = {hand: hand_rank(hand) + card_rank(hand) for hand in hands}
    ranks = dict(sorted(ranks.items(), key=lambda r: r[1]))

    score = sum(int(hands[hand]) * (i + 1) for i, hand in enumerate(ranks.keys())) 
    return score


def solve2(strings: list[str]) -> int:
    hands = dict(s.split() for s in strings)
    ranks = {hand: hand_rank(hand, wildcards=True) + card_rank(hand, wildcards=True) for hand in hands}
    ranks = dict(sorted(ranks.items(), key=lambda r: r[1]))

    score = sum(int(hands[hand]) * (i + 1) for i, hand in enumerate(ranks.keys())) 
    return score


if __name__ == "__main__":
    print(f"part 1 test = {solve1(test1())}")
    print(f"part 1 live = {solve1(live())}")
    print(f"part 2 test = {solve2(test1())}")
    print(f"part 2 live = {solve2(live())}")
