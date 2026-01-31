#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from itertools import combinations

import numpy as np

from tools.compute_double_sixes import compute_we6_orbits, construct_e8_roots

roots = construct_e8_roots()
we6 = compute_we6_orbits(roots)
orb = [o for o in we6 if len(o) == 27][0]
print("using orbit len", len(orb))
orbit_roots = roots[orb]
gram = orbit_roots @ orbit_roots.T
for ip_val in [1.0, 0.0]:
    adj = np.zeros((27, 27), dtype=bool)
    for i in range(27):
        for j in range(i + 1, 27):
            if abs(gram[i, j] - ip_val) < 1e-6:
                adj[i, j] = adj[j, i] = True
    print("ip_val", ip_val, "valency", set(adj.sum(axis=1)))
    cnt = 0
    examples = []
    for comb in combinations(range(27), 6):
        ok = True
        for i in range(6):
            for j in range(i + 1, 6):
                if adj[comb[i], comb[j]]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            cnt += 1
            if len(examples) < 5:
                examples.append(comb)
    print("count", cnt, "examples", examples)
