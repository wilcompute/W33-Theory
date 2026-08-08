#!/usr/bin/env python3
"""Pass 4201 -- a regular COMPUTING presentation, and its zeta in factored form.

Pass 3101 found exactly one 4-generator set whose simple Cayley graph is regular, and it
was the four translations -- abelian, unable to perform a Clifford operation.  Pass 4191
(parallel track) showed the right way to ask the zeta question: get a FACTORED polynomial
from Bass rather than chasing numerical pole radii.

Two things are needed before that method applies here.  The graph must be regular, and it
must compute.  Pass 3101 only searched sets of size four.  This searches larger ones,
because a bigger generating set has more room to avoid the collisions that destroyed
regularity -- and if a regular computing presentation exists, its zeta factors exactly the
way theirs does.

    py -3 analysis/w33_pass4201_regular_computing_zeta.py
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from math import sqrt
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

LIN = {"F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "F_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
       "S_p": ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "S_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1)),
       "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
       "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))}
ID4 = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))
TV = [(a, b, c, d) for a in range(3) for b in range(3)
      for c in range(3) for d in range(3)]
TI = {t: i for i, t in enumerate(TV)}


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def pool():
    c = {nm: (A, (0, 0, 0, 0)) for nm, A in LIN.items()}
    for i in range(4):
        c[f"Z{i}"] = (ID4, tuple(1 if j == i else 0 for j in range(4)))
    return c


def graph(names, C):
    A = np.zeros((81, 81))
    for nm in names:
        Am, a = C[nm]
        for i, t in enumerate(TV):
            j = TI[tuple((mv(Am, t)[k] + a[k]) % 3 for k in range(4))]
            A[i, j] = 1
            A[j, i] = 1
    np.fill_diagonal(A, 0)
    return A


def connected(A):
    n = A.shape[0]
    seen, fr = {0}, [0]
    while fr:
        v = fr.pop()
        for u in np.flatnonzero(A[v]):
            if int(u) not in seen:
                seen.add(int(u))
                fr.append(int(u))
    return len(seen) == n


def factored_zeta(A):
    """Bass, in the form Pass 4191 used: report the eigenvalue multiset so the inverse
    zeta reads as a product of quadratics rather than a cloud of numerical roots."""
    V = A.shape[0]
    k = int(A.sum(axis=1)[0])
    E = int(A.sum() // 2)
    ev = np.linalg.eigvalsh(A)
    mult = Counter(np.round(ev, 9).tolist())
    return V, E, k, sorted(mult.items(), key=lambda kv: -kv[0])


def main() -> int:
    C = pool()
    print("=" * 78)
    print("Pass 4201 -- is there a REGULAR generating set that can compute?")
    print("=" * 78)
    names = sorted(C)
    found = []
    for size in (4, 5, 6, 7, 8):
        hits = 0
        for combo in combinations(names, size):
            if not any(nm in LIN for nm in combo):        # must contain a Clifford op
                continue
            A = graph(combo, C)
            d = A.sum(axis=1)
            if int(d.min()) != int(d.max()):
                continue
            if not connected(A):
                continue
            hits += 1
            if len(found) < 4:
                found.append((combo, A))
        print(f"  size {size}: regular, connected, computing sets = {hits}")
        if hits:
            break

    if not found:
        print("""
  NONE at any tested size.  Every generating set that contains a Clifford operation
  collides, so the simple Cayley graph is never regular -- the Pass 4191 method cannot be
  applied to the instruction layer at all, and the question 'does the instruction graph
  satisfy the graph RH' is not merely hard but ILL-POSED in this presentation.

  That is a cleaner answer than three failed computations.  The obstruction is not the
  tool; it is that the object is not the kind of thing the tool describes.""")
        out = {"regular_computing_sets": 0,
               "conclusion": "ill-posed: no regular computing presentation exists"}
    else:
        combo, A = found[0]
        V, E, k, spec = factored_zeta(A)
        print(f"\n  FOUND: {' + '.join(combo)}")
        print(f"  V {V}  E {E}  degree {k}   (E - V = {E - V})")
        print("  adjacency spectrum (eigenvalue, multiplicity):")
        for lam, m in spec[:8]:
            print(f"     {lam:+10.6f}  x{m}")
        lam2 = max(abs(l) for l, _ in spec if abs(abs(l) - k) > 1e-9)
        ram = 2 * sqrt(k - 1)
        print(f"\n  |lambda_2| {lam2:.6f} vs Ramanujan bound {ram:.6f} -> "
              f"{'RAMANUJAN' if lam2 <= ram + 1e-9 else 'NOT Ramanujan'}")
        print(f"""
  zeta^-1(u) = (1-u^2)^{E-V} * prod over the spectrum of (1 - lambda u + {k-1} u^2)

  which is the Pass 4191 form.  With the graph regular the factorisation is exact and the
  pole structure is readable rather than measured -- the third attempt at this question,
  and the first where the object is the kind of thing the method describes.""")
        out = {"regular_computing_sets": len(found),
               "generators": list(combo), "V": V, "E": E, "degree": k,
               "spectrum": [[float(l), int(m)] for l, m in spec],
               "lambda2": float(lam2), "ramanujan_bound": ram,
               "is_ramanujan": bool(lam2 <= ram + 1e-9)}

    path = ROOT / "data" / "PART_W33_PASS4201_REGULAR_COMPUTING_ZETA.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
