#!/usr/bin/env python3
"""Check a "constant = closed form" claim against a fair null before calling it a prediction (Passes 12498, 12504).

    py -3 scripts/check_constant_claim.py --measured 0.307 --sigma 0.012 --predicted 4/13 --cost 2
    py -3 scripts/check_constant_claim.py --measured 137.035999084 --sigma 2.1e-8 --predicted 137 --cost 2 --window 1e-3

Reports, for the claim "measured ~ predicted, by an expression with `cost` integer leaves over the alphabet":
  tension   |predicted - measured| / sigma          (is it a match at all?)
  bits      log2 of the precision the match claims  (window = max(|pred/meas - 1|, sigma/meas) unless --window is given)
  p_random  the fraction of RANDOM alphabets (13 distinct integers from [2, 40] plus the leaf 1) whose expressions of cost <= `cost`
            reach the measured value within the same window -- the chance that a numerologist with a different alphabet does as well
  q3_hit    whether the q = 3 alphabet reaches it at that cost (control)
A claim is EVIDENCE only if the tension is small AND p_random is small.  Uses w33_mdl_shortest.build_expressions (cost = number of
integer leaves; operations + - * /).  Measured lessons: at cost 3 every random alphabet reaches every PMNS angle within 1 sigma; at
cost 2, 88-98% do (Pass 12504).
"""
import argparse
import bisect
import json
import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis"))
from w33_mdl_shortest import build_expressions  # noqa: E402

Q3 = [1, 2, 3, 4, 7, 10, 12, 13, 15, 18, 24, 27, 30, 40]


def reaches(alphabet, x, window, cost):
    vals = sorted(build_expressions(alphabet, max_cost=cost).keys())
    i = bisect.bisect_left(vals, x * (1 - window))
    return i < len(vals) and vals[i] <= x * (1 + window)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--measured", type=float, required=True)
    ap.add_argument("--sigma", type=float, required=True)
    ap.add_argument("--predicted", type=lambda s: float(Fraction(s)), required=True)
    ap.add_argument("--cost", type=int, default=2, help="integer leaves of the claimed expression (1-3)")
    ap.add_argument("--window", type=float, help="relative window to test (default: the claim's own miss or 1 sigma, whichever is larger)")
    ap.add_argument("-n", type=int, default=300, help="random alphabets")
    a = ap.parse_args()
    tension = abs(a.predicted - a.measured) / a.sigma
    window = a.window or max(abs(a.predicted / a.measured - 1), a.sigma / abs(a.measured))
    rng = random.Random(1)
    hits = sum(reaches([1] + sorted(rng.sample(range(2, 41), 13)), a.measured, window, a.cost) for _ in range(a.n))
    out = dict(measured=a.measured, sigma=a.sigma, predicted=a.predicted, cost=a.cost, window=window,
               tension_sigma=round(tension, 3), p_random=round(hits / a.n, 4), q3_hit=reaches(Q3, a.measured, window, a.cost))
    out["verdict"] = ("EXCLUDED by experiment" if tension > 3 else
                      "consistent, but NOT evidence (random alphabets do as well)" if out["p_random"] > 0.05 else
                      "consistent AND rare under the null -- worth a closer look")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
