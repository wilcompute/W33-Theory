"""Rigorous counting bounds beyond the twin-paired ansatz.

The local triple budget is Pass 12488's. Add the >=4 coverage branch and
even-cardinality rounding; these are lower bounds, not exact distances.
"""
from math import comb
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def local_bound(q):
    if q < 3 or q % 2 == 0:
        raise ValueError("The antiregularity argument here requires odd q >= 3")
    mass, budget = q*(q+1), comb(q+1, 3)
    # Convexity of C(c,3) on nonnegative integers makes the balanced
    # distribution the exact minimum at fixed count and fixed total c.
    for D in range(1, mass+1):
        c, rem = divmod(mass, D)
        if c > q+1 or (rem and c == q+1):
            continue
        cost = (D-rem)*comb(c, 3) + rem*comb(c+1, 3)
        if cost <= budget:
            raw = q+2+D
            hyperoval = raw + raw % 2
            heavy = 4*(q+1)
            return dict(q=q, local_distance_two_count=D,
                        triple_budget=budget, balanced_triple_cost=cost,
                        balanced_codegrees={str(c):D-rem, str(c+1):rem},
                        coverage_0_2_lower_bound=hyperoval,
                        coverage_at_least_4_lower_bound=heavy,
                        general_even_set_lower_bound=min(hyperoval, heavy))
    raise AssertionError("No feasible counting distribution")


def main():
    rows = [local_bound(q) for q in (3,5,7,9,11,13,17,19,23,27,31)]
    assert [r['general_even_set_lower_bound'] for r in rows[:3]] == [10,16,24]
    out = dict(status="PROVED_COUNTING_LOWER_BOUNDS_NOT_EXACT_DISTANCES", rows=rows,
               prior="Pass 12488 owns the local antiregularity triple budget; classical hyperoval literature owns general hyperoval bounds and the q=3 minimum.",
               heavy_point_proof="If r>=4 selected lines pass through p, each has q other points requiring another selected line. A line not through p can meet at most one of those r concurrent lines by the GQ axiom. Thus |S|>=r(q+1)>=4(q+1).",
               even_weight_proof="For any point p, sum incidence rows for the points in p-perp. Mod2, this is the indicator of lines not through p: lines through p contribute q+1=0, other lines contribute 1. An even line set therefore has an even number of lines not through p and an even number through p, hence even total weight.",
               scope="Odd prime powers. This does not prove the conjectured quadratic bound for all even line sets.")
    (ROOT/'data/w33_20261031_even_set_bounds.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__ == '__main__':
    main()
