#!/usr/bin/env python3
"""Pass 4475 -- exact module filtration of the 29-dimensional apartment radical.

Pass 4463 gives the apartment code

    C_ap = im(H^T) ~= F_2^40 / <j>,        dim 39,

because ker(H^T)=<j>.  Pass 4464 gives

    rad(C_ap) ~= ker(A*) / <j>,            dim 29,

where A*=N^T N is the line-collinearity adjacency modulo two.  Pass 4469
identifies the 10-dimensional quotient with H10.

This pass resolves the remaining 29 dimensions using the older line-side binary
module of Pass 187.  In line-coordinate space M_L=F_2^40 define

    R = ker N                 (the route code),        dim 15,
    I = im A*,                                          dim 10,
    K = ker A*,                                         dim 30,
    U = R cap I,                                         dim 9,
    S = R + I,                                           dim 16,
    J = <j>,                                              dim 1.

Because A*^2=0 over F2, I <= K; because N j=0 and A*j=0, J lies in U.  Exact
linear algebra gives

    J < U < S < K < M_L

with dimensions

    1 < 9 < 16 < 30 < 40.

Modulo J, this is an invariant filtration of the apartment radical K/J:

    0 < U/J < S/J < K/J,

whose layer dimensions are

    8, 7, 14.

The middle 7-space splits canonically as

    S/U = (R/U) direct-sum (I/U)

with dimensions 6 + 1.  Using two generators of PSp(4,3) on the 40 lines and
exhaustive cyclic-span tests, the 8-, 6-, and 14-dimensional factors are
irreducible over F2; I/U is the trivial one-dimensional factor.  Thus the
radical has the certified invariant-layer profile

    8 | (6 + 1) | 14

(no claim of a uniserial extension is made).

Combining with Pass 4469 yields the exact apartment-code extension

    0 -> K/J (dim 29) -> C_ap (dim 39) -> H10 (dim 10) -> 0.

This explains why 1620 apartment parities contain both a large degenerate
line-module sector and exactly one protected 10-dimensional quotient.

Boundary: the 8,6,14 labels are modular representation dimensions, not particle
multiplicities.  The theorem is a module filtration; it does not imply that a
hardware measurement can discard the radical without an explicit measurement
and decoding protocol.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from w33_pass158_chiral_trade_lattice_two_480s import build_group, build_w33, w33_lines
from w33_pass161_gq42_ihara_inheritance import small_generating_set
from w33_pass187_f2_layer_sandwich import (
    exhaustive_cyclic_irreducible,
    subquotient_action_matrices,
)
from w33_pass4469_apartment_css_h10_intertwiner import nullspace_mod2, rref_rows

ROOT = Path(__file__).resolve().parents[1]


def intersection_basis(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    A = rref_rows(A)
    B = rref_rows(B)
    block = np.hstack((A.T, B.T))
    relations = nullspace_mod2(block)
    if len(relations) == 0:
        return np.zeros((0, A.shape[1]), dtype=np.uint8)
    out = []
    ra = len(A)
    for z in relations:
        u = z[:ra]
        v = (u @ A) % 2
        if v.any():
            out.append(v)
    if not out:
        return np.zeros((0, A.shape[1]), dtype=np.uint8)
    return rref_rows(np.asarray(out, dtype=np.uint8))


def in_span(rows: np.ndarray, v: np.ndarray) -> bool:
    rows = rref_rows(rows)
    return len(rref_rows(np.vstack((rows, v)))) == len(rows)


def contained(big: np.ndarray, small: np.ndarray) -> bool:
    return all(in_span(big, v) for v in rref_rows(small))


def main() -> int:
    points, adjacency, symplectic = build_w33()
    lines = w33_lines(adjacency)
    N = np.zeros((40, 40), dtype=np.uint8)  # points x lines
    for li, line in enumerate(lines):
        for p in line:
            N[p, li] = 1
    Astar = (N.T @ N) % 2
    j = np.ones((1, 40), dtype=np.uint8)

    checks: list[tuple[str, bool]] = []

    def check(name: str, cond) -> None:
        ok = bool(cond)
        checks.append((name, ok))
        if not ok:
            raise AssertionError(name)

    R = rref_rows(nullspace_mod2(N))
    I = rref_rows(Astar)
    K = rref_rows(nullspace_mod2(Astar))
    U = intersection_basis(R, I)
    S = rref_rows(np.vstack((R, I)))

    check("line module dimension 40", N.shape == (40, 40))
    check("route R dimension 15", len(R) == 15)
    check("image I dimension 10", len(I) == 10)
    check("kernel K dimension 30", len(K) == 30)
    check("intersection U dimension 9", len(U) == 9)
    check("sum S dimension 16", len(S) == 16)
    check("J lies in U", contained(U, j))
    check("U lies in R", contained(R, U))
    check("U lies in I", contained(I, U))
    check("R lies in K", contained(K, R))
    check("I lies in K", contained(K, I))
    check("S lies in K", contained(K, S))
    check("Astar squared is zero", not np.any((Astar @ Astar) % 2))

    check("radical K/J dimension 29", len(K) - 1 == 29)
    check("first radical layer U/J dimension 8", len(U) - 1 == 8)
    check("middle radical layer S/U dimension 7", len(S) - len(U) == 7)
    check("top radical layer K/S dimension 14", len(K) - len(S) == 14)
    check("R/U dimension 6", len(R) - len(U) == 6)
    check("I/U dimension 1", len(I) - len(U) == 1)
    check("middle layer splits 6+1", (len(R) - len(U)) + (len(I) - len(U)) == len(S) - len(U))

    # Two point generators, transported canonically to permutations of the 40 lines.
    _, group = build_group(points, symplectic)
    point_gens = small_generating_set(group)
    line_index = {frozenset(line): i for i, line in enumerate(lines)}

    def line_perm(pperm):
        return tuple(
            line_index[frozenset(pperm[p] for p in line)]
            for line in lines
        )

    line_gens = [line_perm(g) for g in point_gens]
    check("two point generators obtained", len(point_gens) == 2)
    check("line generators are permutations", all(sorted(g) == list(range(40)) for g in line_gens))

    # Exact modular irreducibility on the three nontrivial radical factors.
    actions8, dim8 = subquotient_action_matrices(U, j, line_gens)
    actions6, dim6 = subquotient_action_matrices(R, U, line_gens)
    actions14, dim14 = subquotient_action_matrices(K, S, line_gens)
    actions1, dim1 = subquotient_action_matrices(I, U, line_gens)

    irr8, orbits8 = exhaustive_cyclic_irreducible(actions8, dim8)
    irr6, orbits6 = exhaustive_cyclic_irreducible(actions6, dim6)
    irr14, orbits14 = exhaustive_cyclic_irreducible(actions14, dim14)
    check("U/J is irreducible 8", dim8 == 8 and irr8)
    check("R/U is irreducible 6", dim6 == 6 and irr6)
    check("K/S is irreducible 14", dim14 == 14 and irr14)
    check("I/U is one-dimensional", dim1 == 1)
    check("I/U action is trivial over F2", all(np.array_equal(a, np.ones((1, 1), dtype=np.uint8)) for a in actions1))

    result = {
        "pass": 4475,
        "theorem": "W33 apartment-code radical module filtration theorem",
        "spaces": {
            "J=<1>": 1,
            "R=ker(N)": len(R),
            "I=im(Astar)": len(I),
            "U=R_intersect_I": len(U),
            "S=R_plus_I": len(S),
            "K=ker(Astar)": len(K),
            "M_line": 40,
        },
        "apartment_code_exact_sequence": "0 -> K/J (29) -> C_ap (39) -> H10 (10) -> 0",
        "radical_filtration": {
            "chain": "0 < U/J < S/J < K/J",
            "layer_dimensions": [8, 7, 14],
            "middle_split": "S/U = (R/U) direct-sum (I/U) = 6 + 1",
            "irreducible_nontrivial_factors": [8, 6, 14],
            "trivial_factor": 1,
            "vector_orbit_scans": {
                "dim8": orbits8,
                "dim6": orbits6,
                "dim14": orbits14,
            },
        },
        "owners": {
            "line_side_hull_and_rank10": "Pass 187",
            "apartment_code_and_radical_dimensions": "Passes 4463-4464",
            "H10_quotient_identification": "Pass 4469",
        },
        "boundary": (
            "The 8,6,14 labels are modular representation dimensions, not particle multiplicities.  "
            "This is an invariant module filtration and does not imply a physical radical-discarding measurement."
        ),
        "checks": {"passed": sum(ok for _, ok in checks), "total": len(checks)},
    }

    out = ROOT / "data" / "PART_W33_PASS4475_APARTMENT_RADICAL_MODULE_FILTRATION.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Pass 4475 -- apartment radical module filtration")
    print("  exact sequence: 0 -> 29 -> 39 -> H10(10) -> 0")
    print("  radical chain: 8 | (6 + 1) | 14")
    print("  nontrivial factors 8,6,14 pass exhaustive cyclic irreducibility scans")
    print(f"  checks: {result['checks']['passed']}/{result['checks']['total']} PASS")
    print(f"  wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
