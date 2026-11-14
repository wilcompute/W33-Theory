"""Pass 12664: the type B measurements as CZ + Hadamard circuits on four qubits."""
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))

EDGES = {"A": [], "B": [(0, 3), (1, 2), (1, 3)], "C": [(0, 2), (0, 3), (1, 2)], "D": [(0, 2), (1, 3)]}  # qubits a0, a1, b0, b1


def _circuits():
    H1 = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    HH = np.eye(1)
    for _ in range(4):
        HH = np.kron(H1, HH)
    out = {}
    for name, edges in EDGES.items():
        d = np.ones(16)
        for s in range(16):
            for qa, qb in edges:
                if (s >> qa) & 1 and (s >> qb) & 1:
                    d[s] *= -1
        out[name] = HH @ np.diag(d)
    out["E"] = np.eye(16)
    return out


def test_circuit_table_matches_certificate():
    d = load("w33_typeB_hardware_circuits.json")
    assert d["cz_counts"] == {"0": 0, "1": 3, "w": 3, "w^2": 2}
    assert d["circuit_vs_model_max_difference"] < 1e-12 and abs(d["min_F_times_16"] - 1) < 1e-6


def test_five_circuits_are_mutually_unbiased():
    U = _circuits()
    names = list(U)
    for i, a in enumerate(names):
        assert np.allclose(U[a] @ U[a].conj().T, np.eye(16))
        for b in names[i + 1:]:
            overlap = np.abs(U[a].conj() @ U[b].T) ** 2  # |<e_j(a)|e_k(b)>|^2 with rows = measurement vectors
            assert np.allclose(overlap, 1 / 16), (a, b)


def test_total_collision_floor_on_samples():
    U = _circuits()
    rng = np.random.default_rng(1)
    for _ in range(200):
        psi = rng.standard_normal(16) + 1j * rng.standard_normal(16)
        psi /= np.linalg.norm(psi)
        tot = sum((np.abs(M @ psi) ** 4).sum() for M in U.values())
        assert tot >= 5 / 16 + 11 / 250 - 1e-12
    psi = np.zeros(16); psi[0] = 1
    assert abs(sum((np.abs(M @ psi) ** 4).sum() for M in U.values()) - (1 + 4 / 16)) < 1e-12
    rho = np.eye(16) / 16
    assert abs(sum((np.real(np.diag(M @ rho @ M.conj().T)) ** 2).sum() for M in U.values()) - 5 / 16) < 1e-12
