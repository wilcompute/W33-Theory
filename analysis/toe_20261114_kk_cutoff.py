"""Exact cutoff checks for the first two continuum spin-2 overlap sum rules."""

import json
from fractions import Fraction
from itertools import product
from pathlib import Path


def center(k, size):
    half_width = size // 2
    return (k + half_width) % size - half_width


def fourier_cutoff(size):
    half_width = size // 2
    external = range(-(half_width // 2), half_width // 2 + 1)
    square_defects = {
        k: 1 - Fraction(center(2 * k, size) ** 2, 4 * k * k)
        for k in range(1, half_width + 1)
    }
    exact_modes = [k for k, defect in square_defects.items() if defect == 0]
    assert exact_modes == list(range(1, half_width // 2 + 1))
    assert square_defects[half_width] == 1 - Fraction(1, 4 * half_width**2)

    mixed_tests = 0
    for a, b, c, d in product(external, repeat=4):
        if (a + b + c + d) % size:
            continue
        assert a + b + c + d == 0
        assert a * a + b * b + c * c + d * d == sum(
            center(a + k, size) ** 2 for k in (b, c, d)
        )
        mixed_tests += 1

    # A flat positive dispersion attains the worst-mode lower bound on odd grids.
    flat_defects = [
        1 - Fraction(int(center(2 * k, size) != 0), 4)
        for k in range(1, half_width + 1)
    ]
    assert set(flat_defects) == {Fraction(3, 4)}
    return {
        "mesh_size": size,
        "positive_external_modes_exact": exact_modes,
        "mixed_momentum_conserving_tuples_tested": mixed_tests,
        "spectral_edge_relative_defect": str(square_defects[half_width]),
        "flat_dispersion_relative_defect": str(max(flat_defects)),
    }


def sphere_product_cutoff(inv_radius_sq_a, inv_radius_sq_b):
    # f = 3xy; 3x^2 = 1 + 2 P_2(x), with E[P_2^2] = 1/5.
    one_sphere_overlap_weight = {0: Fraction(1), 2: Fraction(4, 5)}
    lam = 2 * (inv_radius_sq_a + inv_radius_sq_b)
    overlaps = {
        (a, b): weight_a * weight_b
        for a, weight_a in one_sphere_overlap_weight.items()
        for b, weight_b in one_sphere_overlap_weight.items()
    }
    exchange = {
        (a, b): weight * (a * (a + 1) * inv_radius_sq_a + b * (b + 1) * inv_radius_sq_b)
        for (a, b), weight in overlaps.items()
    }
    quartic = sum(overlaps.values())
    weighted = sum(exchange.values())
    assert quartic == Fraction(81, 25)
    assert 3 * weighted == 4 * lam * quartic
    omitted_quartic = overlaps[2, 2] / quartic
    omitted_weighted = exchange[2, 2] / weighted
    assert omitted_quartic == Fraction(16, 81)
    assert omitted_weighted == Fraction(4, 9)
    return {
        "inverse_squared_radii": [str(inv_radius_sq_a), str(inv_radius_sq_b)],
        "quartic_overlap": str(quartic),
        "weighted_exchange": str(weighted),
        "degree_sum_2_cutoff_missing_unweighted_fraction": str(omitted_quartic),
        "degree_sum_2_cutoff_missing_weighted_fraction": str(omitted_weighted),
    }


def main():
    report = {
        "fourier": [fourier_cutoff(size) for size in (5, 9, 17, 33, 65)],
        "sphere_product": [
            sphere_product_cutoff(Fraction(1), Fraction(1)),
            sphere_product_cutoff(Fraction(2, 3), Fraction(7, 5)),
        ],
    }
    output = json.dumps(report, indent=2) + "\n"
    path = Path(__file__).resolve().parents[1] / "data" / "toe_20261114_kk_cutoff.json"
    path.write_text(output, encoding="utf-8", newline="\n")
    print(output, end="")


if __name__ == "__main__":
    main()
