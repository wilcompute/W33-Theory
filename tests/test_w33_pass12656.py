"""Pass 12656: E6 cubic = Tr X^3 over the 27 quadric three-qubit Paulis; quaternionic sum rule; Shannon sqrt60."""
import itertools
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))
X1 = np.array([[0, 1], [1, 0]], complex); Z1 = np.diag([1, -1]).astype(complex)


def _pauli(v, n=3):
    M = np.eye(1)
    for i in range(n):
        xi, zi = v >> i & 1, v >> (n + i) & 1
        M = np.kron(M, (1j) ** (xi * zi) * np.linalg.matrix_power(X1, xi) @ np.linalg.matrix_power(Z1, zi))
    return M


def test_sum_rule_and_unit_cubic_for_all_28_quaternionic_structures():
    om = lambda a, b: (bin((a & 7) & (b >> 3)).count("1") + bin((a >> 3) & (b & 7)).count("1")) % 2
    q0 = lambda v: bin((v & 7) & (v >> 3)).count("1") % 2
    Ps = {v: _pauli(v) for v in range(1, 64)}
    anti = [a for a in range(1, 64) if q0(a) == 1]
    assert len(anti) == 28
    rng = np.random.default_rng(3)
    for a in anti:
        quad = [v for v in range(1, 64) if q0(v) == om(v, a)]
        assert len(quad) == 27
        psi = rng.standard_normal(8) + 1j * rng.standard_normal(8); psi /= np.linalg.norm(psi)
        z = np.array([np.vdot(psi, Ps[v] @ psi).real for v in quad])
        X = sum(zz * Ps[v] for zz, v in zip(z, quad))
        assert abs((z ** 2).sum() - 3) < 1e-10
        assert abs(np.trace(X @ X @ X).real / 48 - 1) < 1e-10
        ev = np.round(np.linalg.eigvalsh(X), 8)
        assert sorted(ev.tolist()) == [-1.0] * 6 + [3.0, 3.0]


def test_cubic_from_paulis_certificate():
    d = load("w33_e6_cubic_from_three_qubit_paulis.json")
    assert d["TrX3_over_48_equals_N"] and d["adjoint_identity"] and d["stabiliser_dim"] == 78
    assert not d["control_unsigned_adjoint_identity"] and d["n_stabiliser_states"] == 1080
    assert d["stabiliser_states_(support,is_line,N)"] == [dict(support=3, is_line=True, N=1, count=1080)]
    for k in ("Z2_min", "Z2_max"):
        assert abs(d[k] - 3) < 1e-6
    for k in ("N_min", "N_max"):
        assert abs(d[k] - 1) < 1e-6


def test_transpose_lp_trivial_and_identities():
    d = load("w33_transpose_lp_bound.json")
    assert all(max(v) < 1e-9 for v in d["identity_residuals"].values())
    for c in d["cases"]:
        assert abs(c["LP"] - c["trivial"]) < 1e-5 and not c["closes"]


def test_general_n_quadric_sum_rule_n4():
    n, d = 4, 16
    lo = d - 1
    om = lambda a, b: (bin((a & lo) & (b >> n)).count("1") + bin((a >> n) & (b & lo)).count("1")) % 2
    q0 = lambda v: bin((v & lo) & (v >> n)).count("1") % 2
    a = 1 | (1 << n)
    quad = [v for v in range(1, d * d) if q0(v) == om(v, a)]
    rng = np.random.default_rng(5); psi = rng.standard_normal(d) + 1j * rng.standard_normal(d); psi /= np.linalg.norm(psi)
    s = sum(np.vdot(psi, _pauli(v, n) @ psi).real ** 2 for v in quad)
    assert len(quad) == 2 ** (2 * n - 1) - 2 ** (n - 1) - 1 and abs(s - (d / 2 - 1)) < 1e-10


def test_shannon_60_verified():
    d = load("w33_shannon_symmetric_codes.json")
    assert d["control_C5"] == 5 and d["best_size"] == 60 and d["best_record"]["status"] == "OPTIMAL" and d["best_record"]["order"] == 5
    S = [tuple(x) for x in d["best_set"]]
    # independent rebuild of the producer graph and pairwise check
    pts = sorted({min(tuple((c * x) % 3 for x in v) for c in (1, 2)) for v in itertools.product(range(3), repeat=4) if any(v)})
    om = lambda u, v: (u[0] * v[2] + u[1] * v[3] - u[2] * v[0] - u[3] * v[1]) % 3
    close = lambda i, j: i == j or om(pts[i], pts[j]) == 0
    assert len(set(S)) == 60
    assert not any(close(x[0], y[0]) and close(x[1], y[1]) for x, y in itertools.combinations(S, 2))
