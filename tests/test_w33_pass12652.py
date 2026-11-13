"""Pass 12652: the two-moment proof of kappa <= 3 (three-qubit min F = 1/8) and the five/six-qubit rank-code checks."""
import itertools
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I2 = np.eye(2)
X = np.array([[0, 1], [1, 0]])
Z = np.diag([1, -1])
Y = np.array([[0, -1j], [1j, 0]])


def _model():
    return [np.kron(a, b) for a, b in ((I2, I2), (X, I2), (Z, I2), (X, Z), (I2, X), (Z, Y))]


def test_model_products_form_orthogonal_basis():
    R = _model()
    prods = [np.eye(4)] + [R[j].conj().T @ R[k] for j, k in itertools.combinations(range(6), 2)]
    G = np.array([[np.trace(P.conj().T @ Q) for Q in prods] for P in prods])
    assert np.allclose(G, 4 * np.eye(16))


def test_moment_identities_and_bound():
    R = _model()
    rng = np.random.default_rng(0)
    for _ in range(200):
        y = rng.standard_normal(4) + 1j * rng.standard_normal(4)
        y /= np.linalg.norm(y)
        W = np.array([M @ y for M in R]).T
        G = W.conj().T @ W
        assert abs(np.trace(G).real - 6) < 1e-9
        assert abs(np.trace(G @ G).real - 12) < 1e-9
        assert np.linalg.eigvalsh(G)[-1] <= 3 + 1e-9
    # Wolkowicz-Styan with rank 4, trace 6, Tr^2 12 gives exactly 3, attained by the commuting triple {I, XI, XZ}
    assert abs((6 + np.sqrt(3 * (4 * 12 - 36))) / 4 - 3) < 1e-12
    M = (R[0] + R[1] + R[3]) / np.sqrt(3)
    assert abs(np.linalg.norm(M, 2) ** 2 - 3) < 1e-9


def test_kappa_proof_on_data():
    p = os.path.join(ROOT, "data", "w33_kappa_moment_proof.json")
    d = json.load(open(p))
    assert d["proved"] and d["sixteen_products_HS_orthogonal"] and d["lemmaA_bijection"] and d["lemmaB_six_pairs"]
    assert abs(d["kappa_alternating"] - 3) < 1e-8 and d["spectrum_at_max"][:4] == [3.0, 1.0, 1.0, 1.0]


def test_floor24_states_are_nine_sets_minus_one():
    d = json.load(open(os.path.join(ROOT, "data", "w33_five_qubit_floor24.json")))
    assert d["n_states"] >= 5
    for s in d["states"]:
        assert len(s["E"]) == 24
        assert [1, True] in s["maximal_after_clique"]
        assert 0 in {int(k) for k in s["degrees"]}


def test_six_qubit_size9_min_f():
    d = json.load(open(os.path.join(ROOT, "data", "w33_six_qubit_size9_minF_size8.json")))
    assert abs(d["min_F_times_64"] - 1) < 1e-6
