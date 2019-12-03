from operator import add, mul
from typing import Dict,    Tuple

Instruction = Tuple[int, int, int, int]
ADD = 1
MUL = 2
EXIT = 99


def compute(op_abc: Instruction, rs: Dict[int,int]) -> Dict[int,int]:
    op, a, b, c = op_abc
    f = {
        ADD: add,
        MUL: mul,
    }[op]
    return {**rs, c: f(rs[a], rs[b])}


def part1(program: Dict[int,int], noun=12, verb=2) -> Dict[int,int]:
    """
    The inputs should still be provided to the program by replacing the values at addresses 1 and 2,
    just like before. In this program, the value placed in address 1 is called the noun,
    and the value placed in address 2 is called the verb.
    Each of the two input values will be between 0 and 99, inclusive.
    """
    p = {**program, 1: noun, 2: verb}
    i = 0
    while i < len(program) and program[i] != EXIT:
        op_abc = tuple(p[j] for j in range(i, i + 4))
        p = compute(op_abc, p)
        i += 4
    return p


def part2(p0: Dict[int, int], target=19690720) -> int:
    program, noun, verb = next(
        (program, noun, verb)
        for noun in range(100)
        for verb in range(100)
        if (program := part1(p0, noun, verb))[0] == target
    )
    return 100 * noun + verb


def main():
    with open('/home/dmb/aoc-2019/data/d02.txt') as fp:
        program = dict(enumerate(map(int, fp.read().strip().split(','))))
        print(part1(program)[0])
        print(part2(program))


if __name__ == '__main__':
    main()
