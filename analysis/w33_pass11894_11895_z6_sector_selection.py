"""Passes 11894-11895: the Z6 W(3,3) orbifold sector -- flat modulus, one-loop SU(3)xSU(2)xU(1), and its matter.

Z6 = (A8-class Z3 element, the W(3,3) twist) x (sigma, the D8 'parity': +1 on the 5 CZ3 zero-phase levels {xy = 0},
-1 on the other 4; flagship holonomies, w33_paper 79.81-79.86). Local gauge algebra s(u5 + u4) (dim 40). Untwisted
matter: planes 1, 2 (rotation 1/6) carry the sigma-odd 44 of the 84 = the Z6 grade-1 space; plane 3 (rotation 2/3,
the qutrit plane) the sigma-even 40.

  * 11894 FLAT MODULUS. For (S(GL5 x GL4), sigma-odd 44): generic stabiliser 0, commuting subspace of a generic element 4
    -- a 4-dimensional Vinberg Cartan (the Z6 regular-element degrees 12, 18, 24, 30). After the Kempf-Ness flow to a
    minimal vector (|mu| < 1e-10) the Cartan through it lies in mu^{-1}(0) (|mu| ~ 1e-11), and on it the vector-mass
    traces are constant (sum e = 10, sum e^2 = 4): the Z3 Siegel modulus survives at order six, in the family planes.
    The qutrit plane (sigma-even 40) has a 2-dimensional generic stabiliser: 2-dimensional moduli.
  * 11895 ONE LOOP AND THE STANDARD-MODEL TEST. The bosonic one-loop function F = sum e^2 log e on that Cartan has its
    global minimum -3 log 3 (all runs), spectrum 0^12 (1/3)^27 1^1. At the polished point the unbroken compact algebra
    has dimension 12, rank 4, centre 1 and three ideals of dimensions 1, 3, 8: SU(3) x SU(2) x U(1); on C^9 the 5 = 3 + 2
    and the 4 = 3 + 1, so the SU(3) is diagonal in the two triplets, not Georgi-Glashow colour. Its matter: each family
    plane 44 = 2(3,1)_{-1} + (3,2)_{-1/2} + 3(1,1)_0 + (8,1)_0 + (3,2)_{1/2} + (6,2)_{1/2} + (3,1)_{1}; the qutrit plane
    40 likewise contains an octet and a sextet. Colour octets and sextets, and no colour-singlet SU(2) doublet (no lepton
    doublet): the right gauge group with the wrong matter -- no Standard Model in the untwisted Z6 sector at this vacuum.
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares, minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11681_e8_from_two_qutrits as E  # noqa: E402

OUT = ROOT / "data" / "w33_pass11894_11895_z6_sector_selection.json"
PTS = [(a, b) for a in range(3) for b in range(3)]
SIG = np.array([1.0 if a * b % 3 == 0 else -1.0 for a, b in PTS])


def sigma_split():
    Sg = np.diag(SIG)
    I84 = np.eye(84)
    Smat = np.array([E.sorted_c(np.einsum("ai,bj,ck,ijk->abc", Sg, Sg, Sg, E.full(I84[i]))) for i in range(84)]).T
    ev, V = np.linalg.eigh(Smat)
    return V[:, ev > 0], V[:, ev < 0]


def g0_basis():
    B = []
    for i in range(9):
        for j in range(i + 1, 9):
            if SIG[i] == SIG[j]:
                A = np.zeros((9, 9), complex)
                A[i, j], A[j, i] = 1, -1
                B.append(A / np.sqrt(2))
                A = np.zeros((9, 9), complex)
                A[i, j], A[j, i] = 1j, 1j
                B.append(A / np.sqrt(2))
    Qd, _ = np.linalg.qr(np.vstack([np.ones(9), np.eye(9)[:8]]).T)
    B += [1j * np.diag(Qd[:, m]) for m in range(1, 9)]
    return np.array(B)


B = g0_basis()
HERM = [1j * A for A in B]


def act(A, x):
    return E.sorted_c(E._act(A, E.full(x)))


def mu(x):
    return np.array([np.vdot(x, act(Hm, x)).real for Hm in HERM])


def stab_dim_gl(x, sig_blocks=True):
    T = E.full(x)
    G = [np.eye(9)[:, [i]] @ np.eye(9)[[j], :] for i in range(9) for j in range(9) if SIG[i] == SIG[j]]
    M = np.array([E.sorted_c(E._act(A, T)) for A in G]).T
    s = np.linalg.svd(M, compute_uv=False)
    return int(np.sum(s < 1e-9 * s[0]))


def commuting_dim(y, V):
    Cm = np.array([E.wedge_star(y, V[:, k]) for k in range(V.shape[1])]).T
    s = np.linalg.svd(Cm, compute_uv=False)
    return int(np.sum(s < 1e-9 * s[0]))


def kempf_ness(y, iters=6000):
    y = y / np.linalg.norm(y)
    for it in range(iters):
        m = mu(y)
        if np.linalg.norm(m) < 1e-12:
            break
        y = y - 0.2 * sum(m[a] * act(HERM[a], y) for a in range(len(HERM)))
        y /= np.linalg.norm(y)
    return y, float(np.linalg.norm(mu(y)))


def spectrum(C6, c):
    x = C6 @ c
    T = E.full(x)
    T = T / np.linalg.norm(T)
    V = np.array([E._act(A, T).ravel() for A in B])
    return np.sort(np.linalg.eigvalsh((V.conj() @ V.T).real))


def F_of(e):
    e = e[e > 1e-12]
    return float(np.sum(e ** 2 * np.log(e)))


def unbroken(C6, c):
    x = C6 @ c
    x = x / np.linalg.norm(x)
    T = E.full(x)
    Mm = np.array([E._act(A, T).ravel() for A in B]).T
    _, sr, vr = np.linalg.svd(np.vstack([Mm.real, Mm.imag]))
    k = int(np.sum(sr < 1e-8 * sr[0]))
    R = vr[-k:]
    return [sum(R[i, a] * B[a] for a in range(len(B))) for i in range(k)]


def structure(gens, rng):
    k = len(gens)
    Gf = np.array([g.ravel() for g in gens])

    def coords(m):
        return np.linalg.lstsq(Gf.T, m.ravel(), rcond=None)[0]
    ad = [np.array([coords(a @ b - b @ a) for b in gens]).T for a in gens]
    cen = int(np.sum(np.linalg.svd(np.vstack(ad), compute_uv=False) < 1e-8))
    g = sum(rng.normal() * h for h in gens)
    rank = int(np.sum(abs(np.linalg.eigvals(np.array([coords(g @ b - b @ g) for b in gens]).T)) < 1e-8))
    A_ = np.vstack([np.kron(np.eye(k), a.real) - np.kron(a.real.T, np.eye(k)) for a in ad])
    _, sv, vv = np.linalg.svd(A_)
    comm = int(np.sum(sv < 1e-8))
    X = sum(rng.normal() * vv[-i - 1].reshape(k, k).T for i in range(comm))
    w_, V_ = np.linalg.eig(X)
    groups = {}
    for i, val in enumerate(np.round(w_, 6)):
        groups.setdefault(val, []).append(i)
    ideals = sorted([[sum(V_[a, i] * gens[a] for a in range(k)) for i in idx] for idx in groups.values()], key=len)
    blocks = {}
    for name, idx in (("5", np.where(SIG > 0)[0]), ("4", np.where(SIG < 0)[0])):
        reps = [g_[np.ix_(idx, idx)] for g_ in gens]
        d = len(idx)
        A9 = np.vstack([np.kron(np.eye(d), r) - np.kron(r.T, np.eye(d)) for r in reps])
        _, s9, v9 = np.linalg.svd(A9)
        kk = int(np.sum(s9 < 1e-8))
        Xb = sum(rng.normal() * v9[-i - 1].reshape(d, d).T for i in range(kk))
        blocks[name] = sorted(Counter(np.round(np.linalg.eigvals(Xb), 6)).values())
    return dict(dim=k, centre=cen, rank=rank, ideal_dims=[len(i) for i in ideals], blocks=blocks), ideals


def decompose(ideals, Vsub):
    Yb, SU2b, SU3b = ideals
    Y = Yb[0]
    evY = np.linalg.eigvals(-1j * Y).real
    Y = Y / evY[np.argmax(abs(evY))]

    def rep84(g):
        return np.array([E.sorted_c(E._act(g, E.full(np.eye(84)[i]))) for i in range(84)]).T

    def casimir(basis):
        Gm = np.array([[np.trace(a @ b) for b in basis] for a in basis])
        Gi = np.linalg.inv(Gm)
        R = [rep84(g) for g in basis]
        return sum(Gi[i, j] * R[i] @ R[j] for i in range(len(basis)) for j in range(len(basis)))
    RY, C2, C3 = rep84(-1j * Y), casimir(SU2b), casimir(SU3b)
    P = Vsub
    mY, m2, m3 = (np.linalg.lstsq(P, Mx @ P, rcond=None)[0] for Mx in (RY, C2, C3))
    w, Vv = np.linalg.eig(mY + np.pi * m2 + np.e * m3)
    out = Counter()
    names3 = {0.0: "1", 1.3333: "3", 3.0: "8", 3.3333: "6"}
    names2 = {0.0: "1", 1.5: "2"}
    for i in range(len(w)):
        v = Vv[:, i]
        nrm = v.conj() @ v
        y = round(float((v.conj() @ mY @ v / nrm).real), 4) + 0.0
        c2 = round(float((v.conj() @ m2 @ v / nrm).real), 4) + 0.0
        c3 = round(float((v.conj() @ m3 @ v / nrm).real), 4) + 0.0
        out[f"({names3.get(c3, c3)},{names2.get(c2, c2)})_{y}"] += 1
    return dict(out)


def main():
    rng = np.random.default_rng(11894)
    Vp, Vm = sigma_split()
    yodd = Vm @ (rng.normal(size=44) + 1j * rng.normal(size=44))
    yeven = Vp @ (rng.normal(size=40) + 1j * rng.normal(size=40))
    res = dict(pass_ids=[11894, 11895], split=dict(even=Vp.shape[1], odd=Vm.shape[1]))
    res["grade1_odd"] = dict(generic_stabiliser=stab_dim_gl(yodd), commuting=commuting_dim(yodd, Vm))
    res["qutrit_plane_even"] = dict(generic_stabiliser=stab_dim_gl(yeven), commuting=commuting_dim(yeven, Vp))
    y0, munorm = kempf_ness(yodd)
    Cm = np.array([E.wedge_star(y0, Vm[:, k]) for k in range(44)]).T
    _, sv, vh = np.linalg.svd(Cm)
    k = int(np.sum(sv < 1e-9 * sv[0]))
    C6 = Vm @ vh[-k:].conj().T
    cart_mu = max(float(np.linalg.norm(mu((C6 @ c) / np.linalg.norm(C6 @ c))))
                  for c in (rng.normal(size=4) + 1j * rng.normal(size=4) for _ in range(4)))
    traces = [(float(e.sum()), float(np.sum(e ** 2))) for e in
              (spectrum(C6, rng.normal(size=4) + 1j * rng.normal(size=4)) for _ in range(3))]
    res["11894"] = dict(kempf_ness_mu=munorm, cartan_dim=k, cartan_max_mu=cart_mu, traces=traces)
    runs = []
    for _ in range(4):
        r = minimize(lambda q: F_of(spectrum(C6, q[:4] + 1j * q[4:])), rng.normal(size=8), method="Nelder-Mead",
                     options=dict(maxiter=3000, xatol=1e-9, fatol=1e-12))
        r = minimize(lambda q: F_of(spectrum(C6, q[:4] + 1j * q[4:])), r.x, method="Nelder-Mead",
                     options=dict(maxiter=3000, xatol=1e-10, fatol=1e-13))
        runs.append(r)
    best = min(runs, key=lambda t: t.fun)
    c = best.x[:4] + 1j * best.x[4:]
    c = c / np.linalg.norm(c)
    q0 = np.concatenate([c.real, c.imag])
    rp = least_squares(lambda q: np.concatenate([np.sqrt(np.clip(spectrum(C6, q[:4] + 1j * q[4:])[:12], 0, None)) * 1e3,
                                                 [np.linalg.norm(q) - 1]]), q0, xtol=1e-15, ftol=1e-15, gtol=1e-15)
    cp = rp.x[:4] + 1j * rp.x[4:]
    e = spectrum(C6, cp)
    gens = unbroken(C6, cp)
    st, ideals = structure(gens, rng)
    res["11895"] = dict(min_F_runs=[float(r.fun) for r in runs], minus_3_log3=-3 * np.log(3), polished_F=F_of(e),
                        spectrum=dict(Counter(np.round(e, 6).tolist())), unbroken=st,
                        family_plane_44=decompose(ideals, Vm), qutrit_plane_40=decompose(ideals, Vp))
    fam = res["11895"]["family_plane_44"]
    res["checks"] = {kk: bool(v) for kk, v in dict(
        split_40_44=res["split"] == dict(even=40, odd=44),
        z6_cartan_4=res["grade1_odd"] == dict(generic_stabiliser=0, commuting=4) and k == 4,
        qutrit_plane_moduli_2=res["qutrit_plane_even"]["generic_stabiliser"] == 2,
        kempf_ness_flat=munorm < 1e-8 and cart_mu < 1e-7,
        traces_constant=all(abs(a - 10) < 1e-8 and abs(b - 4) < 1e-8 for a, b in traces),
        one_loop_min=all(abs(r.fun + 3 * np.log(3)) < 1e-6 for r in runs),
        unbroken_su3_su2_u1=st["dim"] == 12 and st["centre"] == 1 and st["rank"] == 4 and st["ideal_dims"] == [1, 3, 8],
        five_is_3plus2_four_is_3plus1=st["blocks"] == {"5": [2, 3], "4": [1, 3]},
        exotic_matter=any(key.startswith("(8,") for key in fam) and any(key.startswith("(6,2)") for key in fam),
        no_lepton_doublet=not any(key.startswith("(1,2)") for key in fam)
        and not any(key.startswith("(1,2)") for key in res["11895"]["qutrit_plane_40"]),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(res["checks"], indent=1))
    print(json.dumps(res["11895"], indent=1, default=str))
    print("all", res["all_checks_pass"])


if __name__ == "__main__":
    main()
