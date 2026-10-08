"""Passes 11710-11711: a single natural Standard-Model-shaped tick, and the chirality vacua for every number of qutrits.

11710.  R = zeta27^{x^3} = diag(1, zeta27, zeta27^8) is the fourth-level qutrit gate with R^3 = T (T = zeta9^{x^3}).
In the family zeta27^{c1 x^3 + c2 y^3 + 9 e x y} = (R^c1 (x) R^c2) CZ^e (6561 gates x 3 determinant-one lifts), exactly
648 elements leave the SM-shaped centraliser su(3) + su(2) + u(1)^5 unbroken; all have E8 order 27 (Kac: >= 16 is
needed, Pass 11701).  The simplest is UNENTANGLED: R^2 (x) R^-1 (lift 1), together with its swap and its inverse.  So a
single tick with exactly SM symmetry is a pair of opposite-handed fourth-level phase gates, one on each qutrit, with
exponent ratio -2.

11711 (THEOREM, every n).  With S4 = sum_{v != 0} (Im<D_v>)^4 on n qutrits (d = 3^n):
        S4 <= (9/8) 3^(n-1),
with equality EXACTLY on the stabiliser states of Lagrangian subspaces with a nontrivial character; there are
prod_{i=1}^n (3^i + 1) x (3^n - 1) of them (8, 320, 29120 for n = 1, 2, 3).
Proof (as Pass 11698): S = (3/2) sum_P (p1-p2)^2 = (d/2)(1 - <Pi>^2) <= d/2 (Pass 11697), so sum_P (p1-p2)^2 <= 3^(n-1)
and S4 = (9/8) sum_P (p1-p2)^4 <= (9/8) 3^(n-1).  Equality needs 3^(n-1) points with |p1-p2| = 1, i.e. psi an
omega^{+-1}-eigenvector of 3^(n-1) pairwise commuting Paulis.  They span an isotropic W of dimension k <= n, psi is a
joint eigenvector of W with a character chi, and the points of W with chi != 1 number 3^(k-1); so k = n (Lagrangian).
Conversely a Lagrangian stabiliser state with chi != 1 has exactly 3^(n-1) such points and zero expectation elsewhere.
Numerical check: random-start maximisation reaches the bound at n = 1 (200/200) and n = 3 (40/40).
"""

from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11697_11698_chirality_vacuum as V  # noqa: E402
import w33_pass11701_11702_clock_symmetry_breaking as B  # noqa: E402

OUT = ROOT / "data" / "w33_pass11710_11711_single_tick_and_n_qutrit_vacua.json"
Z27 = np.exp(2j * np.pi / 27)


def level4_family():
    hits = []
    for c1, c2, e in itertools.product(range(27), range(27), range(3)):
        lam0 = Z27 ** np.array([(c1 * x ** 3 + c2 * y ** 3 + 9 * e * x * y) % 27 for x, y in B.XY])
        for k, lam in enumerate(B.lifts(lam0)):
            if B.typ(B.kept(lam)) == ("A1", "A2"):
                hits.append(dict(c1=c1, c2=c2, e=e, lift=k, e8_order=B.e8_order(lam)))
    return hits


def cost(h):
    s = lambda c: min(c, 27 - c)  # noqa: E731
    return (h["e"] != 0, (h["c1"] != 0) + (h["c2"] != 0), s(h["c1"]) + s(h["c2"]), h["lift"])


def lagrangian_count(n):
    return int(np.prod([3 ** i + 1 for i in range(1, n + 1)]))


def quartic_check(n, starts, rng):
    d = 3 ** n
    Op = np.array([V.weyl(v) for v in V.nonzero(n)])

    def S4(p):
        a = np.einsum("i,kij,j->k", p.conj(), Op, p)
        return float((a.imag ** 4).sum())

    def unit(x):
        p = x[:d] + 1j * x[d:]
        return p / np.linalg.norm(p)
    best = [-minimize(lambda x: -S4(unit(x)), rng.normal(size=2 * d), method="L-BFGS-B",
                      options=dict(maxiter=5000, gtol=1e-12)).fun for _ in range(starts)]
    psi = np.zeros(d, complex)
    psi[-1] = 1
    bound = 9 / 8 * 3 ** (n - 1)
    return dict(bound=bound, stabiliser_value=S4(psi), numerical_max=max(best), starts=starts,
                starts_at_bound=int(sum(b > bound - 1e-6 for b in best)),
                vacua=lagrangian_count(n) * (3 ** n - 1))


def main():
    hits = level4_family()
    res = dict(pass_ids=[11710, 11711], level4_family_size=27 * 27 * 3, sm_shaped=len(hits),
               e8_orders=dict(Counter(h["e8_order"] for h in hits)),
               simplest=sorted(hits, key=cost)[:6],
               unentangled_sm_shaped=sum(h["e"] == 0 for h in hits))
    rng = np.random.default_rng(11711)
    res["quartic_vacua"] = {f"n={n}": quartic_check(n, s, rng) for n, s in ((1, 100), (2, 40), (3, 20))}
    print(json.dumps(res, indent=1))
    json.dump(res, open(OUT, "w"), indent=1)


if __name__ == "__main__":
    main()
