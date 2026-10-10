"""Passes 11849-11851: spinorial Lorentz inside E8, the Standard-Model algebra from Lorentz + central Z3, and generations.

Setting (Passes 11843-11846): E8 > SU(6) x SU(3) x SU(2); the faithful finite Lorentz group A6 (adjacent Tits words of
the A5 chain) commutes with su(5)_GUT; E8 > SU(5)_L x SU(5)_GUT with su(5)_L the commutant of su(5)_GUT.

11849  Spinors.  su(5)_L is built as the commutant of su(5)_GUT, with an explicit sl5 -> su(5)_L homomorphism from its
       own Chevalley basis.  The spinorial Lorentz group SL(2,9) is embedded through its 4-dim representation Di (the
       odd Weil half of Pass 11834, restricted to the Lorentz centraliser) as diag(Di, 1) in SU(5)_L.  Its commutant
       and the decomposition of E8 into (GUT representation, u(1)_L charge, spinor sign of -1) are computed.
11850  The central Z3 translation.  The radical line of the A5 lattice mod 3 (Pass 11844) gives an order-3 torus element
       t_c; the commutant of (A6 lift, t_c) is computed.
11851  Generations.  The E6 x A2 structure against su(5)_GUT: dim(e6 n su(5)_GUT), whether A2 is the colour factor, and
       the multiplicity space of the Lorentz spinor Di in E8 as a GUT module.
"""

from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11831_11833_finite_ads4 as F  # noqa: E402
import w33_pass11834_11837_singletons_bulk_poincare_e8 as S  # noqa: E402
import w33_pass11843_e8_tits_lorentz_commutant as T  # noqa: E402
import w33_pass11844_11846_e8_poincare_lifts_matter as L  # noqa: E402

OUT = ROOT / "data" / "w33_pass11849_11851_spinor_lorentz_central_z3_generations.json"
N = T.N


def nullspace(M, tol=1e-8):
    _, s, vh = np.linalg.svd(M)
    return vh[np.sum(s > tol):].conj().T


def centraliser(B, basis):
    """all x in E8 with [x, b] = 0 for every column b of basis."""
    M = np.vstack([T.ad(B, b) for b in basis.T])
    return nullspace(M)


def chevalley_sl5(B, Lb, rng):
    """explicit homomorphism sl5 -> span(Lb) (an sl5 inside E8)."""
    pinv = np.linalg.pinv(Lb)
    n = Lb.shape[1]

    def ad_in(x):
        return pinv @ T.ad(B, x) @ Lb
    x0 = Lb @ (rng.normal(size=n) + 1j * rng.normal(size=n))
    H = Lb @ nullspace(ad_in(x0))
    assert H.shape[1] == 4, H.shape
    h = H @ (rng.normal(size=4) + 1j * rng.normal(size=4))
    w, V = np.linalg.eig(ad_in(h))
    roots, vecs = [], []
    adH = [ad_in(H[:, k]) for k in range(4)]
    for k in range(n):
        if abs(w[k]) < 1e-6:
            continue
        v = V[:, k]
        lam = np.array([(v.conj() @ a @ v) / (v.conj() @ v) for a in adH])
        roots.append(lam)
        vecs.append(Lb @ v)
    assert len(roots) == 20
    f = rng.normal(size=4)
    pos = [i for i, r in enumerate(roots) if np.real(r @ f) > 0]
    def is_sum(i):
        return any(np.allclose(roots[i], roots[a] + roots[b], atol=1e-6) for a in pos for b in pos if a != i and b != i)
    simple = [i for i in pos if not is_sum(i)]
    assert len(simple) == 4
    neg = {i: next(j for j in range(20) if np.allclose(roots[j], -roots[i], atol=1e-6)) for i in simple}
    E, Fm, Hh = [], [], []
    for i in simple:
        e, fv = vecs[i], vecs[neg[i]]
        hv = T.br(B, e, fv)
        c = (pinv @ T.br(B, hv, e))[np.argmax(abs(pinv @ e))] / (pinv @ e)[np.argmax(abs(pinv @ e))]
        fv = fv * 2 / c
        E.append(e)
        Fm.append(fv)
        Hh.append(T.br(B, e, fv))
    # Cartan matrix and chain order
    A = np.zeros((4, 4))
    for a in range(4):
        for b in range(4):
            v = T.br(B, Hh[a], E[b])
            k = np.argmax(abs(E[b]))
            A[a, b] = np.real(v[k] / E[b][k])
    A = np.round(A).astype(int)
    adj = {a: [b for b in range(4) if b != a and A[a, b] == -1] for a in range(4)}
    chain = [next(a for a in range(4) if len(adj[a]) == 1)]
    while len(chain) < 4:
        chain.append(next(b for b in adj[chain[-1]] if b not in chain))
    E = [E[a] for a in chain]
    Fm = [Fm[a] for a in chain]
    Hh = [Hh[a] for a in chain]
    unit = {}
    for i in range(4):
        unit[(i, i + 1)] = E[i]
        unit[(i + 1, i)] = Fm[i]
    for span_ in range(2, 5):
        for i in range(5 - span_):
            j = i + span_
            unit[(i, j)] = T.br(B, unit[(i, j - 1)], unit[(j - 1, j)])
            unit[(j, i)] = T.br(B, unit[(j, j - 1)], unit[(j - 1, i)])

    def phi(X):
        out = np.zeros(N, complex)
        for (i, j), u in unit.items():
            out = out + X[i, j] * u
        d = np.diag(X)
        cum = np.cumsum(d)[:4]
        for i in range(4):
            out = out + cum[i] * Hh[i]
        return out
    # homomorphism check
    err = 0.0
    for _ in range(4):
        X = rng.normal(size=(5, 5)) + 1j * rng.normal(size=(5, 5))
        Y = rng.normal(size=(5, 5)) + 1j * rng.normal(size=(5, 5))
        X -= np.trace(X) / 5 * np.eye(5)
        Y -= np.trace(Y) / 5 * np.eye(5)
        err = max(err, float(abs(phi(X @ Y - Y @ X) - T.br(B, phi(X), phi(Y))).max()))
    return phi, err, A.tolist()


def fixed_c(gens):
    """common fixed space of complex automorphisms (conjugation-correct null space)."""
    return nullspace(np.vstack([g - np.eye(N) for g in gens]))


def log_su(U):
    """traceless logarithm of minimal norm: spread the 2 pi k trace correction over the angles nearest +-pi."""
    w, V = np.linalg.eig(U)
    th = np.angle(w)
    k = int(round(th.sum() / (2 * np.pi)))
    order = np.argsort(-th) if k > 0 else np.argsort(th)
    for j in order[:abs(k)]:
        th[j] -= 2 * np.pi * np.sign(k)
    X = V @ np.diag(1j * th) @ np.linalg.inv(V)
    assert np.allclose(expm(X), U, atol=1e-9) and abs(np.trace(X)) < 1e-9
    return X


def di_generators(rng):
    keys, mats, Vs, index, _ = S.weil_group()
    k0 = next(k for k in F.PTS if F.Q[k] == 2)
    J0 = F.JM[k0]
    cent = [i for i, g in enumerate(mats) if np.array_equal(F.m(g, J0), F.m(J0, g))]
    P = Vs[index[F.key((-F.I4) % 3)]]
    w, U = np.linalg.eigh(P)
    Q = U[:, np.isclose(w, -1)]
    Di = {i: Q.conj().T @ Vs[i] @ Q for i in cent}
    # Frobenius-Schur indicator of Di restricted to SL(2,9)
    sq = {i: index[F.key(F.m(mats[i], mats[i]))] for i in cent}
    fs = float(np.real(np.mean([np.trace(Di[sq[i]]) for i in cent])))
    # pick generators that generate all 720 elements
    for _ in range(50):
        gens_idx = list(rng.choice(cent, 2, replace=False))
        keyf = lambda M: tuple(np.round(M, 6).ravel())  # noqa: E731
        seen = {keyf(np.eye(4))}
        fr = [np.eye(4, dtype=complex)]
        while fr:
            nx = []
            for h in fr:
                for i in gens_idx:
                    x = Di[i] @ h
                    k = keyf(x)
                    if k not in seen:
                        seen.add(k)
                        nx.append(x)
            fr = nx
        if len(seen) == 720:
            break
    minus = index[F.key((-F.I4) % 3)]
    # is the so(5)-vector 5 = Lambda^2 Di - 1 the restriction of Rac to SL(2,9)?
    Pe = (np.eye(9) + P) / 2
    rac = np.array([np.trace(Vs[i] @ Pe) for i in cent])
    di = np.array([np.trace(Di[i]) for i in cent])
    di2 = np.array([np.trace(Di[sq[i]]) for i in cent])
    vec5 = (di**2 - di2) / 2 - 1
    global RAC_VS_VECTOR
    RAC_VS_VECTOR = dict(vector5_norm=round(float(np.real(np.mean(abs(vec5) ** 2))), 6),
                         rac_norm_on_SL29=round(float(np.real(np.mean(abs(rac) ** 2))), 6),
                         overlap=round(float(np.real(np.mean(vec5 * np.conj(rac)))), 6))
    return [Di[i] for i in gens_idx], Di[minus], fs, len(seen), Q, Vs, index, mats


def casimir(B, basis):
    G = basis
    kil = np.array([[np.trace(T.ad(B, a) @ T.ad(B, b)) for b in G.T] for a in G.T])
    kinv = np.linalg.inv(kil)
    ads = [T.ad(B, a) for a in G.T]
    K = np.zeros((N, N), complex)
    for i in range(len(ads)):
        for j in range(len(ads)):
            if abs(kinv[i, j]) > 1e-12:
                K = K + kinv[i, j] * ads[i] @ ads[j]
    return K


def main():
    rng = np.random.default_rng(11849)
    B, sub = L.setup(rng)
    chain = sub["chain"]
    tits = [T.tits(B, b) for b in chain]
    adj_gens = [tits[i] @ tits[i + 1] for i in range(4)]
    C_gut = T.fixed_subalgebra(adj_gens)  # su(5)_GUT
    res = {"pass_ids": [11849, 11850, 11851]}
    # ---------------- 11850: central Z3
    Gmod3 = L.weyl_mod3(chain)
    subs = L.submodules(Gmod3)
    W5 = next(s for s in subs if len(s) == 5)
    vecs = [v for v in L.span_vectors(W5) if any(v)]
    c = next(v for v in vecs if all(T.ip(v, w) % 3 == 0 for w in W5))
    tc = L.torus_order3(np.array(c))
    fixes = {nm: all(T.ip(c, r) % 3 == 0 for r in sub[nm]) for nm in ("A5", "A2", "A1")}
    commutes = all(np.allclose(tc @ g, g @ tc, atol=1e-9) for g in adj_gens)
    C_sm = T.fixed_subalgebra(adj_gens + [tc])
    sm = L.analyse_complex(B, C_sm, rng)
    sm["contains_su3_A2"] = L.basis_contains(np.column_stack([T.vec_root(r) for r in sub["A2"]]), C_sm)
    sm["contains_su2_alpha"] = L.basis_contains(np.column_stack([T.vec_root(r) for r in sub["A1"]]), C_sm)
    res["central_Z3"] = dict(c=[int(x) for x in c], fixes_A5_A2_A1_roots=fixes, commutes_with_A6_lift=commutes,
                             commutant_of_A6_and_tc=sm)
    print("central", res["central_Z3"], flush=True)
    # ---------------- 11849: su(5)_L and the spinorial Lorentz group
    C_L = centraliser(B, C_gut)
    res["su5_L"] = dict(dim=int(C_L.shape[1]), analysis=L.analyse_complex(B, C_L, rng))
    phi, herr, cart = chevalley_sl5(B, C_L, rng)
    res["su5_L"].update(homomorphism_error=herr, cartan_matrix=cart)
    gens4, minus4, fs, order, Q, Vs, index, mats = di_generators(rng)
    res["vector5_versus_Rac"] = RAC_VS_VECTOR
    res["Di"] = dict(SL29_generated_order=order, frobenius_schur_indicator_on_SL29=round(fs, 6),
                     minus_one_is_minus_identity=bool(np.allclose(minus4, -np.eye(4))))

    def auto(D):
        g5 = np.eye(5, dtype=complex)
        g5[:4, :4] = D
        return expm(T.ad(B, phi(log_su(g5))))
    A_gens = [auto(D) for D in gens4]
    Z = auto(minus4)
    aut_err = max(T.is_automorphism(B, a.real if np.allclose(a.imag, 0) else a, rng) if False else
                  float(abs(a @ T.br(B, x, y) - T.br(B, a @ x, a @ y)).max())
                  for a in A_gens + [Z] for x, y in [rng.normal(size=(2, N))])
    C_spin = fixed_c(A_gens)
    res["generator_order_errors"] = [float(abs(np.linalg.matrix_power(a, n) - np.eye(N)).max()) for a, n in
                                    zip(A_gens, [next(m for m in range(1, 40) if np.allclose(np.linalg.matrix_power(D, m), np.eye(4))) for D in gens4])]
    res["Z_fixes_commutant"] = float(abs(Z @ C_spin - C_spin).max())
    sp = L.analyse_complex(B, C_spin, rng)
    sp["contains_su5_gut"] = L.basis_contains(C_gut, C_spin)
    res["spinor_lorentz"] = dict(automorphism_error=aut_err, minus_one_acts_nontrivially=bool(not np.allclose(Z, np.eye(N), atol=1e-8)),
                                 commutant=sp)
    print("spinor", res["spinor_lorentz"], flush=True)
    # decomposition of E8 under the commutant (Casimir eigenvalue multiplicities) and the spinor sign of -1
    Cc = casimir(B, C_spin)
    w = np.linalg.eigvals(Cc)
    vals = []
    for x in sorted(np.real(w)):
        if not vals or abs(x - vals[-1][-1]) > 1e-4:
            vals.append([x])
        else:
            vals[-1].append(x)
    cs = [float(np.mean(v)) for v in vals]
    table = []
    for k, ck in enumerate(cs):
        Pk = np.eye(N, dtype=complex)
        for j, cj in enumerate(cs):
            if j != k:
                Pk = Pk @ (Cc - cj * np.eye(N)) / (ck - cj)
        table.append(dict(casimir=round(ck, 6), dim=int(round(np.real(np.trace(Pk))))))
    # spinor sign: Casimir spectrum inside the exact +-1 eigenspaces of Z (Z^2 = 1)
    sign_counts = {}
    for sgn in (1, -1):
        Ps = (np.eye(N) + sgn * Z) / 2
        u_, s_, _ = np.linalg.svd(Ps)
        Vs = u_[:, s_ > 0.5]
        Cs = Vs.conj().T @ Cc @ Vs
        ev = np.real(np.linalg.eigvals(Cs))
        cnt = Counter(int(np.argmin([abs(x - c) for c in cs])) for x in ev)
        sign_counts[str(sgn)] = {str(round(cs[k], 6)): v for k, v in sorted(cnt.items())}
    res["casimir_counts_by_spinor_sign"] = sign_counts
    res["Z_squared_is_identity"] = bool(np.allclose(Z @ Z, np.eye(N), atol=1e-7))
    res["spinor_matter"] = table
    adjc = max(r["casimir"] for r in table)
    res["casimir_ratios_to_adjoint"] = {str(r["dim"]) + "_" + str(i): round(r["casimir"] / adjc, 5) for i, r in enumerate(table)}
    res["so11_ratios_expected"] = {"vector 10/18": round(10 / 18, 4), "spinor 13.75/18": round(13.75 / 18, 4)}
    res["spinor_matter_blocks_match_so11_x_sp4"] = sorted(r["dim"] for r in table) == sorted([55, 55, 128, 10])
    for row in table:
        print(row, flush=True)
    # ---------------- 11851: E6 x A2 versus su(5)_GUT
    E6r = sub["E6"]
    e6 = np.column_stack([T.vec_root(r) for r in E6r] + [np.concatenate([np.array(r, float), np.zeros(240)]) for r in E6r])
    q, rr = np.linalg.qr(e6)
    e6 = q[:, np.abs(np.diag(rr)) > 1e-9]
    inter = e6.shape[1] + C_gut.shape[1] - np.linalg.matrix_rank(np.hstack([e6, C_gut]), tol=1e-7)
    res["generations"] = dict(e6_dim=int(e6.shape[1]), e6_cap_su5gut_dim=int(inter),
                              A2_inside_su5gut=L.basis_contains(np.column_stack([T.vec_root(r) for r in sub["A2"]]), C_gut))
    print("generations", res["generations"], flush=True)
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
