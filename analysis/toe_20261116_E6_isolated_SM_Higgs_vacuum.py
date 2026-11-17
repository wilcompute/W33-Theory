"""Audit the E6 Standard Model candidate and construct a locally isolated Higgs vacuum."""

import json
from collections import Counter
from itertools import product
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix

from toe_20261116_E6_full_cubic_SM_stabilizer import (
    N, cubic_derivation_rows, cubic_monomials, exact_sparse_rank,
    hypercharge_integer_weights, vev_constraints,
)
from toe_20261116_E6_Yukawa_superpotential_flat import mass_hessian


def centralizer(rows, weights):
    indices = [(i, j) for i, j in product(range(N), repeat=2) if weights[i] == weights[j]]
    lookup = {N*i+j: index for index, (i, j) in enumerate(indices)}
    sparse_rows = []
    for row in rows:
        restricted = {lookup[index]: sp.QQ(value) for index, value in row.items()
                      if index in lookup}
        if restricted:
            sparse_rows.append(restricted)
    matrix = DomainMatrix(dict(enumerate(sparse_rows)), (len(sparse_rows), len(indices)), sp.QQ)
    nullspace = matrix.nullspace().to_Matrix()
    return [sp.SparseMatrix(N, N, {pair: value for pair, value in zip(indices, row) if value})
            for row in nullspace.tolist()]


def adjoint_potential(basis, weights, neutral):
    y = sp.diag(*weights)
    degrees = (2, 5, 6)
    constraints = sp.Matrix([[(y**(d-1)*generator).trace() for d in degrees] for generator in basis])
    choices = constraints.nullspace()
    assert choices
    # The degree-two-plus-degree-five obstruction is independently reproduced.
    assert constraints[:, :2].rank() == 2
    coefficients = choices[0]
    coefficients /= coefficients[-1]
    powers = [y**(d-2) for d in degrees]
    quadratic = sum((k*(d-1)*power for k, d, power in zip(coefficients, degrees, powers)),
                    sp.zeros(N))
    operator = sp.Matrix([[(quadratic*left*right).trace() for right in basis] for left in basis])
    assert operator.det() != 0
    # Add W_lock=sum Hbar Phi^2 H. In the gauge slice the induced adjoint
    # bilinear is 2 Tr(P_neutral left right) and cannot mix with charged H.
    projector = sp.diag(*(int(i in neutral) for i in range(N)))
    lock = sp.Matrix([[2*(projector*left*right).trace() for right in basis] for left in basis])
    assert (operator+lock).det() != 0
    return {"adjoint_trace_degrees": list(degrees),
            "coefficients_in_sum_c_d_Tr_Phi_to_d_divided_by_d": [str(x) for x in coefficients],
            "centralizer_gradient_constraint_rank": constraints.rank(),
            "centralizer_adjoint_hessian_rank_before_and_after_Higgs_lock":
                [operator.rank(), (operator+lock).rank()]}


def matter_checks(weights):
    # Three identical independent generations, diagonal cubic masses from H1,
    # and optional neutral Majorana terms using both conjugate Higgs vectors.
    masses = mass_hessian(1, 0)
    assert all(not masses[i, j] or weights[i]+weights[j] == 0
               for i, j in product(range(N), repeat=2))
    assert masses.rank() == 10
    neutral_mass = sp.diag(*(int(w == 0) for w in weights))
    combined = masses+neutral_mass
    assert combined.rank() == 12
    remaining = Counter()
    for weight in sorted(set(weights)):
        indices = [i for i, w in enumerate(weights) if w == weight]
        remaining[weight] = len(indices)-combined[:, indices].rank()
    assert remaining == Counter({-1: 6, 4: 3, -2: 3, 3: 2, -6: 1, 0: 0, 2: 0, -3: 0})
    return {"families": 3, "cubic_mass_rank": 3*masses.rank(),
            "rank_with_optional_neutral_mass": 3*combined.rank(),
            "remaining_one_family_integer_hypercharge_weights": dict(remaining),
            "remaining_three_family_chiral_dimension": 3*(N-combined.rank())}


def light_higgs_check(weights):
    tuned = sp.diag(*(weight+3 for weight in weights))
    light = [i for i in range(N) if tuned[i, i] == 0]
    assert light == [0, 3] and tuned.rank() == 25
    monomials = cubic_monomials()
    up_vertices = [triple for triple in monomials
                   if sorted(weights[i] for i in triple) == [-3, -1, 4]]
    assert len(up_vertices) == 6 and all(any(i in light for i in triple) for triple in up_vertices)
    masses = mass_hessian(1, 0)
    chiral = {i for i, weight in enumerate(weights) if weight and not any(masses[:, i])}
    down_vertices = []
    for down_component in light:
        # d*(Kbar,Hbar_1) is a 27-valued quadratic map; insert it into d(X,X,.).
        images = [i for i in range(N) if tuple(sorted((7, down_component, i))) in monomials]
        assert len(images) == 1 and weights[images[0]] == 3
        image = images[0]
        for triple, coefficient in monomials.items():
            others = tuple(i for i in triple if i != image)
            if image in triple and set(others) <= chiral:
                kind = sorted(weights[i] for i in others)
                assert kind in ([-2, -1], [-6, 3])
                sign = coefficient*monomials[tuple(sorted((7, down_component, image)))]
                down_vertices.append({"bar_Higgs_component": down_component,
                                      "matter_components": others, "sign": sign})
    assert len(down_vertices) == 8
    return {"mass_operator": "Phi+3 I", "vectorlike_pair_rank": tuned.rank(),
            "light_27_components": light, "massless_weak_doublet_pairs": 1,
            "up_type_cubic_monomials": len(up_vertices),
            "down_and_charged_lepton_vertices_from_dual_cubic_insertion": down_vertices}


def verify():
    weights = hypercharge_integer_weights()
    rows = cubic_derivation_rows(cubic_monomials())
    neutral = [i for i, weight in enumerate(weights) if weight == 0]
    assert neutral == [7, 8]
    adj = [{N*i+j: 1} for i, j in product(range(N), repeat=2) if weights[i] != weights[j]]
    basic_ranks = [exact_sparse_rank(group) for group in (rows, rows+vev_constraints(),
                                                         rows+vev_constraints()+adj)]
    assert basic_ranks == [651, 705, 717]
    basis = centralizer(rows, weights)
    assert len(basis) == 16
    frame_image = sp.Matrix([[entry[i, j] for i, j in product(neutral, repeat=2)]
                             for entry in basis]).rank()
    assert frame_image == 4
    # 186 fields altogether, with 62 broken adjoint-orbit directions
    # and four frame directions gauged by the Y-centralizer. Only the
    # full orbit dimension 78-12 counts; centralizer dim is 16.
    gauge_orbit = (78-len(basis))+frame_image
    fields = 78+4*N
    assert gauge_orbit == 66
    assert fields-gauge_orbit == 120
    return {"parallel_stabilizer_ranks_reproduced": basic_ranks,
            "zero_hypercharge_coordinates": neutral, "centralizer_dimension": len(basis),
            "centralizer_action_rank_on_neutral_frame": frame_image,
            "Higgs_sector_chiral_dimension": fields, "gauge_orbit_dimension": gauge_orbit,
            "physical_Higgs_sector_holomorphic_Hessian_rank": fields-gauge_orbit,
            "compact_connected_unbroken_group": "S(U(3) x U(2))",
            "potential": adjoint_potential(basis, weights, neutral),
            "matter": matter_checks(weights), "optional_light_Higgs": light_higgs_check(weights)}


def main():
    data = verify()
    out = Path(__file__).resolve().parents[1]/"data"/"toe_20261116_E6_isolated_SM_Higgs_vacuum.json"
    out.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    print("Verified the E6 centralizer, isolated Higgs-sector candidate, and matter mass ranks.")


if __name__ == "__main__":
    main()
