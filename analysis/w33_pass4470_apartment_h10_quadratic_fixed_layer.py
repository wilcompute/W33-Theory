#!/usr/bin/env python3
"""Pass 4470 -- quadratic refinement and the fixed H10 layer.

Pass 4469 proved a canonical symplectic isomorphism

    Phi : A_ap/rad(A_ap) -> H10 = C^perp/C,
    Phi([H^T b]) = [N b],

where H is line/apartment incidence, N is point/line incidence and
C=ker(N^T) is the [40,15,8] sentinel code.

Both quotient spaces carry a natural binary quadratic refinement from Hamming
weight:

    q_ap([y])  = wt(y)/2 mod 2,       y in A_ap,
    q_H10([x]) = wt(x)/2 mod 2,       x in C^perp.

This pass proves four sharper facts.

(1) BOTH QUADRATICS DESCEND.  The apartment radical is totally singular for
q_ap (its basis has weight 0 mod 4 and is orthogonal to all of A_ap).  The
sentinel C is doubly even and orthogonal to C^perp, so q_H10 is well defined.

(2) BOTH ARE PLUS TYPE.  Each 10-dimensional quotient has exactly 528 singular
classes including zero, hence is O^+(10,2).  The 528 on H10 is owned by Pass
201; its independent reappearance on apartment parity is new evidence for the
bridge, not a new claim about the CSS code.

(3) THE RAW INCIDENCE MAP MISSES BY ONE FIXED LINE.  Although Phi preserves the
symplectic form, q_ap and q_H10 o Phi are not equal.  Their difference is a
nonzero linear functional ell.  Nondegeneracy gives a unique class a with

    ell(v) = B(v,a).

The verifier identifies Phi(a) exactly with

    im(A_point mod 2) / C,

which Pass 187 already owns as the fixed 1-layer inside the uniserial
H10 = 1 | 8 | 1 filtration.  Algebraically we check

    span(C, Phi(a)) = im(A_point mod 2).

Because this quotient is one-dimensional over F2 and incidence automorphisms
preserve both subspaces, its nonzero class is fixed by the whole incidence
automorphism group.

(4) ONE TRANSVECTION REPAIRS THE QUADRATIC.  The defect class is isotropic,
q_H10(a)=0.  Therefore the symplectic transvection

    T_a(v) = v + B(v,a) a

satisfies

    q_H10(T_a Phi(v)) = q_ap(v)

for all 2^10 quotient classes.  Since a is fixed, T_a commutes with the
incidence-automorphism action.  Thus Psi=T_a o Phi is an equivariant quadratic
isometry between the apartment-parity quotient and the established O^+(10,2)
logical-label shadow.

Boundary: the transvection is a comparison map between two quotient models.
It is not asserted to be a physical gate, an error-correction operation, or a
new logical degree of freedom.  The fixed 1-layer and the 528 H10 singular
classes predate this pass (Passes 187 and 201 respectively).
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

ROOT = Path(__file__).resolve().parents[1]


def q_half_weight(v: np.ndarray) -> int:
    w = int(np.asarray(v, dtype=np.uint8).sum())
    if w % 2:
        raise ValueError("q=wt/2 mod 2 requires even Hamming weight")
    return (w // 2) & 1


def solve_mod2(M: np.ndarray, rhs: np.ndarray) -> np.ndarray:
    A = np.hstack(
        ((np.asarray(M, dtype=np.uint8) & 1).copy(),
         (np.asarray(rhs, dtype=np.uint8) & 1).reshape(-1, 1))
    )
    m, n = M.shape
    r = 0
    pivots: list[int] = []
    for c in range(n):
        piv = next((i for i in range(r, m) if A[i, c]), None)
        if piv is None:
            continue
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        for i in range(m):
            if i != r and A[i, c]:
                A[i] ^= A[r]
        pivots.append(c)
        r += 1
    for i in range(r, m):
        if not A[i, :n].any() and A[i, n]:
            raise ValueError("inconsistent F2 system")
    x = np.zeros(n, dtype=np.uint8)
    for rr, c in enumerate(pivots):
        x[c] = A[rr, n]
    return x


def same_span(A: np.ndarray, B: np.ndarray) -> bool:
    A = rref_rows(A)
    B = rref_rows(B)
    return (
        len(A) == len(B)
        and all(in_span(B, a) for a in A)
        and all(in_span(A, b) for b in B)
    )


def main() -> int:
    _, _, A_int, N_int, edge_line = geometry()
    N = (N_int % 2).astype(np.uint8)
    Apoint = (N @ N.T) % 2
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

    check("Pass4464 Gram identity", np.array_equal((H @ H.T) % 2, Astar))
    check("rank Astar 10", rank_mod2(Astar) == 10)

    sentinel = nullspace_mod2(N.T)
    context = rref_rows(N.T)
    ker_astar = nullspace_mod2(Astar)
    quotient_coeff = complement_to(ker_astar, 40)
    ap_reps = np.asarray([(H.T @ b) % 2 for b in quotient_coeff], dtype=np.uint8)
    h10_reps = np.asarray([(N @ b) % 2 for b in quotient_coeff], dtype=np.uint8)
    gram = (quotient_coeff @ Astar @ quotient_coeff.T) % 2

    check("sentinel dim 15", len(sentinel) == 15)
    check("context dim 25", len(context) == 25)
    check("quotient basis dim 10", len(quotient_coeff) == 10)
    check("quotient symplectic Gram rank 10", rank_mod2(gram) == 10)
    check("quotient symplectic Gram alternating", np.all(np.diag(gram) == 0))

    # Apartment q descends: radical is orthogonal to the full apartment code
    # and is totally singular for wt/2 mod 2.
    apartment_code = rref_rows(H.T)
    radical_images = np.asarray([(H.T @ k) % 2 for k in ker_astar], dtype=np.uint8)
    apartment_radical = rref_rows(radical_images)
    check("apartment code dim 39", len(apartment_code) == 39)
    check("apartment radical dim 29", len(apartment_radical) == 29)
    check(
        "apartment radical orthogonal to apartment code",
        not np.any((apartment_radical @ apartment_code.T) % 2),
    )
    check(
        "apartment radical basis doubly even",
        all(int(r.sum()) % 4 == 0 for r in apartment_radical),
    )

    # H10 q descends: C is doubly even and C is orthogonal to C^perp.
    check("sentinel basis doubly even", all(int(c.sum()) % 4 == 0 for c in sentinel))
    check("sentinel orthogonal to context", not np.any((sentinel @ context.T) % 2))
    check("context basis even", all(int(x.sum()) % 2 == 0 for x in context))

    # Exhaust all quotient classes and record both quadratic refinements.
    q_ap: list[int] = []
    q_h10: list[int] = []
    coeffs: list[np.ndarray] = []
    for mask in range(1 << 10):
        coeff = np.array([(mask >> i) & 1 for i in range(10)], dtype=np.uint8)
        coeffs.append(coeff)
        y = (coeff @ ap_reps) % 2
        x = (coeff @ h10_reps) % 2
        q_ap.append(q_half_weight(y))
        q_h10.append(q_half_weight(x))

    check("apartment quotient plus-type count 528", q_ap.count(0) == 528)
    check("H10 quotient plus-type count 528", q_h10.count(0) == 528)

    # The difference of two quadratic refinements with the same polar form must
    # be linear; verify it exhaustively rather than assuming the theorem.
    defect = np.asarray([a ^ b for a, b in zip(q_ap, q_h10)], dtype=np.uint8)
    defect_basis = np.asarray(
        [q_ap[1 << i] ^ q_h10[1 << i] for i in range(10)], dtype=np.uint8
    )
    check("quadratic refinements genuinely differ", np.any(defect_basis))
    check(
        "quadratic defect is linear on all 1024 classes",
        all(int(defect[m]) == int((coeffs[m] @ defect_basis) % 2) for m in range(1 << 10)),
    )
    check("nonzero defect is balanced", int(defect.sum()) == 512)

    # Unique symplectic representative a of the defect functional.
    a = solve_mod2(gram, defect_basis)
    check("defect representative nonzero", np.any(a))
    check("defect represented by B(-,a)", np.array_equal((gram @ a) % 2, defect_basis))

    a_ap = (a @ ap_reps) % 2
    a_h10 = (a @ h10_reps) % 2
    check("defect class isotropic in apartment q", q_half_weight(a_ap) == 0)
    check("defect class isotropic in H10 q", q_half_weight(a_h10) == 0)

    # Identify the H10 class with Pass 187's fixed 1-layer im(A2)/C.
    im_apoint = rref_rows(Apoint)
    check("rank im Apoint = 16", len(im_apoint) == 16)
    check("defect target lies in im Apoint", in_span(im_apoint, a_h10))
    check("defect target not in sentinel", not in_span(sentinel, a_h10))
    check(
        "defect target generates im(Apoint)/C fixed line",
        same_span(np.vstack((sentinel, a_h10)), im_apoint),
    )

    # One symplectic transvection along the isotropic fixed class repairs Phi.
    def transvection_coords(c: np.ndarray) -> np.ndarray:
        pairing = int((c @ gram @ a) % 2)
        return c ^ (a if pairing else np.zeros_like(a))

    repaired = True
    for m, c in enumerate(coeffs):
        tc = transvection_coords(c)
        x_t = (tc @ h10_reps) % 2
        repaired &= q_half_weight(x_t) == q_ap[m]
    check("single transvection repairs all 1024 classes", repaired)

    # Transvection is symplectic on quotient coordinates.
    T_rows = np.asarray([transvection_coords(np.eye(10, dtype=np.uint8)[i]) for i in range(10)])
    check("repair transvection preserves symplectic Gram", np.array_equal((T_rows @ gram @ T_rows.T) % 2, gram))

    result = {
        "pass": 4470,
        "theorem": "W33 apartment/H10 quadratic fixed-layer correction theorem",
        "owners": {
            "H10_fixed_1_8_1_filtration": "Pass 187",
            "H10_plus_type_528": "Pass 201",
            "symplectic_intertwiner": "Pass 4469",
        },
        "quadratic_refinements": {
            "apartment": "q_ap([y]) = wt(y)/2 mod 2",
            "H10": "q_H10([x]) = wt(x)/2 mod 2",
            "apartment_singular_classes_including_zero": q_ap.count(0),
            "H10_singular_classes_including_zero": q_h10.count(0),
            "type": "O+(10,2) on both quotients",
        },
        "raw_incidence_map": {
            "symplectic": True,
            "quadratic": False,
            "defect_nonzero_classes": int(defect.sum()),
            "defect_functional": "ell(v) = q_ap(v) + q_H10(Phi(v)) = B(v,a)",
        },
        "defect_class": {
            "unique_by_nondegeneracy": True,
            "isotropic": True,
            "target_identification": "Phi(a) spans im(A_point mod 2)/C",
            "existing_module_owner": "Pass 187 fixed 1-layer inside H10 = 1|8|1",
            "deterministic_representative_weight_H10": int(a_h10.sum()),
            "deterministic_representative_weight_apartment": int(a_ap.sum()),
        },
        "repair": {
            "formula": "T_a(v)=v+B(v,a)a; Psi=T_a o Phi",
            "all_1024_classes_verified": repaired,
            "equivariance_reason": (
                "im(A_point)/C is a one-dimensional invariant F2 quotient, hence its nonzero class a is fixed; "
                "therefore T_a commutes with every incidence automorphism"
            ),
        },
        "boundary": (
            "T_a is a comparison-map correction between two natural quadratic quotient models.  It is not "
            "asserted to be a physical gate or a new logical degree of freedom.  The fixed layer and H10 "
            "plus-type structure are prior results; the new content is their exact role in the apartment/H10 bridge."
        ),
        "checks": {"passed": sum(ok for _, ok in checks), "total": len(checks)},
    }

    out = ROOT / "data" / "PART_W33_PASS4470_APARTMENT_H10_QUADRATIC_FIXED_LAYER.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Pass 4470 -- apartment/H10 quadratic fixed-layer theorem")
    print("  both quotient quadratics: O+(10,2), 528 singular classes including zero")
    print("  raw Phi is symplectic but not quadratic")
    print("  unique defect class = Pass-187 fixed im(Apoint)/C layer")
    print("  one isotropic transvection repairs q on all 1024 classes")
    print(f"  defect representative weights: H10={int(a_h10.sum())}, apartment={int(a_ap.sum())}")
    print(f"  checks: {result['checks']['passed']}/{result['checks']['total']} PASS")
    print(f"  wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
