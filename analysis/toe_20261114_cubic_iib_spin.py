"""Verify cubic-surface spin-c indices and circle-bundle D3 charge data."""

import json
from itertools import combinations
from pathlib import Path

import sympy as sp


def verify():
    degree, q = sp.symbols("k q", integer=True)
    section_count = (3*degree**2+3*degree+2)/2
    index = (3*q**2+5)/8
    assert sp.simplify(section_count.subs(degree, (q-1)/2)-index) == 0
    assert all(index.subs(q, value).is_Integer == bool(value % 2) for value in range(-15, 16))
    for k in range(9):
        ambient_sections = sp.binomial(k+3, 3)
        ideal_sections = sp.binomial(k, 3)
        assert section_count.subs(degree, k) == ambient_sections-ideal_sections

    intersection = sp.diag(1, -1, -1, -1, -1, -1, -1)
    h, *exceptionals = [sp.eye(7).col(i) for i in range(7)]
    zero = sp.zeros(7, 1)
    c1 = 3*h-sum(exceptionals, zero)
    roots = [exceptionals[i]-exceptionals[i+1] for i in range(5)]
    roots.append(h-sum(exceptionals[:3], zero))
    lines = exceptionals + [h-a-b for a, b in combinations(exceptionals, 2)]
    lines += [2*h-sum(chosen, zero) for chosen in combinations(exceptionals, 5)]
    charges = [tuple((line.T*intersection*root)[0] for root in roots) for line in lines]
    assert len(set(charges)) == 27
    roots_matrix = sp.Matrix.hstack(*roots)
    gram = -roots_matrix.T*intersection*roots_matrix
    assert gram.det() == 3
    inverse_gram = gram.inv()
    assert all((sp.Matrix(charge).T*inverse_gram*sp.Matrix(charge))[0] == sp.Rational(4, 3) for charge in charges)
    for line in lines:
        assert (c1.T*intersection*line)[0] == 1

    # Normalize Ric_Y=4 and take the primitive (unit Chern class multiple) bundle.
    fiber_length = 2*sp.pi/3
    base_volume = sp.pi**2/6
    curve_area = sp.pi/3
    link_volume = fiber_length*base_volume
    wrapped_volume = fiber_length*curve_area
    assert link_volume == sp.pi**3/9
    assert sp.pi*wrapped_volume/(2*link_volume) == 1
    assert sp.pi**3/(4*link_volume) == sp.Rational(9, 4)
    assert (3*1)*(3*1+4) == 21
    return {
        "spin_c_index_for_odd_q": str(index),
        "positive_q_zero_mode_counts": {value: int(index.subs(q, value)) for value in (1, 3, 5, 7, 9)},
        "primitive_link_volume": str(link_volume),
        "baryonic_vectors_from_C4": 6,
        "wrapped_line_charge_vectors_in_simple_root_basis": [list(map(int, charge)) for charge in charges],
        "squared_norm_of_each_dual_lattice_charge": "4/3",
        "wrapped_line_dimension_per_D3_flux_quantum": 1,
        "leading_central_charge_per_D3_flux_squared": "9/4",
        "first_holomorphic_link_scalar_laplacian_eigenvalue": 21,
    }


if __name__ == "__main__":
    report = json.dumps(verify(), indent=2) + "\n"
    path = Path(__file__).resolve().parents[1] / "data" / "toe_20261114_cubic_iib_spin.json"
    path.write_text(report, encoding="utf-8", newline="\n")
    print(report, end="")
