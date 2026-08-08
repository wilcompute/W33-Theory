#!/usr/bin/env python3
"""Pass 4353 -- "thermodynamic reversibility costs 2.00x the cells" is an over-read.

Pass 4352 asked the Codex track whether "reversible" is the right word for machines C and
D.  The question is answerable here, and the answer is that the blueprint currently implies
something stronger than what was computed.

WHAT WAS COMPUTED (Pass 4252).  Drive the machine with UNIFORMLY RANDOM opcodes.  That is a
Markov chain on 81 frames.  For machines A and B the chain is not reversible in the
detailed-balance sense -- there are ordered pairs with a forward move and no reverse move --
so the stationary entropy production is infinite.  Closing the opcode set under inverses
makes the transition matrix symmetric and the entropy production exactly zero.

WHAT THE BLUEPRINT IMPLIES.  "Thermodynamic reversibility costs 2.00x the cells" reads as:
machine A dissipates heat while machine D does not, so pay 2x to stop dissipating.

THOSE ARE DIFFERENT CLAIMS, and this pass separates them.  Every opcode of every machine
here is a BIJECTION on the 81 frames.  A deterministic program is a composition of
bijections, so it erases nothing and its Landauer cost is zero -- on machine A as much as on
machine D.  The entropy production figure describes a machine driven by random instructions,
which is not how a computer is used.

    py -3 analysis/w33_pass4353_what_reversible_actually_means.py
"""

from __future__ import annotations

import json
from math import log
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ID4 = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))
TV = [(a, b, c, d) for a in range(3) for b in range(3)
      for c in range(3) for d in range(3)]
TI = {t: i for i, t in enumerate(TV)}
LIN = {"F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "F_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
       "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
       "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))}
Z = {i: (ID4, tuple(1 if j == i else 0 for j in range(4))) for i in range(4)}


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % 3 for j in range(4))
                 for i in range(4))


def minv(M):
    a = [list(M[i]) + [1 if j == i else 0 for j in range(4)] for i in range(4)]
    r = 0
    for c in range(4):
        p = next(i for i in range(r, 4) if a[i][c] % 3)
        a[r], a[p] = a[p], a[r]
        iv = 1 if a[r][c] % 3 == 1 else 2
        a[r] = [(x * iv) % 3 for x in a[r]]
        for i in range(4):
            if i != r and a[i][c] % 3:
                f = a[i][c] % 3
                a[i] = [(a[i][k] - f * a[r][k]) % 3 for k in range(8)]
        r += 1
    return tuple(tuple(a[i][4:]) for i in range(4))


def inv_op(g):
    M, t = g
    Mi = minv(M)
    return (Mi, tuple((-mv(Mi, t)[i]) % 3 for i in range(4)))


def act(g, x):
    M, t = g
    return tuple((mv(M, x)[k] + t[k]) % 3 for k in range(4))


BIASED = [(LIN["F_p"], (0, 0, 0, 0)), (LIN["CX_pf"], (0, 0, 0, 0)),
          (LIN["CX_fp"], (0, 0, 0, 0)), Z[0]]


def close(gs):
    out, seen = [], set()
    for g in gs:
        for h in (g, inv_op(g)):
            if h not in seen:
                seen.add(h)
                out.append(h)
    return out


def main() -> int:
    print("=" * 78)
    print("Pass 4353 -- is every opcode already reversible?")
    print("=" * 78)
    machines = {"A shipped (4 opcodes)": BIASED,
                "C closure (8 opcodes)": close(BIASED)}
    for name, gens in machines.items():
        bij = all(len({act(g, x) for x in TV}) == 81 for g in gens)
        print(f"  {name:24s} every opcode a bijection on the 81 frames: {bij}")

    print("\n  a deterministic program is a composition of bijections, so it is")
    print("  information-preserving on BOTH machines.  Check it on a random program:")
    rng = np.random.default_rng(4353)
    for name, gens in machines.items():
        seq = [int(v) for v in rng.integers(0, len(gens), size=200)]
        # run every start state through the same program: injective iff no info lost
        ends = set()
        for x in TV:
            y = x
            for s in seq:
                y = act(gens[s], y)
            ends.add(y)
        print(f"  {name:24s} 200-instruction program maps 81 states to "
              f"{len(ends)} states  -> {'injective, zero erasure' if len(ends) == 81 else 'LOSSY'}")

    print(f"""
  SO THE LANDAUER COST OF COMPUTING IS ZERO ON BOTH MACHINES, and the blueprint's phrasing
  is an over-read.  "Thermodynamic reversibility costs 2.00x the cells" reads as: machine A
  dissipates and machine D does not.  It does not.  Every opcode in every machine here is a
  bijection, a program is a composition of bijections, and nothing is erased on either.

  WHAT PASS 4252 ACTUALLY MEASURED is a property of a different object: the Markov chain you
  get by driving the machine with UNIFORMLY RANDOM opcodes.  That chain fails detailed
  balance for machine A -- some frame pairs admit a forward move and no reverse -- so its
  stationary entropy production diverges, while the closure's chain is symmetric and its
  entropy production is exactly zero.

  THAT IS A REAL AND USEFUL QUANTITY, but it is about the instruction set as a RANDOMNESS
  SOURCE, not about executing a program.  It says: watch a random instruction stream on
  machine A and you can tell which way time runs; watch one on machine D and you cannot.
  For a machine used as a scrambler, a physical randomness source, or anything whose
  security rests on trajectory indistinguishability, that difference is the whole point.
  For a machine running a program, it is not a dissipation at all.

  The correction to make: say "the random-instruction walk is reversible" rather than "the
  machine is thermodynamically reversible", and price the 2.00x against the property it
  actually buys.""")

    # the two quantities, side by side
    def entropy_production(gens):
        n = 81
        P = np.zeros((n, n))
        for g in gens:
            for x in TV:
                P[TI[x], TI[act(g, x)]] += 1.0 / len(gens)
        ow = int(((P > 0) & (P.T == 0)).sum())
        if ow:
            return float("inf"), ow
        s = 0.0
        for i in range(n):
            for j in range(n):
                if P[i, j] > 0 and P[j, i] > 0:
                    s += (1.0 / n) * P[i, j] * log(P[i, j] / P[j, i])
        return s / log(2), 0

    print(f"\n  {'machine':24s} {'program erasure':>16s} {'random-walk entropy':>22s}")
    out = {}
    for name, gens in machines.items():
        e, ow = entropy_production(gens)
        out[name] = {"opcodes": len(gens), "program_erasure_bits": 0.0,
                     "random_walk_entropy_bits": None if e == float("inf") else e,
                     "one_way_pairs": ow}
        print(f"  {name:24s} {'0 bits':>16s} "
              f"{('infinite' if e == float('inf') else f'{e:.3e} bits'):>22s}")

    p = ROOT / "data" / "PART_W33_PASS4353_WHAT_REVERSIBLE_MEANS.json"
    p.parent.mkdir(exist_ok=True)
    res = {"machines": out,
           "every_opcode_bijective": True,
           "program_landauer_cost_bits": 0.0,
           "over_read": ("'thermodynamic reversibility costs 2.00x' implies machine A "
                         "dissipates while D does not; both erase nothing"),
           "correct_statement": ("closing the opcode set under inverses makes the "
                                 "UNIFORM-RANDOM-INSTRUCTION walk satisfy detailed "
                                 "balance; it buys trajectory time-symmetry, not a "
                                 "reduction in the Landauer cost of computing")}
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(res)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
