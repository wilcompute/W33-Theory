"""Check the five-dimensional geodesic, redshift, and radiation formulas."""

from collections import Counter
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
from itertools import combinations, product
from math import asinh, cosh, exp, fsum, log, pi, sqrt, tanh
from pathlib import Path
import json


def continued_fraction_checks():
    with localcontext() as ctx:
        ctx.prec = 70
        redshift_power = 1 / D(6).sqrt()
        critical_mu = 2 / (1 - redshift_power)
        peak_factor = ((1 + redshift_power)**((1 + redshift_power)/2)
                       * (1 - redshift_power)**((1 - redshift_power)/2) / 2)
        rows = {}
        for profile in ("bounded", "mu_four", "critical_log_growth", "critical_log_decay"):
            previous, denominator = 1, 10
            row = []
            for _ in range(7):
                q = D(denominator)
                if profile == "bounded":
                    next_digit = 1
                elif profile == "mu_four":
                    next_digit = denominator**2
                else:
                    log_power = 2 if profile == "critical_log_growth" else -2
                    next_digit = max(1, int(q**(critical_mu-2) * q.ln()**log_power))
                # Bounds follow from the continued-fraction error interval:
                # (a+2)^-1 < q^2 |x - p/q| < a^-1.
                lower, upper = (peak_factor * q**(-2*redshift_power)
                                * D(digit)**(1-redshift_power)
                                for digit in (next_digit, next_digit+2))
                row.append({"log_denominator": float(q.ln()),
                            "lower_bound_on_peak_probe_to_gap_squared": float(lower),
                            "upper_bound_on_peak_probe_to_gap_squared": float(upper)})
                previous, denominator = denominator, next_digit * denominator + previous
            rows[profile] = row
        for profile in ("bounded", "critical_log_decay"):
            assert rows[profile][-1]["upper_bound_on_peak_probe_to_gap_squared"] < 1
        for profile in ("mu_four", "critical_log_growth"):
            assert rows[profile][-1]["lower_bound_on_peak_probe_to_gap_squared"] > 1
        return float(critical_mu), rows


def redshift_peak_checks():
    power = 1 / sqrt(6)
    peak_location = sqrt((1+power) / (1-power))
    peak_constant = 0.5 * (1+power)**((1+power)/2) * (1-power)**((1-power)/2)
    for error in (0.24, 0.003, 1e-17):
        location = error * peak_location

        def weight(y):
            return y**(1+power) / (y*y + error*error)

        assert abs(weight(location) / (peak_constant * error**(power-1)) - 1) < 1e-13
        assert all(weight(location) > weight(location*factor) for factor in (0.8, 0.99, 1.01, 1.2))
    return {"y_at_probe_peak_over_rational_error": peak_location,
            "probe_peak_constant": peak_constant}


def semicircle_checks():
    center, radius = 0.7, 0.4
    endpoint = center + radius
    rows = []
    for path_time in (2.0, 5.0, 8.0):
        x = center + radius * tanh(path_time)
        y = radius / cosh(path_time)
        # Compare at the same height. Horizontal distance bounds hyperbolic distance.
        log_distance_bound = abs(x-endpoint) / y
        largest_gap_log_change = 0.0
        for p, q in product(range(-6, 7), repeat=2):
            if p == q == 0:
                continue
            first = ((q*x-p)**2 + q*q*y*y) / y
            second = ((q*endpoint-p)**2 + q*q*y*y) / y
            largest_gap_log_change = max(largest_gap_log_change, abs(log(first/second)))
        assert largest_gap_log_change <= log_distance_bound + 1e-12
        assert log_distance_bound <= y / radius
        rows.append({"hyperbolic_path_time": path_time, "volume": y,
                     "upper_bound_on_squared_mass_log_change": log_distance_bound,
                     "maximum_squared_mass_log_change_in_test": largest_gap_log_change})
    return rows


def radiation_checks():
    rows = []
    for initial_ratio in (1e-6, 0.01, 1.0, 100.0):
        exact = 4/sqrt(3) * asinh(1/sqrt(initial_ratio))
        intervals, stop = 4096, 26
        step = stop / intervals

        def speed(log_expansion):
            return sqrt(12) / sqrt(1 + initial_ratio * exp(3*log_expansion))

        interior = fsum((4 if i % 2 else 2) * speed(i*step) for i in range(1, intervals))
        numeric = step/3 * (speed(0) + interior + speed(stop))
        assert abs(numeric - exact) < 1e-9
        rows.append({"initial_radiation_to_kinetic_density": initial_ratio,
                     "remaining_field_distance": exact,
                     "independent_quadrature": numeric})
    return rows


def golden_height_checks():
    bound = sqrt(5)/2
    heights = []
    for c, d in product(range(-20, 21), repeat=2):
        if c == d == 0:
            continue
        norm = d*d + c*d - c*c
        assert norm != 0
        heights.append(bound / abs(norm))
    assert max(heights) == bound
    return {"golden_geodesic_maximum_height": bound,
            "log_time_mean_above_one": 3/pi,
            "log_time_mean_above_golden_height": 3/(pi*bound)}


def e6_weight_checks():
    momenta = [tuple(F(int(k == i)) + F(1, 3) for k in range(6)) for i in range(6)]
    membranes = [tuple(F(1, 3) - int(k in pair) for k in range(6))
                 for pair in combinations(range(6), 2)]
    fivebranes = [tuple(F(int(k == i)) - F(2, 3) for k in range(6)) for i in range(6)]
    weights = momenta + membranes + fivebranes
    assert len(set(weights)) == 27

    def weight_inner(left, right):
        return sum(a*b for a, b in zip(left, right)) - sum(left)*sum(right)/9

    assert {weight_inner(weight, weight) for weight in weights} == {F(4, 3)}
    assert {weight_inner(left, right) for left, right in combinations(weights, 2)} == {F(1, 3), F(-2, 3)}
    for selected in weights:
        velocity = tuple(F(3, 4) * (entry - sum(selected)/9) for entry in selected)
        assert sum(entry**2 for entry in velocity) + sum(velocity)**2/3 == F(3, 4)
        exponents = Counter(sum(a*b for a, b in zip(weight, velocity)) for weight in weights)
        assert exponents == {F(1): 1, F(1, 4): 16, F(-1, 2): 10}
    assert tuple(F(3, 4) * (entry - sum(momenta[0])/9) for entry in momenta[0]) == (F(3, 4), 0, 0, 0, 0, 0)
    return {"charge_weight_count": 27, "dual_norm_squared": "4/3",
            "marginal_mass_decay_exponents_with_multiplicities": {"1": 1, "1/4": 16, "-1/2": 10},
            "single_radius_exponent_in_five_dimensional_proper_time": "3/4"}


def main():
    scalar_speed_squared = F(3, 4)
    hubble_exponent = F(1, 4)
    assert 6*hubble_exponent**2 == scalar_speed_squared/2
    assert 4*hubble_exponent == 1
    modular_speed = sqrt(2 * scalar_speed_squared)
    assert modular_speed/2 < 1
    critical_mu, cf_rows = continued_fraction_checks()
    assert 2 < critical_mu < 4
    assert abs(modular_speed * (1-2/critical_mu) - 0.5) < 1e-14
    data = {"modular_speed_per_log_cosmic_time": modular_speed,
            "worst_gap_decay_exponent_in_cosmic_time": modular_speed/2,
            "critical_irrationality_exponent": critical_mu,
            "redshift_peaks": redshift_peak_checks(),
            "continued_fraction_examples": cf_rows,
            "nonvertical_geodesic_checks": semicircle_checks(),
            "remaining_distance_with_radiation": radiation_checks(),
            "proper_time_occupation_controls": golden_height_checks(),
            "e6_hubble_bound": e6_weight_checks()}
    output = Path(__file__).resolve().parents[1] / "data" / "toe_20261116_dynamical_axion_thresholds.json"
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Verified dynamical axion thresholds, radiation freezing, and the 27 E6 Hubble weights.")


if __name__ == "__main__":
    main()
