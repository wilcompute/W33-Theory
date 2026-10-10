"""Passes 11864-11866: chirality and the finite Lorentz group; B-L breaking; little groups of the charged sectors.

11864  Chirality.  (a) SL(2,9) is ambivalent (every element conjugate to its inverse), so every irreducible
       representation is self-conjugate: the finite Lorentz group has no Weyl spinors; equivalently #{g^2 = 1} = 2 forces
       all faithful irreps quaternionic and all A6 irreps real.  (b) Chirality is still possible at the Poincare level:
       the massless helicity modules H_1, H_3 (Pass 11840) are conjugate, inequivalent irreducibles, and the isotypic
       (Weyl) projector is Poincare-covariant.  Matter R x Di x (functions on null momenta) contains H_1 and H_3 with the
       multiplicities m_1, m_3 of the helicity characters in Di restricted to the massless little group.  With
       m_1 = m_3 every field content of the form R x Di is vector-like unless a Weyl projection is imposed; with it,
       each R carries m_1 copies of a chiral helicity module.  The triality orbifold (quarks in the charged sectors)
       does not change this index.
11865  B-L breaking.  In the spinorial structure (commutant su(3)+so(5)+u(1), centre B-L, Pass 11862): all Standard-Model
       singlets with nonzero B-L lie in the Lorentz-spinor block.  Lorentz-invariant bilinears (condensates) of them
       exist (Di quaternionic); the stabiliser of a generic such condensate inside the commutant is computed.
11866  Little groups of the charged (k = 1, 2) sectors of the translations, against the neutral sector (Pass 11860).
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
import w33_pass11849_11851_spinor_lorentz_central_z3_generations as M  # noqa: E402
import w33_pass11859_11862_parity_orbifold_sectors_breaking as P  # noqa: E402

OUT = ROOT / "data" / "w33_pass11864_11866_weyl_chirality_bl_quark_sectors.json"
N = T.N


def frac(x, d=12):
    return str(Fraction(float(x)).limit_denominator(d))


# ---------------------------------------------------------------- 11864
def chirality_finite(mats, Vs, index, cent, Q):
    keyset = {F.key(mats[i]): i for i in cent}
    G = [mats[i] for i in cent]
    inv_ok = 0
    for g in G:
        gi = F.inv(g)
        if any(np.array_equal(F.m(h, g, F.inv(h)), gi) for h in G):
            inv_ok += 1
    ambivalent = inv_ok == len(G)
    sq_one = sum(1 for g in G if np.array_equal(F.m(g, g), F.I4))
    sq_minus = sum(1 for g in G if np.array_equal(F.m(g, g), (-F.I4) % 3))
    # massless little group: stabiliser of a null vector of the tangent Minkowski space
    k0 = next(k for k in F.PTS if F.Q[k] == 2)
    null = next(F.JM[k] for k in F.PTS if F.Q[k] == 0 and F.beta(k, k0) == 0)
    Lg = [i for i in cent if np.array_equal(F.m(mats[i], null, F.inv(mats[i])), null)]

    def order(g):
        x, n = g, 1
        while not np.array_equal(x, F.I4):
            x, n = F.m(x, g), n + 1
        return n
    T9 = {F.key(mats[i]) for i in Lg if order(mats[i]) in (1, 3)}
    r = next(i for i in Lg if order(mats[i]) == 4)
    rk = [F.I4]
    for _ in range(3):
        rk.append(F.m(rk[-1], mats[r]))

    def phi(g):
        for k in range(4):
            if F.key(F.m(F.inv(rk[k]), g)) in T9:
                return k
        raise AssertionError
    ph = np.array([phi(mats[i]) for i in Lg])
    di = np.array([np.trace(Q.conj().T @ Vs[i] @ Q) for i in Lg])
    mult = {f"n={n}": round(float(np.real(np.mean(di * np.conj((1j) ** (n * ph))))), 6) for n in range(4)}
    rest = 4 - sum(mult.values())
    return dict(SL29_ambivalent=ambivalent, elements_with_g2_eq_1=sq_one, elements_with_g2_eq_minus1=sq_minus,
                A6_involution_count=(sq_one + sq_minus) // 2 - 1,
                frobenius_schur_conclusion="all A6 irreps real, all faithful SL(2,9) irreps quaternionic",
                null_little_group_order=len(Lg), Di_helicity_multiplicities=mult, Di_in_2dim_little_group_reps=rest,
                weyl_balance=mult["n=1"] == mult["n=3"])


# ---------------------------------------------------------------- 11866
def charged_sector_little_groups():
    gens = []
    for k in (2, 3, 4, 5):
        gens.append([1 if i == 0 else (k if i == 1 else (0 if i == k else i)) for i in range(6)])
    G = {tuple(range(6))}
    fr = [tuple(range(6))]
    while fr:
        nx = []
        for p in fr:
            for g in gens:
                q = tuple(p[g[i]] for i in range(6))
                if q not in G:
                    G.add(q)
                    nx.append(q)
        fr = nx
    G = list(G)

    def canon(a):
        return min(tuple((x + c) % 3 for x in a) for c in range(3))

    def porder(p):
        x, n = p, 1
        while x != tuple(range(6)):
            x, n = tuple(p[x[i]] for i in range(6)), n + 1
        return n
    classes = {canon(a) for a in itertools.product(range(3), repeat=6)}
    out = {}
    for k in range(3):
        sec = [a for a in classes if sum(a) % 3 == k]
        seen = set()
        rows = []
        for a in sorted(sec):
            if a in seen:
                continue
            orb = {canon(tuple(a[p[i]] for i in range(6))) for p in G}
            seen |= orb
            stab = [p for p in G if canon(tuple(a[p[i]] for i in range(6))) == a]
            stats = Counter(porder(p) for p in stab)
            name = {60: "A5", 24: "S4", 12: "A4", 18: "3^2:2", 6: "S3" if stats.get(2, 0) == 3 else "Z6", 360: "A6"}.get(len(stab), "?")
            rows.append(dict(orbit=len(orb), stabiliser_order=len(stab), element_orders=dict(sorted(stats.items())),
                             structure=name, spin_lift_order=2 * len(stab)))
        out[str(k)] = sorted(rows, key=lambda r: r["orbit"])
    return out


# ---------------------------------------------------------------- 11865 (E8)
def bl_breaking(rng):
    B, sub = L.setup(rng)
    chain = sub["chain"]
    tits = [T.tits(B, b) for b in chain]
    adj = [tits[i] @ tits[i + 1] for i in range(4)]
    ext = [a @ b for a, b in itertools.permutations(tits, 2)]
    Cg = T.fixed_subalgebra(adj)
    Ce = T.fixed_subalgebra(ext)
    Y = L.centraliser_within(B, Cg, Ce)[:, 0]
    adY = T.ad(B, Y)
    ev = np.linalg.eigvals(adY)
    adY = adY / ev[np.argmax(abs(ev))]
    CL = M.centraliser(B, Cg)
    phi, _, _ = M.chevalley_sl5(B, CL, rng)
    gens4, minus4, *_ = M.di_generators(rng)

    def auto5(D):
        g5 = np.eye(5, dtype=complex)
        g5[:4, :4] = D
        return expm(T.ad(B, phi(M.log_su(g5))))
    A = [auto5(D) for D in gens4]
    Z = auto5(minus4)
    Gm = L.weyl_mod3(chain)
    subs = L.submodules(Gm)
    W5 = next(s for s in subs if len(s) == 5)
    c = next(v for v in L.span_vectors(W5) if any(v) and all(T.ip(v, w) % 3 == 0 for w in W5))
    tc = L.torus_order3(np.array(c))
    Cb = M.fixed_c(A + [tc])
    adC = [np.linalg.pinv(Cb) @ T.ad(B, Cb[:, i]) @ Cb for i in range(Cb.shape[1])]
    cz = M.nullspace(np.vstack([np.column_stack([adC[i][:, j] for i in range(len(adC))]) for j in range(len(adC))]))
    z = Cb @ cz[:, 0]
    adz = T.ad(B, z)
    ez = np.linalg.eigvals(adz)
    adz = adz / ez[np.argmax(abs(ez))]
    su3 = np.column_stack([T.vec_root(r) for r in sub["A2"]] + [np.concatenate([np.array(r, float), np.zeros(240)]) for r in sub["A2"][:2]])
    su2 = np.column_stack([T.vec_root(r) for r in sub["A1"]] + [np.concatenate([np.array(sub["A1"][0], float), np.zeros(240)])])
    # SM singlets: annihilated by Y, su(3), su(2)
    ann = M.nullspace(np.vstack([adY] + [T.ad(B, x) for x in su3.T] + [T.ad(B, x) for x in su2.T]))
    zr = np.linalg.pinv(ann) @ adz @ ann
    wz, Vz = np.linalg.eig(zr)
    Zr = np.linalg.pinv(ann) @ Z @ ann
    rows = Counter()
    for k in range(len(wz)):
        v = Vz[:, k]
        sgn = int(round(float(np.real((v.conj() @ Zr @ v) / (v.conj() @ v)))))
        rows[(frac(np.real(wz[k])), sgn)] += 1
    singlets = {f"BL={a},spinor_sign={b}": n for (a, b), n in sorted(rows.items(), key=lambda t: (float(Fraction(t[0][0])), t[0][1]))}
    charged_all_spinor = all(b == -1 for (a, b) in rows if a != "0")
    # Lorentz-invariant bilinears of the B-L = +3/4 SM singlets
    pos = ann @ Vz[:, np.isclose(np.real(wz), 0.75, atol=1e-6)]
    q_, r_ = np.linalg.qr(pos)
    Wb = q_[:, np.abs(np.diag(r_)) > 1e-9] if pos.shape[1] else pos
    d = Wb.shape[1]
    out = dict(sm_singlet_dim=int(ann.shape[1]), sm_singlets_by_BL_and_spinor_sign=singlets,
               BL_charged_sm_singlets_all_in_spinor_block=bool(charged_all_spinor), BL_plus_singlet_dim=int(d))
    if d:
        Wp = np.linalg.pinv(Wb)
        Ar = [Wp @ a @ Wb for a in A]  # Lorentz acts on W (W is Lorentz-invariant: commutes with the SM)
        inv_ok = float(max(abs(Wb @ ar - a @ Wb).max() for a, ar in zip(A, Ar)))
        # invariant bilinear tensors T in W x W: a T a^T = T for the Lorentz generators
        rowsT = [np.kron(ar, ar) - np.eye(d * d) for ar in Ar]
        sv = np.linalg.svd(np.vstack(rowsT), compute_uv=False)
        out["bilinear_singular_values_smallest"] = [float(x) for x in sv[-3:]]
        Tn = M.nullspace(np.vstack(rowsT), tol=1e-5)
        sym = antisym = 0
        for i in range(Tn.shape[1]):
            Tm = Tn[:, i].reshape(d, d)
            sym += int(np.allclose(Tm, Tm.T, atol=1e-8))
            antisym += int(np.allclose(Tm, -Tm.T, atol=1e-8))
        out.update(W_invariant_under_lorentz_error=inv_ok, lorentz_invariant_bilinears=int(Tn.shape[1]),
                   symmetric=sym, antisymmetric=antisym)
        if Tn.shape[1]:
            Tm = Tn @ (rng.normal(size=Tn.shape[1]) + 1j * rng.normal(size=Tn.shape[1]))
            Tm = Tm.reshape(d, d)
            MT = Wb @ Tm @ Wb.T  # 248 x 248 tensor
            eqs = np.column_stack([(T.ad(B, Cb[:, i]) @ MT + MT @ T.ad(B, Cb[:, i]).T).ravel() for i in range(Cb.shape[1])])
            _, sv2, vh2 = np.linalg.svd(eqs, full_matrices=False)
            out["stabiliser_singular_values"] = [float(x) for x in sv2]
            rel = sv2 / sv2.max()
            stab = Cb @ vh2[rel < 1e-6].conj().T
            info = L.analyse_complex(B, stab, rng) if stab.shape[1] else dict(dim=0)
            info["contains_su3"] = L.basis_contains(su3, stab) if stab.shape[1] else False
            info["contains_su2_alpha"] = L.basis_contains(su2, stab) if stab.shape[1] else False
            info["contains_Y"] = L.basis_contains(Y.reshape(-1, 1), stab) if stab.shape[1] else False
            # Levi (reductive) part = stabiliser modulo the radical of the E8 Killing form restricted to it
            if stab.shape[1]:
                ads = [T.ad(B, x) for x in stab.T]
                kil = np.array([[np.trace(a @ b) for b in ads] for a in ads])
                skil = np.linalg.svd(kil, compute_uv=False)
                info["killing_rank"] = int(np.sum(skil / skil.max() > 1e-7))
                info["nilradical_dim"] = int(stab.shape[1] - info["killing_rank"])
                info["levi_is_SM_algebra"] = bool(info["killing_rank"] == 12 and info["contains_su3"] and info["contains_su2_alpha"]
                                                  and info["contains_Y"])
            out["stabiliser_of_generic_condensate"] = info
    return out


def main():
    rng = np.random.default_rng(11864)
    mats, Vs, index, cent, anti, Q = P.weil_data()
    res = {"pass_ids": [11864, 11865, 11866]}
    res["chirality"] = chirality_finite(mats, Vs, index, cent, Q)
    print("11864", res["chirality"], flush=True)
    res["charged_sector_little_groups"] = charged_sector_little_groups()
    print("11866", json.dumps(res["charged_sector_little_groups"]), flush=True)
    res["bl_breaking"] = bl_breaking(rng)
    print("11865", res["bl_breaking"], flush=True)
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
