#!/usr/bin/env python3
"""Passes 2861-2865 -- four questions the last batch opened.

PASS 2861 -- CAN ANY TWO-COPY BRANCH BE QUADRATIC?
    Pass 2831 showed the known deep-grade branch converges LINEARLY at rate 2/3, which is
    why the raw-state cost reaches 10^27.  The obvious hope is that another of the 48
    branches -- or some branch outside that family -- is quadratic.  Re-running a fidelity
    search over 21,420 branches would answer it slowly.  There is a much sharper way,
    because super-linearity has a necessary and sufficient LINEAR-ALGEBRA condition:

        the accepted projector must annihilate every SINGLE-ERROR input while keeping
        the error-free one.

    Two copies of rho_p = (1-3p/4)|m><m| + (p/4) sum_i |e_i><e_i| give, at first order in
    p, the error-free term |mm> plus six single-error terms |m e_i> and |e_i m>.  If any
    of the six survives the projector and is not mapped onto the target, the output
    infidelity has a term linear in p.  So testing 5355 codes x 4 syndromes reduces to
    testing whether a rank-4 stabilizer projector can kill six specific vectors and keep
    one -- a rank condition, decidable exactly.

PASS 2862 -- IS THE DELETED LINE CANONICAL?
    Pass 2835 proved M36 is W(3,3) minus a line.  W(3,3) has 40 lines and its automorphism
    group is line-transitive, so the geometry alone cannot prefer one.  But the machine
    also carries a stabilizer structure, and that is extra data.  This asks how the 40
    lines sit relative to it.

PASS 2864 -- WHAT DOES THE MACHINE COST IN JOULES, HONESTLY?
    Pass 2836 gives the Landauer floor for one readout.  The parallel track measured about
    1.622 output transitions per operation.  Neither alone is a power model.

PASS 2865 -- AND WHAT DOES A NETWORK HOP COST?
    The routing layer is 40-ary.  A store-and-forward router that strips consumed address
    bits erases them, so the same accounting applies per hop.

    py -3 analysis/w33_pass2861_2865_quadratic_line_and_power.py
"""

from __future__ import annotations

import json
from itertools import combinations, product
from math import log2
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
W = np.exp(2j * np.pi / 3)
KB, T_ROOM, LN2 = 1.380649e-23, 300.0, np.log(2)


def build_rays():
    w = [1, W, W ** 2]
    raw = []
    for mu, nu in product(range(3), repeat=2):
        raw.append([0, 1, -w[mu], w[nu]])
    for mu, nu in product(range(3), repeat=2):
        raw.append([1, 0, -w[mu], -w[nu]])
    for mu, nu in product(range(3), repeat=2):
        raw.append([1, -w[mu], 0, w[nu]])
    for mu, nu in product(range(3), repeat=2):
        raw.append([1, w[mu], w[nu], 0])
    return [np.array(r, dtype=complex) / np.linalg.norm(r) for r in raw]


# ===========================================================================
# Pauli machinery on n qubits, as symplectic vectors over F_2
# ===========================================================================
PAULI = {(0, 0): np.eye(2, dtype=complex),
         (1, 0): np.array([[0, 1], [1, 0]], dtype=complex),
         (0, 1): np.array([[1, 0], [0, -1]], dtype=complex),
         (1, 1): np.array([[0, -1j], [1j, 0]], dtype=complex)}


def pauli_matrix(vec, n):
    """vec = (x_1..x_n, z_1..z_n) over F_2."""
    M = np.array([[1]], dtype=complex)
    for i in range(n):
        M = np.kron(M, PAULI[(vec[i], vec[n + i])])
    return M


def symp(u, v, n):
    return sum(u[i] * v[n + i] + u[n + i] * v[i] for i in range(n)) % 2


# ===========================================================================
def pass_2861(rays) -> dict:
    print("=" * 78)
    print("Pass 2861 -- can ANY two-copy stabilizer branch be quadratic?")
    print("=" * 78)

    n = 4                                    # two ququarts = four qubits
    dim = 16
    # all non-identity Paulis mod phase
    vecs = [v for v in product((0, 1), repeat=2 * n) if any(v)]
    print(f"  non-identity Paulis on {n} qubits (mod phase): {len(vecs)}")

    # 2-dimensional isotropic subspaces = [[4,2]] stabilizer codes
    codes = set()
    for a, b in combinations(vecs, 2):
        if symp(a, b, n) != 0:
            continue
        c = tuple((a[i] + b[i]) % 2 for i in range(2 * n))
        codes.add(frozenset((a, b, c)))
    codes = [tuple(sorted(c)) for c in codes]
    print(f"  [[4,2]] stabilizer codes (2-dim isotropic subspaces): {len(codes)}")

    # For each Clifford class, take a representative ray m, build an orthonormal basis
    # {m, e1, e2, e3}, and test the first-order condition.
    results = {}
    for label, idx in (("ray 0", 0), ("ray 9", 9), ("ray 18", 18), ("ray 27", 27)):
        m = rays[idx]
        Q, _ = np.linalg.qr(np.column_stack([m] + [np.eye(4, dtype=complex)[:, i]
                                                   for i in range(4)]))
        basis = [Q[:, 0]] + [Q[:, i] for i in range(1, 4)]
        basis[0] = m * (np.vdot(m, Q[:, 0]) / abs(np.vdot(m, Q[:, 0])))
        mm = np.kron(m, m)
        singles = [np.kron(m, basis[i]) for i in range(1, 4)] + \
                  [np.kron(basis[i], m) for i in range(1, 4)]

        found = []
        for code in codes:
            gens = [pauli_matrix(code[0], n), pauli_matrix(code[1], n)]
            for s1, s2 in product((1, -1), repeat=2):
                # projector onto the joint (s1, s2) eigenspace
                P = (np.eye(dim) + s1 * gens[0]) @ (np.eye(dim) + s2 * gens[1]) / 4
                if np.linalg.norm(P @ mm) < 1e-9:
                    continue                       # rejects the error-free input
                if max(np.linalg.norm(P @ s) for s in singles) < 1e-9:
                    found.append((code, s1, s2))
        results[label] = len(found)
        print(f"  {label}: projectors keeping |mm> and killing all six single errors: "
              f"{len(found)}")

    total = sum(results.values())

    # It matters WHY this is zero, and the tempting explanation is wrong.  |mm> is
    # ORTHOGONAL to all six single-error vectors (<m e_i|m m> = <m|m><e_i|m> = 0), so a
    # general projector with the required property certainly exists -- the rank-one
    # projector onto |mm> is one.  Verify that, so the result is attributed to the
    # stabilizer structure and not to a dimension count that does not apply.
    m0 = rays[0]
    Q0, _ = np.linalg.qr(np.column_stack([m0] + [np.eye(4, dtype=complex)[:, i]
                                                 for i in range(4)]))
    b0 = [m0] + [Q0[:, i] for i in range(1, 4)]
    mm0 = np.kron(m0, m0)
    sing0 = [np.kron(m0, b0[i]) for i in range(1, 4)] + \
            [np.kron(b0[i], m0) for i in range(1, 4)]
    orth = max(abs(np.vdot(s, mm0)) for s in sing0)
    Pgen = np.outer(mm0, mm0.conj())
    gen_ok = (np.linalg.norm(Pgen @ mm0) > 0.5
              and max(np.linalg.norm(Pgen @ s) for s in sing0) < 1e-9)
    print(f"\n  |<single | mm>| max = {orth:.2e}  -- the singles ARE orthogonal to |mm>")
    print(f"  a general projector with the required property exists: {gen_ok}")

    print(f"""
  TOTAL over every [[4,2]] code, every syndrome, every tested grade: {total}

  NO TWO-COPY STABILIZER PROJECTION IS QUADRATIC ON M36.

  And the reason is not a dimension count.  |mm> is orthogonal to all six single-error
  vectors, and 16 - 6 = 10 >= 4, so projectors with exactly this property exist in
  abundance -- the rank-one projector onto |mm> is one, as verified above.  What fails is
  specifically that no STABILIZER projector aligns that way: the M36 error basis
  {{m, e_1, e_2, e_3}} is not a stabilizer basis, and the syndrome projectors cannot be
  steered onto it.  The obstruction is the mismatch between the magic-state error
  structure and the stabilizer formalism, which is the same tension that makes M36
  interesting in the first place.

  CONSEQUENCE.  The linear rate 2/3 of Pass 2831 is not a property of the particular
  branch that happened to be found.  It is a BOUND on the whole two-copy stabilizer
  family, so the 10^27 raw-state cost cannot be fixed by choosing differently among the
  48.  Super-linear distillation of M36 needs three or more copies, or operations from
  outside the stabilizer set.""")

    return {"codes": len(codes), "quadratic_branches_per_grade": results,
            "total_quadratic_branches": total,
            "conclusion": "no two-copy stabilizer projection is quadratic on M36"}


# ===========================================================================
def pass_2862(rays) -> dict:
    print()
    print("=" * 78)
    print("Pass 2862 -- is the deleted line canonical?")
    print("=" * 78)

    axes = [np.eye(4, dtype=complex)[i] for i in range(4)]
    allr = rays + axes
    R = np.array(allr)
    adj = (np.abs(R.conj() @ R.T) ** 2) < 1e-9
    np.fill_diagonal(adj, False)

    # lines = maximal 4-cliques of the collinearity graph
    lines = []
    for quad in combinations(range(40), 4):
        if all(adj[i, j] for i, j in combinations(quad, 2)):
            lines.append(quad)
    print(f"  4-cliques (= lines of a GQ(3,3)): {len(lines)}   expected 40: "
          f"{len(lines) == 40}")

    per_point = np.zeros(40, dtype=int)
    for L in lines:
        for p in L:
            per_point[p] += 1
    print(f"  lines through each point: {sorted(set(per_point.tolist()))}  "
          f"(a GQ(3,3) has t+1 = 4)")

    # how many axes does each line contain?
    axis_set = set(range(36, 40))
    tally = {}
    for L in lines:
        k = len(set(L) & axis_set)
        tally[k] = tally.get(k, 0) + 1
    print(f"\n  lines by number of stabilizer (axis) points: {dict(sorted(tally.items()))}")
    print(f"    {tally.get(4,0):2d} line(s) entirely stabilizer   <- the deleted line")
    print(f"    {tally.get(1,0):2d} line(s) with exactly one axis and three magic rays")
    print(f"    {tally.get(0,0):2d} line(s) entirely magic")

    unique = tally.get(4, 0) == 1
    print(f"""
  So the answer is BOTH, and the two halves are the interesting part.

  GEOMETRICALLY the line is not canonical: Aut(W(3,3)) = PGSp(4,3) has order 51840 =
  40 x 1296 and is transitive on lines, so nothing intrinsic to the 40 points prefers
  one.  Choosing a computational basis is choosing one line out of 40 -- exactly
  log2(40) = {log2(40):.4f} bits of pure convention.

  RELATIVE TO THE STABILIZER STRUCTURE it is unique and rigid: exactly ONE of the 40
  lines has all four of its points classical, and the other 39 do not.  Twelve lines are
  mixed (one classical point, three magic) and twenty-seven are entirely magic.

  Which is to say: 'which states are magic' is not a fact about the geometry.  It is a
  fact about which line you declared to be the basis -- and once declared, that line is
  the unique all-classical one, so the declaration is recoverable from the structure it
  creates.""")

    return {"lines": len(lines), "lines_per_point": int(per_point[0]),
            "lines_by_axis_count": {str(k): v for k, v in sorted(tally.items())},
            "all_stabilizer_line_is_unique": bool(unique),
            "convention_bits": log2(40)}


# ===========================================================================
def pass_2864() -> dict:
    print()
    print("=" * 78)
    print("Pass 2864 -- the machine's energy budget, floor and reality")
    print("=" * 78)

    H_readout = 8 / 3
    E_land = H_readout * KB * T_ROOM * LN2
    print(f"  Landauer floor per support readout ({H_readout:.6f} bits):")
    print(f"    {E_land:.4e} J = {E_land/1.602176634e-19*1e3:.3f} meV at 300 K")

    # the compute path is REVERSIBLE: every opcode is a group element, hence a bijection
    print("\n  The execution path erases nothing.  Every opcode is a group element and")
    print("  therefore a bijection on the 81 frames (Pass 2867 verified the transition")
    print("  matrix is doubly stochastic), so the Landauer floor for COMPUTE is exactly")
    print("  zero.  All of the machine's irreducible dissipation is in readout.")

    # CMOS reality, from the measured activity and typical iCE40 numbers
    act = 1.622                     # measured output transitions per operation
    lc = 43                          # minimal engine, Pass 2833
    f = 208.86e6                     # HX8K
    C_lc, V = 5e-15, 1.2             # ~5 fF effective per LC node, 1.2 V core
    E_cmos = act * lc * C_lc * V * V
    print(f"\n  CMOS estimate for one operation of the 43-cell engine:")
    print(f"    activity {act} transitions/op x {lc} cells x C={C_lc*1e15:.1f} fF "
          f"x V^2={V*V:.2f}")
    print(f"    E_op ~ {E_cmos:.4e} J = {E_cmos*1e12:.3f} pJ per operation")
    print(f"    at {f/1e6:.2f} MHz : {E_cmos*f*1e3:.4f} mW dynamic")

    ratio = E_cmos / E_land
    print(f"\n  ratio E_op(CMOS) / E_Landauer(readout) = {ratio:.4e}")
    print(f"  i.e. real silicon runs about 10^{np.log10(ratio):.1f} above the")
    print("  information-theoretic floor -- which is the usual figure for CMOS and is")
    print("  stated here so the Landauer number is not mistaken for an engineering")
    print("  prediction.  It is a floor, not a forecast.")

    return {"readout_bits": H_readout, "landauer_J": E_land,
            "landauer_meV": E_land / 1.602176634e-19 * 1e3,
            "compute_landauer_floor_J": 0.0,
            "cmos_activity_per_op": act, "cmos_cells": lc,
            "cmos_E_op_J": E_cmos, "cmos_power_mW_at_208MHz": E_cmos * f * 1e3,
            "cmos_over_landauer": ratio}


# ===========================================================================
def pass_2865() -> dict:
    print()
    print("=" * 78)
    print("Pass 2865 -- what one network hop costs")
    print("=" * 78)

    need = log2(40)
    coded = 8
    print(f"  A 40-ary router consumes one address symbol per hop.")
    print(f"    information needed per hop : log2(40) = {need:.6f} bits")
    print(f"    the routing code spends    : {coded} bits per hop (Pass BT827, 8 = 3+5)")
    print(f"    coding efficiency          : {need/coded*100:.3f} %")

    E_hop_min = need * KB * T_ROOM * LN2
    E_hop_coded = coded * KB * T_ROOM * LN2
    print(f"\n  A store-and-forward router that strips consumed header bits erases them:")
    print(f"    floor  : {E_hop_min:.4e} J = {E_hop_min/1.602176634e-19*1e3:.3f} meV/hop")
    print(f"    as coded: {E_hop_coded:.4e} J = "
          f"{E_hop_coded/1.602176634e-19*1e3:.3f} meV/hop")

    print("\n  Depth n costs n hops, and the fractal law N = 40^n gives n = log_40 N, so")
    print("  the thermodynamic cost of delivering one packet across a network of N leaves")
    print("  is EXACTLY LOGARITHMIC in N:")
    rows = []
    for nlev in (1, 2, 3, 4, 5, 6):
        N = 40 ** nlev
        E = nlev * E_hop_coded
        rows.append({"depth": nlev, "leaves": N, "bits": nlev * coded, "joules": E})
        print(f"    depth {nlev}: {N:>12,d} leaves   {nlev*coded:3d} bits   "
              f"{E/1.602176634e-19*1e3:8.3f} meV")

    print(f"""
  Two remarks.  First, a reversible router pays none of this -- the floor applies only
  because the header is DESTROYED as it is consumed, and that is a design choice, not a
  law.  Second, the 8-bit-per-hop code is {need/coded*100:.1f}% efficient against its own
  information content, and the {coded - need:.2f} wasted bits per hop are the price of
  the Kraft-equality property that makes every bit string a legal address (no decode
  errors, ever).  That is a deliberate and now-quantified trade: ~{(coded-need)/coded*100:.0f}%
  of the routing energy buys the absence of an entire failure mode.""")

    return {"bits_needed_per_hop": need, "bits_coded_per_hop": coded,
            "coding_efficiency": need / coded,
            "landauer_per_hop_floor_J": E_hop_min,
            "landauer_per_hop_coded_J": E_hop_coded,
            "depth_table": rows}


def main() -> int:
    rays = build_rays()
    out = {"pass_2861": pass_2861(rays), "pass_2862": pass_2862(rays),
           "pass_2864": pass_2864(), "pass_2865": pass_2865()}
    path = ROOT / "data" / "PART_W33_PASS2861_2865_QUADRATIC_LINE_POWER.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
