#!/usr/bin/env python3
"""Passes 3120-3122 -- the question that failed twice, now with a validated tool.

PASS 3120 -- THE GRAPH RH FOR THE INSTRUCTION LAYER.
    Pass 3060 used a k-regular formula on a non-regular graph.  Pass 3080's replacement
    was untrustworthy.  Pass 3100 validated the Bass routine against K_4.  Third attempt,
    first time with a checked tool.

PASS 3121 -- HOW BADLY DOES A COMPUTING GENERATING SET COLLIDE?
    Pass 3101 established that every four-generator set which can compute collides, and
    that the only collision-free set is abelian.  "Collides" is qualitative; the minimum
    collision count over computing sets is the actual cost, and it has never been measured.

PASS 3122 -- IS THE 8-REGULAR TRANSLATION GRAPH USEFUL AS A SUB-LAYER?
    It cannot compute, and it is Ramanujan.  The routing layer might want exactly that.

    py -3 analysis/w33_pass3120_3122_bass_on_the_frame_collisions.py
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


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def cands():
    c = {nm: (A, (0, 0, 0, 0)) for nm, A in LIN.items()}
    for i in range(4):
        c[f"Z{i}"] = (ID4, tuple(1 if j == i else 0 for j in range(4)))
    return c


def graph(names, C):
    A = np.zeros((81, 81))
    collisions = 0
    for i, t in enumerate(TV):
        seen = set()
        for nm in names:
            Am, a = C[nm]
            j = TI[tuple((mv(Am, t)[k] + a[k]) % 3 for k in range(4))]
            if j in seen or j == i:
                collisions += 1
            seen.add(j)
            A[i, j] = 1
            A[j, i] = 1
    np.fill_diagonal(A, 0)
    return A, collisions


def bass_poles(A):
    V = A.shape[0]
    Q = np.diag(A.sum(axis=1)) - np.eye(V)
    Z, I = np.zeros((V, V)), np.eye(V)
    M0 = np.block([[A, -I], [I, Z]])
    M1 = np.block([[Q, Z], [Z, I]])
    try:
        from scipy.linalg import eig
        w = eig(M0, M1, right=False)
    except Exception:                                   # noqa: BLE001
        w = np.linalg.eigvals(np.linalg.pinv(M1) @ M0)
    return np.array([x for x in w if np.isfinite(x)])


def main() -> int:
    C = cands()
    ISA = ["F_p", "CX_pf", "CX_fp", "Z1"]

    print("=" * 78)
    print("Pass 3120 -- the graph RH for the instruction layer, third attempt")
    print("=" * 78)
    A, coll = graph(ISA, C)
    deg = A.sum(axis=1)
    dmin, dmax = int(deg.min()), int(deg.max())
    u = bass_poles(A)
    r = np.abs(u)
    body = r[np.abs(r - 1.0) > 1e-6]
    lo, hi = 1 / sqrt(dmax - 1), 1 / sqrt(dmin - 1)
    inside = int(np.sum((body >= lo - 1e-9) & (body <= hi + 1e-9)))
    print(f"  V 81  E {int(A.sum()//2)}  degrees {dmin}..{dmax}")
    print(f"  RH band for a non-regular graph: |u| in [{lo:.6f}, {hi:.6f}]")
    print(f"  non-trivial poles {len(body)}, inside {inside} "
          f"({inside/max(1,len(body))*100:.1f}%)")
    print(f"  pole radii: min {body.min():.6f}  median {np.median(body):.6f}  "
          f"max {body.max():.6f}")
    frac = inside / max(1, len(body))
    print(f"""
  A REAL ANSWER, FROM A TOOL THAT REPRODUCES K_4.  {frac*100:.1f}% of the instruction
  layer's non-trivial poles lie in the band a non-regular graph can be held to.  The
  address layer, by contrast, has 100% of its poles on a single circle -- it satisfies the
  graph Riemann Hypothesis exactly, which is the strongest form of this statement there is.

  Third attempt at this question, and the first that produced a number rather than a
  symptom.  The difference was validating the routine first.""")

    print()
    print("=" * 78)
    print("Pass 3121 -- the minimum collision count over COMPUTING generating sets")
    print("=" * 78)
    best, rows = None, []
    for combo in combinations(sorted(C), 4):
        A2, cl = graph(combo, C)
        n = A2.shape[0]
        seen, fr = {0}, [0]
        while fr:
            v = fr.pop()
            for u2 in np.flatnonzero(A2[v]):
                if int(u2) not in seen:
                    seen.add(int(u2))
                    fr.append(int(u2))
        if len(seen) != n:
            continue
        computing = any(nm in LIN for nm in combo)     # at least one non-translation
        rows.append((cl, computing, combo))
        if computing and (best is None or cl < best[0]):
            best = (cl, combo)
    comp = [r for r in rows if r[1]]
    abel = [r for r in rows if not r[1]]
    print(f"  connected 4-sets: {len(rows)}  computing {len(comp)}  abelian {len(abel)}")
    print(f"  minimum collisions over COMPUTING sets : {best[0]}  ({' + '.join(best[1])})")
    print(f"  collisions for the abelian set          : {abel[0][0] if abel else '-'}")
    print(f"  ISA in use ({' + '.join(ISA)}): {coll}")
    print(f"""
  So the cost of being able to compute is exactly {best[0]} collisions out of 324 outgoing
  edges -- {best[0]/324*100:.1f}% of the frame graph's out-degree is wasted on generators that
  land where another generator already went.  The abelian set wastes none.  That is the
  price of non-commutativity, measured rather than asserted.""")

    print()
    print("=" * 78)
    print("Pass 3122 -- is the abelian 8-regular graph useful as a routing sub-layer?")
    print("=" * 78)
    Aab, _ = graph(["Z0", "Z1", "Z2", "Z3"], C)
    ev = np.sort(np.linalg.eigvalsh(Aab))[::-1]
    k = int(Aab.sum(axis=1)[0])
    lam2 = max(abs(ev[1]), abs(ev[-1]))
    ram = 2 * sqrt(k - 1)
    # diameter
    D = (Aab > 0).astype(int)
    reach, d, cur = np.eye(81, dtype=bool) | (D > 0), 1, (np.eye(81, dtype=bool) | (D > 0))
    while not reach.all():
        cur = (cur @ (D > 0)) > 0
        reach = reach | cur
        d += 1
        if d > 20:
            break
    print(f"  {k}-regular, |lambda_2| {lam2:.4f} vs bound {ram:.4f} -> "
          f"{'RAMANUJAN' if lam2 <= ram + 1e-9 else 'not'}")
    print(f"  diameter {d}")
    print(f"""
  It is a {k}-regular Ramanujan graph of diameter {d} on the 81 frames, and it is abelian --
  which is exactly the profile a ROUTING layer wants and exactly the wrong profile for a
  compute layer.  The machine already separates those two concerns (address transport by
  transvections, frame algebra by opcodes), and this says the separation is not a
  convenience: the two jobs want structurally different graphs, and no single generating
  set is good at both.""")

    out = {"pass_3120": {"degrees": [dmin, dmax], "band": [lo, hi],
                         "nontrivial_poles": int(len(body)), "inside": inside,
                         "fraction_inside": frac,
                         "radii": {"min": float(body.min()),
                                   "median": float(np.median(body)),
                                   "max": float(body.max())}},
           "pass_3121": {"connected_sets": len(rows), "computing": len(comp),
                         "min_collisions_computing": best[0],
                         "min_collisions_set": list(best[1]),
                         "isa_collisions": coll, "out_edges": 324},
           "pass_3122": {"degree": k, "lambda2": float(lam2), "bound": ram,
                         "is_ramanujan": bool(lam2 <= ram + 1e-9), "diameter": d}}
    path = ROOT / "data" / "PART_W33_PASS3120_3122_BASS_COLLISIONS.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
