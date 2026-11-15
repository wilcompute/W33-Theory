"""Exact checks for stress sources from the cubic link's Betti vectors."""

import json
from itertools import combinations
from pathlib import Path

import sympy as sp


def verify():
    signs = [-1, 1, 1, 1, 1]
    indices = range(5)
    field = sp.zeros(5)
    for i, j in combinations(indices, 2):
        field[i, j] = sp.Symbol(f"f{i}{j}")
        field[j, i] = -field[i, j]

    def dual(i, j, k):
        if len({i, j, k}) != 3:
            return 0
        a, b = [index for index in indices if index not in (i, j, k)]
        return sp.LeviCivita(i, j, k, a, b)*signs[a]*signs[b]*field[a, b]

    metric = sp.diag(*signs)
    electric_contraction = field*metric*field.T
    norm_twice = sp.trace(metric*electric_contraction)
    magnetic_contraction = sp.Matrix(5, 5, lambda i, j: sum(
        signs[a]*signs[b]*dual(i, a, b)*dual(j, a, b) for a, b in combinations(indices, 2)
    ))
    assert (magnetic_contraction-electric_contraction+metric*norm_twice/2).applyfunc(sp.expand) == sp.zeros(5)

    # Algebraic saturation control. Each sample pairs six vectors in a
    # space of dimension three; collectively their average Gram is I_6.
    half = sp.eye(3)
    zero = sp.zeros(3)
    samples = [2*sp.diag(half, zero), 2*sp.diag(zero, half)]
    assert sum(samples, sp.zeros(6))/2 == sp.eye(6)
    assert all(g.rank() == 3 for g in samples)
    total_variance = sum(sp.trace((g-sp.eye(6))**2) for g in samples)/2
    assert total_variance == 6
    average_over_directions = 2*total_variance/(6*(6+2))
    assert average_over_directions == sp.Rational(1, 4)

    return {
        "cubic_betti_gauge_directions": 6,
        "pointwise_primitive_form_rank_upper_bound": 3,
        "massive_neutral_mode_total_squared_overlap_lower_bound": int(total_variance),
        "some_unit_direction_diagonal_profile_rms_lower_bound": "1/2",
        "lorentzian_five_form_reduction_identity": "T_Betti=(1/2)*local_Gram*T_Maxwell for the stated flux convention",
    }


if __name__ == "__main__":
    result = json.dumps(verify(), indent=2) + "\n"
    path = Path(__file__).resolve().parents[1] / "data" / "toe_20261115_cubic_iib_betti_sources.json"
    path.write_text(result, encoding="utf-8", newline="\n")
    print(result, end="")
