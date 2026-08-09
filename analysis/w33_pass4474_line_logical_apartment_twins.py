#!/usr/bin/env python3
"""Pass 4474 -- line-logical / apartment-generator twin W33 theorem.

Passes 4469--4470 built the canonical symplectic bridge from the apartment
parity quotient to H10 and found the unique fixed isotropic defect class f.
This pass evaluates that bridge on the 40 most geometric generators: the
individual W33 lines.

For line ell let e_ell be its coefficient vector.  Then

    g_ell = H^T e_ell

is the apartment-code generator recording which of the 1620 apartments contain
ell, while

    x_ell = N e_ell

is the 4-point incidence vector of ell.  Pass 201 already owns the theorem that
the x_ell are the weight-4 minimum logical operators of the [[40,10,4]] CSS
code.  The new bridge makes the correspondence literal:

    [g_ell]  -->  [x_ell].

The exact consequences are stronger.

* wt(g_ell)=162 and wt(x_ell)=4 for all 40 lines.
* The 40 H10 classes [x_ell] are distinct, nonzero, and span H10 modulo C.
* Their polar graph is the dual W33 line-collinearity graph:
      B(x_ell,x_m)=1 iff ell,m meet.
  The apartment generators have the identical polar graph because HH^T=N^TN.
* q_ap(g_ell)=1 while q_H10(x_ell)=0 for every ell.  Thus the quadratic defect
  of Pass 4470 is UNIFORM on the complete 40-line geometry.
* The unique defect/fixed class f is characterized intrinsically by
      B(x_ell,f)=1 for every one of the 40 minimum logical line classes.
  Exhaustion of all 2^10 H10 classes proves uniqueness.
* The Pass-4470 transvection therefore sends every line class by
      T_f(x_ell)=x_ell+f.
  The shifted 40-set is anisotropic (q=1), remains pairwise W33 under B, and is
  distinct.  Hence the bridge exhibits a singular W33 40-set and an anisotropic
  W33 40-set inside the same O+(10,2) shadow, exchanged by the fixed-layer
  transvection.

Boundary: "singular/anisotropic twin" refers to the finite quadratic space
H10.  It is not a new physical particle doubling, not a second CSS code, and
not a statement that the comparison transvection is an implemented gate.
Minimum distance 4 and the identification of line vectors as minimum logicals
remain owned by Pass 201.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from w33_pass4461_line_signing_apartment_trace import geometry, simple_four_cycles
from w33_pass4463_apartment_parity_tomography import rank_mod2
from w33_pass4469_apartment_css_h10_intertwiner import (
    complement_to,
    in_span,
    nullspace_mod2,
    rref_rows,
)
from w33_pass4470_apartment_h10_quadratic_fixed_layer import q_half_weight, solve_mod2

ROOT = Path(__file__).resolve().parents[1]


def class_key_mod_subspace(v: np.ndarray, subspace: np.ndarray) -> tuple[int, ...]:
    """Canonical RREF-reduction key modulo a row subspace."""
    residual = np.asarray(v, dtype=np.uint8).copy()
    basis = rref_rows(subspace)
    for b in basis:
        pivot = int(np.flatnonzero(b)[0])
        if residual[pivot]:
            residual ^= b
    return tuple(int(x) for x in residual)


def main() -> int:
    _, lines, A_int, N_int, edge_line = geometry()
    N = (N_int % 2).astype(np.uint8)  # points x lines
    Astar = (N.T @ N) % 2
    cycles = simple_four_cycles(A_int)
    supports = [frozenset(edge_line[e] for e in C4) for C4 in cycles]
    H = np.zeros((40, 1620), dtype=np.uint8)
    for j, support in enumerate(supports):
        for li in support:
            H[li, j] = 1

    checks: list[tuple[str, bool]] = []

    def check(name: str, cond) -> None:
        ok = bool(cond)
        checks.append((name, ok))
        if not ok:
            raise AssertionError(name)

    sentinel = nullspace_mod2(N.T)
    context = rref_rows(N.T)
    ker_astar = nullspace_mod2(Astar)
    quotient_coeff = complement_to(ker_astar, 40)
    h10_basis_reps = np.asarray([(N @ b) % 2 for b in quotient_coeff], dtype=np.uint8)
    ap_basis_reps = np.asarray([(H.T @ b) % 2 for b in quotient_coeff], dtype=np.uint8)
    gram = (quotient_coeff @ Astar @ quotient_coeff.T) % 2

    check("40 geometric lines", len(lines) == 40)
    check("sentinel dimension 15", len(sentinel) == 15)
    check("H10 quotient dimension 10", rank_mod2(np.vstack((sentinel, h10_basis_reps))) - len(sentinel) == 10)
    check("quotient Gram rank 10", rank_mod2(gram) == 10)

    # Reconstruct the Pass-4470 defect class in quotient coordinates.
    defect_basis = np.asarray(
        [q_half_weight(ap_basis_reps[i]) ^ q_half_weight(h10_basis_reps[i]) for i in range(10)],
        dtype=np.uint8,
    )
    f_coords = solve_mod2(gram, defect_basis)
    f = (f_coords @ h10_basis_reps) % 2
    check("fixed defect class is isotropic", q_half_weight(f) == 0)
    check("fixed defect class not in sentinel", not in_span(sentinel, f))

    # The 40 single-line objects on both sides.
    g = H.copy()          # row ell = H^T e_ell, represented as row of H
    x = N.T.copy()        # row ell = N e_ell, line's 4 point indicators

    check("all apartment line generators weight 162", all(int(row.sum()) == 162 for row in g))
    check("all line logical representatives weight 4", all(int(row.sum()) == 4 for row in x))
    check("all line logical representatives lie in Cperp", all(in_span(context, row) for row in x))
    check("no line logical representative lies in C", all(not in_span(sentinel, row) for row in x))

    logical_keys = [class_key_mod_subspace(row, sentinel) for row in x]
    check("40 distinct nonzero H10 line classes", len(set(logical_keys)) == 40 and all(any(k) for k in logical_keys))
    check("40 line classes span H10 over C", rank_mod2(np.vstack((sentinel, x))) == 25)

    # Same polar W33 geometry on both 40-sets.
    gram_ap_lines = (g @ g.T) % 2
    gram_h10_lines = (x @ x.T) % 2
    check("line-generator Gram is Astar", np.array_equal(gram_ap_lines, Astar))
    check("logical-line Gram is Astar", np.array_equal(gram_h10_lines, Astar))
    check("the two 40-set polar Grams coincide", np.array_equal(gram_ap_lines, gram_h10_lines))

    # Raw quadratic types are opposite on every geometric line.
    qg = [q_half_weight(row) for row in g]
    qx = [q_half_weight(row) for row in x]
    check("all 40 apartment line generators anisotropic", qg == [1] * 40)
    check("all 40 raw logical line classes singular", qx == [0] * 40)

    pair_f = np.asarray([(row @ f) % 2 for row in x], dtype=np.uint8)
    check("fixed class pairs one with every line logical", np.all(pair_f == 1))

    # Unique H10 class with B(x_ell, candidate)=1 for every line ell.
    universal_pairing_classes = []
    for mask in range(1 << 10):
        c = np.array([(mask >> i) & 1 for i in range(10)], dtype=np.uint8)
        candidate = (c @ h10_basis_reps) % 2
        if np.all((x @ candidate) % 2 == 1):
            universal_pairing_classes.append(mask)
    check("universal pairing class unique", len(universal_pairing_classes) == 1)
    f_mask = sum(int(bit) << i for i, bit in enumerate(f_coords))
    check("unique universal pairing class is Pass4470 defect", universal_pairing_classes == [f_mask])

    # The fixed transvection maps the singular 40-set to an anisotropic twin.
    shifted = x ^ f
    shifted_keys = [class_key_mod_subspace(row, sentinel) for row in shifted]
    check("shifted 40 classes distinct", len(set(shifted_keys)) == 40)
    check("shifted classes anisotropic", all(q_half_weight(row) == 1 for row in shifted))
    check("shifted polar Gram remains Astar", np.array_equal((shifted @ shifted.T) % 2, Astar))
    check("transvection rule applies to every line", np.all(pair_f == 1))

    # The shifted set is not accidentally the same set of H10 classes.
    check("singular and anisotropic W33 class sets are disjoint", set(logical_keys).isdisjoint(set(shifted_keys)))

    result = {
        "pass": 4474,
        "theorem": "W33 line-logical / apartment-generator singular-anisotropic twin theorem",
        "owners": {
            "minimum_logical_weight_4_and_40_line_logicals": "Pass 201",
            "H10_fixed_layer": "Pass 187",
            "apartment_H10_symplectic_bridge": "Pass 4469",
            "fixed_quadratic_defect_transvection": "Pass 4470",
        },
        "single_line_correspondence": {
            "apartment_generator": "g_l = H^T e_l",
            "apartment_generator_weight": 162,
            "logical_line": "x_l = N e_l",
            "logical_line_weight": 4,
            "number_of_distinct_H10_line_classes": len(set(logical_keys)),
            "span_with_C_dimension": rank_mod2(np.vstack((sentinel, x))),
            "pairing_graph": "Astar: dual W33 line-collinearity",
        },
        "quadratic_twin": {
            "raw_line_classes": "40 singular H10 classes q=0",
            "apartment_line_generators": "40 anisotropic apartment classes q=1",
            "fixed_class_characterization": "unique H10 class f with B(x_l,f)=1 for all 40 lines",
            "fixed_class_isotropic": True,
            "transvection": "T_f(x_l)=x_l+f for every line l",
            "shifted_line_classes": "40 anisotropic H10 classes q=1",
            "shifted_pairing_graph": "same Astar/W33 polar graph",
            "raw_and_shifted_class_sets_disjoint": True,
        },
        "boundary": (
            "The singular/anisotropic twin is a statement inside the finite quadratic label space H10.  "
            "It is not a physical particle doubling, not a second CSS code, and does not promote the comparison "
            "transvection to an implemented logical gate.  Minimum distance 4 remains owned by Pass 201."
        ),
        "checks": {"passed": sum(ok for _, ok in checks), "total": len(checks)},
    }

    out = ROOT / "data" / "PART_W33_PASS4474_LINE_LOGICAL_APARTMENT_TWINS.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Pass 4474 -- line-logical / apartment-generator twin theorem")
    print("  40 x weight-162 apartment generators -> 40 x weight-4 minimum logical line classes")
    print("  both 40-sets carry the same W33 polar pairing graph")
    print("  raw logical lines q=0; apartment generators q=1")
    print("  fixed f is the unique class pairing 1 with every line logical")
    print("  T_f exchanges singular W33 with an anisotropic W33 twin")
    print(f"  checks: {result['checks']['passed']}/{result['checks']['total']} PASS")
    print(f"  wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
