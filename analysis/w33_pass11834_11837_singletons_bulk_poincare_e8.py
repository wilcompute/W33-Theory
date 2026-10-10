"""Passes 11834-11837: the finite AdS4 of two qutrits (Passes 11831-11833) as a field theory skeleton.

11834  Finite Dirac singletons.  The linear Weil representation of Sp(4,3) on C^9 (built here exactly: transvection
       lifts with det 1 and order 3, the residual mu3 cocycle solved) splits as Rac + Di = W_e (5) + W_o (4).
       Flato-Fronsdal test: decompose singleton bilinears against the bulk (36 Kramers), boundary (40 contexts),
       split (45) and point (40) permutation modules.
11835  Bulk modes and boundary reconstruction: C[36] irreducible content, the orthogonality graph on the bulk, and the
       rank of the bulk-boundary incidence (which bulk modes the boundary can see).
11836  Finite Poincare group M x SL(2,9) on the tangent Minkowski space of a Kramers reversal: plane-wave spectra of the
       invariant operators (mass shells), and Wigner little groups of null, Kramers-type and split-type momenta.
11837  The two-qutrit E8 (Pass 11681) under the Weil-lifted Clifford group: Sp(4,3) content of sl9 and Lambda^3, and
       the centraliser in E8 of the finite Lorentz group SL(2,9).
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
import w33_pass11681_e8_from_two_qutrits as E  # noqa: E402
import w33_pass11831_11833_finite_ads4 as F  # noqa: E402

OUT = ROOT / "data" / "w33_pass11834_11837_singletons_bulk_poincare_e8.json"
P3 = 3
W3 = np.exp(2j * np.pi / 3)
TAU = W3**2  # tau^2 = omega, tau^3 = 1: symmetric Weyl operators, Clifford action without phases
X1 = np.roll(np.eye(3), 1, 0)
Z1 = np.diag([1, W3, W3 * W3])


def d1(x, z):
    return np.linalg.matrix_power(X1, x) @ np.linalg.matrix_power(Z1, z) * TAU ** ((x * z) % 3)


def weyl(v):
    """v = (x1, x2, z1, z2), the coordinate order of Passes 11831-11833."""
    v = [int(t) % 3 for t in v]
    return np.kron(d1(v[0], v[2]), d1(v[1], v[3]))


def intertwiner(g):
    """U with U D(e_i) U^-1 = D(g e_i) for the four basis vectors (unique up to scalar)."""
    rows = []
    I9 = np.eye(9)
    for i in range(4):
        e = np.zeros(4, dtype=np.int64)
        e[i] = 1
        Di, Dg = weyl(e), weyl(g @ e % 3)
        rows.append(np.kron(I9, Di.T) - np.kron(Dg, I9))
    M = np.vstack(rows)
    _, s, vh = np.linalg.svd(M)
    assert s[-1] < 1e-9 and s[-2] > 1e-3
    U = vh[-1].conj().reshape(9, 9)
    return U / abs(np.linalg.det(U)) ** (1 / 9)


def det1_order3(U):
    U = U / np.linalg.det(U) ** (1 / 9)
    for k in range(9):
        V = U * np.exp(2j * np.pi * k / 9)
        if np.allclose(V @ V @ V, np.eye(9), atol=1e-9) and abs(np.linalg.det(V) - 1) < 1e-9:
            return V
    raise AssertionError("no det-1 order-3 lift")


GEN_VECS = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1), (1, 1, 0, 0), (1, 0, 0, 1)]


def weil_group():
    """BFS over Sp(4,3) with det-1 order-3 transvection lifts, then remove the mu3 cocycle."""
    gens = [F.transvection(np.array(v)) for v in GEN_VECS]
    lifts = [det1_order3(intertwiner(g)) for g in gens]
    keys, mats, Vs, cnt = [F.key(F.I4)], [F.I4], [np.eye(9, dtype=complex)], [np.zeros(6, dtype=np.int64)]
    index = {keys[0]: 0}
    edges = []
    frontier = [0]
    while frontier:
        nxt = []
        for h in frontier:
            for s, (g, L) in enumerate(zip(gens, lifts)):
                x = F.m(g, mats[h])
                k = F.key(x)
                prod = L @ Vs[h]
                if k not in index:
                    index[k] = len(keys)
                    keys.append(k)
                    mats.append(x)
                    Vs.append(prod)
                    c = cnt[h].copy()
                    c[s] += 1
                    cnt.append(c % 3)
                    nxt.append(index[k])
                else:
                    j = index[k]
                    a, b = np.unravel_index(np.argmax(abs(Vs[j])), (9, 9))
                    r = prod[a, b] / Vs[j][a, b]
                    assert np.allclose(prod, r * Vs[j], atol=1e-8)
                    edges.append((s, h, j, int(round(np.angle(r) / (2 * np.pi / 3))) % 3))
        frontier = nxt
    assert len(keys) == 51840
    cnt = np.array(cnt)
    ok = None
    for e in itertools.product(range(3), repeat=6):
        e = np.array(e)
        Ex = cnt @ e % 3
        if all((a + e[s] + Ex[h] - Ex[j]) % 3 == 0 for s, h, j, a in edges):
            ok = Ex
            break
    assert ok is not None, "cocycle not a coboundary"
    Vs = [V * W3 ** int(x) for V, x in zip(Vs, ok)]
    cocycle_nontrivial = any(a for _, _, _, a in edges)
    return keys, mats, Vs, index, cocycle_nontrivial


def check_weil(keys, mats, Vs, index, rng):
    worst = 0.0
    for _ in range(300):
        i, j = rng.integers(0, len(keys), 2)
        k = index[F.key(F.m(mats[i], mats[j]))]
        worst = max(worst, float(abs(Vs[i] @ Vs[j] - Vs[k]).max()))
    exact = 0.0
    for i in rng.integers(0, len(keys), 40):
        for v in F.VECS[::9]:
            exact = max(exact, float(abs(Vs[i] @ weyl(v) @ Vs[i].conj().T - weyl(mats[i] @ v % 3)).max()))
    return dict(homomorphism_max_error=worst, clifford_action_max_error=exact)


# ---------------------------------------------------------------- characters
def ip(a, b):
    return complex(np.sum(a * np.conj(b)) / len(a))


def r(z, nd=6):
    z = complex(z)
    return round(z.real, nd) if abs(z.imag) < 1e-7 else [round(z.real, nd), round(z.imag, nd)]


def characters(keys, mats, Vs, index):
    N = len(keys)
    P = Vs[index[F.key((-F.I4) % 3)]]
    assert np.allclose(P @ P, np.eye(9)) and abs(np.trace(P) - 1) < 1e-9  # 5 - 4
    Pe = (np.eye(9) + P) / 2
    chi = np.array([np.trace(V) for V in Vs])
    chie = np.array([np.trace(V @ Pe) for V in Vs])
    chio = chi - chie
    sq = np.array([index[F.key(F.m(g, g))] for g in mats])
    cu = np.array([index[F.key(F.m(g, g, g))] for g in mats])
    # permutation characters on the bivector quadric classes and on points / nonzero vectors
    Jarr = np.array([F.JM[k] for k in F.PTS])
    cls = np.array([F.Q[k] for k in F.PTS])
    vecs = np.array(F.VECS)
    perm = {c: np.zeros(N) for c in ("contexts40", "splits45", "kramers36", "points40", "vectors80")}
    for n, g in enumerate(mats):
        gi = F.inv(g)
        M = np.einsum("ij,njk,kl->nil", g, Jarr, gi) % 3
        fixed = np.all(M == Jarr, axis=(1, 2)) | np.all(M == (-Jarr) % 3, axis=(1, 2))
        perm["contexts40"][n] = np.sum(fixed & (cls == 0))
        perm["splits45"][n] = np.sum(fixed & (cls == 1))
        perm["kramers36"][n] = np.sum(fixed & (cls == 2))
        gv = (vecs @ g.T) % 3
        fv = np.all(gv == vecs, axis=1)
        perm["vectors80"][n] = np.sum(fv)
        perm["points40"][n] = np.sum(fv | np.all(gv == (-vecs) % 3, axis=1)) / 2
    return dict(N=N, chi=chi, chie=chie, chio=chio, sq=sq, cu=cu, perm=perm, P=P)


def sym2(c, sq):
    return (c**2 + c[sq]) / 2


def alt2(c, sq):
    return (c**2 - c[sq]) / 2


def alt3(c, sq, cu):
    return (c**3 - 3 * c[sq] * c + 2 * c[cu]) / 6


def singletons(C):
    """11834: Rac = W_e (5), Di = W_o (4); Flato-Fronsdal style decompositions."""
    chie, chio, sq, perm = C["chie"], C["chio"], C["sq"], C["perm"]
    one = np.ones(C["N"])
    mods = {"1": one, **perm}
    out = {"norms": {"Rac": r(ip(chie, chie)), "Di": r(ip(chio, chio)), "Rac_vs_conj": r(ip(chie, np.conj(chie))),
                     "Di_vs_conj": r(ip(chio, np.conj(chio))), "Rac_vs_Di": r(ip(chie, chio))},
           "frobenius_schur": {"Rac": r(np.mean(chie[sq])), "Di": r(np.mean(chio[sq]))}}
    prods = {
        "Rac x Rac*": chie * np.conj(chie), "Di x Di*": chio * np.conj(chio), "Rac x Di*": chie * np.conj(chio),
        "Rac x Rac": chie**2, "Di x Di": chio**2, "Rac x Di": chie * chio,
        "Sym2 Rac": sym2(chie, sq), "Alt2 Rac": alt2(chie, sq), "Sym2 Di": sym2(chio, sq), "Alt2 Di": alt2(chio, sq),
    }
    table = {}
    for name, c in prods.items():
        table[name] = dict(dim=r(c[0]), norm=r(ip(c, c)), **{f"<{m}>": r(ip(c, v)) for m, v in mods.items()})
    out["bilinears"] = table
    # identities: two-singleton states = functions on phase space
    even = chie * np.conj(chie) + chio * np.conj(chio)
    odd = chie * np.conj(chio) + chio * np.conj(chie)
    out["Rac.Rac* + Di.Di* == 1 + C[40 points]"] = bool(np.allclose(even, 1 + perm["points40"]))
    out["Rac.Di* + Di.Rac* == C[80 vectors] - C[40 points]"] = bool(np.allclose(odd, perm["vectors80"] - perm["points40"]))
    # irreducible pieces by peeling
    pieces = {}
    base = {"C[36]-1": perm["kramers36"] - 1, "C[40c]-1": perm["contexts40"] - 1, "C[45]-1": perm["splits45"] - 1,
            "C[40p]-1": perm["points40"] - 1, "RacRac*-1": chie * np.conj(chie) - 1, "DiDi*-1": chio * np.conj(chio) - 1,
            "RacDi*": chie * np.conj(chio), "Sym2Rac": sym2(chie, sq), "Alt2Rac": alt2(chie, sq),
            "Sym2Di": sym2(chio, sq), "Alt2Di": alt2(chio, sq), "RacDi": chie * chio}
    gram = {a: {b: r(ip(x, y), 4) for b, y in base.items()} for a, x in base.items()}
    pieces["gram"] = gram
    out["overlaps"] = pieces
    return out


def bulk_boundary(C):
    """11835: bulk modes on the 36, boundary reconstruction rank."""
    K = [k for k in F.PTS if F.Q[k] == 2]
    X = [k for k in F.PTS if F.Q[k] == 0]
    S = [k for k in F.PTS if F.Q[k] == 1]
    A = np.array([[1.0 if a != b and F.beta(a, b) == 0 else 0.0 for b in K] for a in K])
    ev = Counter(int(round(x)) for x in np.linalg.eigvalsh(A))
    A2 = A @ A
    lam = sorted({int(A2[i, j]) for i in range(36) for j in range(36) if i != j and A[i, j]})
    mu = sorted({int(A2[i, j]) for i in range(36) for j in range(36) if i != j and not A[i, j]})
    Nkb = np.array([[1.0 if F.beta(a, x) == 0 else 0.0 for x in X] for a in K])
    Nks = np.array([[1.0 if F.beta(a, f) == 0 else 0.0 for f in S] for a in K])
    perm = C["perm"]
    # eigenspaces of A against the boundary image
    w, U = np.linalg.eigh(A)
    img = Nkb @ np.linalg.pinv(Nkb)  # projector onto the column space of Nkb (in C[36])
    seen = {}
    for lamb in sorted(set(int(round(x)) for x in w)):
        cols = U[:, np.isclose(w, lamb)]
        seen[str(lamb)] = dict(dim=int(cols.shape[1]), visible_from_boundary=int(round(np.trace(cols.T @ img @ cols))))
    return dict(
        orthogonality_graph=dict(degree=sorted({int(x) for x in A.sum(1)}), lam=lam, mu=mu, spectrum=dict(sorted(ev.items(), reverse=True))),
        rank_C36=r(ip(perm["kramers36"], perm["kramers36"])),
        common_bulk_boundary=r(ip(perm["kramers36"], perm["contexts40"])),
        common_bulk_splits=r(ip(perm["kramers36"], perm["splits45"])),
        incidence_bulk_boundary=dict(shape=[36, 40], row_sum=sorted({int(x) for x in Nkb.sum(1)}), col_sum=sorted({int(x) for x in Nkb.sum(0)}),
                                     rank=int(np.linalg.matrix_rank(Nkb))),
        incidence_bulk_splits=dict(rank=int(np.linalg.matrix_rank(Nks))),
        bulk_eigenspaces_seen_by_boundary=seen,
    )


# ---------------------------------------------------------------- Poincare
SL23 = {1: 1, 2: 1, 3: 8, 4: 6, 6: 8}


def poincare(mats):
    k0 = next(k for k in F.PTS if F.Q[k] == 2)
    J0 = F.JM[k0]
    cent = [g for g in mats if np.array_equal(F.m(g, J0), F.m(J0, g))]
    stab = [g for g in mats if F.act(g, k0) == k0]
    vecs = {F.key(F.I4 * 0)}
    for k in F.PTS:
        if F.beta(k, k0) == 0:
            for s in (1, 2):
                vecs.add(F.key(s * F.JM[k]))
    vecs = sorted(vecs)
    Vm = {v: np.array(v, dtype=np.int64).reshape(4, 4) for v in vecs}
    Q = {v: F.scalar_of(F.m(Vm[v], Vm[v])) for v in vecs}

    def bet(a, b):
        return (F.scalar_of(F.m(Vm[a], Vm[b]) + F.m(Vm[b], Vm[a])) * 2) % 3

    name = {0: "null", 1: "split_type", 2: "kramers_type"}
    shells = {c: [v for v in vecs if any(v) and Q[v] == c] for c in (0, 1, 2)}
    # plane-wave eigenvalues of the three invariant Cayley operators on each momentum shell
    disp = {}
    for c, S in shells.items():
        row = {}
        for kc, Ks in shells.items():
            vals = {round(float(np.real(sum(W3 ** bet(k, s) for s in S))), 6) for k in Ks}
            row[name[kc]] = sorted(vals)
        row["zero"] = [len(S)]
        disp[f"connection_{name[c]}"] = row

    def order(g):
        x, n = g, 1
        while not np.array_equal(x, F.I4):
            x, n = F.m(x, g), n + 1
        return n

    little = {}
    for c, S in shells.items():
        v = S[0]
        L = [g for g in cent if F.key(F.m(g, Vm[v], F.inv(g))) == v]
        Lf = [g for g in stab if F.key(F.m(g, Vm[v], F.inv(g))) == v]
        stats = Counter(order(g) for g in L)
        o3 = [g for g in L if order(g) == 3]
        abel3 = all(np.array_equal(F.m(a, b), F.m(b, a)) for a in o3 for b in o3)
        seen, classes = set(), []
        for g in L:
            if F.key(g) in seen:
                continue
            cl = {F.key(F.m(h, g, F.inv(h))) for h in L}
            seen |= cl
            classes.append(len(cl))
        byk = {F.key(g): g for g in L}
        D = {F.key(F.m(a, b, F.inv(a), F.inv(b))) for a in L for b in L}
        while True:
            new = {F.key(F.m(byk[x], byk[y])) for x in D for y in D} - D
            if not new:
                break
            D |= new
        little[name[c]] = dict(order=len(L), with_parity=len(Lf), element_orders=dict(sorted(stats.items())),
                               n_classes=len(classes), n_linear_characters=len(L) // len(D),
                               is_SL23_by_order_statistics=dict(stats) == SL23,
                               order3_elements_commute=bool(abel3), n_order3=len(o3))
    return dict(shell_sizes={name[c]: len(S) for c, S in shells.items()}, plane_wave_spectra=disp, little_groups=little,
                lorentz_order=len(cent))


# ---------------------------------------------------------------- E8
TRA = np.array(E.TR)
PERMS = [(p, E.psign(p)) for p in itertools.permutations(range(3))]


def lam3(V):
    out = np.zeros((84, 84), complex)
    for p, s in PERMS:
        term = np.ones((84, 84), complex)
        for row in range(3):
            term = term * V[TRA[:, row][:, None], TRA[:, p[row]][None, :]]
        out += s * term
    return out


def e8(C, mats, Vs):
    chi, sq, cu, perm = C["chi"], C["sq"], C["cu"], C["perm"]
    adj = chi * np.conj(chi) - 1
    l3 = alt3(chi, sq, cu)
    mods = {"1": np.ones(C["N"]), **perm}
    content = {nm: dict(dim=r(c[0]), norm=r(ip(c, c)), **{f"<{m}>": r(ip(c, v)) for m, v in mods.items()})
               for nm, c in (("sl9 (80)", adj), ("Lambda3 (84)", l3))}
    content["<Lambda3, Lambda3*>"] = r(ip(l3, np.conj(l3)))
    # centraliser of the finite Lorentz group SL(2,9) (and of all of Sp(4,3)) in E8
    k0 = next(k for k in F.PTS if F.Q[k] == 2)
    J0 = F.JM[k0]
    Lidx = [i for i, g in enumerate(mats) if np.array_equal(F.m(g, J0), F.m(J0, g))]

    def inv_spaces(idx):
        Pa = sum(np.kron(Vs[i], Vs[i].conj()) for i in idx) / len(idx)  # vec_r(V A V^dag) = (V kron conj V) vec_r(A)
        Px = sum(lam3(Vs[i]) for i in idx) / len(idx)
        Pk = Px.conj()  # dual: Lambda^3 (V^-T) = conj(Lambda^3 V) for unitary V
        def basis(Pm):
            w, U = np.linalg.eig(Pm)
            B = U[:, np.isclose(w, 1, atol=1e-7)]
            q, _ = np.linalg.qr(B)
            return q
        Ba = basis(Pa)
        # drop the identity (trace) direction
        Ba = np.array([b for b in Ba.T])
        A_list = []
        for b in Ba:
            M = b.reshape(9, 9)
            M = M - np.trace(M) / 9 * np.eye(9)
            if np.abs(M).max() > 1e-8:
                A_list.append(M)
        # orthonormalise traceless part
        if A_list:
            Mat = np.array([a.ravel() for a in A_list]).T
            q, rr = np.linalg.qr(Mat)
            keep = np.abs(np.diag(rr)) > 1e-8
            A_list = [q[:, i].reshape(9, 9) for i in range(q.shape[1]) if keep[i]]
        return A_list, basis(Px), basis(Pk)

    out = {"content": content}
    for label, idx in (("lorentz_SL29", Lidx), ("all_Sp43", list(range(len(mats))))):
        A_list, Bx, Bk = inv_spaces(idx)
        dims = dict(sl9=len(A_list), wedge3=int(Bx.shape[1]), wedge3_dual=int(Bk.shape[1]))
        basis = ([(a, np.zeros(84, complex), np.zeros(84, complex)) for a in A_list]
                 + [(np.zeros((9, 9), complex), Bx[:, i], np.zeros(84, complex)) for i in range(Bx.shape[1])]
                 + [(np.zeros((9, 9), complex), np.zeros(84, complex), Bk[:, i]) for i in range(Bk.shape[1])])
        n = len(basis)
        info = dict(dims=dims, total=n)
        if 0 < n <= 40:
            vecs = np.array([E._vec(b) for b in basis]).T
            pinv = np.linalg.pinv(vecs)
            struct = np.zeros((n, n, n), complex)
            closure = 0.0
            for i in range(n):
                for j in range(n):
                    br = E._vec(E.bracket(basis[i], basis[j]))
                    coef = pinv @ br
                    closure = max(closure, float(abs(vecs @ coef - br).max()))
                    struct[i, j] = coef
            ad = np.transpose(struct, (0, 2, 1))  # ad(e_i)[k, j] = c_ij^k
            kill = np.einsum("ikl,jlk->ij", ad, ad)
            der = np.linalg.matrix_rank(struct.reshape(n * n, n).T, tol=1e-7)
            centre = n - np.linalg.matrix_rank(np.concatenate([ad[i] for i in range(n)], axis=0), tol=1e-7)
            rng = np.random.default_rng(11837)
            x = sum(rng.normal() * ad[i] for i in range(n))
            rank_generic = n - np.linalg.matrix_rank(x, tol=1e-7)
            info.update(closure_error=closure, killing_rank=int(np.linalg.matrix_rank(kill, tol=1e-6)),
                        derived_dim=int(der), centre_dim=int(centre), generic_centraliser_dim=int(rank_generic))
        out[label] = info
    return out


def main():
    rng = np.random.default_rng(11834)
    keys, mats, Vs, index, coc = weil_group()
    res = {"pass_ids": [11834, 11835, 11836, 11837], "weil": dict(order=len(keys), mu3_cocycle_was_nontrivial=coc,
                                                                  **check_weil(keys, mats, Vs, index, rng))}
    print("weil", res["weil"], flush=True)
    C = characters(keys, mats, Vs, index)
    res["singletons"] = singletons(C)
    print("singletons", json.dumps(res["singletons"], default=str)[:3000], flush=True)
    res["bulk"] = bulk_boundary(C)
    print("bulk", res["bulk"], flush=True)
    res["poincare"] = poincare(mats)
    print("poincare", res["poincare"], flush=True)
    res["e8"] = e8(C, mats, Vs)
    print("e8", res["e8"], flush=True)
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
