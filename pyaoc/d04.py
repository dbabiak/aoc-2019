from pyaoc.utils import irange

def non_decreasing(digits: str) -> bool:
    return all(
        d0 <= d1 for d0, d1 in zip(digits, digits[1:])
    )


def two_adjacent_same(digits: str) -> bool:
    return any(
        d0 == d1 for d0, d1 in zip(digits, digits[1:])
    )


def baab(xs: str) -> bool:
    # ^aab...$
    aa_ = xs[0] == xs[1] and xs[1] != xs[2]

    _aa_ = any(
        xs[i - 1] != xs[i] and xs[i] == xs[i + 1] and xs[i + 1] != xs[i + 2]
        for i in range(1, len(xs) - 2)
    )

    # ^...baa$
    _aa = xs[-3] != xs[-2] and xs[-2] == xs[-1]

    return aa_ or _aa or _aa_


def part1(lo: int, hi: int) -> int:
    return sum(
        1
        for n in map(str, irange(lo, hi))
        if non_decreasing(n) and two_adjacent_same(n)
    )


def part2(lo: int, hi: int) -> int:
    return sum(
        1
        for digits in map(str, irange(lo, hi))
        if non_decreasing(digits) and baab(digits)
    )

LO = 197487
HI = 673251

print(part1(LO, HI))
print(part2(LO, HI))
