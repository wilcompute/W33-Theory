"""Canonical exchange partition functions for two-regular graph ensembles."""
import json
from math import exp, log
from pathlib import Path

import numpy as np

from toe_20261127_cycle_connectivity import connected_probability


def cycle_types(n, minimum=3):
    for first in range(minimum, n - minimum + 1):
        for rest in cycle_types(n - first, first):
            yield (first, *rest)
    if n >= minimum:
        yield (n,)


def cycle_spectra(length):
    edges = [(i, (i + 1) % length) for i in range(length)]
    spectra = []
    for particles in range(length // 2 + 1):
        states = [state for state in range(1 << length) if state.bit_count() == particles]
        index = {state: i for i, state in enumerate(states)}
        matrix = np.zeros((len(states), len(states)))
        for i, state in enumerate(states):
            for a, b in edges:
                if ((state >> a) ^ (state >> b)) & 1:
                    matrix[i, i] += 1
                    matrix[i, index[state ^ (1 << a) ^ (1 << b)]] -= 1
        spectra.append(np.linalg.eigvalsh(matrix))
    return [spectra[min(k, length - k)] for k in range(length + 1)]


def build():
    sizes = (6, 8, 10, 12)
    spectra = {length: cycle_spectra(length) for length in range(3, max(sizes) + 1)}
    rows = []
    q = (1 + 2 * exp(-3)) / 3
    for beta in (0., .25, 1., 3.):
        z = {length: [float(np.exp(-beta * es).sum()) for es in sectors]
             for length, sectors in spectra.items()}
        for n in sizes:
            comparisons = []
            numerator = np.array(z[n]) * q/(2*n)
            denominator = numerator.copy()
            for lengths in cycle_types(n):
                m = len(lengths)
                if m == 1:
                    continue
                polynomial = np.array([1.])
                weight = 1.
                repetitions = {}
                for length in lengths:
                    polynomial = np.convolve(polynomial, z[length])
                    repetitions[length] = repetitions.get(length, 0) + 1
                    weight *= q / (2*length*repetitions[length])
                denominator += weight * polynomial
                ratios = np.log(polynomial/np.array(z[n]))
                assert np.max(np.abs(ratios)) <= beta*m + 1e-10
                comparisons.append(float(np.max(np.abs(ratios))))
            p = numerator/denominator
            odds_low = 1/connected_probability(n, q*exp(-beta))-1
            odds_high = 1/connected_probability(n, q*exp(beta))-1
            lower = 1/(1+exp(beta)*odds_high)
            upper = 1/(1+exp(-beta)*odds_low)
            assert float(min(p)) >= lower - 1e-12 and float(max(p)) <= upper + 1e-12
            if beta == 0:
                assert all(abs(value-connected_probability(n,q)) < 1e-12 for value in p)
            rows.append({"n": n, "matter_beta": beta, "probabilities_by_particle_number": p.tolist(),
                         "half_filling": float(p[n//2]), "lower_bound": lower, "upper_bound": upper,
                         "max_absolute_log_partition_ratio": max(comparisons)})
    return {"status": "PASS", "wilson_cycle_weight": q, "rows": rows,
            "uniform_upper_power": "n^(-q*exp(-beta)/2) up to a constant for fixed q,beta",
            "uniform_lower_power": "n^(-q*exp(beta)/2) up to a constant for fixed q,beta"}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
