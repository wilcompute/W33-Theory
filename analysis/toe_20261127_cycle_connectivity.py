"""Thermodynamic control for the degree-two exchange graph ensemble."""
import json
from fractions import Fraction
from itertools import combinations
from math import exp, factorial, gamma, log
from pathlib import Path

import numpy as np


def partition_coefficient(n, theta):
    """Coefficient of exp(theta * sum_{l>=3} z**l/l), in O(n) time."""
    if n < 3 or theta <= 0:
        raise ValueError("require n >= 3 and positive theta")
    coefficients = [1, 0, 0]
    prefix = 0
    for size in range(3, n + 1):
        prefix += coefficients[size - 3]
        coefficients.append(theta * prefix / size)
    return coefficients[n]


def connected_probability(n, fugacity):
    theta = fugacity / 2
    return theta / (n * partition_coefficient(n, theta))


def token_heat_trace(lengths, beta):
    """Build the two-token Laplacian directly from disjoint cycles."""
    n = sum(lengths)
    edges = []
    offset = 0
    for length in lengths:
        edges.extend((offset + i, offset + (i + 1) % length) for i in range(length))
        offset += length
    states = [frozenset(pair) for pair in combinations(range(n), 2)]
    index = {state: i for i, state in enumerate(states)}
    laplacian = np.zeros((len(states), len(states)))
    for i, state in enumerate(states):
        for left, right in edges:
            edge = frozenset((left, right))
            if len(state & edge) == 1:
                laplacian[i, i] += 1
                laplacian[i, index[state ^ edge]] -= 1
    return float(np.exp(-beta * np.linalg.eigvalsh(laplacian)).sum())


def build():
    theta = Fraction(1, 2)
    # Direct symmetry factors for C8, C5+C3, and C4+C4.
    counts = [factorial(8) // denominator for denominator in (16, 60, 128)]
    assert partition_coefficient(8, theta)*factorial(8) == sum(counts) == 3507
    gauge_beta, matter_beta = 2., .5
    q = (1 + 2*exp(-1.5*gauge_beta))/3
    heat_traces = [token_heat_trace(lengths, matter_beta) for lengths in ((8,), (5, 3), (4, 4))]
    weights = [count*trace*q**cycles for count, trace, cycles in zip(counts, heat_traces, (1, 2, 2))]
    p8 = weights[0]/sum(weights)
    cold_weights = [count * cycles*(cycles+1)//2 * q**cycles
                    for count, cycles in zip(counts, (1, 2, 2))]
    previous = Path(__file__).resolve().parents[1] / "data/toe_20261127_dynamic_graph_exchange.json"
    baseline = next(row for row in json.loads(previous.read_text(encoding="utf-8-sig"))["rows"]
                    if row["gauge_beta"] == gauge_beta and row["matter_beta"] == matter_beta and row["shifted"])
    assert abs(p8-baseline["probabilities"][0]) < 1e-11
    sizes = (8, 128, 2048, 32768, 524288)
    fixed = []
    for n in sizes:
        p = connected_probability(n, q)
        power_law = gamma(1+q/2)*exp(3*q/4)*n**(-q/2)
        fixed.append({"n": n, "probability": p, "asymptotic": power_law,
                      "upper_with_fixed_two_token_matter": min(1., exp(4*matter_beta)*p)})
    assert abs(fixed[-1]["probability"]/fixed[-1]["asymptotic"]-1) < 1e-5
    crossover = [{"n": n, "q": 2/log(n), "probability": connected_probability(n, 2/log(n))}
                 for n in sizes]
    return {"status": "PASS", "model": "labeled simple degree-two graphs with q per cycle",
            "n8_counts": counts, "n8_two_token_heat_traces": heat_traces,
            "n8_matter_and_gauge_connected_probability": p8, "fixed_q": q,
            "n8_zero_temperature_matter_first_probability": cold_weights[0]/sum(cold_weights),
            "fixed_q_scan": fixed, "crossover_scan": crossover, "crossover_limit": exp(-1),
            "matter_bound": "e^(-4b) P_gauge <= P_gauge+two-token <= e^(4b) P_gauge, fixed b>=0"}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
