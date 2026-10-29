"""Exact finite-cover census and a variational near-zero bound.

The finite-field screen is only a necessary condition.  Each survivor is
independently reduced modulo the appropriate integer cyclotomic polynomial.
No conclusion about uncomputed cover sizes is inferred from the census.
"""
from itertools import product
from math import gcd, isqrt
from pathlib import Path
import hashlib
import json
import sys

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_20261027_five_front_followthrough as prior
import w33_20261027_native_bloch_face_module as native

N = np.array([[10, -5, 1, -6], [-5, 10, -5, 6],
              [1, -5, 10, -6], [-6, 6, -6, 12]], dtype=np.int64)
R = np.array([[1, 0, 5, -5, 1, 0], [0, 1, -1, 0, 1, 0],
              [0, 0, 5, -5, 0, 1]], dtype=np.int64)


def cyclotomic_zero(labels, n, reduced_powers):
    """Test 2Q(zeta**labels - 1)=0 in Z[x]/(Phi_n)."""
    coefficients = [0] * n
    for i, j in product(range(4), repeat=2):
        m = int(N[i, j]); a, b = labels[i], labels[j]
        coefficients[(a + b) % n] += m
        coefficients[a] -= m; coefficients[b] -= m
        coefficients[0] += m
    return all(sum(coefficients[k] * reduced_powers[k][j] for k in range(n)) == 0
               for j in range(len(reduced_powers[0])))


def census(n):
    assert 2 <= n <= 64
    prime = ((10_000_000 + n - 1) // n) * n + 1
    while not sp.isprime(prime):
        prime += n
    assert prime < 11_000_000 and 100 * prime * prime < 2**63
    root = pow(int(sp.primitive_root(prime)), (prime - 1) // n, prime)
    assert int(sp.n_order(root, prime)) == n
    d = np.array([(pow(root, j, prime) - 1) % prime for j in range(n)],
                 dtype=np.int64)
    c, e = d[:, None], d[None, :]
    tail = (10*c*c + 12*e*e - 12*c*e) % prime
    candidates = []
    for i, a in enumerate(d):
        for j, b in enumerate(d):
            values = (tail + 10*a*a + 10*b*b - 10*a*b + 2*a*c
                      - 12*a*e - 10*b*c + 12*b*e) % prime
            candidates.extend((i, j, int(k), int(l)) for k, l in np.argwhere(values == 0))
    x = sp.Symbol("x")
    phi = sp.Poly(sp.cyclotomic_poly(n, x), x)
    powers = []
    for k in range(n):
        rem = sp.Poly(x**k, x).rem(phi)
        powers.append([int(rem.nth(j)) for j in range(phi.degree())])
    zeros = [v for v in candidates if cyclotomic_zero(v, n, powers)]
    assert (0, 0, 0, 0) in zeros
    primitive = [v for v in zeros if gcd(n, *v) == 1]
    nonidentity = [v for v in zeros if any(v)]
    return dict(n=n, screen_prime=int(prime), screen_primitive_root=int(root),
                modular_candidates=len(candidates), cyclotomic_degree=phi.degree(),
                nonidentity_count=len(nonidentity),
                primitive_nonidentity_count=len(primitive),
                nonidentity_loop_labels=[list(v) for v in nonidentity])


def occurrence_bound(path, voltage):
    """Per-edge sum of position l1 norms, a Lipschitz row bound."""
    bounds = np.zeros(135, dtype=np.int64)
    pos = np.zeros(4, dtype=np.int64)
    for edge, sign in path:
        edge, sign = int(edge), int(sign)
        if sign < 0:
            pos -= voltage[edge]
        bounds[edge] += int(np.abs(pos).sum())
        if sign > 0:
            pos += voltage[edge]
    return bounds


def soft_mode_control():
    _, voltage, edges, loops, W, commutators, _, _ = prior.inputs()
    baseline = json.loads((ROOT / "data/w33_pass12341_12345_geometry.json").read_text())
    assert N.tolist() == baseline["symbol"]["N"]
    faces = json.loads((ROOT / "data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json").read_text())
    short = [v["boundary"] for v in faces["independent_face_basis"]]
    path_bounds = np.stack([occurrence_bound(q, voltage) for q in short])
    comm_bounds = np.stack([occurrence_bound(q, voltage) for q in commutators])
    matrix_bounds = np.vstack((path_bounds, np.abs(R) @ comm_bounds))
    curl_lipschitz_squared = int(np.square(matrix_bounds).sum())
    gauge_lipschitz_squared = int(np.square(np.abs(voltage).sum(axis=1)).sum())
    loop_length = len(loops[0])
    assert loop_length == 4 and list(W[0]) == [0, 1, 1, -1]
    edge, sign = loops[0][0]
    root = edges[edge][0 if sign > 0 else 1]
    current = root
    for edge, sign in loops[0]:
        a, b = edges[edge]
        start, end = (a, b) if sign > 0 else (b, a)
        assert current == start
        current = end
    assert root == current == 0
    # Connectivity gives a path of <=26 quotient edges to each vertex.
    seen = {0}; frontier = [0]
    while frontier:
        a = frontier.pop()
        for u, v in edges:
            b = v if u == a else u if v == a else None
            if b is not None and b not in seen:
                seen.add(b); frontier.append(b)
    assert len(seen) == 27
    # sigma_min(D(k*)) >= 1 / sqrt(18 L^2 + 1404).
    sigma_inverse_squared = 18*loop_length**2 + 1404
    # ceil(16 sqrt(L_G^2 / sigma_lower^2)), without floating rounding.
    radicand = 256*gauge_lipschitz_squared*sigma_inverse_squared
    n0 = isqrt(radicand) + (isqrt(radicand)**2 < radicand)
    w = json.loads((ROOT / "data/w33_pass12340_mixed_loop_exception.json").read_text())["witness"]
    omega = np.exp(2j*np.pi/3)
    vector = np.array(w["a"], dtype=float) + omega*np.array(w["b"], dtype=float)
    vector /= np.linalg.norm(vector)
    kstar = np.array([2*np.pi/3, 2*np.pi/3, 0, 0])
    curl = lambda k: np.vstack((native.curl(short, voltage, k),
                               R @ native.curl(commutators, voltage, k)))
    Gstar = native.gradient(voltage, edges, kstar)
    assert np.linalg.norm(curl(kstar) @ vector) < 1e-11
    assert np.linalg.norm(Gstar.conj().T @ vector) < 1e-11
    numeric = []
    for n in (31, 40, 61, 100, 127, 160):
        m = (n + 1)//3
        k = np.array([2*np.pi*m/n, 2*np.pi*m/n, 0, 0])
        G = native.gradient(voltage, edges, k)
        transverse = vector - G @ np.linalg.lstsq(G, vector, rcond=None)[0]
        rayleigh = float(np.linalg.norm(curl(k) @ transverse)**2 /
                         np.linalg.norm(transverse)**2)
        numeric.append(dict(n=n, rayleigh_upper_bound=rayleigh,
                            n_squared_times_rayleigh=n*n*rayleigh))
    return dict(period_path_length=loop_length,
                gradient_lipschitz_squared=gauge_lipschitz_squared,
                curl_lipschitz_squared=curl_lipschitz_squared,
                sigma_inverse_lower_bound_squared=sigma_inverse_squared,
                certified_n0=n0, certified_rayleigh_coefficient=64*curl_lipschitz_squared,
                numeric_rayleigh_controls=numeric,
                bound="For n >= n0, lambda_min on the transverse sector at a grid character approaching (omega,omega,1,1) is <= certified_rayleigh_coefficient/n^2.")


def main():
    rows = [census(n) for n in range(2, 65)]
    for item in rows:
        n = item["n"]
        assert item["nonidentity_count"] == (10 if n % 3 == 0 else 0)
        assert item["primitive_nonidentity_count"] == (10 if n == 3 else 0)
    result = dict(schema="w33.pass12341_12345.torsion_census.v1", census=rows,
                  soft_mode=soft_mode_control(),
                  scope="Exact enumeration only for periods 2 through 64; no all-period torsion classification.",
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (ROOT / "data/w33_pass12341_12345_torsion_census.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(dict(periods=len(rows), soft_mode=result["soft_mode"]), indent=2))


if __name__ == "__main__":
    main()
