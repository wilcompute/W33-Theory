"""Check hypercharge reflection and boundary proton-decay operators in the E6 cubic."""

import json
from collections import Counter, defaultdict
from itertools import product

import sympy as sp
from sympy.polys.matrices import DomainMatrix

from toe_20261116_E6_full_cubic_SM_stabilizer import (
    cubic_derivation_rows, cubic_monomials,
)
from toe_20261116_E6_triplet_exchange_filter import source_tensors


def adjoint_grades(weights, invariant):
    columns = defaultdict(list)
    for i, j in product(range(len(weights)), repeat=2):
        columns[weights[i] - weights[j]].append(len(weights)*i + j)
    rows = list(cubic_derivation_rows(invariant))
    grades = {}
    for grade, indices in sorted(columns.items()):
        lookup = {index: position for position, index in enumerate(indices)}
        projected = []
        for row in rows:
            restricted = {lookup[k]: sp.QQ(v) for k, v in row.items() if k in lookup}
            if restricted:
                projected.append(restricted)
        matrix = DomainMatrix(dict(enumerate(projected)), (len(projected), len(indices)), sp.QQ)
        if (dimension := len(indices) - matrix.rank()):
            grades[grade] = dimension
    return grades


def boundary_selection():
    weights, up, down = source_tensors()
    invariant = cubic_monomials()
    assert all(sum(weights[i] for i in triple) == 0 for triple in invariant)
    assert weights[7] == weights[8] == 0
    grades = adjoint_grades(weights, invariant)
    even_dimension = sum(dim for grade, dim in grades.items() if grade % 2 == 0)
    assert sum(grades.values()) == 78 and even_dimension == 38
    assert Counter(w % 2 for w in weights) == {0: 15, 1: 12}
    assert grades[5] == 6

    # Add weight-zero singlets with baryon number zero, so the current test
    # includes them whether the neutral-sector lifting is imposed or omitted.
    baryon = {-6: 0, -2: -1, -1: 1, 0: 0, 3: 0, 4: -1}
    currents = defaultdict(set)
    for row, column in product(baryon, repeat=2):
        if (grade := row - column) in grades:
            currents[grade].add(baryon[column] - baryon[row])
    assert all(len(values) == 1 for grade, values in currents.items() if grade % 2 == 0)
    assert len(currents[5]) > 1

    assert {i for i in up if weights[i] == -3} == {0, 3}
    assert {i for i in down if weights[i] == -3} == {0, 3}
    # A boundary singlet formed by contracting the two chiral sources over
    # the even subspace is allowed without an explicit propagating triplet.
    contacts = Counter()
    for i in set(up) & set(down):
        if weights[i] % 2 == 0:
            for (a, b, s), (c, d, t) in product(up[i], down[i]):
                contacts[a, b, c, d] += s*t
    witnesses = {term: value for term, value in contacts.items()
                 if value and sum(baryon[weights[i]] for i in term)}
    assert {tuple(sorted(weights[i] for i in term)) for term in witnesses} == {
        (-1, -1, -1, 3), (-6, -2, 4, 4),
    }
    assert witnesses[(21, 25, 1, 18)] == 1
    assert witnesses[(6, 9, 10, 17)] == -1
    return {
        "adjoint_grade_dimensions": grades,
        "adjoint_reflection_dimensions": [even_dimension, 78-even_dimension],
        "fundamental_reflection_dimensions": [15, 12],
        "even_grade_current_baryon_charges_times_three": {
            grade: sorted(values) for grade, values in sorted(currents.items()) if grade % 2 == 0
        },
        "baryon_violating_even_boundary_contact_slots": len(witnesses),
        "boundary_contact_witnesses": [
            {"indices": list(term), "coefficient": witnesses[term]}
            for term in [(21, 25, 1, 18), (6, 9, 10, 17)]
        ],
    }


def green_functions():
    length, mass, y, z, displacement = sp.symbols("L m y z delta", positive=True)
    # y <= z. At equal points its derivative from the other side has jump -1.
    green = sp.cosh(mass*y)*sp.sinh(mass*(length-z))/(mass*sp.cosh(mass*length))
    assert sp.diff(green, y).subs(y, 0) == 0
    assert green.subs(z, length) == 0
    jump = (sp.diff(green, z)-sp.diff(green, y)).subs(z, y)
    assert sp.expand_trig(sp.simplify(jump)) == -1
    diagonal = green.subs({y: length-displacement, z: length-displacement})
    assert diagonal.subs(displacement, 0) == 0
    assert sp.simplify(sp.diff(diagonal, displacement).subs(displacement, 0)) == 1
    assert sp.limit(diagonal, mass, 0) == displacement

    # Antiperiodic circle: coincident Green function from its image sum.
    q = sp.exp(-mass*length)
    circle = (1 - 2*q/(1+q))/(2*mass)
    assert sp.limit(circle, mass, 0) == length/4
    # The finite ND derivative subtraction follows from G(0,0).
    assert sp.simplify(-mass**2*green.subs({y: 0, z: 0})) == -mass*sp.tanh(mass*length)
    return {
        "interval_ND_G_at_delta_from_boundary": str(diagonal),
        "massless_interval_ND_G_at_delta_from_boundary": "delta",
        "derivative_exchange_massless_N_modes": "2*N/L",
        "derivative_exchange_finite_mass_subtraction_as_N_grows": "-m*tanh(m*L)",
        "massless_antiperiodic_circle_coincident_G": "L/4",
    }


def abelian_charge_constraint():
    # Any allowed constant spectator mass and the two allowed Yukawa
    # vertices imply the same charge for the contact and superpotential.
    up, down, higgs, conjugate, superpotential = sp.symbols("u d h hbar W")
    vertices = [up+higgs-superpotential, down+conjugate-superpotential]
    mass = higgs+conjugate-superpotential
    assert sp.expand(sum(vertices)-mass) == up+down-superpotential
    r_matter, r_higgs, r_partner, r_w = 1, 0, 2, 2
    assert (2*r_matter+r_higgs-r_w) % 4 == 0
    assert (r_higgs+r_partner-r_w) % 4 == 0
    assert (4*r_matter+r_higgs-r_w) % 4 != 0
    return {
        "allowed_constant_direct_mass_forces_abelian_allowed_contact": True,
        "Z4R_charges_W_X_H_partner": [r_w, r_matter, r_higgs, r_partner],
        "Z4R_forbids_contact_and_direct_H_Hbar_mass": True,
    }


if __name__ == "__main__":
    print(json.dumps({
        "E6": boundary_selection(),
        "propagators": green_functions(),
        "charges": abelian_charge_constraint(),
    }, indent=2))
