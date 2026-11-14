"""Pass 12665: attractors of the E6(6) cubic in the three-qubit Pauli realisation are pure states."""
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_attractor_flows():
    d = load("w33_attractor_pure_states.json")
    assert (d["dim_g"], d["dim_skew"], d["dim_sym"]) == (78, 36, 42) and d["skew_preserve_TrX2_TrX4"] < 1e-9
    assert d["pure_state_gradient_max"] < 1e-12
    assert len(d["flows"]) == 12
    for r in d["flows"]:
        assert abs(r["V_min"] - r["three_N23"]) < 1e-9 * r["V_min"] and r["spectrum_matches"]
        if r["N"] > 0:
            assert r["is_state"] and r["projector_rank2"] and r["reconstructed_pure_state_charge_error"] < 1e-6
        else:
            assert not r["is_state"] and abs(r["I_plus_X_min_eig"] + 2) < 1e-9
    assert d["N_zero_charge"]["V_min_found"] < 1e-10
    assert d["mixed_state_N"]["(0.5, 0, 0, 0)"] == 1.0


def test_mixed_state_cubic_formula_and_bound():
    rng = np.random.default_rng(0)
    for _ in range(2000):
        p = rng.dirichlet(np.ones(4)) / 2
        N = sum((8 * x - 1) ** 3 for x in p) / 24
        assert N <= 1 + 1e-12
    p = np.array([0.5, 0, 0, 0]); assert abs(sum((8 * x - 1) ** 3 for x in p) / 24 - 1) < 1e-15


def test_quaternionic_line_mixture_also_has_unit_cubic():
    """N = 1 does not force purity: rho = (|psi><psi| + |J psi><J psi|)/2 has the same charge as psi."""
    import itertools
    X1 = np.array([[0, 1], [1, 0]], complex); Z1 = np.diag([1, -1]).astype(complex)

    def P(v):
        M = np.eye(1)
        for i in range(3):
            xi, zi = v >> i & 1, v >> (3 + i) & 1
            M = np.kron(M, (1j) ** (xi * zi) * np.linalg.matrix_power(X1, xi) @ np.linalg.matrix_power(Z1, zi))
        return M

    om = lambda a, b: (bin((a & 7) & (b >> 3)).count("1") + bin((a >> 3) & (b & 7)).count("1")) % 2
    q0 = lambda v: bin((v & 7) & (v >> 3)).count("1") % 2
    a = 1 | 8
    quad = [v for v in range(1, 64) if q0(v) == om(v, a)]
    Pa = P(a)
    rng = np.random.default_rng(2)
    psi = rng.standard_normal(8) + 1j * rng.standard_normal(8); psi /= np.linalg.norm(psi)
    jpsi = Pa @ psi.conj()
    assert abs(np.vdot(psi, jpsi)) < 1e-12
    rho = (np.outer(psi, psi.conj()) + np.outer(jpsi, jpsi.conj())) / 2
    q_pure = np.array([np.vdot(psi, P(v) @ psi).real for v in quad])
    q_mix = np.array([np.trace(rho @ P(v)).real for v in quad])
    assert np.allclose(q_pure, q_mix, atol=1e-12)
    X = sum(c * P(v) for c, v in zip(q_mix, quad))
    assert abs(np.trace(X @ X @ X).real / 48 - 1) < 1e-10 and abs(np.trace(rho @ rho).real - 0.5) < 1e-12


def test_nearest_attractor_is_top_eigenspace():
    d = load("w33_attractor_of_mixed_states.json")
    assert d["n_positive"] == 10 and all(r["overlap_with_top"] > 0.9999 for r in d["rows"])
    e = load("w33_attractor_mixed_precision.json")
    for r in e:
        assert abs(r["V_vs_3N23"]) < 1e-12 and r["max_grad"] < 1e-7
        assert r["deviations_by_start"][0] < 1e-7  # start at the origin
        assert r["displacement_norms"][0] == min(r["displacement_norms"])
        assert max(r["deviations_by_start"][1:]) > 1e-4  # other minima differ: flat directions
