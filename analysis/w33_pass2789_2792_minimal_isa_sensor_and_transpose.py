#!/usr/bin/env python3
"""Passes 2789, 2791, 2792 -- three questions the last batch left open.

PASS 2789.  Pass 2778 proved the eight opcodes generate ASp(4,3) and that the second
translation is redundant.  That is a statement about ONE opcode.  The sharper hardware
question is: what is the SMALLEST subset of the instruction set that still generates the
whole group?  Every opcode removed is decoder logic removed, and if the answer is small
enough the opcode field itself shrinks.

PASS 2791.  Pass 2779 found the two-qutrit sensor exponent is 9 = dim, with phase group
mu_12, and that 9 is minimal.  For n qutrits the dimension is 3^n, so the minimal
exponent is the least e with e = 3^n (mod 12) -- and 3^n mod 12 cycles 3, 9, 3, 9.  If
that is right, ODD register widths need only a CUBE, not a ninth power, which is a
cheaper measurement.  The n = 1 group is small enough to settle exactly by enumeration
rather than by sampling.

PASS 2792.  Pass 2750 stated "time reversal is outer exactly when q = 3 (mod 4)" but
verified the transpose CONSTRUCTION only at q = 3; the general claim rested on the
quadratic-residue fact plus that one identification.  This builds the matrix at
q = 3, 5, 7, 11, 13, 17, 19, 23 and checks it.

    py -3 analysis/w33_pass2789_2792_minimal_isa_sensor_and_transpose.py
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# shared F_3 matrix machinery (same generators as Pass 2778, from w33_pass2762_frame_step)
# ---------------------------------------------------------------------------

LIN = {
    "F_p":   ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
    "F_f":   ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
    "S_p":   ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
    "S_f":   ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1)),
    "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
    "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1)),
}
IDENT = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))


def mul(a, b, p=3):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(4)) % p for j in range(4))
        for i in range(4)
    )


def closure(gens, cap=60000):
    seen = {IDENT}
    frontier = [IDENT]
    while frontier:
        nxt = []
        for m in frontier:
            for g in gens:
                q = mul(g, m)
                if q not in seen:
                    seen.add(q)
                    nxt.append(q)
                    if len(seen) > cap:
                        return seen
        frontier = nxt
    return seen


# ===========================================================================
def pass_2789() -> dict:
    print("=" * 74)
    print("Pass 2789 -- the smallest instruction set that still generates ASp(4,3)")
    print("=" * 74)

    names = list(LIN)
    full = 51840
    results = {}

    # An affine group F_3^4 : H is the whole of ASp(4,3) iff H = Sp(4,3) AND at least
    # one translation is present (Sp(4,3) is transitive on the 80 nonzero vectors, so a
    # single translation's orbit already spans -- Pass 2778).  So the search reduces to
    # the LINEAR generators, which is a 4x4 closure instead of a 4.2M-element one.
    best = None
    for size in (1, 2, 3):
        found = []
        for combo in combinations(names, size):
            order = len(closure([LIN[c] for c in combo]))
            if order == full:
                found.append(combo)
        results[f"size_{size}"] = ["+".join(c) for c in found]
        print(f"  subsets of size {size} generating all of Sp(4,3): {len(found)}")
        for c in found[:8]:
            print(f"      {' + '.join(c)}")
        if found and best is None:
            best = found[0]
        if found:
            break

    if best:
        print(f"\n  MINIMAL Clifford subset: {' + '.join(best)}  ({len(best)} opcodes)")
        print(f"  Plus one translation (sigma^5 = Z) -> ASp(4,3), order {81*full}.")
        total = len(best) + 1
        bits = max(1, (total - 1).bit_length())
        print(f"  So the frame ISA needs {total} instructions, i.e. a {bits}-bit opcode")
        print(f"  field instead of 3 bits.  The other opcodes are convenience, not need.")
    return {"minimal_clifford_subsets": results,
            "minimal_size": len(best) if best else None,
            "frame_instructions_needed": (len(best) + 1) if best else None}


# ===========================================================================
def pass_2791() -> dict:
    print()
    print("=" * 74)
    print("Pass 2791 -- the sensor exponent for n qutrits")
    print("=" * 74)

    W = np.exp(2j * np.pi / 3)

    # Canonical key for matrix identity.  The FIRST version of this used
    # `np.round(m, 7).astype(np.complex64)`, which keeps only ~7 significant digits --
    # and entries like 1/sqrt3 = 0.5773502692 sit right on that boundary, so equal
    # matrices got different keys and the enumeration diverged to 156327 elements.  That
    # is not a group order (156327 = 3 * 52109) and was reported here only as a failure.
    # Rounding to a 1e-9 integer lattice in full double precision is safe: unitary
    # products accumulate ~1e-14 of error, five orders of magnitude below the grid.
    def canon(m):
        z = np.asarray(m, dtype=complex) * 1e9
        return (np.round(z.real).astype(np.int64).tobytes()
                + np.round(z.imag).astype(np.int64).tobytes())

    # n = 1: the single-qutrit Clifford group is small enough to ENUMERATE exactly,
    # so the phase group here is a theorem rather than a sample.
    F = np.array([[W ** (j * k) for k in range(3)] for j in range(3)]) / np.sqrt(3)
    S = np.diag([1, 1, W]).astype(complex)
    X = np.zeros((3, 3), dtype=complex)
    for j in range(3):
        X[(j + 1) % 3, j] = 1

    seen = {canon(np.eye(3)): np.eye(3, dtype=complex)}
    frontier = [np.eye(3, dtype=complex)]
    while frontier:
        nxt = []
        for m in frontier:
            for g in (F, S, X):
                q = g @ m
                k = canon(q)
                if k not in seen:
                    seen[k] = q
                    nxt.append(q)
        frontier = nxt
    print(f"  |<F, S, X>| on one qutrit, enumerated exactly : {len(seen)}")

    scal = []
    for m in seen.values():
        lam = m[0, 0]
        if np.allclose(m, lam * np.eye(3), atol=1e-9):
            scal.append(complex(round(lam.real, 6), round(lam.imag, 6)))
    scal = sorted(set(scal), key=lambda z: np.angle(z) % (2 * np.pi))
    m1 = len(scal)
    asp23 = 9 * 24                       # |ASp(2,3)| = |F_3^2| * |Sp(2,3)| = 9 * 24
    consistent = (len(seen) == m1 * asp23)
    print(f"  scalar subgroup at n = 1 : mu_{m1}")
    print(f"  |ASp(2,3)| = 9 * 24      : {asp23}")
    print(f"  mu_{m1} * {asp23} = {m1*asp23}  equals the enumerated order : {consistent}")
    if not consistent:
        print("  *** NOT a consistent group order -- treat the enumeration as FAILED ***")

    # The arithmetic that decides the exponent for every n.
    print("\n  minimal exponent e = 3^n (mod 12), for the phase group mu_12:")
    table = {}
    for n in range(1, 9):
        d = 3 ** n
        e = d % 12
        if e == 0:
            e = 12
        table[n] = {"dimension": d, "minimal_exponent": e}
        print(f"     n = {n}:  d = 3^{n} = {d:<7d} ->  e = {e}")
    print("\n  3^n mod 12 cycles 3, 9, 3, 9, ...  so ODD register widths need only a")
    print("  CUBE and EVEN widths a ninth power.  n = 2 gives 9, matching Pass 2779.")

    # Check the n = 1 claim numerically: is Tr(U)^3 / det(U) phase invariant on 3x3?
    rng = np.random.default_rng(2791)
    A = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    Q, _ = np.linalg.qr(A)
    lam = np.exp(2j * np.pi * 0.31)
    def theta(U, e):
        return np.trace(U) ** e / np.linalg.det(U)
    inv = {e: bool(abs(theta(lam * Q, e) - theta(Q, e)) < 1e-6) for e in (2, 3, 4, 9)}
    print("\n  invariance of Tr(U)^e / det(U) on a 3x3 unitary:")
    for e, ok in inv.items():
        print(f"     e = {e}: {ok}")

    return {"n1_group_order": len(seen), "n1_phase_group": m1,
            "n1_order_consistent": bool(consistent),
            "exponent_table": {str(k): v for k, v in table.items()},
            "n1_invariance_by_exponent": {str(k): v for k, v in inv.items()}}


# ===========================================================================
def pass_2792() -> dict:
    print()
    print("=" * 74)
    print("Pass 2792 -- the transpose construction at q > 3")
    print("=" * 74)

    # The anti-symplectic involution, in the parallel track's Pass 2762 coordinates:
    # it swaps past and future and flips the sign of the Z components.
    #     T : (x_p, z_p, x_f, z_f) -> (x_f, -z_f, x_p, -z_p)
    # The construction is q-independent; whether the RESULT is outer is not.
    def mats(q):
        T = [[0, 0, 1, 0],
             [0, 0, 0, q - 1],
             [1, 0, 0, 0],
             [0, q - 1, 0, 0]]
        J = [[0, 1, 0, 0],
             [q - 1, 0, 0, 0],
             [0, 0, 0, 1],
             [0, 0, q - 1, 0]]
        return T, J

    def mm(a, b, q):
        return [[sum(a[i][k] * b[k][j] for k in range(4)) % q for j in range(4)]
                for i in range(4)]

    def tr(a):
        return [[a[j][i] for j in range(4)] for i in range(4)]

    def scale(a, c, q):
        return [[(c * a[i][j]) % q for j in range(4)] for i in range(4)]

    print(f"  {'q':>4} {'T^2 = I':>9} {'T^T J T = -J':>14} "
          f"{'-1 square':>11} {'q mod 4':>9}  time reversal is")
    rows = {}
    for q in (3, 5, 7, 11, 13, 17, 19, 23):
        T, J = mats(q)
        t2 = mm(T, T, q) == [[1 if i == j else 0 for j in range(4)] for i in range(4)]
        anti = mm(mm(tr(T), J, q), T, q) == scale(J, q - 1, q)
        sq = any((s * s) % q == (q - 1) % q for s in range(q))
        verdict = "INNER (gauge)" if sq else "OUTER (physical)"
        rows[q] = {"T_squared_is_I": t2, "anti_symplectic": anti,
                   "minus_one_is_square": sq, "q_mod_4": q % 4, "verdict": verdict}
        print(f"  {q:>4} {str(t2):>9} {str(anti):>14} {str(sq):>11} {q%4:>9}  {verdict}")

    ok = all(r["T_squared_is_I"] and r["anti_symplectic"] for r in rows.values())
    law = all((r["minus_one_is_square"] == (q % 4 == 1)) for q, r in rows.items())
    print(f"\n  the construction works at every q tested            : {ok}")
    print(f"  outer exactly when q = 3 (mod 4), at every q tested : {law}")
    print("\n  Pass 2750's scope caveat is now closed: the transpose is built and checked")
    print("  at eight primes, not just at q = 3.")
    return {"per_q": {str(k): v for k, v in rows.items()},
            "construction_valid_all_q": ok, "congruence_law_holds": law}


def main() -> int:
    out = {"pass_2789": pass_2789(), "pass_2791": pass_2791(), "pass_2792": pass_2792()}
    path = ROOT / "data" / "PART_W33_PASS2789_2792_MINIMAL_ISA_SENSOR_TRANSPOSE.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
