"""
List of reactions

Reaction: 

quantity of input chem -> quantity of output chem

Almost every chem is produced by exactly one reaction

(use a dict)
ORE - raw input to entire process, not produced by a reaction

need to know how much ORE to collect before you can produce one unit of FUEL


"""
from pprint import pprint
from collections import deque, defaultdict
from typing import Tuple, Dict, Sequence
 
M = dict

Chem = str

def parse(lines: Sequence[str]) -> Dict[Chem, Tuple[Dict[Chem, int], int]]:
    m = {}
    for line in lines:
        reqs, chem = line.split(' => ')

        n_prod, chem = chem.split(' ')
        n_prod = int(n_prod)

        req_map = {}

        for n_need, c in (n_c.split(' ') for n_c in reqs.split(', ')):
            n_need = int(n_need)
            req_map[c] = n_need

        m[chem] = (n_prod, req_map)     
    return m
S = '''\
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
'''.splitlines()


  #       chem  (requires)   these (for) n
m0: Dict[Chem, Tuple[Dict[Chem, int], int]] = M( 
  A=(2, M(ORE=9)),
  B=(3, M(ORE=8)),
  C=(5, M(ORE=7)),
  AB=(1, M(A=3, B=4)),
  BC=(1, M(B=5, C=7)),
  CA=(1, M(C=4, A=1)),
  FUEL=(1, M(AB=2, BC=3, CA=4)),
)

m = parse(S)
pprint(m0)

needs = deque([("FUEL", 1)])
need_map = defaultdict(int)
need_map["FUEL"] += 1
supply = {}

from pprint import pprint
pprint(m)
n_ore = 0
while needs:
    chem, n_need0 = needs.popleft()
    n_need = need_map[chem]
    print()
    print(f'i: need {n_need} {chem}')

    if chem == 'ORE':
        n_ore += n_need0
        print()
        print(f"n_ore: {n_ore}")
        print(needs)
        continue

    if n_need == 0:
        print(needs)
        continue

    if n_need < supply.get(chem, 0):
        supply[chem] -= n_need
        print(f'already have {n_need} of {chem}')
    else:
        from math import ceil
        # we are going to run the reaction for chemical
        n_prod, deps = m[chem]

        # run the reaction k times
        k = ceil(n_need / n_prod)
        for c, n_c in deps.items():
            needs.append((c, k*n_c))
            need_map[c] += (k*n_c)
        print(needs)
    need_map[chem] = 0

print()
print(f"FINAL ORE : {n_ore}")
