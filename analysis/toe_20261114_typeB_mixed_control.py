"""Exact rank-two control and purity-aware bound for the five F4 settings."""

import json
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/toe_20261114_typeB_mixed_control.json"
# Outcomes use the computational bit order in Pass 12664.
GRAPHS = [(), ((0, 3), (1, 2), (1, 3)), ((0, 2), (0, 3), (1, 2)), ((0, 2), (1, 3))]
DIM = 16
GENERATOR_LABELS = [17, 35, 72]
PURE_FLOOR = Fraction(11, 250)


def calculate():
    table = [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]
    trace = [0, 0, 1, 1]
    sites = range(DIM)
    identity = np.eye(DIM, dtype=np.int64)

    def dot(a, b):
        return trace[table[a & 3][b & 3] ^ table[a >> 2][b >> 2]]

    def pauli(v):
        x, z = v & 15, v >> 4
        return identity[:, [a ^ x for a in sites]] @ np.diag(
            [1j**dot(x, z) * (-1)**dot(a, z) for a in sites])

    rho_numerator = identity.astype(complex)
    for v in GENERATOR_LABELS:
        rho_numerator = rho_numerator @ (identity + pauli(v))
    assert np.array_equal(rho_numerator, rho_numerator.conj().T)
    assert np.array_equal(rho_numerator @ rho_numerator, 8 * rho_numerator)
    assert rho_numerator.trace() == 16
    assert np.array_equal(np.diag(rho_numerator), np.ones(DIM))

    hadamard = np.array([[(-1)**((a & b).bit_count()) for b in sites] for a in sites])
    circuits = [identity]
    for graph in GRAPHS:
        signs = [(-1)**sum(((a >> i) & 1)*((a >> j) & 1) for i, j in graph) for a in sites]
        circuit_numerator = hadamard * signs
        assert np.array_equal(np.diag(circuit_numerator @ rho_numerator @ circuit_numerator.T),
                              DIM*np.ones(DIM))
        circuits.append(circuit_numerator/4)
    for i, a in enumerate(circuits):
        for b in circuits[i+1:]:
            assert np.array_equal(np.abs(a @ b.T)**2, np.full((DIM, DIM), 1/DIM))

    # Purity data tighten a uniform bound with no specific noise channel.
    samples = []
    for purity in (.5, .8, .9, .95, .99, 1.):
        eigenvalue = (1 + np.sqrt(2*purity-1))/2
        excess = max(0., np.sqrt(float(PURE_FLOOR))*eigenvalue
                     - np.sqrt(15/16)*(1-eigenvalue))**2
        samples.append(dict(purity=purity, collision_lower_bound=5/16+excess))
    return dict(status="PASS", generators=GENERATOR_LABELS, rank=2, purity="1/2",
                probability_each_outcome="1/16", collision_sum="5/16",
                pure_collision_floor=str(Fraction(5, 16)+PURE_FLOOR),
                purity_lower_bounds=samples)


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result, flush=True)
