"""Check modular statistics for the equal-flux winding BF band."""

import json
from math import asin, ceil, floor, fsum, log, pi, sqrt
from pathlib import Path

from toe_20261116_circle_bundle_ring_winding_lattice import lower_mass, winding_census


def depth_interval(depth):
    """Eigenvalue interval with squared BF depth greater than depth**2."""
    midpoint = 6-depth**2
    half_width = 2*sqrt(9-4*depth**2)
    return midpoint-half_width, midpoint+half_width


def conditional_deepest_tail(depth):
    """Small-flux conditional probability that some winding pair exceeds depth."""
    if depth == 0:
        return 1.0, 1
    if depth == 1.5:
        return 0.0, None
    lower, upper = depth_interval(depth)
    first_overlap = ceil(1/(sqrt(upper/lower)-1))
    discrete = fsum(1/(j*j) for j in range(1, first_overlap))
    return ((upper-lower)*discrete + upper/first_overlap**2)/12, first_overlap


def direct_depth_grid(depths, grid_size=24000):
    """Integrate on uniform inverse normalized height using the actual masses."""
    counts = [0] * len(depths)
    for i in range(grid_size):
        inverse_height = (i+0.5)/grid_size
        largest_depth_sq = max(
            -4-lower_mass(12*j*j*inverse_height)
            for j in range(1, floor(1/sqrt(inverse_height))+1)
        )
        for index, depth in enumerate(depths):
            counts[index] += largest_depth_sq > depth**2
    return [count/grid_size for count in counts]


def count_controls():
    rows = []
    for n, n0 in ((1, 4), (1, 2), (3, 4), (2, 1), (6, 1)):
        radius_squared = 4*n/(pi*n0)
        for y in (0.91, 1.2, 2.3, 7.3, 51.8, 109.7):
            tau = complex(0.47, y)
            assert abs(tau) >= 1
            result = winding_census(n, n0, tau)
            count = result["number_of_unstable_nonzero_Fourier_labels"]
            if radius_squared <= 1 or y >= max(1, radius_squared):
                expected = 2*(ceil(sqrt(radius_squared*y))-1)
                assert count == expected
            rows.append({"flux_ratio": f"{n}/{n0}", "tau": [tau.real, tau.imag],
                         "signed_labels": count, "one_line_formula_checked":
                         radius_squared <= 1 or y >= max(1, radius_squared)})
    return rows


def moment_controls():
    # Conditional on at least one unstable mode, the small-flux law depends
    # only on integer squares. Verify the logarithmic second-moment slope.
    def conditional_second_partial(limit):
        return fsum(4*(1-(j/(j+1))**2) for j in range(1, limit+1))

    for limit in (1000, 4000):
        subtotal = conditional_second_partial(limit)
        assert abs(subtotal-8*log(limit)) < 10
    measured_slope = (conditional_second_partial(40000)-conditional_second_partial(4000))/log(10)
    assert abs(measured_slope-8) < 0.002
    return {"conditional_probability_of_exactly_one_opposite_pair": 0.75,
            "conditional_mean_signed_count": pi*pi/3,
            "conditional_truncated_second_moment_slope": measured_slope}


def nonempty_measure_controls():
    rows = []
    for radius_squared in (0.25, 0.7, 1.0, 1.03, 1.1, 2/sqrt(3), 2.0):
        edge = min(0.5, sqrt(max(0, 1-1/radius_squared**2)))
        exact = (3/pi)*(2*asin(edge)+(1-2*edge)*radius_squared)
        steps = 12000
        numeric = (3/pi)*fsum(min(radius_squared, 1/sqrt(1-((i+0.5)/steps-0.5)**2))
                                for i in range(steps))/steps
        assert abs(exact-numeric) < 1e-8
        rows.append({"R": radius_squared, "measure_with_at_least_one_unstable_mode": exact})
    return rows


def main():
    depths = (0.0, 0.3, 0.7, 1.1, 1.35, 1.45, 1.49, 1.5)
    exact_rows = []
    for depth, observed in zip(depths, direct_depth_grid(depths)):
        exact, first_overlap = conditional_deepest_tail(depth)
        assert abs(exact-observed) < 0.003, (depth, exact, observed)
        lo, hi = depth_interval(depth)
        assert abs((hi-lo)-4*sqrt(9-4*depth**2)) < 1e-12
        exact_rows.append({"depth": depth, "lambda_interval": [lo, hi],
                           "first_overlapping_multiplier": first_overlap,
                           "conditional_probability": exact,
                           "grid_probability": observed})
    certificate = {"law": {"mean_for_any_flux_ratio": "4*N/N0",
                           "large_count_tail": "P(U>=2*j) = 3*R/(pi*j^2) for large j",
                           "small_flux_probability_at_least_one_mode": "3*R/pi",
                           "second_moment_log_coefficient_for_count_cap": "24*R/pi",
                           "R": "4*N/(pi*N0)"},
                   "mode_count_controls": count_controls(),
                   "nonempty_shape_measure": nonempty_measure_controls(),
                   "conditional_moment_controls": moment_controls(),
                   "conditional_deepest_mode": exact_rows}
    output = Path(__file__).resolve().parents[1] / "data" / "toe_20261116_winding_modular_statistics.json"
    output.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    print("Verified the winding modular tail, conditional depth law, and second-moment slope.")


if __name__ == "__main__":
    main()
