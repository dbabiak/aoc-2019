from collections import defaultdict, deque
from itertools import chain
from typing import Sequence, Set, Dict

Planet = str


def parse(lines: Sequence[str]) -> Dict[Planet, Set[Planet]]:
    G = defaultdict(set)
    for p, c in (l.split(')') for l in map(str.strip, lines) if l):
        G[p].add(c)
    return G


def traverse(G: Dict[Planet, Set[Planet]]):
    depths = {}
    q = deque([('COM', 0)])
    while q:
        node, depth = q.popleft()
        depths[node] = depth
        for planet in G[node]:
            q.append((planet, depth + 1))
    return depths


def de_dagify(dag: Dict[Planet, Set[Planet]]) -> Dict[Planet, Set[Planet]]:
    from copy import deepcopy
    G = deepcopy(dag)
    for parent, children in dag.items():
        for c in children:
            G[c].add(parent)
    return G



def part2(dag: Dict[Planet, Set[Planet]]) -> int:
    G = de_dagify(dag)
    [source] = G['YOU']
    [target] = G['SAN']
    marked = set(source)
    q = deque([(source, 0)])
    while q:
        planet, depth = q.popleft()
        if planet == target:
            return depth

        for nbr in G[planet]:
            if nbr in marked:
                continue
            q.append((nbr, depth + 1))
            marked.add(nbr)


def main():
    with open('/home/dmb/aoc-2019/data/d06.txt') as fp:
        dag = parse(fp)
        depths = traverse(dag)
        print(sum(chain(depths.values())))
        print(part2(dag))

main()
