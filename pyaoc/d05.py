"""
This is completely taken from: https://github.com/0x8b/advent-of-code-2019/blob/master/05.py
"""

from operator import setitem

with open('/home/dmb/aoc-2019/data/d05.txt') as fp:
    program = [int(x) for x in fp.read().strip().split(',')]

# neat trick! didn't know you could open self
# with open(__file__, "r") as f:
#     c = f.read()
#     line = c[c.rindex("🎅") + 1 : c.rindex("🐍")].rstrip().split(",")


def run(inp):
    mem = program[:]
    pc = 0
    output = []

    d = {
        1: {"p": 4, "op": lambda a, b, c: setitem(mem, c, a + b)},
        2: {"p": 4, "op": lambda a, b, c: setitem(mem, c, a * b)},
        3: {"p": 2, "op": lambda a, b, c: setitem(mem, a, inp)},
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
            raise Exception(f"run: unknown opcode {opcode}")
    return output[-1]


part_one = run(1)
print(part_one)
assert part_one == 9654885

part_two = run(5)
print(part_two)
assert part_two == 7079459

