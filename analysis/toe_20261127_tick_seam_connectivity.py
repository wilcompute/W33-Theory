"""Check a seam bound for higher-order interactions on cycle ensembles."""
import json
from fractions import Fraction
from itertools import product
from math import exp, factorial, log

import numpy as np


def cumulant_majorants(max_order, block_bound=1):
    stirling = [[1]]
    majorants = []
    for r in range(1, max_order + 1):
        old = stirling[-1]
        row = [0] + [old[k-1] + (k*old[k] if k < r else 0) for k in range(1, r+1)]
        stirling.append(row)
        majorants.append(sum(factorial(k-1)*row[k]*block_bound**k for k in range(1, r+1)))
    return majorants


def cycle_windows(cycles, width):
    return [tuple(cycle[(i+j) % len(cycle)] for j in range(width))
            for cycle in cycles if len(cycle) >= width for i in range(len(cycle))]


def step_matrix(states, window, reflection):
    """Single-qutrit factor of the repo triple projector or fourth reflection."""
    n = states.shape[1]
    weights = 3**np.arange(n-1, -1, -1)
    columns = np.arange(len(states))
    local = states[:, window].astype(int)
    matrix = np.zeros((len(states), len(states)))
    if reflection:
        signs = np.array((1, 1, -1, -1))
        for pairing in ((0, 1, 2, 3), (0, 2, 1, 3), (0, 2, 3, 1)):
            vector = signs[list(pairing)]
            image = (local + (local @ vector)[:, None]*vector) % 3
            rows = columns + (image-local) @ weights[list(window)]
            matrix[rows, columns] += 1/3
    else:
        valid = local.sum(axis=1) % 3 == 0
        for shift in range(3):
            image = (local+shift) % 3
            rows = columns + (image-local) @ weights[list(window)]
            matrix[rows[valid], columns[valid]] += 1/3
    return matrix


def build():
    majorants = cumulant_majorants(30)
    assert majorants[:5] == [1, 2, 6, 26, 150]
    tick_majorants = cumulant_majorants(70, Fraction(1, 3))
    convergence = []
    for t in (.1, .4, .8, 1.0):
        bound = t*exp(t)/(4-exp(t))+log((4-exp(t))/3)
        subtotal = sum((r-1)*float(a)*t**r/factorial(r)
                       for r, a in enumerate(tick_majorants, 1))
        assert -1e-14 <= bound-subtotal < 1e-6
        convergence.append({"t": t, "seam_constant": bound, "partial_sum_70": subtotal})
    # The factor model retains noncommuting signed three- and four-site terms.
    states = np.array(list(product(range(3), repeat=6)))
    split = [(0, 1, 2), (3, 4, 5)]
    joined = [tuple(range(6))]
    hamiltonians = []
    for cycles in (split, joined):
        projectors = sum(step_matrix(states, window, False)
                         for window in cycle_windows(cycles, 3))
        reflections = sum((step_matrix(states, window, True)
                           for window in cycle_windows(cycles, 4)), np.zeros_like(projectors))
        hamiltonians.append(projectors - .3*reflections)
    probe_a = step_matrix(states, (0, 1, 2), False)
    probe_b = step_matrix(states, (1, 2, 3, 4), True)
    commutator = np.linalg.norm(probe_a@probe_b-probe_b@probe_a)
    assert commutator > 1
    split_h, joined_h = hamiltonians
    assert np.allclose(split_h, split_h.T) and np.allclose(joined_h, joined_h.T)
    # With both cycles shorter than the four-site term, the width-four windows
    # all lie on the joined side. Count the actual changed windows on each side.
    cost = 0.
    for width, norm in ((3, 1.), (4, .3)):
        a = set(cycle_windows(split, width))
        b = set(cycle_windows(joined, width))
        cost += len(a ^ b)*norm
    seam_norm = float(max(abs(np.linalg.eigvalsh(split_h-joined_h))))
    assert seam_norm <= cost + 1e-10
    spectra = [np.linalg.eigvalsh(h) for h in hamiltonians]
    cycle_weight = (1+2*exp(-3))/3
    thermal = []
    for beta in (.25, 1., 3.):
        logs = [float(np.logaddexp.reduce(-beta*es)) for es in spectra]
        ratio = logs[0]-logs[1]
        assert abs(ratio) <= beta*seam_norm + 1e-10
        # On six labeled vertices there are 60 rings and 10 pairs of triangles.
        thermal.append({"beta": beta, "log_split_over_ring": ratio,
                        "connected_probability": 1/(1+cycle_weight*exp(ratio)/6)})
    return {"status": "PASS", "majorants_first_five": majorants[:5],
            "tick_majorants_first_five": [str(a) for a in tick_majorants[:5]],
            "convergent_tick_series": convergence, "commutator_frobenius_norm": commutator,
            "factor_probe_seam_norm": seam_norm, "changed_window_bound": cost,
            "factor_probe_cycle_weight": cycle_weight, "factor_probe_thermal": thermal}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
