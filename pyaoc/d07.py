"""
This is completely taken from: https://github.com/0x8b/advent-of-code-2019/blob/master/05.py
"""

from typing import List, Iterable, Tuple
from operator import setitem





def run(_program, in0):
    from _collections import deque
    inputs = deque(in0)
    mem = _program[:]
    pc = 0
    output = []

    d = {
        1: {"p": 4, "op": lambda a, b, c: setitem(mem, c, a + b)},
        2: {"p": 4, "op": lambda a, b, c: setitem(mem, c, a * b)},
        3: {"p": 2, "op": lambda a, b, c: setitem(mem, a, inputs.popleft())},
        4: {"p": 2, "op": lambda a, b, c: output.append(mem[a])},
        5: {"p": 3, "op": lambda a, b, c: b if a != 0 else pc + 3},
        6: {"p": 3, "op": lambda a, b, c: b if a == 0 else pc + 3},
        7: {"p": 4, "op": lambda a, b, c: setitem(mem, c, 1 if a < b else 0)},
        8: {"p": 4, "op": lambda a, b, c: setitem(mem, c, 1 if a == b else 0)},
    }

    while mem[pc] != 99:
        opcode, *args = mem[pc:][:4]

        opcode = str(opcode).zfill(5)
        operation = int(opcode[-2:])

        if operation in {1, 2, 5, 6, 7, 8}:
            if opcode[2] == "0": args[0] = mem[args[0]]
            if opcode[1] == "0": args[1] = mem[args[1]]

        if 1 <= operation <= 8:
            o = d[operation]
            width = o["p"]
            ret = o["op"](*args)

            if operation in {5, 6}:
                pc = ret
            else:
                pc += width
        else:
            breakpoint()
            raise Exception(f"run: unknown opcode {opcode}")
    return output[-1]


def permutations(xs: List) -> Iterable[List]:
    # todo - is this in the standard library?
    if not xs:
        yield []
    else:
        for i in range(len(xs)):
            ys = xs[:]
            ys.pop(i)
            smaller_perms = permutations(ys)
            for perm in smaller_perms:
                yield [xs[i]] + perm


def run_phases(_program, phases: List[int]) -> int:
    inputs = {0: 0}

    for amplifier, phase in enumerate(phases):
        phase = phases[amplifier]
        in0 = inputs[amplifier]
        out = run(_program[:], [phase, in0])
        inputs[amplifier + 1] = out
    return out


def part1(_program) -> Tuple[int, List]:
    phases = list(range(5))
    acc  = None
    max_perm = None
    for perm in permutations(phases):
        out = run_phases(_program[:], perm)
        if acc is None or out > acc:
            acc = out
            max_perm = perm
    return acc, max_perm


p1 = [int(x) for x in '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'.split(',')]
print(p1)
print(part1(p1))
print()


p2 = [int(x) for x in '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'.split(',')]
print(p2)
print(part1(p2))
print()


p3 = [int(x) for x in '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'.split(',')]
print(p3)
print(part1(p3))
print()

with open('/home/dmb/aoc-2019/data/d07.txt') as f:
    part1_program = [int(x) for x in f.read().strip().split(',')]
    print()
    print(part1(part1_program))
