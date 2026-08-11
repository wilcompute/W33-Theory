#!/usr/bin/env python3
"""Pass4951 — third-moment covering-radius bound for K=[360,36,20]_2.

Uses only frozen enumerator data from Pass4867 and the exact hard-word lower
witness from Pass4940.  For every coset of K, dual minimum 3 makes the 360
coordinate signs pairwise independent.  The 1080 dual weight-3 words bound the
third centered distance moment.  A one-sided moment polynomial excludes coset
leader >=175; the equality case at 174 forces a two-weight 174/195 coset with
population ratio 5:2, impossible because |K|=2^36 is not divisible by 7.
"""
from fractions import Fraction
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4951_THIRD_MOMENT_RADIUS_BOUND.json"


def main() -> int:
    n = 360
    dim = 36
    code_size = 2 ** dim
    dual_A1 = 0
    dual_A2 = 0
    dual_A3 = 1080

    mean = Fraction(n, 2)
    variance = Fraction(n, 4)  # pairwise independence from A1=A2=0
    third_abs_bound = Fraction(3, 4) * dual_A3

    # If a coset leader is delta, X=W-n/2 obeys X >= -a, a=n/2-delta.
    # E[(X+a)(X-t)^2]>=0 optimized at t=variance/a gives
    # mu3 >= variance*(variance/a-a).
    def mu3_lower(delta: int) -> Fraction:
        a = mean - delta
        assert a > 0
        return variance * (variance / a - a)

    lower_175 = mu3_lower(175)
    assert lower_175 == 1170
    assert lower_175 > third_abs_bound

    # At delta=174, a=6 and t=15.  The optimized inequality becomes
    # E[(X+6)(X-15)^2] = mu3-810 >= 0.  But |mu3|<=810, so equality
    # forces support only at X=-6 or X=15, i.e. weights 174 and 195.
    lower_174 = mu3_lower(174)
    assert lower_174 == third_abs_bound == 810
    weight_low = 174
    weight_high = 195
    x_low = weight_low - mean
    x_high = weight_high - mean
    assert (x_low, x_high) == (Fraction(-6), Fraction(15))

    # Mean zero forces -6*N174 + 15*N195 = 0, hence N174:N195=5:2.
    ratio_low = 5
    ratio_high = 2
    ratio_total = ratio_low + ratio_high
    assert ratio_total == 7
    divisibility_obstruction = code_size % ratio_total
    assert divisibility_obstruction != 0

    upper = 173
    lower = 134  # exact Pass4940 received-word distance
    out = {
        "pass": 4951,
        "code": "K=[360,36,20]_2",
        "frozen_inputs": {
            "length": n,
            "dimension": dim,
            "coset_size": code_size,
            "dual_A1": dual_A1,
            "dual_A2": dual_A2,
            "dual_A3": dual_A3,
            "Pass4940_exact_lower_witness": lower,
        },
        "coset_moments": {
            "mean_weight": int(mean),
            "variance": int(variance),
            "third_centered_moment_absolute_bound": int(third_abs_bound),
            "identity": "mu3=-(3/4)*sum_{h in K^perp, wt(h)=3} (-1)^(y.h)",
        },
        "one_sided_bound": {
            "inequality": "for X=W-180 >= -a: mu3 >= 90*(90/a-a)",
            "delta_175_lower_mu3": int(lower_175),
            "delta_175_contradicts_abs_bound": True,
        },
        "delta_174_equality_obstruction": {
            "a": 6,
            "optimized_t": 15,
            "nonnegative_polynomial": "(X+6)(X-15)^2",
            "forced_weights_if_equal": [weight_low, weight_high],
            "forced_population_ratio": "N174:N195=5:2",
            "required_total_divisor": ratio_total,
            "coset_size_mod_7": divisibility_obstruction,
            "impossible": True,
        },
        "covering_radius": {
            "lower_bound": lower,
            "upper_bound": upper,
            "exact_closed": False,
            "interval": [lower, upper],
        },
        "theorem": "Every coset of K has a representative of weight at most 173. Together with the Pass4940 exact hard word, 134 <= rho(K) <= 173.",
        "boundary": "This is a universal moment/divisibility bound, not an exact covering-radius computation. It uses only the frozen dual A1=A2=0, A3=1080 data and the Pass4940 lower witness.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
