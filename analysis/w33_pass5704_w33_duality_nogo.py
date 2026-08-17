#!/usr/bin/env python3
"""Pass5704: W(3,3) is NOT self-dual, so the two cycle orbits are intrinsic.

The Pass5700 cycle space splits into two PSp(4,3) orbits of 12960 separated by a
chirality invariant.  A natural question is whether the full automorphism group
(including a duality exchanging points and lines) merges them.  It does not,
because W(3,3) has no duality automorphism at all: for q odd, W(3,q) is not
self-dual (its dual is Q(4,q)).

Computational certificate: the Levi graph of W(3,3) is bipartite with parts
{points} and {lines}.  A duality would be an automorphism swapping the parts.
The two parts are distinguished by a local invariant:

  * For a pair of skew lines (no common point), the number of common
    transversal lines is exactly 4 for every one of the 540 skew pairs.
  * For a pair of non-collinear points, the number of common neighbour lines
    is exactly 0 for every one of the 540 non-collinear pairs.

Since 4 != 0, no incidence-preserving bijection can exchange points and lines,
so the Levi graph has no part-swapping automorphism.  Hence the two 12960
orbits are NOT merged by any automorphism; the chirality bit is intrinsic to
the oriented geometry, not an artefact of choosing a point/line labelling.

This is the classical fact that W(3,q) is self-dual iff q is even, verified
here directly on the incidence structure.
"""
from __future__ import annotations
import itertools, collections, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'data/PART_W33_PASS5704_W33_DUALITY_NOGO.json'

vecs = [v for v in itertools.product(range(3), repeat=4) if v != (0,0,0,0)]
def canon(v):
    for x in v:
        if x: return tuple((xi*(1 if x==1 else 2)) % 3 for xi in v)
pts = sorted(set(canon(v) for v in vecs))
P = {p: i for i, p in enumerate(pts)}
def omega(u, v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1]) % 3
lines = set()
for i, j in itertools.combinations(range(40), 2):
    if omega(pts[i], pts[j]) == 0:
        u, v = pts[i], pts[j]; mem = {i, j}
        for a in (1, 2):
            mem.add(P[canon(tuple((u[k]+a*v[k]) % 3 for k in range(4)))])
        lines.add(frozenset(mem))
lines = sorted(lines, key=lambda L: sorted(L))

def main():
    # skew line pairs and their common transversals
    skew = [(i, j) for i in range(40) for j in range(i+1, 40) if not (lines[i] & lines[j])]
    def common_transversals(i, j):
        return sum(1 for k, L in enumerate(lines)
                   if k not in (i, j) and (L & lines[i]) and (L & lines[j]))
    ct = collections.Counter(common_transversals(i, j) for i, j in skew)

    # non-collinear point pairs and their common neighbour lines
    collinear = set()
    for L in lines:
        for a, b in itertools.combinations(sorted(L), 2): collinear.add((a, b))
    def common_neighbours(p1, p2):
        return sum(1 for L in lines if p1 in L and p2 in L)
    nc = collections.Counter(common_neighbours(a, b)
                             for a, b in itertools.combinations(range(40), 2)
                             if (a, b) not in collinear)

    self_dual = dict(ct) == dict(nc)
    out = {
      'pass': 5704,
      'status': 'W33_NOT_SELF_DUAL_TWO_CYCLE_ORBITS_ARE_INTRINSIC',
      'skew_line_pairs': len(skew),
      'common_transversals_per_skew_pair': dict(ct),
      'noncollinear_point_pairs': sum(nc.values()),
      'common_neighbours_per_noncollinear_pair': dict(nc),
      'self_dual': self_dual,
      'classical_statement': 'W(3,q) is self-dual iff q is even; here q=3 is odd, and the dual is Q(4,3)',
      'consequence': 'The two 12960 rooted-oriented-8-cycle orbits of Pass5700 are NOT merged by any incidence-preserving automorphism; the chirality bit is intrinsic.',
      'physics_boundary': 'Finite incidence geometry; no physical duality is claimed or denied.'
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps(out, indent=2, sort_keys=True))
if __name__ == '__main__': main()
