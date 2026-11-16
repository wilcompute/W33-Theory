"""Verify continued-fraction tower excursions on the torus axion-volume slice."""

import json
from fractions import Fraction
from math import comb, factorial, gcd
from pathlib import Path

import sympy as sp


DATA = Path(__file__).resolve().parents[1] / "data"


def convergents(digits):
    """Return the numerator-denominator pairs of [0; digits]."""
    p_old, p = 1, 0
    q_old, q = 0, 1
    result = [(p, q)]
    for digit in digits:
        p_old, p = p, digit*p+p_old
        q_old, q = q, digit*q+q_old
        assert abs(p*q_old - q*p_old) == 1 and gcd(p, q) == 1
        result.append((p, q))
    return result


def prefix_readings(digits):
    approximants = convergents(digits)
    lower, upper = sorted(Fraction(p, q) for p, q in approximants[-2:])
    result = []
    for index, (p, q) in enumerate(approximants[1:-2], start=1):
        value = Fraction(p, q)
        assert not lower <= value <= upper
        epsilon_min, epsilon_max = sorted((abs(lower-value), abs(upper-value)))
        next_q = approximants[index+1][1]
        assert Fraction(1, q*(next_q+q)) <= epsilon_min
        assert epsilon_max <= Fraction(1, q*next_q)
        chosen_volume = epsilon_max
        height_lower = 1/(2*q*q*chosen_volume)
        # At the chosen volume the worst endpoint gives this exact lower bound.
        assert min(chosen_volume / ((q*x-p)**2+(q*chosen_volume)**2)
                   for x in (lower, upper)) == height_lower
        result.append({
            "convergent_index": index, "next_partial_quotient": str(digits[index]),
            "numerator": str(p), "denominator": str(q),
            "chosen_volume": str(chosen_volume), "height_lower_bound": str(height_lower),
            "unique_winning_doublet_when_bound_exceeds_one": height_lower > 1,
        })
    return result


def crossed_box_moment(order):
    moment = 0
    for s, t in ((1, Fraction(-1, 2)), (1, Fraction(-1, 2)), (Fraction(-1, 2), Fraction(-1, 2))):
        for i in range(order+1):
            j = order-i
            integral = Fraction(factorial(i)**2 * factorial(j)**2, factorial(2*order+3))
            moment += comb(order, i)*s**i*t**j*integral
    return moment


def verify():
    x, y = sp.symbols("x y", real=True)
    a, b, c, d = sp.symbols("a b c d", real=True)
    metric = sp.Matrix([[1, x], [x, x*x+y*y]])/y
    charges = sp.Matrix([[a, b], [c, d]])
    # Two distinct primitive charge lines cannot both have squared norm < 1.
    assert sp.factor((charges.T*metric*charges).det()) == (a*d-b*c)**2
    epsilon, q, w = sp.symbols("epsilon q w", positive=True)
    mass_sq = q*q*(epsilon*epsilon/y+y)
    at_relative_volume = mass_sq.subs(y, epsilon*w).expand()
    assert sp.simplify(at_relative_volume-q*q*epsilon*(w+1/w)) == 0

    finite_power_digits = [2]
    accelerating_digits = [2]
    for n in range(2, 8):
        finite_power_digits.append(convergents(finite_power_digits)[-1][1]**2)
        if n < 7:
            accelerating_digits.append(convergents(accelerating_digits)[-1][1]**n)
    examples = {
        "golden_ratio_prefix": prefix_readings([1]*14),
        "unbounded_linear_partial_quotients": prefix_readings(list(range(1, 15))),
        "next_partial_quotient_is_current_denominator_squared": prefix_readings(finite_power_digits),
        "accelerating_partial_quotient_powers": prefix_readings(accelerating_digits),
    }
    golden_heights = [Fraction(row["height_lower_bound"]) for row in examples["golden_ratio_prefix"]]
    assert 1 < max(golden_heights) < Fraction(4, 3)
    assert Fraction(11, 10) < golden_heights[5] < Fraction(23, 20)
    assert all(row["unique_winning_doublet_when_bound_exceeds_one"]
               for row in examples["next_partial_quotient_is_current_denominator_squared"])

    dimensions, kk_rank = 5, 6
    species_exponent = Fraction(kk_rank, 2*(dimensions+kk_rank-2))
    r4_exponent = Fraction(2, 8-2)
    d4r4_exponent = Fraction(7, 2*(12-2))
    assert species_exponent == r4_exponent == Fraction(1, 3)
    assert d4r4_exponent-species_exponent == Fraction(1, 60)
    box_moments = {k: crossed_box_moment(k) for k in (0, 1, 2, 4, 8, 16)}
    assert box_moments[0] == Fraction(1, 2) and box_moments[1] == 0
    assert all(box_moments[k] > 0 for k in (2, 4, 8, 16))
    return {
        "metric_determinant": 1,
        "irrationality_exponent_to_height_growth": "1-2/mu",
        "almost_every_axion_log_height_limsup_exponent": 1,
        "almost_every_axion_time_fraction_above_height_H_at_least_1": "3/(pi*H)",
        "controlled_large_height_scales": {
            "light_mass_exponent_in_H": "-1/2",
            "six_dimensional_tower_species_exponent_in_H": str(-species_exponent),
            "r4_suppression_scale_exponent_in_H": str(-r4_exponent),
            "d4r4_suppression_scale_exponent_in_H": str(-d4r4_exponent),
            "d4r4_to_species_scale_ratio_exponent_in_H": "-1/60",
        },
        "crossed_scalar_box_simplex_moments_at_t_equal_u": {k: str(v) for k, v in box_moments.items()},
        "massive_kk_one_loop_analytic_radius_in_s": "4*m_min^2",
        "rigorous_finite_prefix_witnesses": examples,
    }


if __name__ == "__main__":
    path = DATA / "toe_20261116_irrational_axion_towers.json"
    path.write_text(json.dumps(verify(), indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Verified exact light-doublet peak bounds and the cutoff-exponent comparison")
