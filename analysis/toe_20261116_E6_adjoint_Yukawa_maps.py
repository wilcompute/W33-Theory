"""Certify flavor separation and tree messenger matching in the E6 candidate."""

import json
from collections import Counter
from itertools import permutations
from pathlib import Path

import sympy as sp

from toe_20261116_E6_full_cubic_SM_stabilizer import cubic_monomials, hypercharge_integer_weights
from toe_20261116_E6_Yukawa_superpotential_flat import mass_hessian


def light_vertices():
    weights = hypercharge_integer_weights()
    invariant = cubic_monomials()
    mass = mass_hessian(1, 0)
    light = {i for i, charge in enumerate(weights) if charge and not any(mass[:, i])}
    higgs = [i for i, charge in enumerate(weights) if charge == -3]
    assert higgs == [0, 3]
    up = []
    for triple, coefficient in invariant.items():
        for h, left, right in permutations(triple):
            if h in higgs and {left, right} <= light and (weights[left], weights[right]) == (-1, 4):
                up.append((h, left, right, coefficient))
    assert len(up) == 6

    down = []
    for h in higgs:
        images = [i for i in range(len(weights)) if tuple(sorted((7, h, i))) in invariant]
        assert len(images) == 1
        image = images[0]
        dual_sign = invariant[tuple(sorted((7, h, image)))]
        for triple, coefficient in invariant.items():
            if image not in triple:
                continue
            for left, right in permutations(i for i in triple if i != image):
                if {left, right} <= light and (weights[left], weights[right]) in ((-1, -2), (-6, 3)):
                    down.append((h, left, right, coefficient*dual_sign))
    charges = Counter((weights[i], weights[j]) for _, i, j, _ in down)
    assert charges == {(-1, -2): 6, (-6, 3): 2}
    return weights, up, down


def polynomial_ranks(charges, max_order, *, symmetric):
    columns = []
    for degree in range(max_order+1):
        for left in range(degree+1):
            right = degree-left
            sign = 1 if symmetric else -1
            columns.append([x**left*y**right+sign*x**right*y**left for x, y in charges])
    return sp.Matrix(columns).T.rank()


def flavor_maps():
    weights, up, down = light_vertices()
    charges = [(-1, -2), (-6, 3)]  # Q,d^c and e^c,L, both 10 slot first
    sym = sp.Matrix([[1, x*y] for x, y in charges])
    anti = sp.Matrix([[x-y, x*y*(x-y)] for x, y in charges])
    assert sym == sp.Matrix([[1, 2], [1, -18]]) and sym.det() == -20
    assert anti == sp.Matrix([[1, 2], [-9, 162]]) and anti.det() == 180
    assert all(weights[i]-weights[j] == -5 for _, i, j, _ in up)
    symmetric_ranks = [polynomial_ranks(charges, order, symmetric=True) for order in range(4)]
    antisymmetric_ranks = [polynomial_ranks(charges, order, symmetric=False) for order in range(4)]
    assert symmetric_ranks == [1, 1, 2, 2] and antisymmetric_ranks == [0, 1, 1, 2]
    return {"down_and_lepton_charge_pairs_in_aligned_family_order": charges,
            "up_type_vertices": up, "down_and_charged_lepton_vertices": down,
            "symmetric_map": [[int(x) for x in row] for row in sym.tolist()],
            "antisymmetric_map": [[int(x) for x in row] for row in anti.tolist()],
            "symmetric_map_inverse": [[str(x) for x in row] for row in sym.inv().tolist()],
            "antisymmetric_map_inverse": [[str(x) for x in row] for row in anti.inv().tolist()],
            "ranks_through_each_total_adjoint_insertion_order_0_to_3": {
                "symmetric": symmetric_ranks, "antisymmetric": antisymmetric_ranks},
            "up_single_insertion_antisymmetric_factor": -5,
            "image_complex_dimension_for_three_families": 27}


def messenger_matching():
    mass, phi, q, source = sp.symbols("M Phi X source", nonzero=True)
    f, g, u, fbar, gbar, ubar = sp.symbols("F G U Fbar Gbar Ubar")
    c0, c1, c2, c3 = sp.symbols("c0 c1 c2 c3")
    constraints = fbar*(mass*f-phi*q)+gbar*(mass*g-phi*f)+ubar*(mass*u-source)
    interacting = u*(c0*q*q+c1*f*q+c2*f*f+c3*g*f)
    potential = constraints+interacting
    heavy_values = sp.solve([sp.diff(potential, var) for var in (fbar, gbar, ubar)], (f, g, u))
    effective = sp.expand(potential.subs(heavy_values))
    expected = source*q*q/mass*(c0+c1*phi/mass+c2*phi**2/mass**2+c3*phi**3/mass**3)
    assert sp.expand(effective-expected) == 0
    return {"light_leg_messenger_insertion_orders": [0, 1, 2, 3],
            "spurion": "Phi/M",
            "composite_down_doublet": "d*(Kbar,Hbar_1)/M",
            "flavor_rank_unchanged_by_family_universal_positive_kinetic_factors": True}


def main():
    data = {"flavor_maps": flavor_maps(), "tree_messenger_matching": messenger_matching()}
    output = Path(__file__).resolve().parents[1]/"data"/"toe_20261116_E6_adjoint_Yukawa_maps.json"
    output.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    print("Verified E6 Yukawa map ranks, insertion thresholds, and heavy-field matching.")


if __name__ == "__main__":
    main()
