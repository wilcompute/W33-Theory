#!/usr/bin/env python3
"""Pass 4202 -- is there ANY regular presentation that also generates the whole group?

Pass 4201 left three data points: the 4-opcode ISA generates ASp(4,3) and is not regular;
two regular presentations exist and generate only 81 and 243 elements respectively.  The
pattern suggested "extremality and universality are in tension", which is a slogan until
the search is exhausted.

This searches every subset of the ten natural generators at sizes 4 through 8, checks
regularity of the simple Cayley graph on the 81 frames, and -- only for the regular ones,
since that is the expensive step -- computes the order of the group actually generated.

If no regular set generates ASp(4,3), the tension is a theorem over this generating pool
rather than an observation.

    py -3 analysis/w33_pass4202_regular_and_universal.py
"""

from __future__ import annotations

import json
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
FULL = 81 * 51840


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % 3 for j in range(4))
                 for i in range(4))


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


def group_order(names, C, cap=FULL):
    """Order of the affine group generated, by closure on (matrix, translation)."""
    gens = [C[nm] for nm in names]
    idt = (ID4, (0, 0, 0, 0))
    seen, fr = {idt}, [idt]
    while fr:
        nxt = []
        for M, t in fr:
            for A, a in gens:
                P = (mm(A, M), tuple((mv(A, t)[i] + a[i]) % 3 for i in range(4)))
                if P not in seen:
                    seen.add(P)
                    nxt.append(P)
                    if len(seen) > cap:
                        return len(seen)
        fr = nxt
    return len(seen)


def main() -> int:
    C = pool()
    names = sorted(C)
    print("=" * 78)
    print("Pass 4202 -- can a regular presentation also generate ASp(4,3)?")
    print("=" * 78)
    print(f"  generator pool: {len(names)}   full group order: {FULL:,}")
    print("\n  size  regular&connected   of which generate the full group")
    rows, universal = [], []
    for size in (4, 5, 6, 7, 8):
        reg = []
        for combo in combinations(names, size):
            A = graph(combo, C)
            d = A.sum(axis=1)
            if int(d.min()) != int(d.max()):
                continue
            n = A.shape[0]
            seen, fr = {0}, [0]
            while fr:
                v = fr.pop()
                for u in np.flatnonzero(A[v]):
                    if int(u) not in seen:
                        seen.add(int(u))
                        fr.append(int(u))
            if len(seen) == n:
                reg.append(combo)
        full = []
        for combo in reg:
            o = group_order(combo, C)
            if o >= FULL:
                full.append(combo)
                universal.append(combo)
        print(f"  {size:4d}  {len(reg):17d}   {len(full):d}")
        rows.append({"size": size, "regular": len(reg), "universal": len(full)})

    print()
    if not universal:
        print(f"""  EXHAUSTED OVER THIS POOL, SIZES 4 TO 8: NONE.

  Every subset of the ten natural generators whose simple Cayley graph on the 81 frames is
  regular generates a PROPER subgroup of ASp(4,3), and every subset that generates the
  whole group has an irregular graph.

  So the tension between extremality and universality is not an observation from three
  data points -- over this generating pool it is EXHAUSTIVE.  A universal instruction set
  cannot have a regular Cayley graph here, which means the graph Riemann Hypothesis and
  the Ramanujan property are not merely unproven for the instruction layer: THEY ARE NOT
  DEFINED FOR ANY UNIVERSAL PRESENTATION OF IT.

  Scope, stated plainly: this is exhaustive over the ten generators this project uses, at
  sizes four through eight.  It is not a statement about every conceivable generating set
  of ASp(4,3), and a generator outside this pool could in principle behave differently.""")
    else:
        print(f"  FOUND {len(universal)}: e.g. {' + '.join(universal[0])}")
        A = graph(universal[0], C)
        k = int(A.sum(axis=1)[0])
        ev = np.linalg.eigvalsh(A)
        lam2 = max(abs(l) for l in ev if abs(abs(l) - k) > 1e-9)
        ram = 2 * sqrt(k - 1)
        print(f"  {k}-regular, |lambda_2| {lam2:.6f} vs bound {ram:.6f} -> "
              f"{'RAMANUJAN' if lam2 <= ram + 1e-9 else 'not Ramanujan'}")
        print("\n  The tension is NOT a theorem: a universal presentation can be regular,")
        print("  and the graph RH question is well posed for it after all.")

    out = {"pool": len(names), "full_group_order": FULL, "by_size": rows,
           "universal_regular_sets": [list(c) for c in universal],
           "conclusion": ("exhaustive over this pool sizes 4-8: no regular universal set"
                          if not universal else "a regular universal set exists")}
    path = ROOT / "data" / "PART_W33_PASS4202_REGULAR_AND_UNIVERSAL.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
