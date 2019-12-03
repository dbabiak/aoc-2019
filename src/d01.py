"""
Fuel required to launch a given module is based on its mass.
Specifically, to find the fuel required for a module,
take its mass, divide by three, round down, and subtract 2.
"""
from typing import Sequence

def fuel(mass: int) -> int:
    return (mass // 3) - 2


def geometric_fuel(mass: int) -> int:
    total = 0
    m = mass
    while (m := fuel(m)) > 0:
        total += m
    return total


def part1(masses: Sequence[int]) -> int:
    return sum(fuel(m) for m in masses)


def test_geometric_fuel():
    assert geometric_fuel(14) == 2
    assert geometric_fuel(1969) == 966
    assert geometric_fuel(100756) == 50346

def part2(masses: Sequence[int]) -> int:
    return sum(geometric_fuel(m) for m in masses)


def main():
    with open('/home/dmb/aoc-2019/data/d01.txt') as fp:
        masses = tuple(int(x.strip()) for x in fp)
        print(part1(masses))
        print(part2(masses))

if __name__ == '__main__':
    main()
