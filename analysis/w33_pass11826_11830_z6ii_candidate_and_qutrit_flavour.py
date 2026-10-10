"""Passes 11826-11830: the Z6-II W(3,3) SU(9) Standard Models ranked by their full Yukawa sector, a Froggatt-Nielsen
estimate of masses and mixing, FI-cancelling D-flatness, mu and proton-decay operators, and qutrit flavour in
four-dimensional SU(9) flavour unification.

Input: data/w33_pass11819_z6ii_probe_fields.json.gz (orbifolder field data of the 9 Z6-II A8 Standard Models with the SM
in SU(9), plus the Codex benchmark).  Selection rules: U(1) charges (exact), hidden N-ality, sector, and the Z6-II R rule
of arXiv:1301.2322 (R1 + 6 gamma = -1 mod 6, R2 = -1 mod 3, R3 = -1 mod 2); insertions are hidden-neutral singlets.

11826 (ranking).  For each model and each pair of Higgs candidates (H_u, H_d) of the right hypercharge, the minimal-degree
matrices of q bu H_u, q bd H_d and l be H_d are computed (MILP); each model is scored by the Froggatt-Nielsen estimate
below at its best (H_u, H_d, epsilon).
11827 (Froggatt-Nielsen estimate).  Y_ij = c_ij eps^{d_ij}, c_ij random O(1) complex (median over samples), compared with
GUT-scale ratios m_c/m_t, m_u/m_t, m_s/m_b, m_d/m_b, m_b/m_t, m_mu/m_tau, m_e/m_tau and |V_us|, |V_cb|, |V_ub|; the score
is the sum of squared log10 deviations.  This is an order-of-magnitude texture test, not a prediction: CFT coefficients,
vector-like mixing and running are not included.
11828 (D-flatness).  Existence of an FI-cancelling D-flat monomial of hidden-neutral singlets: all non-anomalous U(1)s and
hidden N-alities zero and anomalous charge opposite in sign to tr Q_anom (Buccella et al. criterion; F-flatness not
addressed).
11829 (mu, R-parity, proton decay).  Minimal singlet degree of H_u H_d, q l bd, bu bd bd, l l be and q q q l (necessary
rules only; vector-like and identification caveats as in Holotrade 2fa6596).
11830 (qutrit flavour in 4D SU(9)).  The two-qutrit Pauli group has 0 invariants in 9 and in the adjoint 80, and 4 in the 84
(the E8 Cartan, not SU(5)-invariant): exact W(3,3) flavour symmetry is incompatible with SU(5) breaking.  A level-diagonal
GUT breaking preserves exactly the Z-type subgroup <Z1, Z2> = Z3 x Z3 (a W(3,3) line); family charges are the qutrit
coordinates of the family levels, and the exact Z3 x Z3 allows at most one up-type entry per family row: rank 1 (one heavy
family), a degenerate antidiagonal pair, a permutation (degenerate) or zero, so hierarchy requires breaking the line
symmetry by flavour-level vevs.

Result: no model fits; single-cubic-top models get the mass hierarchy but invert V_us/V_cb and allow renormalisable QLd.
"""

from __future__ import annotations

import gzip
import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import w33_pass11681_e8_from_two_qutrits as E  # noqa: E402
import w33_pass11697_11698_chirality_vacuum as V  # noqa: E402
import w33_pass11810_11813_yukawa_textures as Y  # noqa: E402

IN = ROOT / "data" / "w33_pass11819_z6ii_probe_fields.json.gz"
OUT = ROOT / "data" / "w33_pass11826_11830_z6ii_candidate_and_qutrit_flavour.json"
VAR = "z6ii"
OBS = dict(mc_mt=1 / 300, mu_mt=6e-6, ms_mb=0.02, md_mb=1e-3, mb_mt=0.012, mmu_mtau=0.06, me_mtau=3e-4,
           th12=0.227, th23=0.04, th13=0.0037)

TR = E.TR


def deg_matrix(fields, fr, L, R, H, ins, hid=()):
    return {(a, b): Y.min_degree(fields, ins, [a, b, H], hid=hid, variant=VAR) for a in L for b in R}


def fn_estimate(Mu, Md, Me, q, bu, bd, l, be, eps, rng, samples=300):
    def mat(M, rows, cols):
        D = np.array([[M[(r, c)] if M[(r, c)] is not None else np.inf for c in cols] for r in rows], float)
        return D
    Du, Dd, De = mat(Mu, q, bu), mat(Md, q, bd), mat(Me, l, be)
    res = []
    for _ in range(samples):
        def build(D):
            C = rng.normal(size=D.shape) + 1j * rng.normal(size=D.shape)
            C /= np.abs(C)
            C *= rng.uniform(0.5, 2.0, size=D.shape)
            return np.where(np.isfinite(D), C * eps ** np.where(np.isfinite(D), D, 0), 0)
        Yu, Yd, Ye = build(Du), build(Dd), build(De)
        Uu, su, _ = np.linalg.svd(Yu)
        Ud, sd, _ = np.linalg.svd(Yd)
        _, se, _ = np.linalg.svd(Ye)
        if su[0] == 0:
            continue
        V = Uu.conj().T @ Ud
        V = V[:3, :3]
        if min(V.shape) < 3:
            continue
        th13 = abs(V[0, 2]); th12 = abs(V[0, 1]); th23 = abs(V[1, 2])
        safe = lambda a, b: a / b if b > 0 else 0.0  # noqa: E731
        res.append(dict(mc_mt=safe(su[1], su[0]) if len(su) > 1 else 0, mu_mt=safe(su[2], su[0]) if len(su) > 2 else 0,
                        ms_mb=safe(sd[1], sd[0]) if len(sd) > 1 else 0, md_mb=safe(sd[2], sd[0]) if len(sd) > 2 else 0,
                        mb_mt=safe(sd[0], su[0]), mmu_mtau=safe(se[1], se[0]) if len(se) > 1 else 0,
                        me_mtau=safe(se[2], se[0]) if len(se) > 2 else 0, th12=th12, th23=th23, th13=th13))
    med = {k: float(np.median([r[k] for r in res])) for k in OBS} if res else {}
    score = sum((math.log10(max(med[k], 1e-30)) - math.log10(OBS[k])) ** 2 for k in OBS) if med else 1e9
    return med, score


def monomial_milp(fields, ins, constraints_rows, rhs, mods, nonempty=True, cap=30):
    ns = len(ins); nm = sum(1 for m in mods if m)
    A = np.zeros((len(constraints_rows) + (1 if nonempty else 0), ns + nm)); j = 0
    for r, (row, m) in enumerate(zip(constraints_rows, mods)):
        A[r, :ns] = row
        if m:
            A[r, ns + j] = -m; j += 1
    lo, hi = np.array(rhs, float) - 1e-9, np.array(rhs, float) + 1e-9
    if nonempty:
        A[-1, :ns] = 1; lo = np.append(lo, 1); hi = np.append(hi, 1e6)
    res = milp(np.concatenate([np.ones(ns), np.zeros(nm)]), constraints=LinearConstraint(A, lo, hi),
               integrality=np.ones(ns + nm), bounds=Bounds(np.concatenate([np.zeros(ns), -1e4 * np.ones(nm)]), np.concatenate([cap * np.ones(ns), 1e4 * np.ones(nm)])))
    return None if res.status != 0 else {ins[i]: int(round(res.x[i])) for i in range(ns) if round(res.x[i])}


def anomalous_index(fields):
    nU = len(next(iter(fields.values()))['u1'])
    tr = []
    for a in range(nU):
        t = 0
        for v in fields.values():
            t += float(v['u1'][a]) * int(np.prod([abs(x) for x in v['dims']]))
        tr.append(t)
    i = int(np.argmax(np.abs(tr)))
    return i, tr[i], tr


def dflat_fi(fields, singlets, hid):
    """FI-cancelling D-flat monomial: all non-anomalous U(1)s zero, hidden N-ality zero, anomalous charge opposite to tr."""
    ia, tra, _ = anomalous_index(fields)
    nU = len(next(iter(fields.values()))['u1'])
    rows, rhs, mods = [], [], []
    for a in range(nU):
        if a == ia:
            continue
        rows.append([float(fields[s]['u1'][a]) for s in singlets]); rhs.append(0.0); mods.append(0)
    for pos, kind in hid:
        m = {'su5': 5, 'su4': 4, 'su2': 2}[kind]
        rows.append([Y.nality(fields[s]['dims'][pos], kind) for s in singlets]); rhs.append(0.0); mods.append(m)
    # anomalous charge: sign opposite to tr, normalise to at least magnitude of one unit (use inequality via slack)
    ns = len(singlets); nm = sum(1 for m in mods if m)
    A = np.zeros((len(rows) + 1, ns + nm)); j = 0
    for r, (row, m) in enumerate(zip(rows, mods)):
        A[r, :ns] = row
        if m:
            A[r, ns + j] = -m; j += 1
    A[-1, :ns] = [float(fields[s]['u1'][ia]) * (1 if tra > 0 else -1) for s in singlets]
    lo = np.append(np.zeros(len(rows)) - 1e-9, -1e9); hi = np.append(np.zeros(len(rows)) + 1e-9, -1e-6)
    res = milp(np.concatenate([np.ones(ns), np.zeros(nm)]), constraints=LinearConstraint(A, lo, hi), integrality=np.ones(ns + nm),
               bounds=Bounds(np.concatenate([np.zeros(ns), -1e4 * np.ones(nm)]), np.concatenate([20 * np.ones(ns), 1e4 * np.ones(nm)])))
    return None if res.status != 0 else {singlets[i]: int(round(res.x[i])) for i in range(ns) if round(res.x[i])}


def analyse(f, text, rng):
    fields = Y.parse_text(text); fr = Y.frame(fields)
    yi = fr['yi']
    q = sorted(n for n in fields if n.startswith('q_')); bu = sorted(n for n in fields if n.startswith('bu_'))
    bd = sorted(n for n in fields if n.startswith('bd_')); l = sorted(n for n in fields if n.startswith('l_')); be = sorted(n for n in fields if n.startswith('be_'))
    ins = fr['pure_singlets']
    yu = -(fields[q[0]]['u1'][yi] + fields[bu[0]]['u1'][yi]); yd = -(fields[q[0]]['u1'][yi] + fields[bd[0]]['u1'][yi])
    hu_c = [h for h in fr['pure_doublets'] if fields[h]['u1'][yi] == yu]
    hd_c = [h for h in fr['pure_doublets'] if fields[h]['u1'][yi] == yd]
    best = None
    # up Higgs: the one with exactly one cubic entry and smallest total degree
    for hu in hu_c:
        Mu = deg_matrix(fields, fr, q, bu, hu, ins)
        fin = [v for v in Mu.values() if v is not None]
        if not fin:
            continue
        for hd in hd_c:
            if hd == hu:
                continue
            Md = deg_matrix(fields, fr, q, bd, hd, ins)
            Me = deg_matrix(fields, fr, [x for x in l if x != hd], be, hd, ins)
            if not [v for v in Md.values() if v is not None]:
                continue
            lred = [x for x in l if x != hd]
            for eps in (0.1, 0.15, 0.2, 0.3):
                med, score = fn_estimate(Mu, Md, Me, q, bu, bd, lred, be, eps, rng, samples=150)
                if best is None or score < best['score']:
                    best = dict(file=f, hu=hu, hd=hd, eps=eps, score=score, est=med,
                                up=Y.finite({f'{a}.{b}': v for (a, b), v in Mu.items()}),
                                n_up_cubic=sum(v == 0 for v in Mu.values()),
                                down_min=min(v for v in Md.values() if v is not None),
                                lep_min=min((v for v in Me.values() if v is not None), default=None))
    if best is None:
        return dict(file=f, viable=False)
    hu, hd = best['hu'], best['hd']
    # mu term and dangerous operators (minimal singlet degree, z6ii rule, pure singlets)
    md = lambda base: Y.min_degree(fields, ins, base, variant=VAR)  # noqa: E731
    lep = [x for x in l if x != hd]
    best['mu_degree'] = md([hu, hd])
    best['qLd_min'] = min((d for d in (md([a, x, b]) for a in q for x in lep[:4] for b in bd[:6]) if d is not None), default=None)
    best['udd_min'] = min((d for d in (md([a, b, c]) for a in bu for b, c in itertools.combinations(bd[:6], 2)) if d is not None), default=None)
    best['LLe_min'] = min((d for d in (md([x, y, e]) for x, y in itertools.combinations(lep[:5], 2) for e in be) if d is not None), default=None)
    best['QQQL_min'] = min((d for d in (md([a, b, c, x]) for a, b, c in itertools.combinations_with_replacement(q, 3) for x in lep[:4]) if d is not None), default=None)
    best['FI_dflat_monomial'] = dflat_fi(fields, ins, fr['hid'])
    best['anomalous_trace'] = anomalous_index(fields)[1]
    return best




TR = E.TR


def invariant_dims():
    ops = [V.weyl(v) for v in V.nonzero(2)]
    gens = [V.weyl((1, 0, 0, 0)), V.weyl((0, 1, 0, 0)), V.weyl((0, 0, 1, 0)), V.weyl((0, 0, 0, 1))]
    # 9: irreducible
    P9 = sum(ops + [np.eye(9)]) / 81
    # adjoint 80: invariants of X -> D X D^-1 on traceless matrices
    adj = lambda D: np.kron(D, D.conj())  # noqa: E731 (acts on vec(X))
    Padj = sum(adj(D) for D in ops + [np.eye(9)]) / 81
    inv_adj = int(round(np.real(np.trace(Padj)))) - 1   # subtract identity (trace part)
    # 84: wedge^3 of the Pauli (projectively: phases cancel only for invariants up to centre; use exact group average)
    P84 = sum(lam3(D) for D in ops + [np.eye(9)]) / 81
    return dict(fundamental_9=int(round(np.real(np.trace(P9)))), adjoint_80=inv_adj, wedge3_84=int(round(np.real(np.trace(P84)))))


def lam3(D):
    """Lambda^3 representation of a group element D (84x84)."""
    M = np.zeros((84, 84), complex)
    for c, T in enumerate(TR):
        cols = D[:, list(T)]
        for r, S in enumerate(TR):
            M[r, c] = np.linalg.det(cols[list(S), :])
    return M




def z3z3_textures():
    gut = [(0, 0), (0, 1), (0, 2), (2, 1), (2, 2)]
    free = [(1, 0), (1, 1), (1, 2), (2, 0)]
    add = lambda *ps: tuple(sum(p[i] for p in ps) % 3 for i in range(2))  # noqa: E731
    gsum = add(*gut)
    out, kinds = {}, {}
    for vac in free:
        fam = [f for f in free if f != vac]
        for hpair in itertools.combinations(free, 2):
            Yt = [[int(add(fi, fj, *hpair, gsum) == (0, 0)) for fj in fam] for fi in fam]
            rows = [sum(r) for r in Yt]
            kind = "rank-1 (one heavy family)" if sum(rows) == 1 else ("permutation (degenerate)" if rows == [1, 1, 1] else
                    ("zero" if sum(rows) == 0 else "pair (antidiagonal)"))
            out[f"vac{vac} H{hpair}"] = dict(texture=Yt, kind=kind)
            kinds[kind] = kinds.get(kind, 0) + 1
    return dict(textures=out, kinds=kinds, max_entries_per_row=max(max(sum(r) for r in v["texture"]) for v in out.values()))


def main():
    with gzip.open(IN, "rt") as g:
        models = json.load(g)["models"]
    rng = np.random.default_rng(11826)
    ranking = {}
    for f, text in models.items():
        ranking[f] = analyse(f, text, rng)
        print(f, {k: ranking[f].get(k) for k in ("score", "eps", "hu", "hd", "n_up_cubic", "mu_degree", "FI_dflat_monomial")}, flush=True)
    ordered = sorted((v for v in ranking.values() if v.get("score") is not None), key=lambda v: v["score"])
    res = dict(pass_ids=[11826, 11827, 11828, 11829, 11830], ranking=ranking,
               best=ordered[0] if ordered else None, order=[(v["file"], round(v["score"], 2)) for v in ordered],
               qutrit_flavour=dict(pauli_invariants=invariant_dims(), z3z3=z3z3_textures()))
    json.dump(res, open(OUT, "w"), indent=1, default=str)
    print(json.dumps(dict(order=res["order"], invariants=res["qutrit_flavour"]["pauli_invariants"],
                          z3z3_kinds=res["qutrit_flavour"]["z3z3"]["kinds"]), indent=1, default=str))


if __name__ == "__main__":
    main()
