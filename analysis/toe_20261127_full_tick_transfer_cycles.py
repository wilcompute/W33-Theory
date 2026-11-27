"""Nonlocality and cycle weights of the full shared-label tick transfer."""
from collections import Counter
from itertools import product
import json
from math import exp, log

import numpy as np


def tick_projectors():
    omega = np.exp(2j*np.pi/3)
    points = list(product(range(3), repeat=2))
    index = {p: i for i, p in enumerate(points)}
    directions = [v for v in product(range(3), repeat=4)
                  if next((x for x in v if x), 0) == 1]
    result = []
    for x, y, z, w in directions:
        W = np.zeros((9, 9), complex)
        for j, (u, v) in enumerate(points):
            W[index[((u+x) % 3, (v+y) % 3)], j] = omega**((z*u+w*v+2*(x*z+y*w)) % 3)
        for k in range(3):
            P = (np.eye(9)+omega**(-k)*W+omega**k*W.conj().T)/3
            assert np.max(abs(P@P-P)) < 1e-14
            assert abs(np.trace(P)-3) < 1e-14
            result.append(P)
    assert len(result) == 120
    return np.array(result)


def build():
    projectors = tick_projectors()
    count = len(projectors)
    s = .5
    A = s*np.eye(9)+(1-s)*projectors
    overlaps = np.einsum('aij,bji->ab', projectors, projectors)
    rounded = np.round(overlaps.real)
    assert np.max(abs(overlaps-rounded)) < 1e-12
    histogram = Counter(map(int, rounded.ravel()))
    assert histogram == {0: 240, 1: 14040, 3: 120}
    u = (1+2*s)/3
    # |00> and |++> have disjoint sets of projectors with expectation one.
    p = projectors[:, 0, 0].real
    f = projectors.sum(axis=(1, 2)).real/9
    pair = np.rint(3*np.column_stack((p, f))).astype(int)
    assert np.max(abs(pair/3-np.column_stack((p, f)))) < 1e-14
    assert not any(x == y == 3 for x, y in pair)
    assert abs(max((s+(1-s)*p)*(s+(1-s)*f))-u) < 1e-14
    nonlocality = [{"sites_per_component": m, "energy_difference_lower_bound": -m*log(u)-2*log(count)}
                   for m in (8, 24, 64, 128)]

    z2 = 3+6*s*s
    cross = {j: (9*s*s+6*s*(1-s)+(1-s)**2*j)/z2 for j in histogram}
    q = (1+2*exp(-3))/3
    nmax = 4096
    n_values = np.arange(nmax+1)
    weights = q*sum(histogram[j]*cross[j]**n_values for j in histogram)/count**2
    coeff = np.zeros(nmax+1)
    coeff[0] = 1
    for n in range(3, nmax+1):
        coeff[n] = weights[3:n+1]@coeff[n-3::-1]/(2*n)
    rows = [{"n": n, "cycle_weight": float(weights[n]),
             "connected_probability": float(weights[n]/(2*n*coeff[n]))}
            for n in (6, 8, 64, 512, 4096)]
    assert abs(weights[-1]-q/count) < 1e-15

    thermal = []
    K = A.copy()
    for length in (1, 2, 3):
        if length > 1:
            K = np.array([np.kron(old, a) for old, a in zip(K, A)])
        average = K.mean(axis=0)
        eigenvalues = np.linalg.eigvalsh(average)
        assert min(eigenvalues) > 0
        for power in (.5, 1., 1.5, 2.):
            normalized = float(sum(eigenvalues**power)/(3+6*s**power)**length)
            low, high = ((1., count**(1-power)) if power <= 1 else (count**(-power), 1.))
            assert low-1e-11 <= normalized <= high+1e-11
            if power == 2:
                assert abs(normalized-weights[length]/q) < 1e-12
            thermal.append({"length": length, "power": power, "bulk_normalized_trace": normalized})
    return {"status": "PASS", "single_site_thermal_eigenvalue_s": s,
            "trace_projector_overlap_histogram": dict(histogram),
            "shared_label_overlap_product_max": u,
            "operator_log_nonlocality": nonlocality,
            "power_two_wilson_weighted_cycles": rows, "power_two_asymptotic_fugacity": q/count,
            "power_two_asymptotic_connected_decay_exponent": q/(2*count),
            "direct_thermal_trace_checks": thermal}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
