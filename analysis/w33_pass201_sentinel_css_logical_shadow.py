#!/usr/bin/env python3
r"""Pass 201: the sentinel CSS code and one logical-label shadow.

Idea #3 of round 7: wire the protected register into an explicit QEC code.
The sentinel trade code C = ker_F2(N) = [40,15,8] is doubly-even and
self-orthogonal (C subset C^perp), so it defines a CSS code

    [[40, dim C^perp - dim C, d]] = [[40, 25 - 15, d]] = [[40, 10, d]],

and one 10-dimensional logical label space is the SO(10)-shadow module
H10 = C^perp / C (Pass 164).  This witness makes that label-space
identification exact without conflating it with the full Pauli space:

1. THE CSS CODE.  C doubly-even + self-orthogonal is verified; the CSS
   code [[40,10,d]] is built with X- and Z-checks both equal to C, and
   its distance d = min weight of C^perp \ C is computed exactly.

2. ONE LABEL COPY = THE SO(10) SHADOW.  C^perp/C labels either the X or
   the dual Z logicals.  Its plus-type polar form is O+(10,2) geometry,
   but the full logical Pauli label space is H_X plus H_Z, dimension 20,
   with its hyperbolic symplectic form.

3. CODE AUTOMORPHISMS.  PSp(4,3) permutes the 40 physical coordinates
   fixing C and acts faithfully on H10 through O+(10,2), with image order
   25920.  This alone does not identify a logical gate inventory.  The
   corrected Clifford lift is diag(M,M^(-T)) in Sp(20,2) (Pass 211).
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
    build_group,
    build_w33,
    saturated_kernel,
    w33_lines,
)
from analysis.w33_pass161_gq42_ihara_inheritance import small_generating_set

OUT = ROOT / "data" / "w33_pass201_sentinel_css_logical_shadow.json"


def rref_f2(rows):
    work = [r.copy().astype(np.uint8) % 2 for r in rows]
    basis = []
    for row in work:
        r = row.copy()
        for b in basis:
            piv = int(np.flatnonzero(b)[0])
            if r[piv]:
                r = r ^ b
        if r.any():
            basis.append(r)
            basis.sort(key=lambda v: int(np.flatnonzero(v)[0]))
            changed = True
            while changed:
                changed = False
                for i in range(len(basis)):
                    for k in range(len(basis)):
                        if i != k:
                            piv = int(np.flatnonzero(basis[k])[0])
                            if basis[i][piv]:
                                basis[i] = basis[i] ^ basis[k]
                                changed = True
                basis = [b for b in basis if b.any()]
                basis.sort(key=lambda v: int(np.flatnonzero(v)[0]))
    return basis


def in_span(basis, vec):
    r = vec.copy().astype(np.uint8) % 2
    for b in basis:
        piv = int(np.flatnonzero(b)[0])
        if r[piv]:
            r = r ^ b
    return not r.any()


def main():
    points, adjacency, symplectic = build_w33()
    lines = w33_lines(adjacency)
    checks = {}

    incidence = np.zeros((40, 40), dtype=np.uint8)
    for row, line in enumerate(lines):
        for p in line:
            incidence[row, p] = 1

    dark = saturated_kernel(incidence.astype(np.int64))
    C = rref_f2([(dark[:, j] % 2).astype(np.uint8) for j in range(15)])
    Cperp = rref_f2([incidence[r] for r in range(40)])
    checks["sentinel_dim_15"] = len(C) == 15
    checks["context_dim_25"] = len(Cperp) == 25

    Cmat = np.array(C, dtype=np.uint8)
    # doubly even + self-orthogonal
    checks["doubly_even"] = all(int(w) % 4 == 0 for w in Cmat.sum(axis=1))
    checks["self_orthogonal"] = all(
        int((Cmat[i] & Cmat[k]).sum()) % 2 == 0 for i in range(15) for k in range(15)
    )
    # C subset C^perp
    checks["C_in_Cperp"] = all(in_span(Cperp, Cmat[i]) for i in range(15))

    # ---- CSS distance: min weight of C^perp \ C ----
    # enumerate cosets: coset reps = C^perp / C, 2^10 cosets; the code
    # distance is min over nonzero cosets of the min weight in that coset.
    # We compute min weight of C^perp \ C directly by scanning C^perp
    # words of increasing weight is 2^25 -- too big. Instead: the CSS
    # distance = min weight of a vector in C^perp not in C = the minimum
    # coset-leader weight. Use the 10 coset generators + C and search low
    # weights by meet-in-the-middle over the 10 logical coordinates plus
    # the 15 stabilizer coordinates capped at weight <= 6.
    # Simpler exact route: the logical space is small (2^10); for each of
    # the 1023 nonzero logical cosets, min weight over C (2^15) is large,
    # but min weight in coset = min weight of (rep XOR c). We bound d by
    # scanning weight-w vectors of F2^40 for the smallest w with a vector
    # in C^perp \ C. Because A_4(C^perp)=40 (Pass 167) and those 40 words
    # are the lines, and lines are NOT in C (they are context words), the
    # CSS distance is 4.
    # Verify: the 40 line indicator vectors are in C^perp, weight 4, and
    # not in C.
    line_vecs = incidence.copy()
    lines_in_cperp = all(in_span(Cperp, line_vecs[r]) for r in range(40))
    lines_not_in_C = all(not in_span(C, line_vecs[r]) for r in range(40))
    # no weight <4 word in C^perp \ C: context code min weight is 4
    # (Pass 167), and weight-1..3 context words don't exist; any weight<4
    # vector in C^perp is 0. Confirm no nonzero context word of weight<4.
    small = 0
    for w in (1, 2, 3):
        for combo in combinations(range(40), w):
            v = np.zeros(40, dtype=np.uint8)
            for c in combo:
                v[c] = 1
            if in_span(Cperp, v):
                small += 1
    checks["no_context_word_below_weight_4"] = small == 0
    checks["css_distance_4"] = lines_in_cperp and lines_not_in_C and small == 0
    css_distance = 4

    # ---- one logical-label copy = SO(10) shadow ----
    # coset coordinates: reduce C^perp mod C, keep 10 free pivots
    Cperp_mat = np.array(Cperp, dtype=np.uint8)

    def reduce_mod_C(vec):
        r = vec.copy()
        for b in C:
            piv = int(np.flatnonzero(b)[0])
            if r[piv]:
                r = r ^ b
        return r

    quotient_basis = rref_f2([reduce_mod_C(Cperp_mat[i]) for i in range(25)])
    checks["logical_dim_10"] = len(quotient_basis) == 10

    # polar form on one label copy = |x cap y| mod 2
    H = np.array(quotient_basis, dtype=np.uint8)
    polar = np.zeros((10, 10), dtype=np.uint8)
    for i in range(10):
        for k in range(10):
            polar[i, k] = int((H[i] & H[k]).sum()) % 2
    # nondegenerate polar form on H10; this is not the full Pauli form
    rank_polar = len(rref_f2([polar[i] for i in range(10)]))
    checks["logical_form_nondegenerate"] = rank_polar == 10

    # plus type: count isotropic under q(x)=wt/2 mod 2
    coeffs = np.array(
        [[(m >> b) & 1 for b in range(10)] for m in range(1024)],
        dtype=np.uint8,
    )
    words = (coeffs @ H) % 2
    qvals = (words.sum(axis=1) // 2) % 2
    isotropic = int((qvals == 0).sum())
    checks["logical_plus_type_528"] = isotropic == 528

    # ---- coordinate automorphisms: PSp(4,3) -> O+(10,2) ----
    generators, group = build_group(points, symplectic)
    checks["group_25920"] = len(group) == 25920
    two_gens = small_generating_set(group)

    pivots = [int(np.flatnonzero(b)[0]) for b in quotient_basis]

    def logical_coords(vec):
        r = reduce_mod_C(vec)
        out = np.zeros(10, dtype=np.uint8)
        for k in range(10):
            if r[pivots[k]]:
                out[k] = 1
                r = r ^ quotient_basis[k]
        return out

    def logical_action(perm):
        cols = []
        for b in quotient_basis:
            image = np.zeros(40, dtype=np.uint8)
            for src in range(40):
                image[perm[src]] = b[src]
            cols.append(logical_coords(image))
        return np.array(cols, dtype=np.uint8).T % 2

    Lmats = [logical_action(g) for g in two_gens]

    # closure order of the logical image
    def mat_key(m):
        return tuple(int(v) for v in m.reshape(-1))

    seen = {mat_key(np.eye(10, dtype=np.uint8))}
    frontier = [np.eye(10, dtype=np.uint8)]
    while frontier:
        nf = []
        for e in frontier:
            for g in Lmats:
                comp = (e @ g) % 2
                key = mat_key(comp)
                if key not in seen:
                    seen.add(key)
                    nf.append(comp)
        frontier = nf
    checks["transversal_image_25920"] = len(seen) == 25920

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass201.sentinel_css_logical_shadow.v2",
        "status": "PASS" if all_pass else "FAIL",
        "css_code": {
            "parameters": f"[[40, 10, {css_distance}]]",
            "stabilizer_code": "C = sentinel [40,15,8], doubly even, self-orthogonal",
            "logical_qubits": 10,
            "full_logical_pauli_dimension": 20,
            "distance": css_distance,
            "distance_witness": "the 40 lines are weight-4 logical operators",
        },
        "one_label_copy_is_so10_shadow": {
            "label_space": "C^perp / C = H10 (Pass 164)",
            "full_pauli_space": "H_X plus H_Z, dimension 20",
            "label_form": "polar form |x cap y| mod 2, nondegenerate",
            "type": "plus (O+(10,2)), 528 isotropic labels",
            "reading": (
                "H10 is one common X/Z label copy, not the whole logical "
                "Pauli algebra; the latter is the 20-dimensional hyperbolic "
                "space H_X plus H_Z"
            ),
        },
        "coordinate_automorphisms": {
            "group": "PSp(4,3) -> O+(10,2)",
            "image_order": 25920,
            "corrected_clifford_lift": "diag(M,M^(-T)) in Sp(20,2) (Pass 211)",
            "reading": (
                "the substrate permutations are weight-preserving code "
                "automorphisms acting faithfully on one label copy; this "
                "certificate does not claim a built-in fault-tolerant gate set"
            ),
        },
        "checks": {name: bool(v) for name, v in checks.items() if isinstance(v, bool)},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
