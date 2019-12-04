import re
from collections import defaultdict
from typing import Tuple, Iterable, Dict, NewType

Point = NewType('Point', Tuple[int,int])
WireID = NewType('WireID', int)


def v_add(p1: Point, p2: Point) -> Point:
    x1, y1 = p1
    x2, y2 = p2
    return Point((x1 + x2, y1 + y2))

rgx = re.compile(r'^([URDL])(\d+)$')


def points(p0: Point, displacement: str) -> Iterable[Point]:
    direction, distance = rgx.match(displacement).groups()
    direction = Point(dict(U=(0,1), R=(1,0), D=(0,-1), L=(-1,0))[direction])
    distance = int(distance)
    p = p0
    return tuple(
        (p := v_add(p, direction))
        for _ in range(1, distance + 1)
    )


def plot_wires(wires: Tuple[str]) -> Dict[Point, Dict[WireID, int]]:
    G: Dict[Point, Dict[WireID, int]] = defaultdict(dict)
    wire_id: WireID
    for wire_id, wire_str in enumerate(wires):
        p = (0,0)
        wire = tuple(wire_str.split(','))
        distance_from_start = 0
        for segment in wire:
            for q in points(p0=p, displacement=segment):
                m: Dict[WireID, int] = G[q]
                distance_from_start += 1
                if wire_id not in m:
                    m[wire_id] = distance_from_start
                p = q
    return G


def closest_intersection(G: Dict[Point, Dict[WireID, int]]) -> Point:
    max_P = max(map(D, G))
    for d in range(max_P):
        for p in level_set(d):
            if len(G[p]) > 1:
                return p


def D(p: Point) -> int:
    return sum(map(abs, p))


def level_set(i: int) -> Iterable[Point]:
    assert i >= 0

    if i == 0:
        yield (0,0)

    else:
        x, y = (-i, 0)

        while y < i:
            x += 1
            y += 1
            yield (x, y)

        while x < i:
            x += 1
            y -= 1
            yield (x, y)

        while y > -i:
            x -= 1
            y -= 1
            yield (x, y)

        while x > -i:
            x -= 1
            y += 1
            yield (x, y)


def part2(wires: Sequence[str]) -> int:
      G = plot_wires(wires)
      intersections = {k: v for k, v in G if len(v) > 1}
      ys = {k: sum(v.values()) for k, v in intersections.items()}
      (p, N) = min(ys.items(), key=lambda kv: kv[1])
      return N


def main():
    with open('/home/dmb/aoc-2019/data/d03.txt') as fp:
        wires = tuple(x.strip() for x in fp)
        G = plot_wires(wires)
        print(closest_intersection(G))
        print(part2(wires))
