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


def test_theta_eig_upper_bound_five_qubit():
    d = json.load(open(os.path.join(ROOT, "data", "w33_five_qubit_size9_theta_eig.json")))
    assert abs(d["hoffman_point"] - 31) < 1e-6
    assert 30 < d["theta_upper"] < 30.46
    assert (31 - d["theta_upper"]) / 32 > 0.017


def test_theta_lower_bound_exceeds_alpha():
    d = json.load(open(os.path.join(ROOT, "data", "w33_five_qubit_size9_theta_lower.json")))
    assert abs(d["control"]["petersen"] - 4) < 1e-3 and abs(d["control"]["petersen_complement"] - 2.5) < 1e-3
    assert d["theta_G_exceeds_30"] and 30.3 < 744 / d["theta_complement_upper"] < 30.45


def test_swap_bell_bound_controls_and_weakness():
    d = json.load(open(os.path.join(ROOT, "data", "w33_swap_bell_bound.json")))
    assert d["controls"] == {"all_n2": 3, "all_n3": 7, "all_n4": 15}
    for s in d["sets"]:
        if "numeric_minF" in s:
            assert s["bound_minF"] <= s["numeric_minF"] + 1e-7
    assert {(s["n"], s["B"]) for s in d["sets"] if s["n"] >= 5} == {(5, 40), (6, 72)}


def test_typeB_lift_reduction():
    d = json.load(open(os.path.join(ROOT, "data", "w33_four_qubit_typeB_lift_reduction.json")))
    A, B = d["A_genuine"], d["B_lifted"]
    assert A["n_lift_points"] == 0 and B["n_lift_points"] == 120
    assert abs(A["SigmaU_max"] - 14.1622) < 1e-3 and abs(B["SigmaU_max"] - 14) < 1e-6
    for r in (B, B["second_lift_point"]):
        assert abs(r["a_max"] - 14) < 1e-6 and abs(r["b_max"] - 14) < 1e-6
        assert abs(r["c_max"] - 36) < 1e-6 and not r["sufficient"]


def test_bell_bound_small_case_by_brute_force():
    # independent check of the Bell-basis eigenvalue formula: two qubits, U = {XI, ZZ, YX}
    import itertools as it
    P1 = {"I": I2, "X": X, "Y": Y, "Z": Z}
    U = ["XI", "ZZ", "YX"]
    Q = sum(np.kron(np.kron(P1[a[0]], P1[a[1]]), np.kron(P1[a[0]], P1[a[1]])) for a in U)
    SW = np.zeros((16, 16))
    for i, j in it.product(range(4), repeat=2):
        SW[4 * j + i, 4 * i + j] = 1
    Pi = (np.eye(16) + SW) / 2
    lam = np.linalg.eigvalsh(Pi @ Q @ Pi)[-1]
    # formula
    enc = {"I": (0, 0), "X": (1, 0), "Z": (0, 1), "Y": (1, 1)}
    def xz(s):
        return [enc[c] for c in s]
    best = -99
    for a in it.product("IXYZ", repeat=2):
        A = xz(a)
        if sum(x * z for x, z in A) % 2:
            continue
        v = 0
        for b in U:
            Bv = xz(b)
            om = sum(A[k][0] * Bv[k][1] + A[k][1] * Bv[k][0] for k in range(2)) % 2
            v += (-1) ** (sum(x * z for x, z in Bv) % 2) * (-1) ** om
        best = max(best, v)
    assert abs(lam - best) < 1e-9


def test_six_qubit_size9_min_f():
    d = json.load(open(os.path.join(ROOT, "data", "w33_six_qubit_size9_minF_size8.json")))
    assert abs(d["min_F_times_64"] - 1) < 1e-6
