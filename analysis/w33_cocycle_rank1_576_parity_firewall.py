#!/usr/bin/env python3
"""Rank-one support, parity firewall, and D8 core of the cube-cover cocycle.

The certified order-96 Heawood stabilizer is the central extension of

    Q = C2_b x S4

with factor set

    alpha((b,sigma),(d,tau)) = d * sgn(sigma) mod 2.

This file extracts structure hidden in that simple formula.

* alpha is a rank-one separable support matrix: it is nonzero exactly when the
  first S4 permutation is odd and the second antipodal bit is one. There are
  24 such first elements and 24 such second elements, hence exactly 576 twisted
  ordered pairs and 1728 untwisted pairs in QxQ.
* alpha vanishes identically when the first S4 component is even. Thus the
  C2 x A4 sector is an exact parity firewall.
* The cocycle commutator factors through the abelianization coordinates
  (b,epsilon) in C2^2 as the nondegenerate alternating form

      kappa((b,e),(d,f)) = e*d + b*f.

  The central extension of this two-bit plane has two involutory generators
  with central commutator z and product of order four: it is D8.

This recovers the D8 ingredient of the independent fiber-product presentation
from the cocycle itself.
"""
from __future__ import annotations

from collections import Counter
from itertools import permutations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = Path(__file__).resolve().parent
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_stabilizer96_cube_central_cover import compose_perm, sign_perm  # noqa: E402

OUT = ROOT / "data" / "w33_cocycle_rank1_576_parity_firewall.json"


def alpha(x, y):
    _b, s = x
    d, _t = y
    return d & sign_perm(s)


def commutator_pair(x, y):
    return alpha(x, y) ^ alpha(y, x)


def extension_mul(x, y):
    # Restricted extension over abelianization B=C2_b x C2_sign.
    # Element is (z,b,e), with alpha((b,e),(d,f))=d*e.
    z, b, e = x
    w, d, f = y
    return (z ^ w ^ (d & e), b ^ d, e ^ f)


def extension_power(x, n):
    out = (0, 0, 0)
    for _ in range(n):
        out = extension_mul(out, x)
    return out


def extension_order(x):
    for n in range(1, 9):
        if extension_power(x, n) == (0, 0, 0):
            return n
    raise AssertionError("order bound")


def build_result() -> dict:
    S4 = tuple(permutations(range(4)))
    id4 = tuple(range(4))
    Q = tuple((b, s) for b in (0, 1) for s in S4)
    assert len(Q) == 48

    odd_first = {q for q in Q if sign_perm(q[1]) == 1}
    antipodal_second = {q for q in Q if q[0] == 1}
    assert len(odd_first) == len(antipodal_second) == 24

    support = {(x, y) for x in Q for y in Q if alpha(x, y)}
    assert len(support) == 576
    assert support == {(x, y) for x in odd_first for y in antipodal_second}
    zero_count = len(Q) ** 2 - len(support)
    assert zero_count == 1728

    row_weights = Counter(sum(alpha(x, y) for y in Q) for x in Q)
    col_weights = Counter(sum(alpha(x, y) for x in Q) for y in Q)
    assert row_weights == {0: 24, 24: 24}
    assert col_weights == {0: 24, 24: 24}

    row_vectors = {tuple(alpha(x, y) for y in Q) for x in Q}
    col_vectors = {tuple(alpha(x, y) for x in Q) for y in Q}
    assert len(row_vectors) == len(col_vectors) == 2
    assert tuple(0 for _ in Q) in row_vectors and tuple(0 for _ in Q) in col_vectors

    A4 = {s for s in S4 if sign_perm(s) == 0}
    Q_even = {(b, s) for b in (0, 1) for s in A4}
    assert len(A4) == 12 and len(Q_even) == 24
    assert all(alpha(x, y) == 0 for x in Q_even for y in Q)

    e_b = (1, 0)
    e_s = (0, 1)

    def form(u, v):
        b, e = u
        d, f = v
        return (e & d) ^ (b & f)

    for b in (0, 1):
        for e in (0, 1):
            s = id4 if e == 0 else next(p for p in S4 if sign_perm(p) == 1)
            x = (b, s)
            for d in (0, 1):
                for f in (0, 1):
                    t = id4 if f == 0 else next(p for p in S4 if sign_perm(p) == 1)
                    y = (d, t)
                    assert commutator_pair(x, y) == form((b, e), (d, f))

    assert form(e_b, e_b) == form(e_s, e_s) == 0
    assert form(e_b, e_s) == form(e_s, e_b) == 1
    nonzero = ((0, 1), (1, 0), (1, 1))
    assert all(any(form(u, v) == 1 for v in nonzero) for u in nonzero)

    Btilde = [(z, b, e) for z in (0, 1) for b in (0, 1) for e in (0, 1)]
    orders = Counter(extension_order(x) for x in Btilde)
    assert orders == {1: 1, 2: 5, 4: 2}
    xb = (0, 1, 0)
    xs = (0, 0, 1)
    z = (1, 0, 0)
    assert extension_order(xb) == extension_order(xs) == 2
    assert extension_mul(extension_mul(extension_mul(xb, xs), xb), xs) == z
    assert extension_order(extension_mul(xb, xs)) == 4

    central = json.loads((ROOT / "data" / "w33_stabilizer96_cube_central_cover.json").read_text(encoding="utf-8"))
    group = json.loads((ROOT / "data" / "w33_heawood_stabilizer96_presentation_lattice.json").read_text(encoding="utf-8"))
    old576 = json.loads((ROOT / "data" / "PART_W33_PASS5468_5475_SIMPLEX_STABILISER_IS_WF4.json").read_text(encoding="utf-8"))
    assert central["status"] == group["status"] == "PASS"
    d8_declared = (
        "D8" in group["fiber_product"]["definition"]
        and "D8" in group["headline"]
        and group["fiber_product"]["D8_character"].startswith("chi(")
    )
    assert d8_declared
    assert old576["pass_5470"]["latin_4x4"] == 576

    checks = {
        "quotient_order_48": len(Q) == 48,
        "cocycle_support_exactly_24_times24_equals576": len(support) == 576,
        "cocycle_zero_entries_1728": zero_count == 1728,
        "support_matrix_rank_one_pattern": len(row_vectors) == len(col_vectors) == 2,
        "even_A4_sector_is_cocycle_firewall": all(alpha(x, y) == 0 for x in Q_even for y in Q),
        "commutator_factors_to_symplectic_C2_squared": form(e_b, e_s) == form(e_s, e_b) == 1,
        "abelianization_pairing_nondegenerate": all(any(form(u, v) for v in nonzero) for u in nonzero),
        "restricted_extension_is_D8_by_order_spectrum": orders == {1: 1, 2: 5, 4: 2},
        "independent_stabilizer_certificate_contains_D8": d8_declared,
        "independent_repo_4x4_latin_count_is576": old576["pass_5470"]["latin_4x4"] == 576,
    }

    return {
        "schema": "w33.cocycle-rank1-576-parity-firewall.v2",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "The cube-cover 2-cocycle is a rank-one parity carry with exactly 576 twisted pairs. "
            "It vanishes on the even A4 sector, and its commutator descends to the nondegenerate "
            "symplectic form on C2^2 whose eight-element central lift is D8."
        ),
        "support_geometry": {
            "quotient_size": len(Q),
            "ordered_pair_count": len(Q) ** 2,
            "odd_first_elements": len(odd_first),
            "antipodal_second_elements": len(antipodal_second),
            "twisted_pairs": len(support),
            "untwisted_pairs": zero_count,
            "factorization": "576=24^2; 1728=3*576",
            "row_weight_histogram": {str(k): v for k, v in sorted(row_weights.items())},
            "column_weight_histogram": {str(k): v for k, v in sorted(col_weights.items())},
            "rank_one_reading": "alpha(x,y)=oddParity(x)*antipodalBit(y), so the 48x48 support matrix is an outer product over F2.",
        },
        "parity_firewall": {
            "A4_size": len(A4),
            "C2_times_A4_size": len(Q_even),
            "law": "alpha((b,sigma),y)=0 for every y whenever sigma is even",
            "reading": "The local orientation-preserving tetrahedral A4 sector carries no central twist; odd S4 parity is required to activate z.",
        },
        "abelianization_core": {
            "coordinates": "(b,epsilon) with b=antipodal bit and epsilon=sgn(sigma)",
            "commutator_form": "kappa((b,e),(d,f))=e*d+b*f mod 2",
            "matrix_in_basis_b_sign": [[0, 1], [1, 0]],
            "nondegenerate": True,
            "central_lift_order": 8,
            "central_lift_order_histogram": {str(k): v for k, v in sorted(orders.items())},
            "central_lift_isomorphism": "D8",
            "recovery": "This D8 is recovered directly from the cocycle and agrees with the independent D8 ingredient in the stabilizer fiber-product certificate.",
        },
        "count_bridges": {
            "576": "Cocycle support size 24^2; independently the repo certifies 576 distinct 4x4 Latin squares and multiple order-576 group constructions. Equality of counts alone is not an isomorphism.",
            "1728": "Untwisted ordered quotient pairs = 1728. This is recorded as a bridge target because 1728 also recurs in Holonet controller ledgers; no canonical identification is asserted here.",
        },
        "claim_boundary": [
            "The 576 and 1728 counts are exact consequences of the certified cocycle formula.",
            "The D8 identification is structural, using the restricted extension multiplication and element-order spectrum, not order alone.",
            "Matches to Latin-square counts or hardware ledgers remain bridge targets until an explicit equivariant dictionary is built.",
            "The parity carry is a finite group-cohomology obstruction; no Spin/Pin or fermionic phase interpretation is asserted.",
        ],
        "checks": checks,
    }


def main() -> int:
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "twisted_pairs": result["support_geometry"]["twisted_pairs"],
        "untwisted_pairs": result["support_geometry"]["untwisted_pairs"],
        "parity_firewall": result["parity_firewall"]["law"],
        "abelianization_lift": result["abelianization_core"]["central_lift_isomorphism"],
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
