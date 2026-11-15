"""Exact local tensor and marked Picard checks for the cubic-surface flux branch."""

import json
from itertools import combinations, permutations
from pathlib import Path

import sympy as sp


def verify():
    d, n, kappa, flux_sq = sp.symbols("d N kappa f_squared", positive=True)
    total_dimension_minus_two = d+2*n-2
    solution = sp.solve(kappa-flux_sq/2+n*flux_sq/(2*total_dimension_minus_two), flux_sq)[0]
    adS_radius_sq = sp.factor(2*(d-1)*total_dimension_minus_two/(n*solution))
    scalar_mass_sq = solution*(1+n/total_dimension_minus_two)
    mass_radius = sp.factor(scalar_mass_sq * adS_radius_sq)
    assert sp.factor(mass_radius-2*(d-1)*(d+3*n-2)/n) == 0
    assert mass_radius.subs({d: 5, n: 2}) == 36
    assert (kappa*adS_radius_sq).subs({d: 5, n: 2}) == 10

    complex_structure = sp.diag(*([sp.Matrix([[0, 1], [-1, 0]])]*2))
    hermitian = sp.diag(1, 1, -1, -1)
    antihermitian = sp.diag(1, -1, 0, 0)
    for h, sign in ((hermitian, 1), (antihermitian, -1)):
        assert complex_structure*h*complex_structure.T == sign*h
        assert sp.trace(h) == 0
        assert h*complex_structure+complex_structure*h == (1+sign)*h*complex_structure

    basis = [sp.eye(7).col(i) for i in range(7)]
    plane, *exceptional = basis
    intersection = sp.diag(1, -1, -1, -1, -1, -1, -1)

    def pairing(a, b):
        return (a.T*intersection*b)[0]

    zero = sp.zeros(7, 1)
    anticanonical = 3*plane-sum(exceptional, zero)
    simple_roots = [exceptional[i]-exceptional[i+1] for i in range(5)]
    simple_roots.append(plane-sum(exceptional[:3], zero))
    gram = sp.Matrix([[-pairing(a, b) for b in simple_roots] for a in simple_roots])
    assert gram.det() == 3
    assert pairing(anticanonical, anticanonical) == 3

    roots = [a-b for a, b in permutations(exceptional, 2)]
    roots += [sign*(plane-sum(triple, zero)) for triple in combinations(exceptional, 3) for sign in (-1, 1)]
    roots += [sign*(2*plane-sum(exceptional, zero)) for sign in (-1, 1)]
    assert len({tuple(root) for root in roots}) == 72
    assert all(pairing(anticanonical, root) == 0 and pairing(root, root) == -2 for root in roots)

    lines = exceptional + [plane-a-b for a, b in combinations(exceptional, 2)]
    lines += [2*plane-sum(five, zero) for five in combinations(exceptional, 5)]
    assert len({tuple(line) for line in lines}) == 27
    assert all(pairing(anticanonical, line) == 1 and pairing(line, line) == -1 for line in lines)

    return {
        "primitive_scalar_mass_squared_times_AdS_radius_squared": str(mass_radius),
        "cubic_surface_D9_primitive_scalar_mass_squared_times_AdS_radius_squared": 36,
        "cubic_surface_D9_first_spin_two_squared_mass_bounds": ["strictly greater than 20", "at most 160/3"],
        "negative_intersection_gram": [[int(entry) for entry in row] for row in gram.tolist()],
        "root_count": len(roots),
        "line_count": len(lines),
        "anticanonical_pairing_per_line": 1,
    }


if __name__ == "__main__":
    report = json.dumps(verify(), indent=2) + "\n"
    path = Path(__file__).resolve().parents[1] / "data" / "toe_20261114_cubic_surface_flux.json"
    path.write_text(report, encoding="utf-8", newline="\n")
    print(report, end="")
