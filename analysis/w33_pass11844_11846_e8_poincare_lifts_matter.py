"""Passes 11844-11846: the finite Poincare group inside E8, the two Weyl lifts of the finite Lorentz group, and the matter.

Setting (Pass 11843): E8 > E6 x A2, a Kramers reversal = an E6 root alpha, its finite Lorentz group = W(A5)' with
A5 = the E6 roots orthogonal to alpha; E8 > SU(6) x SU(3) x SU(2) with SU(6) the A5 group.

11844  Translations.  W(A5)' acts on E8/3E8 = F3^8 through the Weyl group.  Every invariant subspace is found; a 4-dim
       invariant subspace W with elliptic form (lambda,lambda)/2 mod 3 and orbits 1+20+30+30 is a copy of the tangent
       Minkowski space M of Pass 11833.  Its order-3 torus elements t_lambda (t e_beta = omega^{(lambda,beta)} e_beta)
       with the Weyl-lifted Lorentz group form a finite Poincare group M x A6 inside Aut(E8); its commutant is computed.
11845  Two lifts.  Besides the Tits lift (commutant su(3)+su(2), Pass 11843) W(A5)' has the permutation lift inside SU(6)
       (permutation matrices on C^6 = 1 + 5).  Its commutant, the inclusion of the Tits commutant in it, and the
       centraliser of su(3)+su(2) inside it (the direction separating the lifts) with its ad-spectrum on E8.
11846  Matter.  E8 under (that u(1)) x su(3) x su(2) x (Lorentz): multiplicities of every Standard-Model-type multiplet
       and the Lorentz representation each carries.
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
import w33_pass11843_e8_tits_lorentz_commutant as T  # noqa: E402

OUT = ROOT / "data" / "w33_pass11844_11846_e8_poincare_lifts_matter.json"
N = T.N
W3 = np.exp(2j * np.pi / 3)


def setup(rng):
    T.SIGN = 1
    B = T.bracket_basis()
    assert T.jacobi(B, rng) < 1e-8
    R = T.ROOTS
    g1 = R[0]
    g2 = next(r for r in R if T.ip(g1, r) == -1)
    E6 = [r for r in R if T.ip(r, g1) == 0 and T.ip(r, g2) == 0]
    A2 = [r for r in R if all(T.ip(r, e) == 0 for e in E6)]
    alpha = E6[0]
    A5 = [r for r in E6 if T.ip(r, alpha) == 0]
    A1 = [r for r in E6 if all(T.ip(r, e) == 0 for e in A5)]
    simple = T.simple_system(A5, rng)
    # order the A5 simple roots as a chain beta_1 - ... - beta_5
    adj = {b: [c for c in simple if c != b and T.ip(b, c) == -1] for b in simple}
    chain = [next(b for b in simple if len(adj[b]) == 1)]
    while len(chain) < 5:
        chain.append(next(c for c in adj[chain[-1]] if c not in chain))
    return B, dict(E6=E6, A2=A2, A1=A1, A5=A5, alpha=alpha, chain=chain)


def torus_sign(gamma):
    """h_gamma(-1): e_beta -> (-1)^{(gamma, beta)} e_beta."""
    d = np.ones(N)
    for i, b in enumerate(T.ROOTS):
        d[8 + i] = (-1) ** (T.ip(gamma, b) % 2)
    return np.diag(d)


def torus_order3(lam):
    d = np.ones(N, complex)
    for i, b in enumerate(T.ROOTS):
        d[8 + i] = W3 ** (T.ip(lam, b) % 3)
    return np.diag(d)


def e_ab(chain, a, b):
    """root e_a - e_b (positions 1..6) in E8 simple-root coordinates."""
    lo, hi = min(a, b), max(a, b)
    v = np.zeros(8, dtype=int)
    for k in range(lo, hi):
        v += np.array(chain[k - 1])
    return tuple(v if a < b else -v)


def perm_lift(B, chain, convention):
    """even permutations s_i s_j lifted as permutation matrices: n_i n_j D_{s_j(i)} D_j (D_k = -1 at position k)."""
    n = [T.tits(B, b) for b in chain]

    def pos(i):
        return i if convention == 0 else i + 1

    def P(i, j):
        a = pos(i)
        a_img = {j: j + 1, j + 1: j}.get(a, a)
        b = pos(j)
        M = n[i - 1] @ n[j - 1]
        if a_img != b:
            M = M @ torus_sign(e_ab(chain, a_img, b))
        return M
    return P, n


def order_ok(M, k):
    X = np.eye(N)
    for _ in range(k):
        X = X @ M
    return bool(np.allclose(X, np.eye(N), atol=1e-8))


def basis_contains(Bsub, Bbig):
    Pb = Bbig @ np.linalg.pinv(Bbig)
    return bool(np.allclose(Pb @ Bsub, Bsub, atol=1e-7))


def centraliser_within(B, Bbig, Bsmall):
    """y in span(Bbig) with [y, x] = 0 for all x in span(Bsmall)."""
    rows = []
    for j in range(Bsmall.shape[1]):
        rows.append(np.column_stack([T.br(B, Bbig[:, i], Bsmall[:, j]) for i in range(Bbig.shape[1])]))
    A = np.vstack(rows)
    _, s, vh = np.linalg.svd(A)
    null = vh[np.sum(s > 1e-8):].T
    return Bbig @ null


def group_from(gens, limit=2000):
    keyf = lambda M: tuple(np.round(M[::7, ::5].real, 6).ravel()) + tuple(np.round(M[::7, ::5].imag, 6).ravel())  # noqa: E731
    elems = [np.eye(N)]
    keys = {keyf(elems[0])}
    frontier = [elems[0]]
    while frontier:
        nxt = []
        for h in frontier:
            for g in gens:
                x = g @ h
                k = keyf(x)
                if k not in keys:
                    keys.add(k)
                    elems.append(x)
                    nxt.append(x)
                    if len(elems) > limit:
                        return elems
        frontier = nxt
    return elems


# ---------------------------------------------------------------- 11844 translations
def weyl_mod3(chain):
    def refl(b):
        b = np.array(b)
        return np.array([[int(k == j) for k in range(8)] for j in range(8)]) - np.outer(T.C @ b, b).T  # columns act on coords
    S = []
    for b in chain:
        bb = np.array(b)
        M = np.zeros((8, 8), dtype=int)
        for j in range(8):
            e = np.zeros(8, dtype=int)
            e[j] = 1
            M[:, j] = e - T.ip(e, bb) * bb
        S.append(M % 3)
    gens = [(S[i] @ S[i + 1]) % 3 for i in range(4)]
    G = {tuple(np.eye(8, dtype=int).ravel())}
    fr = [np.eye(8, dtype=int)]
    while fr:
        nx = []
        for h in fr:
            for g in gens:
                x = (g @ h) % 3
                k = tuple(x.ravel())
                if k not in G:
                    G.add(k)
                    nx.append(x)
        fr = nx
    return [np.array(k).reshape(8, 8) for k in G]


def rowspace_key(vs):
    """canonical key of a subspace of F3^8 via reduced row echelon form."""
    M = np.array(vs, dtype=int) % 3
    M = M.copy()
    r = 0
    for c in range(8):
        piv = next((i for i in range(r, len(M)) if M[i, c] % 3), None)
        if piv is None:
            continue
        M[[r, piv]] = M[[piv, r]]
        M[r] = (M[r] * (1 if M[r, c] == 1 else 2)) % 3
        for i in range(len(M)):
            if i != r and M[i, c]:
                M[i] = (M[i] - M[i, c] * M[r]) % 3
        r += 1
        if r == len(M):
            break
    return tuple(map(tuple, M[:r]))


def submodules(G):
    subs = set()
    for v in itertools.product(range(3), repeat=8):
        if not any(v):
            continue
        orb = {tuple((g @ np.array(v)) % 3) for g in G}
        subs.add(rowspace_key(list(orb)))
    # close under sums
    changed = True
    while changed:
        changed = False
        cur = list(subs)
        for a, b in itertools.combinations(cur, 2):
            k = rowspace_key(list(a) + list(b))
            if k not in subs:
                subs.add(k)
                changed = True
    return subs


def span_vectors(basis):
    out = []
    for c in itertools.product(range(3), repeat=len(basis)):
        out.append(tuple(int(x) for x in (np.array(c) @ np.array(basis)) % 3))
    return out


def qform(v):
    return (T.ip(v, v) // 2) % 3


def translations(B, sub, G):
    subs = submodules(G)
    dims = Counter(len(s) for s in subs)
    cands = []
    for s in subs:
        if len(s) != 4:
            continue
        vecs = [v for v in span_vectors(s) if any(v)]
        qs = Counter(qform(v) for v in vecs)
        # orbits under G
        seen, orbs = set(), []
        for v in vecs:
            if v in seen:
                continue
            o = {tuple((g @ np.array(v)) % 3) for g in G}
            seen |= o
            orbs.append(len(o))
        # radical of the bilinear form on s
        bil = np.array([[T.ip(a, b) % 3 for b in s] for a in s])
        cands.append(dict(basis=[list(map(int, v)) for v in s], q_counts={str(k): v for k, v in sorted(qs.items())},
                          orbits=sorted(orbs), form_rank_mod3=int(np.linalg.matrix_rank(bil) if False else rank_mod3(bil))))
    return dims, cands


def rank_mod3(M):
    M = np.array(M, dtype=int) % 3
    r = 0
    rows, cols = M.shape
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i, c]), None)
        if piv is None:
            continue
        M[[r, piv]] = M[[piv, r]]
        M[r] = (M[r] * (1 if M[r, c] == 1 else 2)) % 3
        for i in range(rows):
            if i != r and M[i, c]:
                M[i] = (M[i] - M[i, c] * M[r]) % 3
        r += 1
    return r


def joint_labels(B, sub, adY_n):
    """Casimirs of the su(2) (A1) and su(3) (A2) factors; joint eigen-decomposition with the normalised Y."""
    def casimir(gens):
        G = np.array(gens).T
        K = np.zeros((N, N), complex)
        kil = np.array([[np.trace(T.ad(B, a) @ T.ad(B, b)) for b in G.T] for a in G.T])
        kinv = np.linalg.inv(kil)
        ads = [T.ad(B, a) for a in G.T]
        for i in range(len(ads)):
            for j in range(len(ads)):
                if abs(kinv[i, j]) > 1e-12:
                    K = K + kinv[i, j] * ads[i] @ ads[j]
        return K
    su2 = [T.vec_root(r) for r in sub["A1"]] + [np.concatenate([np.array(sub["A1"][0], float), np.zeros(240)])]
    su3 = [T.vec_root(r) for r in sub["A2"]] + [np.concatenate([np.array(r, float), np.zeros(240)]) for r in sub["A2"][:2]]
    C2, C3 = casimir(su2), casimir(su3)
    Mix = adY_n + np.pi * C2 + np.e * C3
    w, V = np.linalg.eig(Mix)
    groups = {}
    for k in range(N):
        v = V[:, k]
        nv = v.conj() @ v
        key = (str(Fraction(float(np.real(v.conj() @ adY_n @ v / nv))).limit_denominator(6)),
               round(float(np.real(v.conj() @ C2 @ v / nv)), 4), round(float(np.real(v.conj() @ C3 @ v / nv)), 4))
        groups.setdefault(key, []).append(k)
    return V, groups


def analyse_complex(B, Bs, rng):
    """T.analyse with complex structure constants (torus elements of order 3 make the fixed basis complex)."""
    n = Bs.shape[1]
    pinv = np.linalg.pinv(Bs)
    st = np.zeros((n, n, n), complex)
    clos = 0.0
    for i in range(n):
        for j in range(n):
            v = T.br(B, Bs[:, i], Bs[:, j])
            c = pinv @ v
            clos = max(clos, float(abs(Bs @ c - v).max()))
            st[i, j] = c
    adm = np.transpose(st, (0, 2, 1))
    der = np.linalg.matrix_rank(st.reshape(n * n, n), tol=1e-7)
    centre = n - np.linalg.matrix_rank(np.concatenate(list(adm), axis=0), tol=1e-7)
    x = np.tensordot(rng.normal(size=n) + 1j * rng.normal(size=n), adm, axes=1)
    rank = n - np.linalg.matrix_rank(x, tol=1e-7)
    return dict(dim=n, closure_error=clos, derived_dim=int(der), centre_dim=int(centre), rank=int(rank))


def five_dim_translations(B, sub, Gmod3, lifts, rng):
    subs = submodules(Gmod3)
    dims = Counter(len(s) for s in subs)
    five = [s for s in subs if len(s) == 5]
    out = dict(submodule_dims={str(k): v for k, v in sorted(dims.items())}, four_dim_submodules=0)
    if len(five) != 1:
        out["five_dim"] = None
        return out
    W5 = five[0]
    vecs = [v for v in span_vectors(W5) if any(v)]
    bil = np.array([[T.ip(a, b) % 3 for b in W5] for a in W5])
    rad = [v for v in vecs if all(T.ip(v, w) % 3 == 0 for w in W5)]
    lines_inside = [s for s in subs if len(s) == 1 and all(tuple(x) in set(vecs) for x in s)]
    # quotient by the radical: orbits of the induced quadratic form classes
    q = Counter(qform(v) for v in vecs)
    # A5 coroot lattice mod 3 check: is W5 spanned by the A5 roots?
    a5span = rowspace_key([list(r) for r in sub["A5"]])
    out["five_dim"] = dict(form_rank_mod3=rank_mod3(bil), radical_size=len(rad) + 1, invariant_lines_inside=len(lines_inside),
                           q_counts={str(k): v for k, v in sorted(q.items())}, equals_A5_lattice_mod3=(a5span == W5))
    # quotient W5/rad: orbit structure of nonzero classes under the Weyl action
    radset = set(rad) | {tuple([0] * 8)}
    classes = {}
    for v in vecs:
        if v in radset:
            continue
        key = min(tuple(int(x) for x in ((np.array(v) + np.array(rv)) % 3)) for rv in radset)
        classes[key] = v
    seen, orbs = set(), []
    for c, v in classes.items():
        if c in seen:
            continue
        o = set()
        for g in Gmod3:
            w = (g @ np.array(v)) % 3
            o.add(min(tuple(int(x) for x in ((w + np.array(rv)) % 3)) for rv in radset))
        seen |= o
        orbs.append(len(o))
    out["five_dim"]["quotient_orbits_nonzero"] = sorted(orbs)
    tg = [torus_order3(np.array(v)) for v in W5]
    comm = {}
    for name, gens in lifts.items():
        Bc = T.fixed_subalgebra(gens + tg)
        info = analyse_complex(B, Bc, rng)
        info["contains_su3_A2"] = basis_contains(np.column_stack([T.vec_root(r) for r in sub["A2"]]), Bc)
        info["contains_su2_alpha"] = basis_contains(np.column_stack([T.vec_root(r) for r in sub["A1"]]), Bc)
        comm[name] = info
    out["poincare_with_central_Z3_commutants"] = comm
    return out


def main():
    rng = np.random.default_rng(11844)
    B, sub = setup(rng)
    chain = sub["chain"]
    res = {"pass_ids": [11844, 11845, 11846]}
    tits = [T.tits(B, b) for b in chain]
    adj_gens = [tits[i] @ tits[i + 1] for i in range(4)]
    ext_gens = [a @ b for a, b in itertools.permutations(tits, 2)]  # the group of Pass 11843
    lift = None
    for conv in (0, 1):
        P, _ = perm_lift(B, chain, conv)
        gens = [P(i, i + 1) for i in range(1, 5)]
        if all(order_ok(g, 3) for g in gens) and all(order_ok(P(i, j), 2) for i in range(1, 6) for j in range(i + 2, 6)):
            lift = (conv, gens)
            break
    assert lift is not None
    conv, perm_gens = lift
    G_adj = group_from(adj_gens, limit=400)
    G_perm = group_from(perm_gens, limit=400)
    # does the extension group contain torus 2-elements?  test h_beta(-1) membership via fixed-space inclusion
    h1 = torus_sign(chain[0])
    res["lifts"] = dict(adjacent_tits_order=len(G_adj), permutation_order=len(G_perm), permutation_convention=conv,
                        extension_contains_h_beta1_product=bool(np.allclose((tits[0] @ tits[1]) @ (tits[1] @ tits[0]), tits[0] @ h1 @ tits[0], atol=1e-8)))
    C_adj = T.fixed_subalgebra(adj_gens)
    C_perm = T.fixed_subalgebra(perm_gens)
    C_ext = T.fixed_subalgebra(ext_gens)
    C_adj_torus = T.fixed_subalgebra(adj_gens + [torus_sign(b) for b in chain])
    res["commutants"] = dict(A6_adjacent=T.analyse(B, C_adj, rng), A6_permutation=T.analyse(B, C_perm, rng),
                             extension_11843=T.analyse(B, C_ext, rng), A6_plus_torus_signs=T.analyse(B, C_adj_torus, rng),
                             ext_inside_A6_adjacent=basis_contains(C_ext, C_adj),
                             A6_adjacent_equals_permutation=basis_contains(C_adj, C_perm) and basis_contains(C_perm, C_adj))
    print(json.dumps(res, default=str), flush=True)
    Y = centraliser_within(B, C_adj, C_ext)
    res["hypercharge"] = dict(centraliser_dim=int(Y.shape[1]))
    if Y.shape[1] == 1:
        adY = T.ad(B, Y[:, 0])
        ev = np.linalg.eigvals(adY)
        top = ev[np.argmax(abs(ev))]
        adY_n = adY / top
        evn = ev / top
        assert np.allclose(evn.imag, 0, atol=1e-6)
        cnt = Counter(np.round(evn.real, 6))
        spec = {str(Fraction(float(k)).limit_denominator(6)): v for k, v in sorted(cnt.items())}
        gg = {"0": 36, "5/6": 6, "-5/6": 6, "1/6": 30, "-1/6": 30, "2/3": 15, "-2/3": 15, "1": 5, "-1": 5,
              "1/3": 30, "-1/3": 30, "1/2": 20, "-1/2": 20}
        res["hypercharge"].update(spectrum=spec, equals_georgi_glashow_pattern=(spec == gg))
        # A6 together with a hypercharge rotation exp(2 pi i Y'/7) (Y' = 6Y integral): commutant = centraliser of Y in su(5)
        evals, evecs = np.linalg.eig(adY_n)
        rot = (evecs @ np.diag(np.exp(2j * np.pi * np.round(6 * evals.real) / 7)) @ np.linalg.inv(evecs)).real
        C_sm = T.fixed_subalgebra(adj_gens + [rot])
        sm = T.analyse(B, C_sm, rng)
        sm["contains_su3_A2"] = basis_contains(np.column_stack([T.vec_root(r) for r in sub["A2"]]), C_sm)
        sm["contains_su2_alpha"] = basis_contains(np.column_stack([T.vec_root(r) for r in sub["A1"]]), C_sm)
        res["A6_plus_hypercharge_rotation_commutant"] = sm
        print("SM commutant", sm, flush=True)
        print(res["hypercharge"], flush=True)
        V, groups = joint_labels(B, sub, adY_n)
        table = []
        for key, idx in sorted(groups.items(), key=lambda t: (Fraction(t[0][0]), t[0][1], t[0][2])):
            Vs = V[:, idx]
            Vp = np.linalg.pinv(Vs)
            chars = np.array([np.trace(Vp @ g @ Vs) for g in G_adj])
            table.append(dict(Y=key[0], su2_casimir=key[1], su3_casimir=key[2], dim=len(idx),
                              lorentz_char_norm=round(float(np.real(np.mean(abs(chars) ** 2))), 4),
                              lorentz_invariants=round(float(np.real(np.mean(chars))), 4)))
        res["matter"] = table
        for row in table:
            print(row, flush=True)
    Gmod3 = weyl_mod3(chain)
    res["translations"] = five_dim_translations(B, sub, Gmod3, {"A6_adjacent": adj_gens, "extension_11843": ext_gens}, rng)
    print("translations", res["translations"], flush=True)
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
