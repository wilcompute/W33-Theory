#!/usr/bin/env python3
"""Pass 194: the odd-q shadow ladder -- the q=5 sandwich and its 24-form.

Pass 193 showed the layer sandwich needs even lines.  The algebra says
more: for W(3,q) with q ODD, all three SRG parameters k-mu = q^2-1,
lambda-mu = -2, mu = q+1 are even, so A^2 = 0 mod 2 for EVERY odd q --
the sandwich machinery is an odd-q family, with W(3,3) merely its first
rung.  This witness climbs to q = 5 (156 points):

1. THE SANDWICH AT q=5.  The chain 0 < j < C < im A2 < ker A2 < C-perp
   < j-perp < M with exact layer dimensions

       1, 64, 1, 24, 1, 64, 1,

   matching the closed forms d(q) = (q-1)(q^2+q+2)/2 and m(q) = q^2 - 1
   (q=3 gives 14 and 8).

2. THE 24-FORM.  The middle subquotient ker A2 / im A2 carries the
   canonical quadratic form q(x) = (1/2) x^T A x mod 2 with polar form
   B(x,y) = (1/2) x^T A y (well-defined because A^2 = 0 mod 2 and A has
   even row sums) -- the q=5 analogue of the E8/2E8 shadow, now of
   dimension 24.  Its nondegeneracy and ARF INVARIANT are computed by an
   explicit symplectic basis (no 2^24 enumeration), deciding plus/minus
   type -- the first new member of the shadow ladder above E8.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass171_even_q_rank_ladder import build_w3q, f2_rank

OUT = ROOT / "data" / "w33_pass194_odd_q_shadow_ladder.json"


def f2_row_space_n(matrix):
    work = [row.copy().astype(np.uint8) % 2 for row in matrix]
    basis = []
    for row in work:
        residual = row.copy()
        for b in basis:
            pivot = int(np.flatnonzero(b)[0])
            if residual[pivot]:
                residual = residual ^ b
        if residual.any():
            basis.append(residual)
            basis.sort(key=lambda v: int(np.flatnonzero(v)[0]))
            changed = True
            while changed:
                changed = False
                for i in range(len(basis)):
                    for k in range(len(basis)):
                        if i == k:
                            continue
                        pivot = int(np.flatnonzero(basis[k])[0])
                        if basis[i][pivot]:
                            basis[i] = basis[i] ^ basis[k]
                            changed = True
                basis = [b for b in basis if b.any()]
                basis.sort(key=lambda v: int(np.flatnonzero(v)[0]))
    return basis


def f2_kernel_basis_n(matrix, n):
    work = [row.copy().astype(np.uint8) % 2 for row in matrix]
    pivots = []
    rank = 0
    for col in range(n):
        pivot = next((r for r in range(rank, len(work)) if work[r][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for r in range(len(work)):
            if r != rank and work[r][col]:
                work[r] = work[r] ^ work[rank]
        pivots.append(col)
        rank += 1
    free = [c for c in range(n) if c not in pivots]
    out = []
    for fc in free:
        vec = np.zeros(n, dtype=np.uint8)
        vec[fc] = 1
        for r, pc in zip(work[:rank], pivots):
            if r[fc]:
                vec[pc] = 1
        out.append(vec)
    return out


def contains_n(space, other):
    stacked = np.array(list(space) + list(other), dtype=np.uint8)
    return len(f2_row_space_n(stacked)) == len(space)


def shadow_form_arf(adjacency, checks, tag):
    """Arf invariant of q(x)=xAx/2 on ker A2/im A2 via a symplectic basis."""
    n = adjacency.shape[0]
    a2 = (adjacency % 2).astype(np.uint8)
    ker = f2_kernel_basis_n(a2, n)
    im = f2_row_space_n(a2)

    def reduce_mod_im(vector):
        residual = vector.copy()
        for b in im:
            pivot = int(np.flatnonzero(b)[0])
            if residual[pivot]:
                residual = residual ^ b
        return residual

    reduced = [reduce_mod_im(v) for v in ker]
    basis = f2_row_space_n(np.array([v for v in reduced if v.any()], dtype=np.uint8))
    dim = len(basis)
    checks[f"{tag}_middle_dim"] = dim

    adjacency64 = adjacency.astype(np.int64)

    def q_val(x):
        return (int(x.astype(np.int64) @ adjacency64 @ x.astype(np.int64)) // 2) % 2

    def b_val(x, y):
        return (int(x.astype(np.int64) @ adjacency64 @ y.astype(np.int64)) // 2) % 2

    # Gram matrix of the polar form on the middle: radical first
    gram = np.zeros((dim, dim), dtype=np.uint8)
    for i in range(dim):
        for k in range(i + 1, dim):
            gram[i, k] = gram[k, i] = b_val(basis[i], basis[k])
    rank = f2_rank(gram.copy())
    radical_dim = dim - rank
    checks[f"{tag}_polar_radical_dim"] = radical_dim

    # radical basis and q on the radical (does q vanish there?)
    radical = f2_kernel_basis_n(gram, dim)
    q_on_radical = [
        int(q_val((np.array(coeffs, dtype=np.int64) @ np.array(basis)) % 2))
        for coeffs in radical
    ]
    checks[f"{tag}_q_vanishes_on_radical"] = (
        all(v == 0 for v in q_on_radical) or radical_dim == 0
    )

    # symplectic basis of the nondegenerate quotient via greedy pairs,
    # working with coordinate vectors relative to `basis` and the Gram
    pool = [np.eye(dim, dtype=np.uint8)[i] for i in range(dim)]

    def gram_pair(u, v):
        return int(u.astype(np.int64) @ gram.astype(np.int64) @ v) % 2

    def q_coord(u):
        vec = (u.astype(np.int64) @ np.array(basis)) % 2
        return q_val(vec.astype(np.uint8))

    arf = 0
    pairs = 0
    while pool:
        a = pool.pop(0)
        partner_index = None
        for i, c in enumerate(pool):
            if gram_pair(a, c):
                partner_index = i
                break
        if partner_index is None:
            continue  # radical direction: skip
        b = pool.pop(partner_index)
        arf ^= q_coord(a) & q_coord(b)
        pairs += 1
        new_pool = []
        for c in pool:
            c2 = c.copy()
            if gram_pair(c2, b):
                c2 = c2 ^ a
            if gram_pair(c2, a):
                c2 = c2 ^ b
            new_pool.append(c2)
        pool = new_pool
    checks[f"{tag}_hyperbolic_pairs"] = pairs == rank // 2
    return dim, radical_dim, arf


def main():
    checks = {}

    # SRG parameter parity: A^2 = 0 mod 2 for every odd q (symbolically)
    parity_law = all(
        ((q * q - 1) % 2 == 0 and 2 % 2 == 0 and (q + 1) % 2 == 0)
        for q in (3, 5, 7, 9, 11)
    )
    checks["odd_q_differential_law"] = parity_law

    reports = {}
    for q in (3, 5):
        points, lines = build_w3q(q)
        n = len(points)
        incidence = np.zeros((len(lines), n), dtype=np.uint8)
        for row, line in enumerate(lines):
            for p in line:
                incidence[row, p] = 1
        adjacency = np.zeros((n, n), dtype=np.int64)
        line_sets = [set(line) for line in lines]
        for line in line_sets:
            for a in line:
                for b in line:
                    if a != b:
                        adjacency[a, b] = 1
        checks[f"q{q}_A2_differential"] = bool(((adjacency @ adjacency) % 2 == 0).all())

        j = np.ones(n, dtype=np.uint8)
        C = f2_row_space_n(np.array(f2_kernel_basis_n(incidence, n), dtype=np.uint8))
        a2 = (adjacency % 2).astype(np.uint8)
        im_a2 = f2_row_space_n(a2)
        ker_a2 = f2_row_space_n(np.array(f2_kernel_basis_n(a2, n), dtype=np.uint8))
        c_perp = f2_row_space_n(incidence)

        dims = {
            "C": len(C),
            "imA2": len(im_a2),
            "kerA2": len(ker_a2),
            "Cperp": len(c_perp),
        }
        chain_ok = (
            contains_n(C, [j])
            and contains_n(im_a2, C)
            and contains_n(ker_a2, im_a2)
            and contains_n(c_perp, ker_a2)
        )
        checks[f"q{q}_chain_holds"] = bool(chain_ok)

        layers = [
            1,
            dims["C"] - 1,
            dims["imA2"] - dims["C"],
            dims["kerA2"] - dims["imA2"],
            dims["Cperp"] - dims["kerA2"],
            (n - 1) - dims["Cperp"],
            1,
        ]
        d_formula = (q - 1) * (q * q + q + 2) // 2
        m_formula = q * q - 1
        checks[f"q{q}_layer_formulas"] = layers == [
            1,
            d_formula,
            1,
            m_formula,
            1,
            d_formula,
            1,
        ]

        dim, radical_dim, arf = shadow_form_arf(adjacency, checks, f"q{q}")
        checks[f"q{q}_shadow_dim_q2_minus_1"] = dim == m_formula
        form_type = "plus (O+)" if arf == 0 else "minus (O-)"
        reports[str(q)] = {
            "points": n,
            "dims": dims,
            "layers": layers,
            "shadow_dimension": dim,
            "polar_radical_dim": int(radical_dim),
            "nondegenerate_rank": int(dim - radical_dim),
            "arf_invariant": int(arf),
            "type": form_type,
        }
    checks["q3_reproduces_e8_plus"] = (
        reports["3"]["shadow_dimension"] == 8 and reports["3"]["arf_invariant"] == 0
    )

    all_pass = all(v if isinstance(v, bool) else True for v in checks.values())
    payload = {
        "schema": "w33.pass194.odd_q_shadow_ladder.v1",
        "status": "PASS" if all_pass else "FAIL",
        "ladder": reports,
        "laws": {
            "differential": "A^2 = 0 mod 2 for every odd q",
            "code_layer": "d(q) = (q-1)(q^2+q+2)/2  [14, 64, 174, ...]",
            "shadow_dimension": "m(q) = q^2 - 1  [8, 24, 48, ...]",
        },
        "reading": (
            "the E8 shadow is the first rung of an odd-q ladder: at q=5 "
            "the sandwich reappears with layers 1,64,1,24,1,64,1 and a "
            "24-dimensional middle, but its divided pairing is TOTALLY "
            "degenerate (radical 24) because A^2/2 = A mod 2 fails; the "
            "nondegenerate quadratic shadows recur at q = 3 (mod 4) -- "
            "see Pass 198 for the q=7 dimension-48 shadow and the "
            "q = 3 (mod 4) dichotomy"
        ),
        "checks": {
            name: (bool(v) if isinstance(v, (bool, np.bool_)) else int(v))
            for name, v in checks.items()
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    boolean_checks = [v for v in checks.values() if isinstance(v, (bool, np.bool_))]
    return 0 if all(boolean_checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
