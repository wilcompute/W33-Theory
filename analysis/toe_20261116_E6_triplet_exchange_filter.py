"""Resolve and remove tree-level color-triplet exchange in the E6 candidate."""

import json
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix

from toe_20261116_E6_full_cubic_SM_stabilizer import (
    cubic_derivation_rows, cubic_monomials, hypercharge_integer_weights,
)
from toe_20261116_E6_Yukawa_superpotential_flat import mass_hessian
from toe_20261116_E6_adjoint_Yukawa_maps import light_vertices


def source_tensors():
    weights = hypercharge_integer_weights()
    invariant = cubic_monomials()
    matter_mass = mass_hessian(1, 0)
    light = {i for i, charge in enumerate(weights) if charge and not any(matter_mass[:, i])}
    up = defaultdict(list)
    for triple, sign in invariant.items():
        for higgs in triple:
            pair = tuple(i for i in triple if i != higgs)
            if set(pair) <= light:
                up[higgs].append((*pair, sign))
    down = defaultdict(list)
    for higgs, image in product(range(len(weights)), repeat=2):
        dual_sign = invariant.get(tuple(sorted((7, higgs, image))), 0)
        if dual_sign:
            down[higgs].extend((i, j, dual_sign*sign) for i, j, sign in up[image])
    return weights, up, down


def exchange_certificate():
    w, up, down = source_tensors()
    # Baryon number from the light 27 weight assignment on the chosen branch.
    baryon = {-6: 0, -2: -1, -1: 1, 3: 0, 4: -1}  # Three times B.
    active = sorted(set(up) & set(down))
    assert sorted(i for i in active if w[i] == -3) == [0, 3]
    baseline = defaultdict(lambda: sp.S.Zero)
    filtered = defaultdict(lambda: sp.S.Zero)
    witnesses = {}
    # Distinct family blocks are retained on the two bilinear sources.
    # Flavor insertions on matter legs only rescale these same supports.
    for h in active:
        mass = w[h]+3
        if mass == 0:
            continue
        factor = sp.Rational(w[h]**2-4, 5)
        for (i, j, sign1), (k, ell, sign2) in product(up[h], down[h]):
            term = (i, j, k, ell)
            coefficient = sp.Rational(-sign1*sign2, mass)
            baseline[term] += coefficient
            filtered[term] += factor*coefficient
            if sum(baryon[w[index]] for index in term):
                witnesses.setdefault(w[h], set()).add(term)
    assert set(witnesses) == {-2, 2}
    violation = {
        term: value for term, value in baseline.items()
        if value and sum(baryon[w[index]] for index in term)
    }
    survive = [term for term, value in filtered.items()
               if value and sum(baryon[w[index]] for index in term)]
    assert not survive
    assert violation[(21, 25, 1, 18)] == -sp.Rational(1, 5)
    assert violation[(6, 9, 10, 17)] == sp.Rational(1, 5)
    assert violation[(1, 18, 21, 25)] == -1
    categories = Counter(tuple(sorted(w[i] for i in term)) for term in violation)
    assert set(categories) == {(-1, -1, -1, 3), (-6, -2, 4, 4)}
    assert sp.Rational((-3)**2-4, 5) == 1
    # No affine function of the Higgs-leg charge kills both signed blocks
    # and retains the light up-type doublet.
    x, y = sp.symbols("x y")
    assert not sp.solve([x+2*y, x-2*y, x-3*y-1], (x, y))
    up_vertices, down_vertices = light_vertices()[1:]
    return {"massive_exchange_support_by_integer_weight":
                dict(Counter(w[i] for i in active if w[i]+3)),
            "baryon_violating_exchange_weights": sorted(witnesses),
            "witnesses_with_family_blocks_preserved": [
                {"kind": "QQQL", "component_indices": [21, 25, 1, 18], "coefficient": "-1/5"},
                {"kind": "U^c U^c D^c E^c", "component_indices": [6, 9, 10, 17],
                 "coefficient": "1/5"},
                {"kind": "QQQL, opposite triplet B-L block",
                 "component_indices": [1, 18, 21, 25], "coefficient": "-1"},
            ],
            "nonzero_baryon_violating_terms_before_filter": len(violation),
            "nonzero_baryon_violating_terms_after_filter": len(survive),
            "minimal_higgs_leg_polynomial_degree_in_this_construction": 2,
            "unchanged_light_yukawa_index_vertices": [len(up_vertices), len(down_vertices)]}


def heavy_field_matching():
    # A charged H/Hbar pair in a gauge slice has an off-diagonal mass.
    mass, source_h, source_bar = sp.symbols("m J_H J_bar", nonzero=True)
    h, hbar = sp.symbols("H Hbar")
    w = mass*h*hbar+source_h*h+source_bar*hbar
    values = sp.solve([sp.diff(w, h), sp.diff(w, hbar)], (h, hbar))
    assert sp.simplify(w.subs(values)+source_h*source_bar/mass) == 0
    assert sp.simplify(w.subs(values).subs(source_bar, 0)) == 0
    # Tree lift of the polynomial on the spectator K leg.
    phi, k, p, q = sp.symbols("Phi K P Q")
    pb, qb = sp.symbols("Pbar Qbar")
    completion = pb*(p-phi*k)+qb*(q-phi*p)+source_h*(q-4*k)/5
    values = sp.solve([sp.diff(completion, pb), sp.diff(completion, qb)], (p, q))
    assert sp.expand(completion.subs(values)-source_h*k*(phi**2-4)/5) == 0
    return {"H_pair_exchange_requires_sources_on_both_chiral_legs": True,
            "renormalizable_filter_messengers": "two vectorlike 27 pairs",
            "effective_up_Higgs_leg_filter": "(Phi^2-4 I)/5"}


def original_gauge_exchange():
    weights = hypercharge_integer_weights()
    indices = [(i, j) for i, j in product(range(len(weights)), repeat=2)
               if weights[i]-weights[j] == 5]
    lookup = {len(weights)*i+j: n for n, (i, j) in enumerate(indices)}
    rows = []
    for full_row in cubic_derivation_rows(cubic_monomials()):
        row = {lookup[k]: sp.QQ(v) for k, v in full_row.items() if k in lookup}
        if row:
            rows.append(row)
    matrix = DomainMatrix(dict(enumerate(rows)), (len(rows), len(indices)), sp.QQ)
    basis = matrix.nullspace().to_Matrix()
    assert basis.rows == 6
    # All six charged generators preserve the stabilizing Higgs frame.
    assert all(not basis[:, n].norm() for n, pair in enumerate(indices) if {7, 8}.intersection(pair))
    # In a Hermitian-normalized kinetic metric the inverse Gram projects
    # onto this complete charged block. Find an explicit nonzero pair of
    # light gauge currents of type Q^dagger e^c and (u^c)^dagger Q.
    gram = basis*basis.T
    projector = basis.T*gram.inv()*basis
    mass = mass_hessian(1, 0)
    light = {i for i, w in enumerate(weights) if w and not any(mass[:, i])}
    witness = None
    for a, (i, j) in enumerate(indices):
        if (weights[i], weights[j]) != (-1, -6) or not {i, j} <= light:
            continue
        for b, (k, ell) in enumerate(indices):
            if ((weights[k], weights[ell]) == (4, -1) and {k, ell} <= light
                    and projector[a, b]):
                witness = {"current_1": [i, j], "current_2_before_conjugation": [k, ell],
                           "trace_metric_projector_coefficient": str(projector[a, b])}
                break
        if witness:
            break
    assert witness
    return {"complex_dimension_of_positive_charge_five_gauge_block": basis.rows,
            "adjoint_mass_squared_over_gauge_coupling_squared_and_vev_squared": 25,
            "nonzero_baryon_violating_gauge_current_product": witness}


def main():
    data = {"tree_exchange": exchange_certificate(), "heavy_field_checks": heavy_field_matching(),
            "gauge_exchange": original_gauge_exchange()}
    output = Path(__file__).resolve().parents[1]/"data"/"toe_20261116_E6_triplet_exchange_filter.json"
    output.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    print("Verified the E6 triplet exchange and its baryon-violating tree-level filter.")


if __name__ == "__main__":
    main()
