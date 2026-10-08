"""Pass 11680: the Heisenberg-invariant cubic tensors of n qutrits are a conjugate copy of the Hilbert space, and their
permutation symmetry is the Weil parity.

THEOREM (every n).  Let V = C^(3^n) with the n-qutrit Pauli (Heisenberg) group acting on V^(x3) by P (x) P (x) P.  The
centre acts trivially and every non-identity Pauli is traceless, so dim (V^(x3))^Heis = 3^(3n)/3^(2n) = 3^n.  The
invariants are exactly
        T_u = sum_a |a> (x) |a + u> (x) |a - u>,    u in F3^n
(Z-invariance forces the three labels to sum to 0; X-invariance forces the translation sum).  A 3-cycle of the tensor
factors fixes every T_u (a -> a + u relabels the sum), and a transposition sends T_u -> T_(-u).  Hence
  * Sym^3 part   = span{T_u + T_(-u)}: dimension (3^n + 1)/2 = the EVEN half (u ~ -u);
  * Lambda^3 part = span{T_u - T_(-u)}: dimension (3^n - 1)/2 = the ODD half;
  * mixed part    = 0;
and the transposition sign of the tensor IS the parity u -> -u, i.e. the central element -1 of Sp(2n,3).  The Clifford
group acts on the 3^n invariants by the complex conjugate of its Weil representation (checked here: even 5 / odd 4 at
n = 2, all spectra matching the conjugate Weil blocks).
  n = 1:  2 + 1  (the Hesse doublet of Pass 11641 + the determinant psi0 ^ psi1 ^ psi2);
  n = 2:  5 + 4  (the Burkhardt space of Passes 11651/11657 + the E8 Cartan of Pass 11681, whose basis is the four
                  parallel classes of lines of AG(2,3): the classical Vinberg-Elashvili Cartan subspace of Lambda^3 C^9);
  n = 3:  14 + 13.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11680_heisenberg_cubic_tensors.json"
w = np.exp(2j * np.pi / 3)
X1 = np.roll(np.eye(3), 1, axis=0)
Z1 = np.diag([1, w, w * w])


def kron_all(ms):
    out = np.eye(1)
    for m in ms:
        out = np.kron(out, m)
    return out


def check(n, rng):
    d = 3 ** n
    pts = list(itertools.product(range(3), repeat=n))
    idx = {p: i for i, p in enumerate(pts)}
    add = lambda a, b, s=1: tuple((x + s * y) % 3 for x, y in zip(a, b))  # noqa: E731

    def T(u):
        t = np.zeros((d, d, d), complex)
        for a in pts:
            t[idx[a], idx[add(a, u)], idx[add(a, u, -1)]] = 1
        return t
    Ts = {u: T(u) for u in pts}
    gens = []
    for i in range(n):
        gens.append(kron_all([X1 if j == i else np.eye(3) for j in range(n)]))
        gens.append(kron_all([Z1 if j == i else np.eye(3) for j in range(n)]))
    inv = all(np.allclose(np.einsum("ai,bj,ck,ijk->abc", g, g, g, t), t) for g in gens for t in Ts.values())
    cyc = all(np.allclose(np.transpose(t, (1, 2, 0)), t) for t in Ts.values())
    tra = all(np.allclose(np.transpose(t, (0, 2, 1)), Ts[tuple((-x) % 3 for x in u)]) for u, t in Ts.items())
    even = {frozenset([u, tuple((-x) % 3 for x in u)]) for u in pts}
    n_sym = len(even)
    n_alt = len([e for e in even if len(e) == 2])
    out = dict(dim_invariants=d, all_T_u_invariant=bool(inv), three_cycles_fix_T_u=bool(cyc),
               transposition_sends_T_u_to_T_minus_u=bool(tra), sym_dim=n_sym, alt_dim=n_alt, mixed_dim=0,
               formula_sym=(d + 1) // 2, formula_alt=(d - 1) // 2)
    if n <= 2:
        # Clifford action vs conjugate Weil blocks (Fourier and Weil phase gate on each qutrit, plus CZ for n = 2)
        F1 = np.array([[w ** (a * b) for b in range(3)] for a in range(3)]) / np.sqrt(3)
        D1 = np.diag([w ** (2 * j * j) for j in range(3)])
        cl = []
        for i in range(n):
            cl.append(kron_all([F1 if j == i else np.eye(3) for j in range(n)]))
            cl.append(kron_all([D1 if j == i else np.eye(3) for j in range(n)]))
        if n == 2:
            cl.append(np.diag([w ** (a[0] * a[1]) for a in pts]))
        Esym = np.array([(Ts[u] + Ts[tuple((-x) % 3 for x in u)]).ravel() for u in pts]).T
        Ealt = np.array([(Ts[u] - Ts[tuple((-x) % 3 for x in u)]).ravel() for u in pts]).T
        Qs = np.linalg.svd(Esym, full_matrices=False)[0][:, :out["sym_dim"]]
        Qa = np.linalg.svd(Ealt, full_matrices=False)[0][:, :out["alt_dim"]]
        neg = np.zeros((d, d))
        for a in pts:
            neg[idx[tuple((-x) % 3 for x in a)], idx[a]] = 1
        ev, Vn = np.linalg.eigh((np.eye(d) + neg) / 2)
        Ve, Vo = Vn[:, ev > 0.5], Vn[:, ev < 0.5]

        def match(A, Bm):
            ea, eb = np.linalg.eigvals(A), np.linalg.eigvals(Bm)
            for ph in eb:
                c = ph / ea[0]
                if all(np.min(np.abs(eb - c * x)) < 1e-7 for x in ea):
                    return True
            return False
        res = dict(sym_conj_even=0, alt_conj_odd=0, words=40)
        for _ in range(40):
            g = np.eye(d, dtype=complex)
            for i in rng.integers(0, len(cl), size=rng.integers(1, 7)):
                g = cl[i] @ g
            g3 = np.kron(np.kron(g, g), g)
            res["sym_conj_even"] += match(Qs.conj().T @ g3 @ Qs, (Ve.conj().T @ g @ Ve).conj())
            if Qa.shape[1]:
                res["alt_conj_odd"] += match(Qa.conj().T @ g3 @ Qa, (Vo.conj().T @ g @ Vo).conj())
        out["clifford_spectra"] = res
    return out


def main():
    rng = np.random.default_rng(11680)
    res = dict(pass_id=11680)
    for n in (1, 2, 3):
        res[f"n{n}"] = check(n, rng)
        print(n, res[f"n{n}"], flush=True)
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
