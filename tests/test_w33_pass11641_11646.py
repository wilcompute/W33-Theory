"""Regression for Passes 11641-11645 (Claude track): Hesse CP = MUB Vandermonde, label-blind time, the transvection
clock, the union-law splitting criterion, and time reversal as conjugation of j."""

import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))


def load(name):
    return json.load(open(ROOT / "data" / name))


W3 = np.exp(2j * np.pi / 3)


def _bases():
    Xm = np.roll(np.eye(3), 1, axis=0)
    Zm = np.diag([1, W3, W3 * W3])
    return [np.eye(3)] + [np.linalg.eig(Xm @ np.linalg.matrix_power(Zm, a))[1] for a in range(3)]


def _axes():
    import sympy as sp
    d = load("w33_pass11600_dynamical_hesse_flavor.json")["tensor"]["Bloch_axes"]
    return np.array([[float(sp.sympify(x)) for x in row] for row in d])


def _n_rho(psi, T):
    u0 = (psi ** 3).sum() / np.sqrt(3)
    u1 = np.sqrt(6) * psi.prod()
    c = np.conj(u0) * u1
    return T.T @ np.array([2 * c.real, 2 * c.imag, abs(u0) ** 2 - abs(u1) ** 2]), abs(u0) ** 2 + abs(u1) ** 2


def test_11641_certificate_and_recompute():
    d = load("w33_pass11641_hesse_cp_is_mub_vandermonde.json")
    eq, th = d["equivariance"], d["theorem"]
    assert eq["R_Fourier_equals_11600_normalized_F"] and eq["R_phase_equals_11600_normalized_P"]
    assert eq["Bloch_actions_match_11600_(10_checks)"] == 10
    for k in ("theorem_rho_equals_3_sum_Pi", "theorem_r_equals_minus9_sum_Pi_m", "cone_identity_sumPi2_eq_3sumPi2sq",
              "rho_equals_M3_minus_M1cubed", "W_equals_c_times_Vandermonde"):
        assert th[k], k
    assert th["c"] == "-1259712" == str(-108 ** 3)
    assert th["sign_of_xyz_at_the_four_MUB_vertices"] == [1, 1, 1, 1]
    assert d["numeric"]["CP_flips_sign_W"] == 2000
    # independent numerical recomputation of r = -9 sum Pi_b m_b and the Vandermonde law
    T = _axes()
    B = _bases()
    m = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) / np.sqrt(3)
    rng = np.random.default_rng(7)
    for _ in range(50):
        psi = rng.normal(size=3) + 1j * rng.normal(size=3)
        psi /= np.linalg.norm(psi)
        n, rho = _n_rho(psi, T)
        Pi = np.array([np.prod(np.abs(b.conj().T @ psi) ** 2) for b in B])
        assert np.allclose(n, -9 * Pi @ m) and np.isclose(rho, 3 * Pi.sum())
        assert np.isclose(Pi.sum() ** 2, 3 * (Pi ** 2).sum())
        x, y, z = n
        W = (x * x - y * y) * (y * y - z * z) * (z * z - x * x)
        V = np.prod([Pi[i] - Pi[j] for i, j in itertools.combinations(range(4), 2)])
        assert np.isclose(W, -108 ** 3 * V, rtol=1e-6, atol=1e-14)


def test_11642_label_blind():
    d = load("w33_pass11642_label_blind_time.json")
    assert d["even_all_label_blind_through_D"]
    assert d["first_label_blind_odd_degree"] == 9
    lb = [d["by_degree"][str(k)]["label_blind_odd"] for k in range(6, 21)]
    assert lb == [0, 0, 0, 1, 2, 4, 7, 11, 16, 23, 31, 41, 54, 69, 86]
    assert d["all_minimal_relations_lift_to_Z"]
    assert {k: v["new_minimal"] for k, v in d["relations"].items() if v["new_minimal"]} == {
        "2": 1, "6": 1, "8": 1, "9": 4, "10": 1}


def test_11643_transvection_clock():
    s = load("w33_pass11643_hamming_cube_is_transvection_clock.json")["summary"]
    for k in ("weil_phase_equals_trace_phase", "outer_reversal_is_inverse_tick", "rotation_120",
              "chi_equals_minus_xyz_sign_of_positive_axis", "conj_is_gate_of_reflected_tick", "wigner_reversal_flips_sheet"):
        assert s[k] == 8, k
    assert s["veronese_positive_axis_stabiliser"] == 4 and s["negative_positive_axis_magic"] == 4


def test_11644_union_law_splitting():
    d = load("w33_pass11644_union_law_splitting.json")
    c = d["n2"]["counts"]
    assert c["Theorem 1 formula = decider"] == c["pairs checked against decider"] == 132192
    assert c["k != 0 with ISOTROPIC cyclic span (Theorem 2)"] == c["k != 0 solutions"] == 7776
    assert c["k = 0 and 3 does not divide order: exact (Theorem 3)"] == c[
        "k = 0: split by averaging (3 does not divide order)"]
    assert c["k = 0 and 3 | order: exact anyway"] == 0
    for cell in ("non-collinear", "collinear, different lines", "same line, other", "same line, M^2 z1 = z1",
                 "same line, M^2 z1 = -z1"):
        assert c[f"{cell}: criterion silent"] == 0, cell
    assert d["n2"]["classes"]["proved"] == 50130
    n3 = d["n3"]
    assert n3["counts"]["k != 0 with ISOTROPIC cyclic span (Theorem 2)"] == n3["counts"]["k != 0 solutions"]
    assert Fraction(n3["mass"]["proved"]) == Fraction(27200133, 28296133)
    assert Fraction(1010880, 28304640) == Fraction(1, 28)


def test_11644_theorem2_trace_identity():
    """the char-poly argument's first coefficient: tr(s^k M^-1) = tr M^-1 + k omega(M^-1 z1, z1)"""
    rng = np.random.default_rng(3)
    for _ in range(20):
        M = rng.integers(0, 3, (4, 4))
        s = np.eye(4, dtype=int)
        s[1, 0] = 1
        for k in range(3):
            lhs = np.trace(np.linalg.matrix_power(s, k) @ M) % 3
            assert lhs == (np.trace(M) + k * M[0, 1]) % 3          # e_x1^T M z1 = M[0, 1]


def test_11645_j_conjugation():
    d = load("w33_pass11645_time_reversal_is_conjugation_of_j.json")
    nm = d["numeric"]
    assert nm["sign_Im_j_equals_sign_W"] == nm["j_Clifford_invariant"] == nm["j_of_conjugate_is_conjugate"] == 20000
    assert nm["C1"] == "27" and nm["C3_pairings"] == "3*sqrt(3)"
    assert d["exact"]["j_minus_1728_is_27_square_over_cube"]
    assert d["exact"]["leading_coefficient_factorisation"] == "{7: 3, 13: 3, 19: 3}"
    T = _axes()
    rng = np.random.default_rng(11)
    for _ in range(300):
        psi = rng.normal(size=3) + 1j * rng.normal(size=3)
        psi /= np.linalg.norm(psi)
        n, _ = _n_rho(psi, T)
        x, y, z = n
        W = (x * x - y * y) * (y * y - z * z) * (z * z - x * x)
        m = (psi ** 3).sum() / (3 * psi.prod())
        j = 27 * m ** 3 * (m ** 3 + 8) ** 3 / (m ** 3 - 1) ** 3
        assert np.sign(j.imag) == np.sign(W)
        mc = (np.conj(psi) ** 3).sum() / (3 * np.conj(psi).prod())
        assert np.isclose(27 * mc ** 3 * (mc ** 3 + 8) ** 3 / (mc ** 3 - 1) ** 3, np.conj(j))
