#!/usr/bin/env python3
"""Pass 183: the discriminant ledger of the incidence square.

Passes 162/180 found a selected Z/8 generator with q(h) = 11/8 on both
dark lattices attached to the nonisomorphic dual pair W(3,3), Q(4,3).
This witness assembles the group-level mechanism from four exact ingredients:

1. UNIMODULAR CUT.  SNF(N) = 1^25 makes N a unimodular-cokernel map:
   N Z^40 is already saturated and equals code_L = L_route^perp.

2. NEGATION LAWS.  In the unimodular ambient, D(L) = D(L^perp) with
   negated form.  Under change of Z/8 generator the dark numerator orbit
   is {3,11} mod 16 and the code orbit is its negative {5,13}; the stored
   representatives are 11/8 and 13/8.  Both code lattices have Milgram
   signature 1 mod 8 (rank 25).

3. THE TRANSPORT.  On code_P the readout Gram N^T N = 4I + A satisfies
   the exact annihilator (A - 2I)(A - 12I) = 0: N scales the Perron line
   by 4 and the 24-dimensional gauge sector by sqrt(6).

4. THE EXACT SEQUENCE.  0 -> code_P --N--> code_L -> Q -> 0 with
   [code_L : N code_P] = 2^17 3^10 = det(L_address) and the invariant
   factors of Q equal to the Smith invariants of the address Gram
   (2^5, 6^9, 24).  This proves an abstract finite-abelian-group
   identification with the address discriminant group.  It does not by
   itself construct a discriminant-quadratic-form isometry.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
import json
import math
from pathlib import Path
import sys

import numpy as np
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
    build_w33,
    lattices_equal,
    saturated_kernel,
    w33_lines,
)
from analysis.w33_pass160_trade_tower_gq42 import generic_saturated_kernel
from analysis.w33_pass162_mod8_anomaly_ledger import (
    eighth_root_index,
    p_adic_snf_generators,
    p_part_gauss_sum,
    p_valuation,
)

OUT = ROOT / "data" / "w33_pass183_incidence_square_ledger.json"


def orthogonal_complement(basis40xk):
    padded = np.zeros((40, 40), dtype=np.int64)
    padded[: basis40xk.shape[1], :] = basis40xk.T
    return saturated_kernel(padded)


def z8_block_q(gram):
    determinant = abs(int(Matrix(gram.tolist()).det()))
    val = p_valuation(determinant, 2, 64)
    generators, _ = p_adic_snf_generators(gram, 2, val)
    for order, column in generators:
        if order == 8:
            reduced = np.array([int(v) % 8 for v in column], dtype=np.int64)
            numerator = int(reduced @ gram @ reduced) % 128
            g = math.gcd(numerator, 64) or 1
            return f"{numerator // g}/{64 // g}"
    return None


def order8_q_distribution(gram):
    """Enumerate every exact-order-eight element of the 2-primary form.

    The Smith coordinates returned by ``p_adic_snf_generators`` are an
    independent direct-product coordinate system.  With common denominator
    eight, the exact element order is therefore the lcm of the component
    orders, and q(x) is computed exactly modulo 2Z.
    """
    determinant = abs(int(Matrix(gram.tolist()).det()))
    generators, dual_ok = p_adic_snf_generators(
        gram, 2, p_valuation(determinant, 2, 64)
    )
    denominator = max(order for order, _ in generators)
    if not dual_ok or denominator != 8:
        return {}, 0, False
    scaled = [
        (
            order,
            (np.asarray(column, dtype=np.int64) * (denominator // order))
            % denominator,
        )
        for order, column in generators
    ]
    expected_total = math.prod(order for order, _ in scaled)
    if expected_total != 2 ** p_valuation(determinant, 2, 64):
        return {}, 0, False
    counts = Counter()
    representatives = set()
    enumerated = 0
    for coefficients in product(*(range(order) for order, _ in scaled)):
        exact_order = 1
        numerator = np.zeros(gram.shape[0], dtype=np.int64)
        for coefficient, (order, vector) in zip(coefficients, scaled):
            numerator = (numerator + coefficient * vector) % denominator
            if coefficient:
                exact_order = math.lcm(
                    exact_order, order // math.gcd(coefficient, order)
                )
        representatives.add(tuple(int(value) for value in numerator))
        if exact_order != 8:
            continue
        q_numerator = int(numerator @ gram @ numerator) % (
            2 * denominator * denominator
        )
        if q_numerator % denominator:
            return {}, enumerated, False
        counts[(q_numerator // denominator) % (2 * denominator)] += 1
        enumerated += 1
    independent = len(representatives) == expected_total
    return dict(sorted(counts.items())), enumerated, independent


def milgram_phase(gram, checks, tag):
    smith = smith_normal_form(Matrix(gram.tolist()), domain=ZZ)
    rank = gram.shape[0]
    determinant = 1
    for i in range(rank):
        determinant *= max(abs(int(smith[i, i])), 1)
    total = 1.0 + 0.0j
    total_size = 1
    for prime in (2, 3, 5):
        val = p_valuation(determinant, prime, 64)
        if not val:
            continue
        generators, _ = p_adic_snf_generators(gram, prime, val)
        size, gauss, _, distinct = p_part_gauss_sum(gram, generators, prime)
        checks[f"{tag}_p{prime}_distinct"] = bool(distinct)
        total *= gauss / math.sqrt(size)
        total_size *= size
    index, residual = eighth_root_index(total)
    checks[f"{tag}_discriminant_complete"] = total_size == determinant
    checks[f"{tag}_milgram_numeric_eighth_root"] = residual < 1e-6
    return index, determinant


def main():
    _, adjacency, _ = build_w33()
    lines = w33_lines(adjacency)
    checks = {}

    incidence = np.zeros((40, 40), dtype=np.int64)
    for row, line in enumerate(lines):
        for p in line:
            incidence[row, p] = 1

    address = saturated_kernel(incidence)
    route = generic_saturated_kernel(incidence.T)
    code_p = orthogonal_complement(address)  # rank 25 in point space
    code_l = orthogonal_complement(route)  # rank 25 in line space
    checks["ranks_25"] = code_p.shape == (40, 25) and code_l.shape == (40, 25)

    # 1. unimodular cut: N Z^40 saturated and equal to code_L
    # N Z^40 has rank 25; a basis: N applied to any 40 columns, reduced.
    # saturation test: solve code_l coords for N e_i and confirm the
    # integral span equals code_l via SNF of the coordinate matrix
    mat_cl = Matrix(code_l.tolist())
    gram_cl = mat_cl.T * mat_cl
    coords = gram_cl.solve(mat_cl.T * Matrix(incidence.tolist()))
    checks["image_inside_code_l"] = mat_cl * coords == Matrix(incidence.tolist())
    coord_matrix = np.array(
        [[int(coords[i, j]) for j in range(40)] for i in range(25)],
        dtype=np.int64,
    )
    smith_img = smith_normal_form(Matrix(coord_matrix.tolist()), domain=ZZ)
    img_invariants = [abs(int(smith_img[i, i])) for i in range(min(25, 40))]
    nonzero_img_invariants = [v for v in img_invariants if v]
    checks["N_image_saturated"] = (
        len(nonzero_img_invariants) == 25
        and all(v == 1 for v in nonzero_img_invariants)
    )

    # 2. negation laws
    gram_addr = np.array(address.T @ address, dtype=np.int64)
    gram_route = np.array(route.T @ route, dtype=np.int64)
    gram_cp = np.array(code_p.T @ code_p, dtype=np.int64)
    gram_clat = np.array(code_l.T @ code_l, dtype=np.int64)

    q_addr = z8_block_q(gram_addr)
    q_route = z8_block_q(gram_route)
    q_cp = z8_block_q(gram_cp)
    q_cl = z8_block_q(gram_clat)

    # Exhaust every order-eight element, rather than extrapolating from one
    # Smith generator.  Odd-unit rescaling and mixing with lower-order
    # components are both included in the complete distributions below.
    dist_addr, count_addr, exact_addr = order8_q_distribution(gram_addr)
    dist_route, count_route, exact_route = order8_q_distribution(gram_route)
    dist_cp, count_cp, exact_cp = order8_q_distribution(gram_cp)
    dist_cl, count_cl, exact_cl = order8_q_distribution(gram_clat)
    expected_large_dark = {3: 32768, 11: 32768}
    expected_small_dark = {3: 512, 11: 512}
    expected_large_code = {5: 32768, 13: 32768}
    expected_small_code = {5: 512, 13: 512}
    checks["all_order8_elements_enumerated"] = (
        exact_addr
        and exact_route
        and exact_cp
        and exact_cl
        and (count_addr, count_route, count_cp, count_cl)
        == (65536, 1024, 65536, 1024)
    )
    checks["dark_order8_distribution_exact"] = (
        dist_addr == expected_large_dark and dist_route == expected_small_dark
    )
    checks["code_order8_distribution_exact"] = (
        dist_cp == expected_large_code and dist_cl == expected_small_code
    )
    checks["order8_orbits_are_negatives_mod16"] = (
        set(dist_cp) == {(-value) % 16 for value in dist_addr}
        and set(dist_cl) == {(-value) % 16 for value in dist_route}
    )

    phase_cp, det_cp = milgram_phase(gram_cp, checks, "codeP")
    phase_cl, det_cl = milgram_phase(gram_clat, checks, "codeL")
    checks["code_signatures_1_mod_8"] = phase_cp == 1 and phase_cl == 1
    checks["det_duality"] = det_cp == 2**17 * 3**10 and det_cl == 2**11 * 3**14

    # 3. the transport annihilator on code_P
    checks["incidence_square_identity"] = bool(
        (
            incidence.T @ incidence
            == 4 * np.eye(40, dtype=np.int64) + adjacency
        ).all()
    )
    annihilator = (adjacency - 2 * np.eye(40, dtype=np.int64)) @ (
        adjacency - 12 * np.eye(40, dtype=np.int64)
    )
    checks["transport_annihilator"] = bool((annihilator @ code_p == 0).all())

    # 4. the exact sequence 0 -> code_P -> code_L -> D(L_addr) -> 0
    n_codep = incidence @ code_p  # 40 x 25, columns in code_L
    coords2 = gram_cl.solve(mat_cl.T * Matrix(n_codep.tolist()))
    checks["N_codeP_inside_codeL"] = mat_cl * coords2 == Matrix(n_codep.tolist())
    inclusion = np.array(
        [[int(coords2[i, j]) for j in range(25)] for i in range(25)],
        dtype=np.int64,
    )
    index = abs(int(Matrix(inclusion.tolist()).det()))
    checks["index_is_det_address"] = index == 2**17 * 3**10

    smith_inc = smith_normal_form(Matrix(inclusion.tolist()), domain=ZZ)
    quotient_invariants = sorted(
        abs(int(smith_inc[i, i])) for i in range(25) if abs(int(smith_inc[i, i])) > 1
    )
    address_smith = sorted(
        abs(int(v))
        for v in np.diag(
            np.array(
                smith_normal_form(
                    Matrix((address.T @ address).tolist()), domain=ZZ
                ).tolist(),
                dtype=object,
            )
        ).tolist()
        if abs(int(v)) > 1
    )
    checks["cokernel_is_address_discriminant"] = (
        quotient_invariants == address_smith == sorted([2] * 5 + [6] * 9 + [24])
    )

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass183.incidence_square_ledger.v2",
        "status": "PASS" if all_pass else "FAIL",
        "ledger": {
            "selected_z8_generators": {
                "dark": {"address": q_addr, "route": q_route},
                "code": {"code_P": q_cp, "code_L": q_cl},
                "boundary": (
                    "these are representatives, not generator-invariant values"
                ),
            },
            "all_order8_q_numerators_mod16": {
                "address": {str(k): v for k, v in dist_addr.items()},
                "route": {str(k): v for k, v in dist_route.items()},
                "code_P": {str(k): v for k, v in dist_cp.items()},
                "code_L": {str(k): v for k, v in dist_cl.items()},
            },
            "negation": (
                "the complete dark orbit {3,11}/8 negates to the complete "
                "code orbit {5,13}/8 in Q/2Z"
            ),
            "code_signatures_mod_8": [int(phase_cp), int(phase_cl)],
            "milgram_boundary": (
                "discriminant enumeration is exact; eighth-root recognition "
                "is a floating numerical corroboration"
            ),
        },
        "mechanism": {
            "unimodular_cut": "SNF(N) = 1^25: N Z^40 = code_L exactly",
            "transport": (
                "(A-2I)(A-12I) annihilates code_P: N scales the Perron "
                "line by 4 and the gauge 24-sector by sqrt(6)"
            ),
            "exact_sequence": (
                "0 -> code_P --N--> code_L -> Q -> 0: index 2^17 3^10; "
                "Q and D(L_address) have invariant factors (2^5, 6^9, 24), "
                "hence are isomorphic as finite abelian groups"
            ),
            "reading": (
                "the full order-eight value distribution, not a selected "
                "generator, obeys dark/code negation on each unimodular "
                "side.  The incidence bridge identifies the intervening "
                "cokernel only as a finite abelian group; compatibility with "
                "the discriminant quadratic form remains open"
            ),
        },
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
