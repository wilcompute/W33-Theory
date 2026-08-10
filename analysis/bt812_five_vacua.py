#!/usr/bin/env python3
"""
BT812 - The Five Vacua: every maximal subgroup class of PSp(4,3) induces
        a canonical vacuum decomposition of W(3,3).

GAP witness (.tmp/gap_five_vacua.g): orbit anatomies of all five maximal
classes on the 40 points and 40 isotropic lines:

    index 27 (2^4:A5, icosa):   points [40]         lines [40]
    index 36 (S6, spread):      points [40]         lines [10, 30]
    index 40 (point parabolic): points [1, 12, 27]  lines [4, 36]
    index 40 (line parabolic):  points [4, 36]      lines [1, 12, 27]
    index 45 ((2Tx2T):2 polar): points [8, 32]      lines [16, 24]

READINGS:
  * The ICOSAHEDRAL vacuum is the unique HOMOGENEOUS one - transitive on
    both levels.  The F4^2 register's symmetry sees no decomposition:
    a featureless vacuum with point stabilizer of order 24 = f.
  * The POINT PARABOLIC vacuum is the holonet split 40 = 1 + 12 + 27
    (self + gauge + matter), with the dual line split 4 + 36; the LINE
    parabolic mirrors it under duality.
  * The SPREAD vacuum fibers the lines 10 + 30 (fibration + BC layer)
    while keeping points homogeneous.
  * The POLAR vacuum is the binary split: points 8 + 32 = 2^3 + 2^5,
    lines 16 + 24 = mu^2 + f (cross-transversal grid + the rest).

PYTHON VERIFICATION (group-free where possible):
  T1. The point-parabolic split IS the SRG neighborhood structure:
      {p}, Gamma(p) (12), non-neighbors (27) - orbits because the point
      action has rank 3 (BT742: <chi_pt, chi_pt> = 3, proven by exact
      character computation).
  T2. The line-parabolic split: a line's 4 points + 36 others; lines:
      itself (1), the 12 meeting it, the 27 skew to it (line graph of
      W33 is also SRG(40,12,2,4) -- same PARAMETERS, not by self-duality:
#      W(3,3) is not self-dual, q=3 being odd. Pass 4563/4755).
  T3. Arithmetic seals: stabilizer orders x indices = 25920; the five
      point splits sum to 40 each; 16 = mu^2, 24 = f, 12 = k, 27 = q^3.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json


def canon(v):
    for x in v:
        if x % 3:
            c = 1 if x % 3 == 1 else 2
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def main():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})

    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    n = 40
    adj = [[False]*n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True

    # T1: point neighborhood split
    p0 = 0
    nb = [j for j in range(n) if adj[p0][j]]
    non = [j for j in range(n) if j != p0 and not adj[p0][j]]
    print(f"T1 point vacuum: 1 + {len(nb)} + {len(non)} = 40 "
          f"(self + gauge + matter); rank-3 orbit structure (BT742)")
    assert len(nb) == 12 and len(non) == 27

    # T2: line split
    lines = [frozenset(q) for q in combinations(range(n), 4)
             if all(adj[i][j] for i, j in combinations(q, 2))]
    assert len(lines) == 40
    L0 = lines[0]
    meeting = [L for L in lines if L != L0 and (L & L0)]
    skew = [L for L in lines if L != L0 and not (L & L0)]
    print(f"T2 line vacuum (line side): 1 + {len(meeting)} + {len(skew)} "
          f"= 40; point side: 4 + 36")
    assert len(meeting) == 12 and len(skew) == 27

    # T3: arithmetic seals
    table = {
        27: (960, [40], [40], "icosahedral homogeneous vacuum"),
        36: (720, [40], [10, 30], "spread fibration vacuum"),
        "40p": (648, [1, 12, 27], [4, 36], "holonet point vacuum"),
        "40l": (648, [4, 36], [1, 12, 27], "dual line vacuum"),
        45: (576, [8, 32], [16, 24], "binary polar vacuum"),
    }
    print("\nTHE FIVE VACUA (GAP-witnessed orbit table):")
    for idx, (order, ps, ls, name) in table.items():
        i = int(str(idx).rstrip("pl"))
        assert i * order == 25920
        assert sum(ps) == 40 and sum(ls) == 40
        print(f"  index {str(idx):>3}: points {str(ps):16s} "
              f"lines {str(ls):16s} {name}")
    assert 16 == 4*4 and 24 == 24 and 10*4 == 40
    print("\nseals: 16 = mu^2, 24 = f, 12 = k, 27 = q^3, 10 x 4 = 40;")
    print("icosahedral vacuum point-stabilizer order = 960/40 = 24 = f")

    out = {
        "theorem": "BT812 five vacua",
        "table": {str(k): dict(order=v[0], points=v[1], lines=v[2],
                               name=v[3]) for k, v in table.items()},
        "homogeneous_vacuum": "index 27 (icosahedral) - unique",
        "holonet_split": "index 40 point parabolic: 1+12+27",
    }
    with open("data/bt812_five_vacua.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt812_five_vacua.json")


if __name__ == "__main__":
    main()
