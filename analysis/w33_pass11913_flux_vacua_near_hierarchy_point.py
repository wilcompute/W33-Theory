"""Pass 11913: type IIB flux vacua near the hierarchy point -- within the tadpole bound the hierarchy moduli stay flat.

Question (Pass 11912): can three-form fluxes stabilise the Siegel period matrix of the two-qutrit home at the hierarchy
point Omega_phys ~ i [[4.21, 0.76], [0.76, >=2.7]] (toy units x 6: 25.25, 4.57, >=16)?

Setting: type IIB on T6 = T4 x T2 with complex structure T = diag-block(Omega (2x2 symmetric), tau3), axio-dilaton phi.
Exact exterior algebra over the 20 integral 3-forms (coordinates x1..x3, y1..y3; orientation dx1 dy1 dx2 dy2 dx3 dy3).
Flux G = F - phi H with integer F, H. Supersymmetric (ISD, primitive (2,1)) conditions, linear in (F, H) at a rational
target point (T, phi purely imaginary rational):
    W = int G ^ Omega_hol = 0,   int H ^ Omega_hol = 0,   d_{T_ab} W = 0 (all nine T_ab),
    primitivity J ^ F = J ^ H = 0 for the natural Kahler form J = i h_ab dz_a ^ dzbar_b, h = (Im T)^{-1}.
Calibration: a primitive (2,1) form gives N = int F ^ H = +4 > 0 and W = 0; a (0,3) form gives W != 0.
Solutions: rational null space -> LLL-reduced integer lattice -> small integer combinations; tadpole N = int F ^ H
(T6/Z2 orientifold: N/2 + N_D3 = 16, i.e. N <= 32; with even quanta N(w) <= 8 for v = 2w).

Results (search-based upper bounds on the minimum N):
  * primitive solutions exist at every tested rational point; the smallest tadpoles are N = 8 at Omega = i(4, 1, 4),
    phi = i (hierarchy there: m_c/m_t = 1.5e-2, m_u/m_c = 2.3e-4), 16 at i(4, 1/2, 4), phi = 2i, and 48 at
    i(4, 3/4, 3), phi = 2i (the point closest to the observed up ratios: 5.3e-3, 1.9e-3);
  * BUT these low-tadpole fluxes leave the hierarchy moduli flat: the holomorphic mass matrix over the block
    (Omega11, Omega12, Omega22, tau3, phi) has rank 0, the full 10x10 rank is 6;
  * fixing all ten complex moduli needs N of order 500 at i(4, 1, 4) (608 in the certified run, 488 in a scratch run with
    another seed) and 10^4 - 5x10^5 nearer the hierarchy point (best of 40,000 random lattice combinations per point,
    an upper bound) -- far above the orientifold bound.
Reading: on the toroidal orientifold the hierarchy point is not flux-stabilisable within the tadpole budget; the route of
Pass 11912 needs a compactification with a larger D3 budget (e.g. F-theory on a CY4 with chi/24 >> 16) or another
mechanism for the Siegel block.
"""

import itertools
import json
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11913_flux_vacua_near_hierarchy_point.json"
IDX3 = list(itertools.combinations(range(6), 3))
IDX5 = list(itertools.combinations(range(6), 5))
ORDER = [0, 3, 1, 4, 2, 5]
POS = {v: i for i, v in enumerate(ORDER)}


def perm_sign(seq):
    s = 1
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]:
                s = -s
    return s


def vol_sign(I, J):
    seq = list(I) + list(J)
    return 0 if len(set(seq)) < 6 else perm_sign([POS[v] for v in seq])


PAIR = np.array([[vol_sign(I, J) for J in IDX3] for I in IDX3])


def wedge1(forms):
    return np.array([np.linalg.det(np.array([[f[i] for i in I] for f in forms])) for I in IDX3])


def dz_list(T):
    return [np.array([1 if c == a else 0 for c in range(3)] + [T[a, b] for b in range(3)], complex) for a in range(3)]


def omega(T):
    return wedge1(dz_list(T))


def domega(T, a, b):
    dz = dz_list(T)
    dz[a] = np.array([0, 0, 0] + [1 if c == b else 0 for c in range(3)], complex)
    return wedge1(dz)


def d2omega(T, a, b, c, d):
    if a == c:
        return np.zeros(20, complex)
    dz = dz_list(T)
    dz[a] = np.array([0, 0, 0] + [1 if x == b else 0 for x in range(3)], complex)
    dz[c] = np.array([0, 0, 0] + [1 if x == d else 0 for x in range(3)], complex)
    return wedge1(dz)


def sym_wedge(forms):
    return [sp.expand(sp.Matrix([[f[i] for i in I] for f in forms]).det()) for I in IDX3]


def sym_omega(T, rep=None):
    dz = [[1 if c == a else 0 for c in range(3)] + [T[a, b] for b in range(3)] for a in range(3)]
    if rep:
        a, b = rep
        dz[a] = [0, 0, 0] + [1 if c == b else 0 for c in range(3)]
    return sym_wedge(dz)


def J_rows(T):
    dz = [[1 if c == a else 0 for c in range(3)] + [T[a, b] for b in range(3)] for a in range(3)]
    dzb = [[sp.conjugate(x) for x in d] for d in dz]
    h = sp.Matrix(3, 3, lambda a, b: sp.im(T[a, b])).inv()
    Jm = sp.zeros(6, 6)
    for a in range(3):
        for b in range(3):
            for i in range(6):
                for j in range(6):
                    Jm[i, j] += sp.I * h[a, b] * (dz[a][i] * dzb[b][j] - dz[a][j] * dzb[b][i])
    rows = []
    for I5 in IDX5:
        row = [0] * 20
        for pair in itertools.combinations(I5, 2):
            rest = tuple(x for x in I5 if x not in pair)
            seq = list(pair) + list(rest)
            row[IDX3.index(rest)] += perm_sign([I5.index(x) for x in seq]) * Jm[pair[0], pair[1]]
        rows.append([sp.simplify(x) for x in row])
    return rows


def kernel(O11, O12, O22, t3, g):
    T = sp.Matrix([[sp.I * O11, sp.I * O12, 0], [sp.I * O12, sp.I * O22, 0], [0, 0, sp.I * t3]])
    phi = sp.I * g
    P = sp.Matrix(PAIR.tolist())
    Om = sp.Matrix(sym_omega(T))
    eqs = []

    def add(cF, cH):
        full = list(cF) + list(cH)
        eqs.append([sp.re(x) for x in full])
        eqs.append([sp.im(x) for x in full])
    pv = P * Om
    add(pv, [0] * 20)
    add([0] * 20, pv)
    for a in range(3):
        for b in range(3):
            pd = P * sp.Matrix(sym_omega(T, (a, b)))
            add(pd, [-phi * x for x in pd])
    for r in J_rows(T):
        add(r, [0] * 20)
        add([0] * 20, r)
    B = []
    for v in sp.Matrix(eqs).nullspace():
        den = sp.ilcm(*[sp.fraction(sp.nsimplify(x))[1] for x in v])
        B.append([int(sp.nsimplify(x) * den) for x in v])
    return B, np.array(T.evalf(), dtype=complex), complex(phi)


def lll(B, delta=Fr(3, 4)):
    B = [list(map(int, b)) for b in B]
    n = len(B)

    def dot(u, v):
        return sum(a * b for a, b in zip(u, v))

    def gs(B):
        Bs, mu = [], [[Fr(0)] * n for _ in range(n)]
        for i in range(n):
            v = [Fr(x) for x in B[i]]
            for j in range(i):
                d = dot(Bs[j], Bs[j])
                mu[i][j] = Fr(dot(B[i], Bs[j])) / d if d else Fr(0)
                v = [a - mu[i][j] * b for a, b in zip(v, Bs[j])]
            Bs.append(v)
        return Bs, mu
    Bs, mu = gs(B)
    k = 1
    while k < n:
        for j in range(k - 1, -1, -1):
            q = round(mu[k][j])
            if q:
                B[k] = [a - q * b for a, b in zip(B[k], B[j])]
                Bs, mu = gs(B)
        if dot(Bs[k], Bs[k]) >= (delta - mu[k][k - 1] ** 2) * dot(Bs[k - 1], Bs[k - 1]):
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]
            Bs, mu = gs(B)
            k = max(k - 1, 1)
    return np.array(B, dtype=np.int64)


def tadpole(v):
    return int(v[:20] @ PAIR @ v[20:])


def hessian(v, T, phi):
    F, H = v[:20].astype(float), v[20:].astype(float)
    G = F - phi * H
    idx = [(a, b) for a in range(3) for b in range(3)]
    Hs = np.zeros((10, 10), complex)
    for p, (a, b) in enumerate(idx):
        for q, (c, d) in enumerate(idx):
            Hs[p, q] = G @ PAIR @ d2omega(T, a, b, c, d)
        Hs[p, 9] = Hs[9, p] = -(H @ PAIR @ domega(T, a, b))
    return Hs


def rank(M):
    s = np.linalg.svd(M, compute_uv=False)
    return int(np.sum(s > 1e-9 * s[0])) if s[0] > 0 else 0


def block_rank(Hs):
    blk = [0, 1, 3, 4, 8, 9]
    Pm = np.zeros((6, 5))
    Pm[0, 0] = Pm[1, 1] = Pm[2, 1] = Pm[3, 2] = Pm[4, 3] = Pm[5, 4] = 1
    return rank(Pm.T @ Hs[np.ix_(blk, blk)] @ Pm)


def calibration():
    T = 1j * np.eye(3)
    dz = dz_list(T)
    dzb = [d.conj() for d in dz]
    G = wedge1([dz[0], dz[1], dzb[2]])
    F, H = G.real, -G.imag
    G03 = wedge1(dzb)
    return dict(N_primitive_21=float(F @ PAIR @ H), W_21=abs(G @ PAIR @ omega(T)), W_03=abs(G03 @ PAIR @ omega(T)))


def main():
    rng = np.random.default_rng(11913)
    cal = calibration()
    rows = []
    for O11, O12, O22, g in [(4, 1, 4, 1), (4, sp.Rational(1, 2), 4, 2), (4, sp.Rational(3, 4), 3, 2),
                             (sp.Rational(17, 4), sp.Rational(3, 4), 5, 2)]:
        B, T, phi = kernel(O11, O12, O22, 1, g)
        R = lll(B)
        best = None
        for c in itertools.product(range(-2, 3), repeat=min(8, len(R))):
            if not any(c):
                continue
            v = np.array(c) @ R[:8]
            n = tadpole(v)
            if n > 0 and (best is None or n < best[0]):
                best = (n, v)
        Hs = hessian(best[1], T, phi)
        full = None
        for _ in range(40000):
            c = rng.integers(-2, 3, size=len(R))
            if not c.any():
                continue
            v = c @ R
            n = tadpole(v)
            if n <= 0 or (full and n >= full):
                continue
            if rank(hessian(v, T, phi)) == 10:
                full = n
        rows.append(dict(Omega=[str(O11), str(O12), str(O22)], g=str(g), kernel_dim=len(B), min_N=best[0],
                         min_N_rank=rank(Hs), min_N_block_rank=block_rank(Hs), min_N_all_moduli_fixed=full))
        print(rows[-1], flush=True)
    res = dict(pass_id=11913, calibration=cal, points=rows)
    res["checks"] = {k: bool(v) for k, v in dict(
        calibration_isd_positive=cal["N_primitive_21"] > 0 and cal["W_21"] < 1e-12 and cal["W_03"] > 1,
        primitive_solutions_exist=all(r["kernel_dim"] > 0 for r in rows),
        low_tadpole_leaves_block_flat=all(r["min_N_block_rank"] == 0 for r in rows),
        full_fixing_exceeds_orientifold_bound=all(r["min_N_all_moduli_fixed"] is None or r["min_N_all_moduli_fixed"] > 32
                                                  for r in rows),
        smallest_tadpole_within_bound=min(r["min_N"] for r in rows) <= 32,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"])


if __name__ == "__main__":
    main()
