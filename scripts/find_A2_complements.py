#!/usr/bin/env python3
"""Search for A2 root pairs in E8 whose orthogonal complement among E8 roots has size 72 (candidate E6 subsystem)."""
import itertools
from fractions import Fraction
import json
from pathlib import Path

# Build E8 roots rational
E8 = []
for i in range(8):
    for j in range(i+1, 8):
        for si in (-1,1):
            for sj in (-1,1):
                r = [0]*8
                r[i] = si
                r[j] = sj
                E8.append(tuple(Fraction(x) for x in r))
for signs in itertools.product([-1,1], repeat=8):
    if sum(1 for s in signs if s<0) % 2 == 0:
        r = tuple(Fraction(s,2) for s in signs)
        E8.append(r)
assert len(E8) == 240

# dot product
def dot(u, v):
    return sum(ui*vi for ui, vi in zip(u, v))

solutions = []
for i, j in itertools.combinations(range(240), 2):
    u = E8[i]; v = E8[j]
    if dot(u, u) != 2 or dot(v, v) != 2:
        continue
    if dot(u, v) != -1:
        continue
    # compute roots orthogonal to both
    orth = [k for k, r in enumerate(E8) if dot(r, u) == 0 and dot(r, v) == 0]
    if len(orth) == 72:
        solutions.append({'pair': (i, j), 'orth_count': len(orth), 'orth_indices': orth})
        print('Found candidate pair', (i,j), 'orth_count', len(orth))
        # Save and break
        Path('PART_CVII_e6_via_A2.json').write_text(json.dumps(solutions, indent=2))
        break
    # cheap break to avoid very long search, but continue a bit
    if i>5000:
        break

Path('PART_CVII_e6_via_A2_search.json').write_text(json.dumps(solutions, indent=2))
print('Done search, found', len(solutions))
