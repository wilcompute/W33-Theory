"""Passes 11839-11842: fields on the finite AdS4 of two qutrits (Passes 11831-11838).

11839  Crosscap holography.  For a Kramers reversal p (anti-symplectic J_p, J_p^2 = -1) the antiunitary
       T_p = U_g K (g = J_p J_K, K complex conjugation, U the exact linear Weil representation of Pass 11834) satisfies
       T_p^2 = P exactly.  Its crosscap form B_p(psi, phi) = <T_p psi, phi> is symmetric on Rac and antisymmetric on Di,
       and p -> B_p is exactly Sp(4,3)-equivariant on Rac.  The map Phi: Sym^2 Rac -> C[36], v -> (p -> B_p(v)) is an
       explicit holographic map; its image is the 15-dimensional bulk mode, its kernel zero.
11840  Finite free fields.  Shell propagators of the finite Poincare group M x SL(2,9), and the finite spinor-helicity
       theorem: massless representations of helicity n (n in Z4) are the functions on the 80 spinors with
       f(J0 psi) = i^n f(psi), translations acting by the phase of the null momentum psi ^ J0 psi.
11841  Sp(4,3)-invariant cubic couplings among the singletons and the bulk/boundary modes (character sums).
11842  Massive spin content: the singletons restricted to the massive little group SL(2,3), with Z3 labels.
"""

from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11831_11833_finite_ads4 as F  # noqa: E402
import w33_pass11834_11837_singletons_bulk_poincare_e8 as S  # noqa: E402

OUT = ROOT / "data" / "w33_pass11839_11842_crosscap_fields_couplings_spin.json"
W3 = S.W3
JK = np.diag([1, 1, 2, 2]).astype(np.int64)  # complex conjugation acts on phase space as (x, z) -> (x, -z)


def r(z, nd=6):
    z = complex(z)
    return round(z.real, nd) if abs(z.imag) < 1e-7 else [round(z.real, nd), round(z.imag, nd)]


# ---------------------------------------------------------------- 11839 crosscaps
def crosscaps(mats, Vs, index):
    I9 = np.eye(9)
    for v in F.VECS:
        assert np.allclose(np.conj(S.weyl(v)), S.weyl(JK @ v % 3))  # K implements J_K
    P = Vs[index[F.key((-F.I4) % 3)]]
    Pe, Po = (I9 + P) / 2, (I9 - P) / 2
    K36 = [k for k in F.PTS if F.Q[k] == 2]
    forms, t2_ok = {}, True
    for k in K36:
        J = F.JM[k]
        g = F.m(J, JK)
        assert np.array_equal(F.m(g.T, F.OM, g), F.OM)
        U = Vs[index[F.key(g)]]
        t2_ok &= bool(np.allclose(U @ np.conj(U), P, atol=1e-9))  # T^2 = U conj(U) = P exactly
        forms[k] = U.conj().T  # B_p(psi, phi) = psi^T U^dag phi
    # symmetry on Rac / Di
    sym_rac = all(np.allclose(Pe.T @ M @ Pe, (Pe.T @ M @ Pe).T, atol=1e-9) for M in forms.values())
    anti_di = all(np.allclose(Po.T @ M @ Po, -(Po.T @ M @ Po).T, atol=1e-9) for M in forms.values())
    mixed_zero = all(np.allclose(Pe.T @ M @ Po, 0, atol=1e-9) for M in forms.values())
    # exact equivariance on Rac: U_h^T B_{hp} U_h = B_p (as forms on Rac), sampled over the group
    rng = np.random.default_rng(11839)
    eq_err = 0.0
    for i in rng.integers(0, len(mats), 60):
        h, Uh = mats[i], Vs[i]
        for k in K36[:6]:
            hk = F.act(h, k)
            lhs = Pe.T @ Uh.T @ forms[hk] @ Uh @ Pe
            eq_err = max(eq_err, float(abs(lhs - Pe.T @ forms[k] @ Pe).max()))
    # holographic map Phi on Sym^2 Rac: rows = bulk points, columns = coordinates of the symmetric form
    ev = np.linalg.eigh(P)[1][:, np.isclose(np.linalg.eigh(P)[0], 1)]  # orthonormal basis of Rac (9x5)
    od = np.linalg.eigh(P)[1][:, np.isclose(np.linalg.eigh(P)[0], -1)]  # Di (9x4)
    rac_forms = np.array([(ev.T @ forms[k] @ ev).ravel() for k in K36])  # 36 x 25
    di_forms = np.array([(od.T @ forms[k] @ od).ravel() for k in K36])
    rank_rac = int(np.linalg.matrix_rank(rac_forms, tol=1e-8))
    rank_di = int(np.linalg.matrix_rank(di_forms, tol=1e-8))
    # image of Phi inside C[36]: compare with eigenspaces of the orthogonality graph
    A = np.array([[1.0 if a != b and F.beta(a, b) == 0 else 0.0 for b in K36] for a in K36])
    img = rac_forms  # columns span the image of Phi (functions of p)
    in3 = float(abs(A @ img - 3 * img).max())
    # bulk two-point function <C_p, C_q> on Rac by relation
    G = rac_forms.conj() @ rac_forms.T
    rel = Counter()
    for i, a in enumerate(K36):
        for j, b in enumerate(K36):
            tag = "same" if i == j else ("orthogonal" if F.beta(a, b) == 0 else "non-orthogonal")
            rel[(tag, r(G[i, j], 6) if not isinstance(r(G[i, j], 6), list) else tuple(r(G[i, j], 6)))] += 1
    # boundary-to-bulk kernel from stabilizer states: sum over the 9 states of a context of |B_p(s_e, s_e)|^2
    X40 = [k for k in F.PTS if F.Q[k] == 0]
    ker = Counter()
    for x in X40:
        L = F.kernel(F.JM[x])
        Lv = [np.zeros(4, dtype=np.int64)] + [np.array(v) for v in L]
        Pl = sum(S.weyl(v) for v in Lv) / 9
        w, U = np.linalg.eigh((Pl + Pl.conj().T) / 2)
        s0 = U[:, np.argmax(w)]
        states = [S.weyl(np.array(t)) @ s0 for t in itertools.product(range(3), repeat=4)]
        uniq = []
        for st in states:
            if all(abs(abs(np.vdot(u, st)) - 1) > 1e-6 for u in uniq):
                uniq.append(st)
        assert len(uniq) == 9
        for p in K36:
            val = sum(abs((Pe @ st) @ forms[p] @ (Pe @ st)) ** 2 for st in uniq)
            ker[("orthogonal" if F.beta(x, p) == 0 else "non-orthogonal", round(float(val), 8))] += 1
    return dict(T_squared_equals_P=t2_ok, symmetric_on_Rac=sym_rac, antisymmetric_on_Di=anti_di, no_Rac_Di_mixing=mixed_zero,
                rac_equivariance_max_error=eq_err, span_rank_rac=rank_rac, span_rank_di=rank_di,
                image_in_bulk_eigenvalue3_max_residual=in3,
                bulk_two_point_by_relation={f"{a}:{b}": c for (a, b), c in sorted(rel.items(), key=str)},
                boundary_to_bulk_kernel={f"{a}:{b}": c for (a, b), c in sorted(ker.items(), key=str)})


# ---------------------------------------------------------------- 11840 free fields
def lorentz_data(mats):
    k0 = next(k for k in F.PTS if F.Q[k] == 2)
    J0 = F.JM[k0]
    cent = [g for g in mats if np.array_equal(F.m(g, J0), F.m(J0, g))]
    return k0, J0, cent


def spinor_square(J0, psi):
    a, b = psi % 3, (J0 @ psi) % 3
    oa, ob = (F.OM @ a) % 3, (F.OM @ b) % 3
    return F.m(F.OMI, (np.outer(oa, ob) - np.outer(ob, oa)) % 3)


def beta_m(A, B):
    return (F.scalar_of(F.m(A, B) + F.m(B, A)) * 2) % 3


def free_fields(mats):
    k0, J0, cent = lorentz_data(mats)
    vecs = {F.key(F.I4 * 0)}
    for k in F.PTS:
        if F.beta(k, k0) == 0:
            for s in (1, 2):
                vecs.add(F.key(s * F.JM[k]))
    vecs = sorted(vecs)
    Vm = {v: np.array(v, dtype=np.int64).reshape(4, 4) for v in vecs}
    cls = {v: ("zero" if not any(v) else {0: "null", 1: "split_type", 2: "kramers_type"}[F.scalar_of(F.m(Vm[v], Vm[v]))]) for v in vecs}
    shells = {c: [v for v in vecs if cls[v] == c] for c in ("null", "split_type", "kramers_type")}
    # position-space shell propagators G_s(x) = (1/81) sum_{k in shell} omega^{beta(k,x)}, by class of x
    prop = {}
    for s, Ks in shells.items():
        row = {}
        for c in ("zero", "null", "split_type", "kramers_type"):
            vals = {r(sum(W3 ** beta_m(Vm[k], Vm[x]) for k in Ks) / 81, 8) for x in vecs if cls[x] == c}
            row[c] = sorted(vals, key=str)
        prop[s] = row
    # spinor-helicity: functions on the 80 spinors with f(J0 psi) = i^n f(psi)
    spinors = [np.array(v) for v in F.VECS]
    sidx = {tuple(int(t) for t in v): i for i, v in enumerate(spinors)}
    kpsi = [F.key(spinor_square(J0, v)) for v in spinors]
    J0idx = [sidx[tuple(int(t) for t in (J0 @ v % 3))] for v in spinors]
    perm = []
    for g in cent:
        gi = F.inv(g)
        perm.append([sidx[tuple(int(t) for t in (gi @ v % 3))] for v in spinors])
    perm = np.array(perm)
    # phases e^{2 pi i beta(k(psi), x)/3} for all translations x
    B = np.array([[beta_m(Vm[kp], Vm[x]) for x in vecs] for kp in kpsi])  # 80 x 81
    phase = W3 ** B
    # trace of (x, g) on H_n:  sum over psi with g^-1 psi = u psi (u = J0^j) of i^{-n j}/... use projector
    J0pow = [np.arange(80)]
    for _ in range(3):
        J0pow.append(np.array(J0idx)[J0pow[-1]])
    res = {}
    for n in range(4):
        chis = []
        for gi_perm in perm:
            # (A R_u f)(psi) = phase(psi) f(u g^-1 psi); projector (1/4) sum_j i^{-nj} R_{J0^j}
            tr = np.zeros(81, complex)
            for j in range(4):
                target = J0pow[j][gi_perm]  # index of J0^j g^-1 psi
                diag = target == np.arange(80)
                tr += (1j) ** (-n * j) / 4 * phase[diag].sum(axis=0)
            chis.append(tr)
        chis = np.array(chis)  # 720 x 81
        res[n] = chis
    norms = {f"helicity_{n}": r(np.sum(abs(res[n]) ** 2) / (720 * 81), 6) for n in range(4)}
    dims = {f"helicity_{n}": r(res[n][0, list(vecs).index(F.key(F.I4 * 0))], 6) for n in range(4)}
    cross = {f"{a}-{b}": r(np.sum(res[a] * np.conj(res[b])) / (720 * 81), 6) for a, b in itertools.combinations(range(4), 2)}
    return dict(shell_propagators=prop, spinor_helicity=dict(dims=dims, norms=norms, cross=cross))


# ---------------------------------------------------------------- 11841 cubic couplings
def couplings(C):
    chie, chio, sq, perm = C["chie"], C["chio"], C["sq"], C["perm"]
    mods = {
        "Rac": chie, "Rac*": np.conj(chie), "Di": chio, "Di*": np.conj(chio),
        "S15 (bulk&boundary)": S.sym2(chie, sq), "b20 (bulk, splits)": perm["kramers36"] - 1 - S.sym2(chie, sq),
        "X24 (boundary, splits)": chie * np.conj(chie) - 1, "D15 (points)": chio * np.conj(chio) - 1,
        "A10 (Alt2 Rac)": S.alt2(chie, sq), "c20 (Rac Di*)": chie * np.conj(chio),
    }
    for nm, c in mods.items():
        assert abs(S.ip(c, c) - 1) < 1e-8, nm
    names = list(mods)
    table = {}
    for a, b, c in itertools.combinations_with_replacement(names, 3):
        v = S.ip(mods[a] * mods[b] * mods[c], np.ones(C["N"]))
        if abs(v) > 1e-8:
            table[f"{a} | {b} | {c}"] = r(v, 6)
    # symmetric cubic self-couplings of the real bulk modes
    sym3 = {}
    for nm in ("S15 (bulk&boundary)", "b20 (bulk, splits)", "X24 (boundary, splits)", "D15 (points)"):
        c = mods[nm]
        sym3[nm] = r(np.mean((c**3 + 3 * c[sq] * c + 2 * c[C["cu"]]) / 6), 6)
    return dict(nonzero_cubic_invariants=table, symmetric_cubic_self_couplings=sym3)


# ---------------------------------------------------------------- 11842 massive spin
def massive_spin(mats, Vs, index):
    k0, J0, cent = lorentz_data(mats)
    vecs = []
    for k in F.PTS:
        if F.beta(k, k0) == 0 and F.Q[k] in (1, 2):
            vecs.append((F.Q[k], F.JM[k]))
    P = Vs[index[F.key((-F.I4) % 3)]]
    Pe = (np.eye(9) + P) / 2
    out = {}
    for q, name in ((2, "kramers_type"), (1, "split_type")):
        v = next(x for c, x in vecs if c == q)
        L = [g for g in cent if np.array_equal(F.m(g, v, F.inv(g)), v)]

        def order(g):
            x, n = g, 1
            while not np.array_equal(x, F.I4):
                x, n = F.m(x, g), n + 1
            return n
        ords = [order(g) for g in L]
        Q8 = [g for g, o in zip(L, ords) if o in (1, 2, 4)]
        Q8k = {F.key(g) for g in Q8}
        c = next(g for g, o in zip(L, ords) if o == 3)
        ci = F.inv(c)

        def phi(g):
            for kk in range(3):
                if F.key(F.m(g, np.linalg.matrix_power(ci, kk) % 3)) in Q8k:
                    return kk
            raise AssertionError
        ph = [phi(g) for g in L]
        # characters of SL(2,3): trivial-on-centre 1_j and 3; faithful 2_j (2_0 has trace -1 on order 3, +1 on order 6)
        def chi2(o):
            return {1: 2, 2: -2, 4: 0, 3: -1, 6: 1}[o]
        def chi3(o):
            return {1: 3, 2: 3, 4: -1, 3: 0, 6: 0}[o]
        irr = {}
        for j in range(3):
            irr[f"1_{j}"] = np.array([W3 ** (j * f) for f in ph])
            irr[f"2_{j}"] = np.array([chi2(o) * W3 ** (j * f) for o, f in zip(ords, ph)])
        irr["3"] = np.array([chi3(o) for o in ords], complex)
        for a in irr:
            for b in irr:
                assert abs(np.mean(irr[a] * np.conj(irr[b])) - (a == b)) < 1e-9, (a, b)
        idx = [index[F.key(g)] for g in L]
        rac = np.array([np.trace(Vs[i] @ Pe) for i in idx])
        di = np.array([np.trace(Vs[i]) for i in idx]) - rac
        dec = {}
        for nm, ch in (("Rac", rac), ("Di", di)):
            dec[nm] = {a: r(np.mean(ch * np.conj(b)), 6) for a, b in irr.items() if abs(np.mean(ch * np.conj(b))) > 1e-8}
        # does the Z3 label of the little group act as a Pauli Z-type (level) grading?  order-3 element's Weil image
        Uc = Vs[index[F.key(c)]]
        diag_in_comp_basis = bool(np.allclose(Uc, np.diag(np.diag(Uc)), atol=1e-9))
        out[name] = dict(order=len(L), decomposition=dec, order3_generator_is_diagonal_phase_gate=diag_in_comp_basis,
                         order3_generator_is_transvection=bool(np.linalg.matrix_rank((c - F.I4) % 3) == 1))
    return out


def main():
    keys, mats, Vs, index, coc = S.weil_group()
    res = {"pass_ids": [11839, 11840, 11841, 11842]}
    res["crosscap"] = crosscaps(mats, Vs, index)
    print("crosscap", res["crosscap"], flush=True)
    res["free_fields"] = free_fields(mats)
    print("free", json.dumps(res["free_fields"], default=str), flush=True)
    C = S.characters(keys, mats, Vs, index)
    res["couplings"] = couplings(C)
    print("couplings", json.dumps(res["couplings"], default=str), flush=True)
    res["massive_spin"] = massive_spin(mats, Vs, index)
    print("spin", res["massive_spin"], flush=True)
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
