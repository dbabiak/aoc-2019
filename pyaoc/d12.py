import re
from copy import deepcopy
from dataclasses import dataclass
from typing import Tuple, TypeVar, Sequence, Iterable, List

N_DIMENSIONS = 3


@dataclass
class Moon:
    pos: List[int]
    v: List[int]

T = TypeVar('T')

def V_add(xs, ys):
    return [x + y for x, y in zip(xs, ys)]

def _apply_gravity(moons: Sequence[Moon]) -> Sequence[Moon]:
    new_moons = deepcopy(moons)

    for m1, m2 in all_pairs(new_moons):
        for d in range(N_DIMENSIONS):
            if m1.pos[d] < m2.pos[d]:
                m1.v[d] += 1
                m2.v[d] -= 1
            elif m2.pos[d] < m1.pos[d]:
                m2.v[d] += 1
                m1.v[d] -= 1
    return new_moons

def _apply_velocity(moons: Sequence[Moon]) -> Sequence[Moon]:
    return [
        Moon(pos=V_add(m.pos, m.v), v=m.v) for m in moons
    ]


def parse(s: str) -> Moon:
    rgx = re.compile(r'^<x=([-\d]+), y=([-\d]+), z=([-\d]+)>$')
    point = [int(n) for n in rgx.match(s.strip()).groups()]
    return Moon(pos=point, v=[0,0,0])


def all_pairs(xs: Sequence[T]) -> Iterable[Tuple[T, T]]:
    for i in range(len(xs) - 1):
        for j in range(i + 1, len(xs)):
            yield xs[i], xs[j]

def _step(moons: Sequence[Moon]) -> Sequence[Moon]:
    new_moons = _apply_velocity(
        _apply_gravity(moons)
    )
    return new_moons


def energy(m: Moon):
    return (
        sum(abs(m.pos[d]) for d in range(N_DIMENSIONS))
      * sum(abs(m.v[d])   for d in range(N_DIMENSIONS))
    )

def print_moons(moons: Sequence[Moon]):
    for m in moons:
        p = m.pos
        v = m.v
        print(
            f"pos=<x={p[0]:3}, y={p[1]:3}, z={p[2]:3}>, vel=<{v[0]:3}, y={v[1]:3}, z={v[2]:3}>"
        )
    print('\n')

S = '''\
<x=3, y=15, z=8>
<x=5, y=-1, z=-2>
<x=-10, y=8, z=2>
<x=8, y=4, z=-5>'''.splitlines()

def main():
    moons = [parse(s) for s in S]
    print_moons(moons)
    for i in range(1000):
        moons = _step(moons)
        print_moons(moons)
    total = sum(energy(m) for m in moons)
    print(total)


if __name__ == '__main__':
    main()
