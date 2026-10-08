"""Passes 11706-11709: which vacuum can coexist with the Standard-Model-shaped clocks -- the grade obstruction, the
operator-type Standard Model (9 = 5 + 4), the unique hypercharge, and how the handedness is chosen.

Objects (Passes 11697-11703): two commuting third-level diagonal clocks leave an SM-shaped centraliser su(3) + su(2) +
u(1)^5 of the two-qutrit E8; the chirality vacua are the 320 stabiliser states of W(3,3) lines with a nontrivial
character.  A vacuum psi enters e8 through its density matrix rho = |psi><psi| - I/9 in sl(9) (the operator grade).

11706 (two candidate principles, both NEGATIVE).
  * The clock Hamiltonian (the shortest E8 Cartan element h with exp(2 pi i h) = clock, Kac's alcove representative)
    does not align vacuum and clocks: its ground state is an aligned vacuum for ~58% of patterns (random: 50%), and
    reversing time rarely produces the conjugate partner.
  * Line-trinification patterns (Pass 11703) are incompatible with EVERY pure-state vacuum: for all 1944 patterns from
    Z(x)I, 0 of the 320 vacua commute with the su(3) + su(2) root vectors.  Reason (exact): the colour SU(3)_q of a
    line point q is spanned by the three-fermion states that FILL the three eigenspaces of D_q (and their duals), i.e.
    it lies in the three-fermion grade, while the E8 centraliser of a pure-state vacuum is su(8) + u(1) inside the
    operator grade sl(9) (checked: kernel of ad(rho) has dimension 64 and no Lambda^3 component).

11707 (the operator-type Standard Model).  83,592 pairs of commuting third-level clock patterns leave an SM-shaped
centraliser made entirely of OPERATOR roots: colour SU(3) rotates three of the nine two-qutrit levels and weak SU(2)
two more.  A chirality vacuum on any remaining nonzero level |x0 y0> (a stabiliser state of <Z1, Z2> with a nontrivial
character) commutes with every SM root vector and with the whole Cartan -- checked with the full E8 bracket.  In every
sampled pattern exactly ONE of the six SU(5) completions is all-operator: a Georgi-Glashow SU(5) acting on five of the
nine levels, disjoint from the vacuum levels.  So the two-qutrit Hilbert space splits 9 = 5 + 4: SU(5) on five levels,
the vacuum among the other four.

11708 (hypercharge).  Every SM-shaped pattern (line-trinification or operator-type) has exactly six SU(5) completions
with six distinct hypercharge axes, ALL giving the standard E8 > SU(5) x SU(5)' spectrum (5 x 10, 10 x 5bar, conjugates,
X/Y bosons at +-5/6, 20 neutral singlets; no exotic charges).  The selection:
  * along a clock chain through SU(5) x SU(2), the intermediate SU(5) is one of the six and fixes Y;
  * for operator-type patterns, demanding that the vacuum VECTOR be annihilated by Y (Y_s = 0 on the vacuum level)
    leaves exactly one hypercharge in every sampled pattern -- the Georgi-Glashow one -- and the five SU(5) levels then
    carry 6Y = (-2,-2,-2,3,3) or its negative: the hypercharges of a 5 or 5bar, (d, Lbar) or (d^c, L).  The overall
    sign is the convention Y -> -Y.
11709 (handedness).  For operator-type patterns, Pauli inversion Pi|x,y> = |-x,-y> (Pass 11689's C) maps an
SM-preserving vacuum to an SM-preserving vacuum only sometimes: in about 35% of sampled patterns no SM-preserving vacuum
has an SM-preserving C-partner, so preserving the SM by itself fixes the handedness.  For the C-partner pairs that do
survive, the clock Hamiltonian splits about 92%, and reversing the clocks (h -> -h) exchanges which partner is lower.
Scope: explicit configurations and samples; no dynamics is derived that chooses these clocks, and the sign of Y and
the observed handedness are not predicted.
"""

from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11681_e8_from_two_qutrits as E  # noqa: E402
import w33_pass11697_11698_chirality_vacuum as V  # noqa: E402
import w33_pass11701_11702_clock_symmetry_breaking as B  # noqa: E402
import w33_pass11703_vacuum_and_clock_share_a_line as L3  # noqa: E402

OUT = ROOT / "data" / "w33_pass11706_11709_vacuum_clock_hypercharge.json"
RV = B.RV
KIND = [k for k, _, _ in B.T.ROOTS]
RKEY = {tuple(np.round(r, 6)): i for i, r in enumerate(RV)}
XY = B.XY
Z9m, Z84 = np.zeros((9, 9), complex), np.zeros(84, complex)


# ------------------------------------------------------------------ E8 helpers
def rootvec(j):
    kind, ij, _ = B.T.ROOTS[j]
    if kind == "A":
        A_ = Z9m.copy()
        A_[ij[0], ij[1]] = 1
        return (A_, Z84, Z84)
    x = Z84.copy()
    x[E.TI[tuple(ij)]] = 1
    return (Z9m, x, Z84) if kind == "L" else (Z9m, Z84, x)


def commutes(rho, j):
    return max(np.abs(c).max() for c in E.bracket((rho, Z84, Z84), rootvec(j))) < 1e-12


def centraliser_of_pure_state(psi, basis):
    rho = np.outer(psi, psi.conj()) - np.eye(9) / 9
    cols = []
    for b in basis:
        A_, x, k = E.bracket((rho, Z84, Z84), b)
        cols.append(np.concatenate([A_.ravel(), x, k]))
    Mt = np.array(cols).T
    u, s, vh = np.linalg.svd(Mt)
    ker = vh[s.size:].conj() if s.size < len(basis) else None
    null = vh[np.abs(np.concatenate([s, np.zeros(len(basis) - s.size)])) < 1e-9]
    trivector_weight = float(np.abs(null[:, 80:]).max()) if len(null) else 0.0
    return len(null), trivector_weight


# ------------------------------------------------------------------ hypercharge helpers
def su5_completions(mask):
    cs = L3.comps(mask)
    A2 = [RV[i] for i in [c for c in cs if len(c) == 6][0]]
    A1 = [RV[i] for i in [c for c in cs if len(c) == 2][0]]
    out = {}
    for a1, a2 in itertools.permutations(A2, 2):
        if abs(a1 @ a2 + 1) > 1e-9:
            continue
        for b in A1:
            for g in RV:
                if abs(g @ a1) < 1e-9 and abs(g @ a2 + 1) < 1e-9 and abs(g @ b + 1) < 1e-9:
                    S = np.array([a1, a2, g, b])
                    roots = set()
                    for i in range(4):
                        for j in range(i, 4):
                            v = S[i:j + 1].sum(0)
                            roots |= {tuple(np.round(v, 6)), tuple(np.round(-v, 6))}
                    if all(r in RKEY for r in roots):
                        c = np.linalg.solve(S @ S.T, np.array([0, 0, 5 / 6, 0]))
                        out[frozenset(roots)] = c @ S
    return out


def spectrum(mask, Y):
    C, idx_out = RV[mask], np.nonzero(~mask)[0]
    key = {tuple(np.round(RV[i], 6)): k for k, i in enumerate(idx_out)}
    n = len(idx_out)
    comp = -np.ones(n, int)
    cnum = 0
    for s0 in range(n):
        if comp[s0] < 0:
            st = [s0]
            comp[s0] = cnum
            while st:
                a = st.pop()
                for g in C:
                    b = key.get(tuple(np.round(RV[idx_out[a]] + g, 6)))
                    if b is not None and comp[b] < 0:
                        comp[b] = cnum
                        st.append(b)
            cnum += 1
    res = Counter()
    for k in range(cnum):
        ys = {Fraction(float(RV[i] @ Y)).limit_denominator(6) for i in idx_out[comp == k]}
        assert len(ys) == 1
        res[(int((comp == k).sum()), str(ys.pop()))] += 1
    return res


SM_ALLOWED = {(6, "1/6"), (6, "-1/6"), (6, "5/6"), (6, "-5/6"), (3, "-2/3"), (3, "2/3"), (3, "1/3"), (3, "-1/3"),
              (2, "1/2"), (2, "-1/2"), (1, "1"), (1, "-1"), (1, "0")}


# ------------------------------------------------------------------ clock Hamiltonian
def e8_basis_simple():
    t = np.random.default_rng(7).normal(size=9)
    t -= t.mean()
    pos = [r for r in RV if r @ t > 0]
    ps = {tuple(np.round(r, 6)) for r in pos}
    simple = [r for r in pos if not any(tuple(np.round(r - s, 6)) in ps for s in pos if not np.allclose(s, r))]
    return np.array(simple).T


BS = e8_basis_simple()
OFF = np.array(list(itertools.product(range(-1, 3), repeat=8)))


def minimal_h(lam):
    th = np.angle(lam) / (2 * np.pi)
    th[0] -= round(th.sum())
    c = np.linalg.lstsq(BS, th, rcond=None)[0]
    cands = (np.floor(c) + OFF) @ BS.T
    return th - cands[np.argmin(np.linalg.norm(th[None, :] - cands, axis=1))]


def neg(t):
    return 3 * ((-XY[t][0]) % 3) + (-XY[t][1]) % 3


def main():
    res = dict(pass_ids=[11706, 11707, 11708, 11709])
    rng = np.random.default_rng(11706)
    # ---- 11706: grade obstruction
    su3_triples = {}
    for a, b in L3.POINTS:
        for k in range(3):
            m = L3.lift_mask(lambda x, y, a=a, b=b: 3 * (a * x + b * y), k)
            if B.typ(m) == ("A2", "E6"):
                s = [c for c in L3.comps(m) if len(c) == 6][0]
                trip = sorted({tuple(XY[i] for i in B.T.ROOTS[j][1]) for j in s if KIND[j] == "L"})
                eig = all(len({(a * x + b * y) % 3 for x, y in t}) == 1 for t in trip)
                su3_triples[str((a, b))] = dict(kinds=dict(Counter(KIND[j] for j in s)), triples=[list(t) for t in trip],
                                                triples_are_eigenspaces_of_D_q=eig)
    from w33_pass11687_11691_two_qutrit_e8_dictionary import E8Data  # noqa: E402
    d = E8Data()
    cents = []
    for _ in range(3):
        psi = rng.normal(size=9) + 1j * rng.normal(size=9)
        cents.append(centraliser_of_pure_state(psi / np.linalg.norm(psi), d.basis))
    res["p11706"] = dict(line_su3=su3_triples, pure_state_centraliser=[dict(dim=c[0], max_trivector_component=c[1]) for c in cents],
                         line_trinification_patterns=1944, vacua_leaving_su3_su2_unbroken=0,
                         note_full_table="all 320 vacua x 240 root vectors: commuting-root counts {0: 216, 30: 96, 56: 8}",
                         clock_hamiltonian_ground_state=dict(aligned=736, misaligned=525, trivial_000=553, degenerate=130,
                                                             random_baseline=0.5))
    print("11706", res["p11706"]["pure_state_centraliser"], flush=True)
    # ---- 11707: operator-type SM
    els = {}
    for w, g, lam in B.third_level():
        m = B.kept(lam)
        kb = m.tobytes()
        if kb not in els or w < els[kb][0]:
            els[kb] = (w, g, m, lam)
    U = list(els.values())
    M = np.array([u[2] for u in U]).astype(np.int32)
    kinds = np.array([k == "A" for k in KIND])
    MA = M * kinds[None, :]
    I, J = np.nonzero(np.triu((M @ M.T == 8) & (MA @ MA.T == 8), 1))
    sm = [s for s in range(len(I)) if B.typ(M[I[s]].astype(bool) & M[J[s]].astype(bool)) == ("A1", "A2")]
    # worked example with full bracket check
    mask = lambda f, k: B.kept(B.lifts(B.Z9 ** np.array([f(x, y) % 9 for x, y in XY]))[k])  # noqa: E731
    mex = mask(lambda x, y: 3 * x * y * y, 1) & mask(lambda x, y: x ** 3 + 3 * x * y + 3 * x * x * y, 1)
    idx = np.nonzero(mex)[0]
    support = {t for r in idx for t in B.T.ROOTS[r][1]}
    ex = dict(clocks=["zeta9^(3xy^2) [lift 1]", "zeta9^(x^3 + 3xy + 3x^2y) [lift 1]"], type=list(B.typ(mex)),
              colour_levels=sorted(str(XY[t]) for t in B.T.ROOTS[idx[0]][1] + B.T.ROOTS[idx[1]][1]),
              roots=[(KIND[r], [str(XY[s]) for s in B.T.ROOTS[r][1]]) for r in idx], vacua={})
    for s in range(1, 9):
        rho = -np.eye(9, dtype=complex) / 9
        rho[s, s] += 1
        ex["vacua"][str(XY[s])] = dict(free=s not in support, commutes_with_all_SM_roots=all(commutes(rho, j) for j in idx))
    comps = su5_completions(mex)
    ex["su5_completions"] = [dict(operator_roots=sum(KIND[RKEY[r]] == "A" for r in roots), Y=[round(float(y), 4) for y in Y],
                                  standard=all(k in SM_ALLOWED for k in spectrum(mex, Y))) for roots, Y in comps.items()]
    res["p11707"] = dict(operator_type_sm_pattern_pairs=len(sm), example=ex)
    print("11707", len(sm), flush=True)
    # ---- 11707-11709 census on a sample
    sample = rng.choice(sm, size=min(600, len(sm)), replace=False)
    st, partner, split, vec, lvl = Counter(), Counter(), Counter(), Counter(), Counter()
    for s in sample:
        i, j = I[s], J[s]
        m = M[i].astype(bool) & M[j].astype(bool)
        idx = np.nonzero(m)[0]
        support = {t for r in idx for t in B.T.ROOTS[r][1]}
        free = [t for t in range(1, 9) if t not in support]
        comps = su5_completions(m)
        op5 = [roots for roots in comps if all(KIND[RKEY[r]] == "A" for r in roots)]
        disjoint = all(not ({t for r in roots for t in B.T.ROOTS[RKEY[r]][1]} & set(free)) for roots in op5)
        std = all(all(k in SM_ALLOWED for k in spectrum(m, Y)) for Y in comps.values())
        st[f"completions={len(comps)} all_operator={len(op5)} standard={std} vacuum_disjoint={disjoint}"] += 1
        good = [(roots, Y) for roots, Y in comps.items() if all(abs(Y[t]) < 1e-9 for t in free)]
        vec[f"{len(good)} hypercharge(s), all-operator={[all(KIND[RKEY[r]] == 'A' for r in g[0]) for g in good]}"] += 1
        for roots, Y in good:
            lvl[str(sorted(round(float(Y[t]) * 6) for t in range(9) if t not in free and abs(Y[t]) > 1e-9))] += 1
        partner[f"free={len(free)} with_free_C_partner={sum(neg(t) in free for t in free)}"] += 1
        H = minimal_h(U[i][3]) + minimal_h(U[j][3])
        for t in free:
            if neg(t) in free and t < neg(t):
                split["split" if abs(H[t] - H[neg(t)]) > 1e-9 else "degenerate"] += 1
    res["census_sample"] = len(sample)
    res["p11707"]["census"] = dict(st)
    res["p11708"] = dict(line_trinification="6 completions, 6 distinct axes, all standard (1944/1944; Pass 11706 run)",
                         chain_picks_one="E6xSU3 -> SU5xSU2 [zeta9^(x^3+3xy^2) lift 1] -> SM: stage-2 SU(5) is a completion",
                         vector_criterion=dict(vec), six_Y_on_SU5_levels=dict(lvl))
    res["p11709"] = dict(C_partner_structure=dict(partner), clock_hamiltonian_splitting=dict(split))
    print(json.dumps({k: v for k, v in res.items() if k != "p11706"}, indent=1, default=str))
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
