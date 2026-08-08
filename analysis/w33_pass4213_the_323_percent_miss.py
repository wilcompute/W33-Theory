#!/usr/bin/env python3
"""Pass 4213 -- the 3.23% Ramanujan miss, and a correction to Pass 4204's own arithmetic.

The blueprint carries a headline from Pass 3042: "the instruction graph is not Ramanujan,
it misses by 3.23%".  That pass took lam2 = 0.893992320 (measured at Pass 2867) and
compared it with 2*sqrt(3)/4 = 0.866025, "the Ramanujan bound for a 4-regular graph".

Pass 4203 then showed the frame graph is a Schreier graph with degrees 2 to 8, not
4-regular.  So the comparison needs re-examining -- but carefully, because the first
attempt at this pass got it wrong in an instructive way.

WHAT THE FIRST ATTEMPT GOT WRONG, AND HOW IT WAS CAUGHT.  It assumed the four-opcode ISA
was F_p, F_f, CX_pf, CX_fp -- four Clifford operations -- and found the origin isolated and
the walk undefined.  That set is not the ISA.  Reading Pass 2866 rather than recalling it,
the actual ISA is F_p, CX_pf, CX_fp, Z_p: THREE linear opcodes and ONE TRANSLATION.  The
machine has a load port, and the three linear opcodes alone generate Sp(4,3); the
translation is what lifts them to the full affine group.  The tell was available without
reading anything: a Clifford-only set cannot be universal, because Pass 4204 had just
proved every linear map fixes the origin.  The wrong set was assumed, and the assumption
contradicted the pass that immediately preceded it.

So this pass does two jobs.

(a) REPRODUCE 0.893992320 from the real ISA and say exactly what it measures.
(b) DECIDE whether the 3.23%% verdict survives, and correct Pass 4204(c), which reported a
    deficiency profile and an isolated origin for the wrong four opcodes.

    py -3 analysis/w33_pass4213_the_323_percent_miss.py
"""

from __future__ import annotations

import json
from collections import Counter
from math import sqrt
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
TARGET = 0.893992320

TV = [(a, b, c, d) for a in range(3) for b in range(3)
      for c in range(3) for d in range(3)]
TI = {t: i for i, t in enumerate(TV)}
ID4 = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))

LIN = {"F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "F_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
       "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
       "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))}

# Pass 2866's ISA, read from the source rather than recalled: three linear opcodes and
# one translation.  Z_p is the load port.
ISA = [(LIN["F_p"], (0, 0, 0, 0)), (LIN["CX_pf"], (0, 0, 0, 0)),
       (LIN["CX_fp"], (0, 0, 0, 0)), (ID4, (1, 0, 0, 0))]
CLIFFORD_ONLY = [(LIN[n], (0, 0, 0, 0)) for n in ("F_p", "F_f", "CX_pf", "CX_fp")]


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def act(g, x):
    M, t = g
    return tuple((mv(M, x)[k] + t[k]) % 3 for k in range(4))


def walk(gens):
    """The walk the machine performs: pick an opcode uniformly, apply it.  Keeps loops
    and multiplicities, so it is defined whether or not the simple graph is regular."""
    P = np.zeros((81, 81))
    for g in gens:
        for i, x in enumerate(TV):
            P[i, TI[act(g, x)]] += 1.0 / len(gens)
    return P


def simple(gens):
    A = np.zeros((81, 81))
    for g in gens:
        for i, x in enumerate(TV):
            j = TI[act(g, x)]
            A[i, j] = 1
            A[j, i] = 1
    np.fill_diagonal(A, 0)
    return A


def lam2(P):
    return float(sorted((abs(v) for v in np.linalg.eigvals(P)), reverse=True)[1])


def main() -> int:
    print("=" * 78)
    print("Pass 4213(a) -- reproducing 0.893992320 from the real ISA")
    print("=" * 78)
    P = walk(ISA)
    L = lam2(P)
    ds = bool(np.allclose(P.sum(0), 1) and np.allclose(P.sum(1), 1))
    A = simple(ISA)
    d = A.sum(axis=1)
    print("  ISA = F_p, CX_pf, CX_fp, Z_p   (three linear opcodes and one translation)")
    print(f"  uniform-opcode walk |lambda_2| : {L:.9f}")
    print(f"  Pass 2867's figure             : {TARGET:.9f}")
    print(f"  reproduced                     : {abs(L - TARGET) < 5e-7}")
    print(f"  doubly stochastic (uniform stationary distribution): {ds}")
    print(f"  simple-graph degrees           : {int(d.min())} to {int(d.max())}"
          f"   regular: {bool(d.min() == d.max())}")
    print(f"""
  The MEASUREMENT is sound and survives intact.  Every opcode is a bijection, so the
  transition matrix is doubly stochastic, the stationary distribution is exactly uniform,
  and the relaxation and mixing times Pass 2867 derived from it -- 9.4 and 15 instructions
  -- are properties of a walk that genuinely exists.  Nothing about the Schreier
  correction touches any of that.""")

    print()
    print("=" * 78)
    print("Pass 4213(b) -- does the 3.23% verdict survive?  No.")
    print("=" * 78)
    bound4 = 2 * sqrt(3) / 4
    print(f"  quoted threshold, 4-regular : 2*sqrt(3)/4 = {bound4:.9f}")
    print(f"  measured                    : {L:.9f}")
    print(f"  quoted shortfall            : {100 * (L - bound4) / bound4:.2f}%")
    print(f"  but the graph's degrees are : {int(d.min())} to {int(d.max())}, so it is"
          f" not 4-regular")
    print(f"""
  The threshold is the wrong number for this object.  2*sqrt(k-1)/k is the Ramanujan
  bound for a k-REGULAR graph, and it is that because the universal cover of a k-regular
  graph is the k-regular tree, whose spectral radius is 2*sqrt(k-1).  A graph with degrees
  {int(d.min())} to {int(d.max())} has a different universal cover and a different radius, so
  0.866025 is not the value it must beat.  The 3.23%% is a precise-looking figure for a
  quantity that is not defined on this graph.

  What is left is a comparison, not a verdict: the address layer attains the optimum for
  its degree, and the instruction layer mixes more slowly.  How much short of optimal it
  falls is not a question this graph admits.

  Third instance of the same category error on this one object: Pass 3060 (withdrawn),
  Pass 4201 (withdrawn at Pass 4204), and now Pass 3042's headline.  One shared cause --
  the graph was called a Cayley graph until Pass 4203, and that made regularity feel like
  something it had to have.""")

    print()
    print("=" * 78)
    print("Pass 4213(c) -- correcting Pass 4204(c), which used the wrong four opcodes")
    print("=" * 78)
    Ac = simple(CLIFFORD_ONLY)
    dc = Ac.sum(axis=1)
    prof = Counter(int(8 - v) for v in d)
    profc = Counter(int(8 - v) for v in dc)
    print("  Pass 4204(c) computed the deficiency profile of F_p, F_f, CX_pf, CX_fp:")
    print(f"    degrees {int(dc.min())} to {int(dc.max())}, profile {dict(sorted(profc.items()))}"
          f", isolated frames {int((dc == 0).sum())}")
    print("  That set is Clifford-only, so by Pass 4204(a) it fixes the origin and by")
    print("  Pass 4202 it is not universal.  It is not the ISA.  The real ISA gives:")
    print(f"    degrees {int(d.min())} to {int(d.max())}, profile {dict(sorted(prof.items()))}"
          f", isolated frames {int((d == 0).sum())}")
    print(f"""
  So Pass 4204(c)'s striking sentence -- "the Clifford-only ISA leaves the origin
  isolated, degree zero" -- is TRUE OF THAT SET and is a fair illustration of Pass 2774
  (symplectic maps fix zero, so a register with no load port is provably constant).  It is
  simply not a statement about the machine's instruction set, because the machine HAS a
  load port: Z_p is one of its four opcodes, and it is precisely what stops the origin
  being isolated.  The real ISA's minimum degree is {int(d.min())}, not 0.

  Read the right way round, that is the sharper result.  The load port is not an
  engineering convenience bolted onto a Clifford core; it is the single opcode that makes
  the frame graph connected at all, and Pass 4204(a) says why -- it is the only kind of
  generator that acts freely.""")

    out = {
        "isa": ["F_p", "CX_pf", "CX_fp", "Z_p"],
        "lambda2_reproduced": L,
        "lambda2_target": TARGET,
        "reproduces": bool(abs(L - TARGET) < 5e-7),
        "doubly_stochastic": ds,
        "degrees": [int(d.min()), int(d.max())],
        "regular": bool(d.min() == d.max()),
        "quoted_threshold_4regular": bound4,
        "verdict": ("the 0.893992320 measurement stands -- doubly stochastic, uniform "
                    "stationary, mixing time 15 -- but the '3.23% short of Ramanujan' "
                    "verdict is withdrawn: it scores a graph with degrees 2-8 against a "
                    "4-regular threshold, which is not defined for it"),
        "pass4204c_correction": {
            "wrong_set": ["F_p", "F_f", "CX_pf", "CX_fp"],
            "wrong_set_degrees": [int(dc.min()), int(dc.max())],
            "wrong_set_isolated": int((dc == 0).sum()),
            "real_isa_degrees": [int(d.min()), int(d.max())],
            "real_isa_isolated": int((d == 0).sum()),
            "note": ("Pass 4204(c) profiled a Clifford-only set that is neither the ISA "
                     "nor universal; the real ISA contains the translation Z_p, and that "
                     "load port is exactly what keeps the origin from being isolated"),
        },
        "address_graph_unaffected": {"regular_degree": 12, "lambda2_over_k": 2.0 / 12.0,
                                     "ramanujan_bound": 2 * sqrt(11) / 12,
                                     "is_ramanujan": True},
    }
    path = ROOT / "data" / "PART_W33_PASS4213_THE_323_PERCENT_MISS.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
