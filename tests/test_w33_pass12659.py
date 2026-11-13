"""Pass 12659: regulus constants, odd-characteristic zeros, quotient lemma, quotient theta."""
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_regulus_constants():
    d = load("w33_regulus_constants_q16_q32.json")
    for q in (2, 4, 16):
        assert abs(d[f"q{q}"]["c"] - 1) < 1e-8
    assert abs(d["q8"]["c"] - 2.498508646688) < 1e-8
    assert abs(d["q4"]["H2_deficit_bits"] - 5 * np.log2(6 / 5)) < 1e-9


def test_odd_characteristic_quadratic_phase_zeros():
    d = load("w33_regulus_odd_characteristic.json")
    for p in (3, 5, 7):
        r = d[str(p)]
        assert r["n_quadratic_phase_zeros"] == (p - 1) ** 2 // 2 and abs(r["min_quadratic_F"]) < 1e-12
        for a, b in r["zeros"]:
            assert pow(a * b % p, (p - 1) // 2, p) == p - 1  # ab is a non-residue


def test_quadratic_phase_unbiased_p3_direct():
    p = 3
    w = np.exp(2j * np.pi / p)
    xs = np.arange(p)
    A = w ** (1 * xs[:, None] ** 2 + 2 * xs[None, :] ** 2) / p
    Xi = w ** np.outer(xs, xs)
    assert np.allclose(np.abs(A) ** 2, 1 / 9)
    for t in range(p):
        K = Xi.conj() @ (A * w ** (t * np.outer(xs, xs))) @ Xi.conj() / p
        assert np.allclose(np.abs(K) ** 2, 1 / 9)


def test_quotient_theta_bounds():
    d = load("w33_five_qubit_quotient_theta.json")
    for k in ("quotient_type27", "quotient_type17"):
        assert 28.5 < d[k]["theta_upper"] < 30.2 and 0.025 < d[k]["minF_lower_bound"] < d[k]["numerical_minF"]


def test_quotient_lemma_numerically():
    reg = load("w33_regulus_mub_sets.json")["q4"]["codes"]
    n, d, lo = 4, 16, 15
    pos = [(i, j) for i in range(n) for j in range(i, n)]
    X1 = np.array([[0, 1], [1, 0]], complex)
    Z1 = np.diag([1, -1]).astype(complex)

    def P(v):
        M = np.eye(1)
        for i in range(n):
            xi, zi = v >> i & 1, v >> (n + i) & 1
            M = np.kron(M, (1j) ** (xi * zi) * np.linalg.matrix_power(X1, xi) @ np.linalg.matrix_power(Z1, zi))
        return M

    C = set()
    for x in range(1, d):
        C.add(x)
        C.add(x << n)
        for c in reg:
            z = 0
            for i in range(n):
                bit = 0
                for j in range(n):
                    a, b = min(i, j), max(i, j)
                    if c >> pos.index((a, b)) & 1 and x >> j & 1:
                        bit ^= 1
                z |= bit << i
            C.add(x | (z << n))
    om = lambda a, b: (bin((a & lo) & (b >> n)).count("1") + bin((a >> n) & (b & lo)).count("1")) % 2
    q0 = lambda v: bin((v & lo) & (v >> n)).count("1") % 2
    assert len(C) == 75 and all(q0(v) == 0 for v in C)
    p = next(v for v in range(1, 256) if q0(v) == 1)
    ev, V = np.linalg.eigh(P(p))
    Vp = V[:, ev > 0]
    rng = np.random.default_rng(0)
    phi = Vp @ (rng.standard_normal(8) + 1j * rng.standard_normal(8))
    phi /= np.linalg.norm(phi)
    tot = sum(np.vdot(phi, P(v) @ phi).real ** 2 for v in C)
    comm = sum(np.vdot(phi, P(v) @ phi).real ** 2 for v in C if om(v, p) == 0)
    assert abs(tot - comm) < 1e-10
    assert all(not ((v in C) and ((v ^ p) in C)) for v in range(1, 256) if om(v, p) == 0)  # cosets inside p-perp
