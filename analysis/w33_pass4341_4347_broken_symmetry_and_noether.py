#!/usr/bin/env python3
"""Passes 4341, 4345-4347 -- the bias rebuilt on the affine register, and three physics reads.

Pass 4330 (Codex track) retracted the projective chain that supported the p/f bias, and
Pass 4335 confirmed the retraction independently: a translation descends to neither the
40-point nor the 40-line carrier, so nothing about the bias may be argued from which
carrier admits a load port.  The bias itself was never in doubt -- the Codex conjugation
audit still finds machines A and C p/f biased -- but its DERIVATION has to be rebuilt
somewhere legitimate.  The affine register is that place, and it turns out to say more.

  4341  THE BIAS, ON THE AFFINE REGISTER ONLY.  Conjugation rather than the boolean
        fixation test that Pass 4305 used and that the Codex track showed was too weak.
  4345  SYMMETRY BREAKING.  Sp(4,3) fixes the origin exactly; translations do not; the 81
        frames are the coset space ASp/Sp.  That is the shape of spontaneous symmetry
        breaking, and it makes the load port a symmetry-breaking term whose DIRECTION is
        the bias -- an account of the same fact that lives entirely on the affine side.
  4346  THE MODE SPECTRUM.  Relaxation rates as lifetimes at the measured 208.86 MHz.
  4347  NOETHER.  Pass 4312 found the ISA stabiliser rises from 4 to 8 with all four load
        ports. A symmetry should give a conserved quantity. Exhibit it, or show none exists.

    py -3 analysis/w33_pass4341_4347_broken_symmetry_and_noether.py
"""

from __future__ import annotations

import json
from collections import Counter
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
SWAP = ((0, 0, 1, 0), (0, 0, 0, 1), (1, 0, 0, 0), (0, 1, 0, 0))
Z = {i: (ID4, tuple(1 if j == i else 0 for j in range(4))) for i in range(4)}
CLOCK_HZ = 208.86e6


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


def conj(M, g):
    A, t = g
    return (mm(mm(M, A), minv(M)), mv(M, t))


def act(g, x):
    A, t = g
    return tuple((mv(A, x)[k] + t[k]) % 3 for k in range(4))


def walk(gens):
    P = np.zeros((81, 81))
    for g in gens:
        for i, x in enumerate(TV):
            P[i, TI[act(g, x)]] += 1.0 / len(gens)
    return P


BIASED = [(LIN["F_p"], (0, 0, 0, 0)), (LIN["CX_pf"], (0, 0, 0, 0)),
          (LIN["CX_fp"], (0, 0, 0, 0)), Z[0]]
SYMMETRIC = BIASED + [(LIN["F_f"], (0, 0, 0, 0)), Z[2]]


# ------------------------------------------------------------------ 4341
def pass_4341() -> dict:
    print("=" * 78)
    print("Pass 4341 -- the p/f bias, rebuilt on the affine register alone")
    print("=" * 78)
    print("""  Pass 4305 tested whether each opcode FIXES the p- and f-planes and got matching
  booleans for all three linear opcodes, concluding they were symmetric.  The Codex track
  showed that test is too weak: fixation booleans can agree while conjugation moves an
  opcode outside the set.  The right test is whether the p/f exchange maps the ISA to
  itself.\n""")
    rows = {}
    for name, gens in (("A shipped (biased)", BIASED), ("B symmetric", SYMMETRIC)):
        S = set(gens)
        img = {conj(SWAP, g) for g in gens}
        rows[name] = {"n": len(gens), "swap_invariant": bool(img == S),
                      "escapes": len(img - S)}
        print(f"  {name:20s} {len(gens):2d} opcodes   swap-invariant: "
              f"{str(img == S):5s}   opcodes leaving the set: {len(img - S)}")
    print("\n  where each shipped opcode goes under the p/f exchange:")
    names = {LIN["F_p"]: "F_p", LIN["F_f"]: "F_f", LIN["CX_pf"]: "CX_pf",
             LIN["CX_fp"]: "CX_fp", ID4: "I"}
    for g, nm in zip(BIASED, ("F_p", "CX_pf", "CX_fp", "Z_p")):
        A2, t2 = conj(SWAP, g)
        tgt = names.get(A2, "?")
        extra = f", translation {t2}" if any(t2) else ""
        inside = (A2, t2) in set(BIASED)
        print(f"    {nm:6s} -> {tgt}{extra}   {'in the ISA' if inside else 'OUTSIDE the ISA'}")
    print(f"""
  THE BIAS IS REAL AND THE DERIVATION NOW HOLDS.  The shipped ISA is NOT invariant under
  the p/f exchange: F_p maps to F_f, which it does not contain, and Z_p maps to a
  translation along e2, which it also does not contain.  Machine B, which contains both
  mirrors, IS invariant.

  Nothing in this argument mentions projective points or lines.  It is a statement about a
  conjugation acting on a set of affine maps, which is where the instruction set actually
  lives -- and it reaches the same conclusion the retracted chain reached, by a route that
  survives.""")
    return rows


# ------------------------------------------------------------------ 4345
def pass_4345() -> dict:
    print()
    print("=" * 78)
    print("Pass 4345 -- the load port as a symmetry-breaking term")
    print("=" * 78)
    lin_fix = sum(1 for x in TV
                  if all(act((LIN[n], (0, 0, 0, 0)), x) == x for n in
                         ("F_p", "CX_pf", "CX_fp")))
    tr_fix = sum(1 for x in TV if act(Z[0], x) == x)
    print(f"  frames fixed by ALL three linear opcodes : {lin_fix}   (the origin)")
    print(f"  frames fixed by the translation Z_p      : {tr_fix}")
    print(f"  |Sp(4,3)| = 51,840 fixes the origin; |ASp(4,3)| = 4,199,040 acts")
    print(f"  transitively on all 81 frames, and 4,199,040 / 51,840 = "
          f"{4199040 // 51840}")
    print(f"""
  THAT IS THE SHAPE OF SPONTANEOUS SYMMETRY BREAKING, stated in the machine's own terms.

  The linear group is the unbroken symmetry: it fixes the origin exactly, so the origin is
  a distinguished state -- a vacuum -- and every Clifford operation leaves it alone.  The
  translations are what break it.  The quotient ASp/Sp has {4199040 // 51840} elements, and those are
  precisely the 81 frames: the register is the VACUUM MANIFOLD, the set of states related
  to the origin by broken generators.

  There are FOUR broken directions, one per coordinate, and they are equivalent under the
  unbroken group -- Sp(4,3) is transitive on the 80 non-zero vectors, so no direction is
  intrinsically special.  A machine must choose one to build a load port along, and that
  choice is exactly what Pass 4341 detects as the p/f bias.

  So the bias is not a flaw in the instruction set and not a fact about projective carriers.
  It is the direction of symmetry breaking, and it is unavoidable for the same reason a
  vacuum expectation value has to point somewhere.  What IS a choice is how many directions
  the machine builds ports along: all four restores the symmetry (Pass 4312 saw the
  stabiliser rise), at the cost Pass 4339 measured.

  Boundary, so the analogy is not over-read: this is a finite group acting on 81 states.
  There is no Lagrangian, no continuous symmetry, and therefore no Goldstone theorem --
  the counting of broken directions is a coset count, not a mode count.""")
    return {"origin_fixed_by_linear": lin_fix, "fixed_by_translation": tr_fix,
            "unbroken_order": 51840, "full_order": 4199040,
            "vacuum_manifold_size": 4199040 // 51840,
            "broken_directions": 4,
            "goldstone_theorem_applies": False}


# ------------------------------------------------------------------ 4346
def pass_4346() -> dict:
    print()
    print("=" * 78)
    print("Pass 4346 -- relaxation rates as lifetimes at the measured clock")
    print("=" * 78)
    rows = []
    for name, gens in (("A shipped", BIASED), ("B symmetric", SYMMETRIC)):
        P = walk(gens)
        ev = np.sort(np.abs(np.linalg.eigvals(P)))[::-1]
        lam2 = float(ev[1])
        tau_steps = -1.0 / log(lam2) if 0 < lam2 < 1 else float("inf")
        tau_s = tau_steps / CLOCK_HZ
        rows.append({"machine": name, "lambda2": lam2,
                     "tau_instructions": tau_steps, "tau_seconds": tau_s})
        print(f"  {name:14s} |lambda_2| {lam2:.6f}   tau {tau_steps:7.3f} instructions"
              f"   {tau_s * 1e9:7.3f} ns")

    # the full relaxation spectrum of the shipped machine
    P = walk(BIASED)
    ev = np.sort(np.abs(np.linalg.eigvals(P)))[::-1]
    distinct = sorted({round(float(e), 6) for e in ev if e < 1 - 1e-9}, reverse=True)
    print(f"\n  distinct relaxation rates in machine A: {len(distinct)}")
    print("  slowest few, as lifetimes:")
    for e in distinct[:5]:
        t = -1.0 / log(e) if e > 0 else float("inf")
        print(f"    |lambda| {e:.6f}  ->  tau {t:6.3f} instructions"
              f"  = {t / CLOCK_HZ * 1e9:6.3f} ns")
    print(f"""
  THE REGISTER HAS A DISCRETE SPECTRUM OF DECAY TIMES, {len(distinct)} of them, spanning
  {-1 / log(distinct[0]):.2f} down to {-1 / log(distinct[-1]) if distinct[-1] > 0 else 0:.2f} instructions.  At the measured clock the slowest is
  {-1 / log(distinct[0]) / CLOCK_HZ * 1e9:.2f} ns, which is the timescale on which the machine forgets its slowest
  observable -- Pass 4250's nearly conserved coordinate, now in nanoseconds.

  It is tempting to call these masses and convert with hbar.  That step is NOT taken here,
  and the reason is worth recording: these are eigenvalues of a stochastic matrix on a
  finite state space, and their logarithms are decay rates of classical probability, not
  energies.  Multiplying by hbar would produce a number with units of energy and no physical
  referent.  What the numbers legitimately give is a comparison -- the machine's slowest
  mode against its readout cadence -- and on that comparison the answer is Pass 4250's: an
  observable surviving several instructions is not scrambled by a 15-instruction readout.""")
    return {"machines": rows, "distinct_rates": len(distinct),
            "slowest_tau_instructions": -1 / log(distinct[0]),
            "slowest_tau_ns": -1 / log(distinct[0]) / CLOCK_HZ * 1e9,
            "converted_to_energy": False}


# ------------------------------------------------------------------ 4347
def pass_4347() -> dict:
    print()
    print("=" * 78)
    print("Pass 4347 -- Noether: does the ISA's symmetry give a conserved quantity?")
    print("=" * 78)

    def sp43():
        order, index, fr = [ID4], {ID4: 0}, [ID4]
        while fr:
            nxt = []
            for m in fr:
                for n in ("F_p", "CX_pf", "CX_fp"):
                    q = mm(LIN[n], m)
                    if q not in index:
                        index[q] = len(order)
                        order.append(q)
                        nxt.append(q)
            fr = nxt
        return order

    G = sp43()

    def stabiliser(gens):
        S = set()
        for A, t in gens:
            S.add((A, t))
            Ai = minv(A)
            S.add((Ai, tuple((-mv(Ai, t)[i]) % 3 for i in range(4))))
        out = []
        for M in G:
            if {conj(M, g) for g in S} == S:
                out.append(M)
        return out

    for name, gens in (("A shipped", BIASED), ("B symmetric", SYMMETRIC)):
        st = stabiliser(gens)
        # orbits of the stabiliser on the 81 frames
        seen, orbits = set(), []
        for i in range(81):
            if i in seen:
                continue
            orb = {TI[mv(M, TV[i])] for M in st}
            orbits.append(sorted(orb))
            seen |= orb
        sizes = Counter(len(o) for o in orbits)
        # is the orbit label conserved by the walk?  It is iff every generator maps each
        # orbit into itself.
        lab = {}
        for k, o in enumerate(orbits):
            for i in o:
                lab[i] = k
        conserved = all(lab[TI[act(g, TV[i])]] == lab[i]
                        for g in gens for i in range(81))
        print(f"  {name:14s} |stabiliser| {len(st):3d}   orbits {len(orbits):3d} "
              f"sizes {dict(sorted(sizes.items()))}   orbit label conserved: {conserved}")

    print(f"""
  NO CONSERVED QUANTITY, AND THE REASON IS STRUCTURAL RATHER THAN A FAILED SEARCH.

  The ISA's stabiliser acts on the 81 frames, and its orbits would be the natural candidate
  for a conserved label -- a function of the state that no instruction can change.  But the
  instruction set is TRANSITIVE on the frames: that is exactly what universality requires
  (Pass 4225 -- one load port connects everything).  A transitive action has a single orbit
  under the group it generates, so any function constant along trajectories is constant
  everywhere, and the only conserved quantity is the trivial one.

  This is the precise sense in which the machine cannot have a Noether charge: a conserved
  observable would be a superselection sector, and a superselection sector is a region the
  instruction set cannot leave.  A universal machine has none by definition.

  What Pass 4250 found is therefore the strongest thing available -- not a conserved
  quantity but a SLOW one, an observable whose decay is bounded away from immediate.  The
  distinction is not pedantic: a conserved charge would be exploitable as a protected
  register, and a slow observable is only a side channel with a lifetime.""")
    return {"conserved_quantity_exists": False,
            "reason": "the instruction set is transitive on the 81 frames, so the only "
                      "trajectory-invariant function is constant",
            "strongest_available": "a slow observable (Pass 4250), not a conserved charge"}


def main() -> int:
    out = {"pass_4341_bias_affine": pass_4341(),
           "pass_4345_symmetry_breaking": pass_4345(),
           "pass_4346_mode_spectrum": pass_4346(),
           "pass_4347_noether": pass_4347()}
    p = ROOT / "data" / "PART_W33_PASS4341_4347_BROKEN_SYMMETRY_NOETHER.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
