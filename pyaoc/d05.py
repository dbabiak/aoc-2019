"""
;_;
"""

from typing import Tuple, NewType, List

Instruction = Tuple[int, int, int, int]
ADD = 1
MUL = 2
IN = 3
OUT = 4
JMP_T = 5
JMP_F = 6
LT = 7
EQ = 8
EXIT = 99

POSITIONAL = 0
IMMEDIATE = 1

# Instruction Pointer
IP = NewType('IP', int)


def parse_program(s: str) -> List[int]:
    return [int(x) for i, x in enumerate(s.strip().split(','))]


def parse_instruction(i: IP, memory: List[int]) -> Tuple[IP, List[int]]:
    X = memory[i]
    op = X % 100
    n_params = {ADD: 3, MUL: 3, IN: 1, OUT: 1, JMP_T: 2, JMP_F: 2, LT: 3, EQ: 3, EXIT: 0}[op]
    modes = {i: POSITIONAL if int(mode) == 0 else IMMEDIATE for i, mode in enumerate(reversed(str(X // 100)))}
    params = []

    for j in range(n_params):
        val = memory[i + j + 1]

        if op in (ADD, MUL, IN, OUT,) and j + 1 == n_params:
            params.append(val)
            break

        mode = modes.get(j, POSITIONAL)
        param = val if mode == IMMEDIATE else memory[val]
        params.append(param)

    return IP(i + 1 + len(params)), tuple((op, *params))


def diff(xs, ys):
    return {
        i: (x, y)
        for i, (x, y) in enumerate(zip(xs,ys))
        if x != y
    }


def compute(memory: List[int], _input=1) -> List[int]:
    ip = IP(0)
    output = []
    while ip < len(memory):
        next_ip, [op, *params] = parse_instruction(ip, memory)

        if op == ADD:
            a, b, c = params
            memory[c] = a + b

        elif op == MUL:
            a, b, c = params
            memory[c] = a * b

        elif op == IN:
            [c] = params
            memory[c] = _input

        elif op == OUT:
            [c] = params
            output.append(memory[c])

        elif op == JMP_T:
            a, b = params
            if a != 0:
                next_ip = b

        elif op == JMP_F:
            a, b = params
            if a == 0:
                next_ip = b

        elif op == LT:
            a, b, c = params
            memory[c] = int(a < b)

        elif op == EQ:
            a, b, c = params
            memory[c] = int(a == b)

        elif op == EXIT:
            break

        ip = next_ip

    return output

