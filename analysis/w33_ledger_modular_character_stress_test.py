#!/usr/bin/env python3
"""Literal Ledger modular-character stress test on a W33-native qutrit carrier.

The Law of the Ledger defines, on two copies,

    chi(A,B) = Tr[(rho x rho) Xi_B Xi_A],
    Xi_R = D_R S_R D_R,
    D_R(theta) = rho_R^s x rho_R^s,
    s = -(1+theta)/4,

where S_R swaps region R between the two replicas.  This verifier implements
that formula literally.

W33 is the projective two-qutrit Pauli commutation geometry over F_3^4.  A
rank-two Tits-building apartment is used to choose a deterministic four-point
W33 Hamiltonian on the first two qutrits.  A third qutrit is then added because
overlapping proper regions do not exist on the canonical two-qutrit carrier;
this is the minimum extension on which the Ledger's complex overlapping-window
channel can be tested.

The result is intentionally a boundary theorem, not an identification of
Tomita mirrors with W33 geometric mirrors: disjoint/coincident windows are real
to numerical precision, while genuinely overlapping windows have nonzero
Im(chi), and reversing the region order conjugates chi.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

Q = 3
N = 3
D = Q ** N
EPS = 1.0e-5
TOL = 2.0e-10


def canon(v):
    for a in v:
        if a % 3:
            inv = 1 if a % 3 == 1 else 2
            return tuple((inv * x) % 3 for x in v)
    raise ValueError("zero vector")


def symp(u, v):
    return (u[0]*v[2] + u[1]*v[3] - u[2]*v[0] - u[3]*v[1]) % 3


def w33_points():
    return sorted({canon(v) for v in itertools.product(range(3), repeat=4) if any(v)})


def first_apartment(points):
    for p0, p1, p2, p3 in itertools.permutations(range(40), 4):
        if p0 != min(p0, p1, p2, p3):
            continue
        if (symp(points[p0], points[p1]) == 0 and
            symp(points[p1], points[p2]) == 0 and
            symp(points[p2], points[p3]) == 0 and
            symp(points[p3], points[p0]) == 0 and
            symp(points[p0], points[p2]) != 0 and
            symp(points[p1], points[p3]) != 0):
            return (p0, p1, p2, p3)
    raise RuntimeError("no apartment")


def qutrit_weyl():
    omega = np.exp(2j * np.pi / 3)
    X = np.roll(np.eye(3, dtype=complex), 1, axis=0)
    Z = np.diag([omega**j for j in range(3)])
    return X, Z


def two_qutrit_pauli(v, X, Z):
    a, b, c, d = v
    return np.kron(np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Z, c),
                   np.linalg.matrix_power(X, b) @ np.linalg.matrix_power(Z, d))


def apartment_gibbs_state(points, apartment):
    X, Z = qutrit_weyl()
    U = [two_qutrit_pauli(points[i], X, Z) for i in apartment]
    A = [(u + u.conj().T) / 2 for u in U]
    B = [(u - u.conj().T) / (2j) for u in U]
    C = (X + X.conj().T) / 2
    D3 = (Z + Z.conj().T) / 2
    E = (X @ Z + (X @ Z).conj().T) / 2
    H = (0.7 * np.kron(A[0], C) +
         0.9 * np.kron(B[1], D3) +
         1.1 * np.kron(A[2], E) +
         0.8 * np.kron(B[3], C) +
         0.5 * np.kron(np.eye(9), D3))
    w, v = np.linalg.eigh(H)
    rho = (v * np.exp(-w)) @ v.conj().T
    rho /= np.trace(rho)
    return rho, H


def digits(i, n=N, q=Q):
    out = [0] * n
    for k in range(n - 1, -1, -1):
        out[k] = i % q
        i //= q
    return out


def basis_index(ds, q=Q):
    z = 0
    for a in ds:
        z = z*q + a
    return z


def partial_trace(rho, R, n=N, q=Q):
    R = tuple(sorted(R))
    C = tuple(i for i in range(n) if i not in R)
    T = rho.reshape([q] * (2*n))
    perm = list(R) + list(C) + [i+n for i in R] + [i+n for i in C]
    T = T.transpose(perm)
    dr, dc = q**len(R), q**len(C)
    T = T.reshape(dr, dc, dr, dc)
    return np.einsum("aibi->ab", T)


def embed(op, R, n=N, q=Q):
    d = q**n
    bs = [digits(i, n, q) for i in range(d)]
    R = tuple(sorted(R))
    C = tuple(i for i in range(n) if i not in R)
    out = np.zeros((d, d), dtype=complex)
    for i, di in enumerate(bs):
        for j, dj in enumerate(bs):
            if all(di[c] == dj[c] for c in C):
                ri = basis_index([di[r] for r in R], q)
                rj = basis_index([dj[r] for r in R], q)
                out[i, j] = op[ri, rj]
    return out


def positive_power(a, s):
    w, v = np.linalg.eigh((a + a.conj().T) / 2)
    if np.min(w) <= 0:
        raise ValueError("state is not faithful")
    return (v * (w**s)) @ v.conj().T


def swap_region(R, n=N, q=Q):
    d = q**n
    bs = [digits(i, n, q) for i in range(d)]
    R = set(R)
    p = np.empty(d*d, dtype=int)
    for a, da in enumerate(bs):
        for b, db in enumerate(bs):
            ea, eb = da.copy(), db.copy()
            for r in R:
                ea[r], eb[r] = eb[r], ea[r]
            p[a*d+b] = basis_index(ea, q)*d + basis_index(eb, q)
    S = np.zeros((d*d, d*d), dtype=complex)
    S[p, np.arange(d*d)] = 1
    return S


def character_table(rho, theta):
    regions = [frozenset(s) for k in range(1, N) for s in itertools.combinations(range(N), k)]
    reduced = {R: partial_trace(rho, R) for R in regions}
    swaps = {R: swap_region(R) for R in regions}
    rr = np.kron(rho, rho)
    xis = {}
    s = -(1.0 + theta) / 4.0
    for R in regions:
        e = embed(positive_power(reduced[R], s), R)
        dress = np.kron(e, e)
        xis[R] = dress @ swaps[R] @ dress
    return regions, {(A, B): np.trace(rr @ xis[B] @ xis[A]) for A in regions for B in regions}


def main():
    points = w33_points()
    edges = sum(symp(points[i], points[j]) == 0 for i in range(40) for j in range(i+1, 40))
    apartment = first_apartment(points)
    rho, _ = apartment_gibbs_state(points, apartment)
    regions, c0 = character_table(rho, 0.0)
    _, cp = character_table(rho, EPS)
    _, cm = character_table(rho, -EPS)

    rows = []
    classes = {"coincident": [], "disjoint": [], "overlap": []}
    conjugation_error = 0.0
    for A in regions:
        for B in regions:
            z = c0[A, B]
            keff = -(np.log(cp[A, B]) - np.log(cm[A, B])) / (2*EPS)
            kind = "coincident" if A == B else ("disjoint" if not (A & B) else "overlap")
            classes[kind].append((z, keff))
            conjugation_error = max(conjugation_error, abs(c0[B, A] - np.conjugate(z)))
            rows.append({"A": sorted(A), "B": sorted(B), "class": kind,
                         "chi_real": float(z.real), "chi_imag": float(z.imag),
                         "Keff_real": float(keff.real), "Keff_imag": float(keff.imag)})

    def max_im(kind, which):
        j = 0 if which == "chi" else 1
        return max(abs(pair[j].imag) for pair in classes[kind])

    coincidence_error = 0.0
    for R in regions:
        expected = float((Q**len(R))**2)
        coincidence_error = max(coincidence_error, abs(c0[R, R].real-expected), abs(c0[R, R].imag))

    checks = {
        "w33_points_40": len(points) == 40, "w33_edges_240": edges == 240,
        "apartment_is_coordinate_quadrangle": apartment == (0, 1, 4, 13),
        "rho_faithful": float(np.min(np.linalg.eigvalsh(rho))) > 1e-6,
        "rho_is_complex": float(np.max(np.abs(rho.imag))) > 1e-3,
        "coincidence_rank_squared": coincidence_error < 1e-9,
        "disjoint_character_real": max_im("disjoint", "chi") < TOL,
        "coincident_character_real": max_im("coincident", "chi") < TOL,
        "overlap_character_complex": max_im("overlap", "chi") > 1e-4,
        "overlap_modular_energy_complex": max_im("overlap", "Keff") > 1e-5,
        "region_order_conjugates": conjugation_error < 2e-10,
    }
    checks = {k: bool(v) for k, v in checks.items()}
    assert all(checks.values()), checks
    out = {
        "schema": "w33.ledger.modular-character-stress.v1",
        "status": "PASS_LITERAL_CHARACTER_WITH_THREE_QUTRITS",
        "source_formula": "chi=Tr[(rho tensor rho) Xi_B Xi_A], Xi_R=D_R S_R D_R, D_R=rho_R^(-(1+theta)/4) tensor itself",
        "w33_anchor": {"interpretation": "first two qutrits carry the W33 two-qutrit Pauli geometry",
                       "points": len(points), "edges": edges, "apartment_point_indices": list(apartment),
                       "apartment_projective_labels": [list(points[i]) for i in apartment]},
        "state": {"hilbert_dimension": D, "sites": 3, "local_dimension": 3,
                  "min_eigenvalue": float(np.min(np.linalg.eigvalsh(rho))),
                  "max_entry_imag": float(np.max(np.abs(rho.imag)))},
        "audit": {"proper_regions": [sorted(R) for R in regions], "ordered_region_pairs": len(rows),
                  "max_abs_im_chi": {k: max_im(k, "chi") for k in classes},
                  "max_abs_im_modular_energy": {k: max_im(k, "Keff") for k in classes},
                  "max_order_reversal_conjugation_error": conjugation_error,
                  "max_coincidence_rank2_error": coincidence_error},
        "boundary": [
            "The W33 quantum carrier itself is two qutrits; it has no genuinely overlapping pair of proper tensor-factor regions.",
            "A third qutrit is therefore a minimal extension for the Ledger overlapping-window phase test.",
            "The test implements the Ledger character literally but does not identify Tomita modular conjugations with W33 geometric anti-symplectic mirrors."],
        "checks": checks,
        "sample_rows": sorted(rows, key=lambda r: abs(r["chi_imag"]), reverse=True)[:8],
    }
    path = Path("data/PART_LEDGER_MODULAR_CHARACTER_STRESS_TEST.json")
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))
    return out


if __name__ == "__main__":
    main()
