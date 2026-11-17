"""Scan SM-commuting endpoint signs against the E6 cubic and gauge currents."""

import json
from collections import Counter, defaultdict
from itertools import product

import sympy as sp
from sympy.polys.matrices import DomainMatrix

from toe_20261116_E6_full_cubic_SM_stabilizer import (
    cubic_derivation_rows, cubic_monomials,
)
from toe_20261116_E6_triplet_exchange_filter import source_tensors
from toe_20261116_E6_Yukawa_superpotential_flat import mass_hessian
from toe_20261117_E6_interval_R_index import certificate, left_reflections


BARYON3 = {-6: 0, -2: -1, -1: 1, 0: 0, 3: 0, 4: -1}


def even_gauge_currents(weights, reflection, light, rows, second_reflection=None):
    dimension = len(weights)
    blocks = defaultdict(list)
    for i, j in product(range(dimension), repeat=2):
        other_even = second_reflection is None or second_reflection[i] == second_reflection[j]
        if reflection[i] == reflection[j] and other_even:
            blocks[weights[i]-weights[j]].append((i, j))
    obstructions = {}
    total_dimension = 0
    for grade, pairs in sorted(blocks.items()):
        columns = {dimension*i+j: slot for slot, (i, j) in enumerate(pairs)}
        projected = []
        for row in rows:
            restricted = {columns[k]: sp.QQ(v) for k, v in row.items() if k in columns}
            if restricted:
                projected.append(restricted)
        matrix = DomainMatrix(dict(enumerate(projected)),
                              (len(projected), len(pairs)), sp.QQ)
        basis = matrix.nullspace().to_Matrix()
        if not basis.rows:
            continue
        total_dimension += basis.rows
        active = [
            (slot, i, j, BARYON3[weights[j]]-BARYON3[weights[i]])
            for slot, (i, j) in enumerate(pairs)
            if {i, j} <= light and any(basis[:, slot])
        ]
        if len({entry[-1] for entry in active}) <= 1:
            continue
        gram_inverse = (basis*basis.T).inv()
        projector = basis.T*gram_inverse*basis
        witness = next((
            {"current_indices": [[i, j], [k, ell]],
             "baryon_difference_times_three": b-c,
             "trace_projector_entry": str(projector[a, x])}
            for (a, i, j, b), (x, k, ell, c) in product(active, repeat=2)
            if b != c and projector[a, x]
        ), None)
        obstructions[grade] = {
            "baryon_charges_times_three": sorted({entry[-1] for entry in active}),
            "trace_metric_witness": witness,
        }
    return total_dimension, obstructions


def projected_sources(weights, reflection, up, down):
    assert reflection[0] == reflection[3]
    higgs_sign = reflection[0]
    # Intrinsic signs are fixed by the required sourced electroweak doublets.
    up = {i: terms for i, terms in up.items() if reflection[i] == higgs_sign}
    down = {i: terms for i, terms in down.items() if reflection[i] == higgs_sign}
    result = Counter()
    for i, j in product(up, down):
        if weights[i] != weights[j]:
            continue
        for (a, b, _), (c, d, _) in product(up[i], down[j]):
            if sum(BARYON3[weights[k]] for k in (a, b, c, d)):
                result[weights[i]] += 1
    return dict(sorted(result.items()))


def scan():
    weights, up, down = source_tensors()
    cubic = cubic_monomials()
    components, reflections = left_reflections(weights, cubic)
    rows = cubic_derivation_rows(cubic)
    mass = mass_hessian(1, 0)
    light = {i for i in range(len(weights)) if not any(mass[:, i])}
    out = []
    protected = []
    for reflection in reflections:
        dim, gauge = even_gauge_currents(weights, reflection, light, rows)
        chiral = projected_sources(weights, reflection, up, down)
        # Q=18, L=1, E^c=6, U^c=9. The parity identities follow from
        # the QQD, U^cE^cD, Q U^c H_u, and Q L D^c terms of the cubic.
        p_q, p_l, p_e, p_u = (reflection[i] for i in (18, 1, 6, 9))
        assert p_e == p_u and reflection[0] == p_q*p_u
        assert (-2 in chiral) == (-1 in gauge) == (p_l*p_u == 1)
        assert (2 in chiral) == (5 in gauge) == (p_q*p_e == 1)
        entry = {
            "odd_SM_blocks": [n for n, block in enumerate(components)
                              if reflection[block[0]] == -1],
            "Higgs_intrinsic_sign": reflection[0],
            "frame_parities": [reflection[7], reflection[8]],
            "boundary_lie_dimension": dim,
            "chiral_candidate_pairs_by_weight": chiral,
            "gauge_mixed_baryon_grades": gauge,
        }
        out.append(entry)
        if not gauge and not chiral:
            protected.append((entry["odd_SM_blocks"], reflection))
    assert [blocks for blocks, _ in protected] == [[0, 1, 2, 9], [0, 2, 3, 5, 6, 8]]
    assert all(entry["gauge_mixed_baryon_grades"] and entry["chiral_candidate_pairs_by_weight"]
               for entry in out if entry["odd_SM_blocks"] not in [p[0] for p in protected])
    first, second = (reflection for _, reflection in protected)
    matter_sign = tuple(x*y for x, y in zip(first, second, strict=True))
    assert all(sum(matter_sign[i] == -1 for i in term) % 2 == 0 for term in cubic)
    assert {i for i in light if matter_sign[i] == 1} == {7}
    assert matter_sign[8] == -1
    assert all(matter_sign[i] == 1 for i in set(up) | set(down))
    matter_dim, _ = even_gauge_currents(weights, matter_sign, light, rows)
    common_dim, _ = even_gauge_currents(weights, first, light, rows, second)
    assert matter_dim == 46 and common_dim == 22
    intervals = []
    for odd_blocks, reflection in protected:
        result = certificate(reflection, include_650=True)
        cases = result["independent_reflection_cases"]
        assert all(case["target_deficit_with_all_four_larger_bulk_representations"]
                   for case in cases)
        intervals.append({
            "right_odd_SM_blocks": odd_blocks,
            "neutral_octet_and_triplet_multiplicities": result[
                "neutral_octet_and_triplet_multiplicities"],
            "candidate_left_endpoints": cases,
        })
    return {
        "right_reflections": out,
        "protected_right_interval_spectra": intervals,
        "product_of_protected_reflections": {
            "adjoint_fixed_dimension": matter_dim,
            "common_adjoint_fixed_dimension_of_the_two_reflections": common_dim,
            "odd_27_coordinates": [i for i, sign in enumerate(matter_sign) if sign == -1],
            "even_light_coordinate": 7,
            "odd_frame_coordinate": 8,
        },
    }


if __name__ == "__main__":
    print(json.dumps(scan(), indent=2))
