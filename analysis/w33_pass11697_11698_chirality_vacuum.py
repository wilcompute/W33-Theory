"""Passes 11697-11698: the chirality order parameter is the Weil parity in disguise, and its quartic condenses on a
W(3,3) flag.

11697 (THEOREM, all n).  For n qutrits (d = 3^n) with symmetric Weyl operators D_v = tau^{x.z} X^x Z^z, tau = omega^2,
and the Pauli-inversion (Weil parity) operator Pi |x> = |-x>:
        S(psi) := sum_{v != 0} (Im <D_v>)^2 = (d/2) (1 - <Pi>^2)        for every unit psi.
Proof.  Im a = (a - a_{-v})/2i with a_{-v} = conj(a_v), so S = (1/2) sum |a_v|^2 - (1/2) Re sum a_v^2.  The first sum is
d - 1 for a pure state.  For the second, sum_v D_v (x) D_v = d (I (x) Pi) SWAP (I (x) Pi) (because Pi D_v Pi = D_{-v} =
D_v^dagger and sum_v D_v (x) D_v^dagger = d SWAP), so sum_{all v} a_v^2 = d <Pi>^2 and sum_{v != 0} a_v^2 = d<Pi>^2 - 1.
Consequences: the quadratic chirality functional is maximal (= d/2) exactly on the states with equal weight in the even
and odd Weil sectors, a huge degenerate set (this is why Pass 11697's numerics found a non-isolated maximum), and
V = lambda(|psi|^2 - 1)^2 - mu S is bounded below iff lambda > (d - 1) mu / ... (S <= d|psi|^4 / 2 homogeneously).

11698 (THEOREM, n = 2).  The quartic S4 := sum_{v != 0} (Im <D_v>)^4 satisfies S4 <= 27/8, with equality EXACTLY on the 320
stabiliser states of a Lagrangian line L with a nontrivial character.
Proof.  For a projective point P with eigenprojector weights p0, p1, p2 (eigenvalues 1, w, w^2), Im<D_v> = +-(sqrt3/2)(p1 -
p2) for both nonzero v in P.  Hence S = (3/2) sum_P (p1 - p2)^2 and S4 = (9/8) sum_P (p1 - p2)^4.  By 11697, S <= 9/2,
so sum_P (p1-p2)^2 <= 3; since (p1-p2)^4 <= (p1-p2)^2, S4 <= 27/8.  Equality forces every |p1 - p2| in {0, 1} and exactly
three points with |p1 - p2| = 1, i.e. psi is an eigenvector, with eigenvalue w or w^2, of three pairwise commuting Paulis.
W(3,3) is a generalised quadrangle (no triangles), so the three points lie on one line L; psi is then the stabiliser
state of L with a character that is nontrivial on exactly those three points and trivial on the fourth point p (the
kernel).  Conversely every such state gives 6 x (3/4)^2 = 27/8.  Count: 40 lines x 8 nontrivial characters = 320 =
160 flags (p in L) x 2 conjugate characters.
So the bounded potential V = lambda (|psi|^2 - 1)^2 + mu ((27/8)|psi|^8 - S4) >= 0 (lambda, mu > 0) has exactly these 320
vacua: the vacuum picks a W(3,3) line L (centraliser SU(3)^4, Pass 11687), a distinguished point p in L (the real one),
and one of two conjugate characters, i.e. the sign of Im<D_q> at the other three points q of L.  The two characters are
exchanged by the Pauli inversion Pi (Pass 11689's C-like epsilon); the potential is C- and T-even, so the selection is
spontaneous.  Scope: a statement about this potential's minima; no claim that nature minimises it.
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11697_11698_chirality_vacuum.json"
W = np.exp(2j * np.pi / 3)
TAU = W * W
X1 = np.roll(np.eye(3), 1, 0)
Z1 = np.diag([1, W, W * W])


def om(a, b):
    return sum(a[2 * i] * b[2 * i + 1] - a[2 * i + 1] * b[2 * i] for i in range(len(a) // 2)) % 3


def d1(x, z):
    return np.linalg.matrix_power(X1, x) @ np.linalg.matrix_power(Z1, z) * TAU ** ((x * z) % 3)


def weyl(v):
    M = np.eye(1)
    for i in range(len(v) // 2):
        M = np.kron(M, d1(v[2 * i], v[2 * i + 1]))
    return M


def parity(n):
    P1 = np.eye(3)[[0, 2, 1]]
    M = np.eye(1)
    for _ in range(n):
        M = np.kron(M, P1)
    return M


def nonzero(n):
    return [v for v in itertools.product(range(3), repeat=2 * n) if any(v)]


def pass11697(rng):
    out = {}
    for n in (1, 2, 3):
        d = 3 ** n
        ops = [weyl(v) for v in nonzero(n)]
        P = parity(n)
        # operator identity  sum_{all v} D_v (x) D_v = d (I (x) Pi) SWAP (I (x) Pi)
        if n <= 2:
            lhs = sum(np.kron(O, O) for O in ops) + np.eye(d * d)
            SW = np.zeros((d * d, d * d))
            for i, j in itertools.product(range(d), repeat=2):
                SW[j * d + i, i * d + j] = 1
            IP = np.kron(np.eye(d), P)
            op_err = float(np.abs(lhs - d * IP @ SW @ IP).max())
        else:
            op_err = None
        worst = 0.0
        for _ in range(20):
            psi = rng.normal(size=d) + 1j * rng.normal(size=d)
            psi /= np.linalg.norm(psi)
            a = np.array([np.vdot(psi, O @ psi) for O in ops])
            worst = max(worst, abs((a.imag ** 2).sum() - d / 2 * (1 - np.vdot(psi, P @ psi).real ** 2)))
        out[f"n={n}"] = dict(d=d, operator_identity_residual=op_err, max_residual_S_vs_parity_formula=worst,
                             max_S=d / 2)
    return out


def pass11698(rng, starts=400):
    ops = [weyl(v) for v in nonzero(2)]
    V = nonzero(2)

    def unit(x):
        p = x[:9] + 1j * x[9:]
        return p / np.linalg.norm(p)

    def S4(p):
        return float((np.array([np.vdot(p, O @ p) for O in ops]).imag ** 4).sum())

    vals, best = [], None
    for _ in range(starts):
        r = minimize(lambda x: -S4(unit(x)), rng.normal(size=18), method="BFGS", options=dict(gtol=1e-12))
        vals.append(-r.fun)
        if best is None or -r.fun > best[0]:
            best = (-r.fun, unit(r.x))
    vals = np.array(vals)
    # exact census of stabiliser states of Lagrangian lines with all characters
    pts = sorted({tuple((x * next(y for y in v if y)) % 3 for x in v) for v in V})
    lines = set()
    for a, b in itertools.combinations(pts, 2):
        if om(a, b) == 0:
            sp = {tuple((i * a[k] + j * b[k]) % 3 for k in range(4)) for i in range(3) for j in range(3)}
            lines.add(tuple(sorted(sp)))
    census = {}
    for L in lines:
        g1 = next(g for g in L if any(g))
        line1 = {tuple((t * x) % 3 for x in g1) for t in range(3)}
        g2 = next(g for g in L if g not in line1)
        A, B = weyl(g1), weyl(g2)
        for ca, cb in itertools.product(range(3), repeat=2):
            Pr = sum((W ** (-ca * s) * np.linalg.matrix_power(A, s)) for s in range(3)) @ \
                sum((W ** (-cb * s) * np.linalg.matrix_power(B, s)) for s in range(3)) / 9
            ev, U = np.linalg.eigh((Pr + Pr.conj().T) / 2)
            psi = U[:, -1]
            val = round(S4(psi), 9)
            census[val] = census.get(val, 0) + 1
    e = np.array([np.vdot(best[1], O @ best[1]) for O in ops])
    carriers = sorted({tuple((x * next(y for y in v if y)) % 3 for x in v) for v, z in zip(V, e) if abs(z.imag) > 0.3})
    return dict(starts=starts, max_S4=float(vals.max()), exact=27 / 8, all_starts_reach_max=bool(np.all(vals > 27 / 8 - 1e-7)),
                lagrangian_lines=len(lines), stabiliser_state_S4_census={str(k): v for k, v in sorted(census.items())},
                vacuum_carrier_points=len(carriers),
                carriers_pairwise_collinear=all(om(a, b) == 0 for a in carriers for b in carriers),
                vacuum_parity_expectation=float(np.vdot(best[1], parity(2) @ best[1]).real))


def main():
    rng = np.random.default_rng(11697)
    res = dict(pass_ids=[11697, 11698], p11697=pass11697(rng), p11698=pass11698(rng))
    print(json.dumps(res, indent=1))
    json.dump(res, open(OUT, "w"), indent=1)


if __name__ == "__main__":
    main()
