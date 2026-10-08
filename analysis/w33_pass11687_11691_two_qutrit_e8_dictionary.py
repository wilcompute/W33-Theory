"""Passes 11687-11691: the two-qutrit E8 dictionary (Claude track).

Uses the explicit e8 = sl(9) + Lambda^3 C^9 + Lambda^3 C^9* of two qutrits (Pass 11681), graded by Pauli charge
v in F3^4 with E8_0 = the Pauli-singlet Cartan h and dim E8_v = 3 (v != 0).  For a subgroup S of Pauli charges the
centraliser is h + sum_{v in S^perp} E8_v (symplectic perp), so the symplectic subspace lattice of F3^4 maps to regular
subalgebras of E8 containing h.

11687  CENTRALISERS AND TRIALITY.
       point p                 -> E6 + A2   (dim 86; prior art BT7175/7181, the 1 + 12 + 27 shell)
       hyperplane p^perp       -> A2        (the point's own SU(3))
       Lagrangian line L       -> A2^4      (one SU(3) per point of the W(3,3) line; L^perp = L)
       one qutrit's Paulis H   -> D4        (roots on the other qutrit's 8 charges); H, H^perp give a dual pair D4 x D4
       For every tensor factorisation the 192 roots at the 64 mixed charges fall into exactly three cosets of
       E8/(D4 + D4) = (8v,8v) + (8s,8s) + (8c,8c), every mixed charge has its three roots in three different cosets, and
       the Eisenstein rotation (the Z3 grading sl9 / Lambda^3 / Lambda^3*) cycles the cosets: D4 TRIALITY is the Z3
       grading, i.e. it cycles the operator, three-fermion and three-hole faces of each Pauli charge.
11688  THE MAGIC GATE.  T (x) I (T = diag(1, zeta9, zeta9^-1)) acts on E8 with fixed subalgebra of dim 82 = E6 + A1 + T1
       and eigenphase multiplicities 82 + 2*54 + 2*27 + 2*2 (the E8 |3|-grading, prior art PASS20260925 and
       Kraft-Regeta-Zimmermann); T^3 = Z (x) I has fixed E6 + A2 (dim 86).  So the qutrit magic gate is
       exp(2 pi i Y/9), Y = diag(1, 1, -2) in the A2 of its cube: it keeps E6 and breaks SU(3)_p to SU(2) x U(1),
       (27,3) -> (27,2) + (27,1).
11689  CHIRALITY = C x T.  For a point p and an extended-Clifford element g with g(p) = eps p (eps = +-1) and
       tau = +1 (unitary) / -1 (antiunitary), g preserves the matter shell (27,3)_p (the omega-eigenspace of Ad P) iff
       eps * tau = +1 and swaps it with (27bar,3bar) iff eps * tau = -1 (checked on all four classes).  Pauli inversion
       (C-like) and antiunitarity (T-like) each flip chirality and their product preserves it.  A Clifford-invariant time
       arrow (tau-odd, eps-even, e.g. h6) therefore cannot select chirality; the lowest-degree selector transforming as
       eps*tau is Im <P> (relative to the chosen point), the omega / omega^2 population imbalance of the family Pauli.
11690  THE INTERTWINER.  With symmetric Weyl operators D_v = tau^(x.z) X^x Z^z, Codex's zero-character projectors (Pass 11663)
       have odd rank 1 and give a Witting configuration.  The Clifford-equivariant intertwiner from that odd sector to the
       trivector Cartan is ANTILINEAR (no linear one exists), unique up to scale and unitary, and maps all 40 Codex rays
       exactly onto the 40 E8 root rays, relabelling points by the anti-symplectic swap (x, z) -> (z, x).  So Codex's
       quartic Maschke-to-Burkhardt map has the E8 root directions as its base locus.  (Corrects Pass 11681's
       "16/40", which used non-symmetric Paulis.)
11691  WHY TWO QUTRITS.  sl(V) + Lambda^3 V + Lambda^3 V* closes into a Z3-graded Lie algebra only when the bracket
       Lambda^3 x Lambda^3 -> Lambda^6 V = Lambda^(n-6) V* lands in Lambda^3 V*, i.e. dim V = 9 = two qutrits; together with
       Pass 11658 (factorisations act as reflections only at n = 2) this singles out two qutrits twice.
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

OUT = ROOT / "data" / "w33_pass11687_11691_two_qutrit_e8_dictionary.json"
W3 = np.exp(2j * np.pi / 3)


def om(a, b):
    return (a[0] * b[1] - a[1] * b[0] + a[2] * b[3] - a[3] * b[2]) % 3


def proj(v):
    lead = next(x for x in v if x)
    return tuple((x * lead) % 3 for x in v)


def span(gens):
    return {tuple(sum(c * g[j] for c, g in zip(cs, gens)) % 3 for j in range(4))
            for cs in itertools.product(range(3), repeat=len(gens))}


def perp(S):
    return {v for v in itertools.product(range(3), repeat=4) if all(om(v, s) == 0 for s in S)}


class E8Data:
    def __init__(self, seed=11687):
        rng = np.random.default_rng(seed)
        self.basis, self.Sl, self.Slp = E.e8_basis()
        hcoef = E.cartan_trivectors()
        Z9, Z84 = np.zeros((9, 9), complex), np.zeros(84, complex)
        self.hcoef = hcoef
        cart = [(Z9, c, Z84) for c in hcoef] + [(Z9, Z84, c) for c in hcoef]
        ad = [np.array([self.coords(E.bracket(h, b)) for b in self.basis]).T for h in cart]
        cg = rng.normal(size=8) + 1j * rng.normal(size=8)
        ev, V = np.linalg.eig(sum(c * a for c, a in zip(cg, ad)))
        self.R = V[:, np.abs(ev) > 1e-6]
        self.alpha = np.array([[np.vdot(self.R[:, i], a @ self.R[:, i]) / np.vdot(self.R[:, i], self.R[:, i]) for a in ad]
                               for i in range(240)])
        gensP = [np.kron(E.X1, np.eye(3)), np.kron(E.Z1, np.eye(3)), np.kron(np.eye(3), E.X1), np.kron(np.eye(3), E.Z1)]
        self.deg = []
        for i in range(240):
            e = self.elem(self.R[:, i])
            v = []
            for D in gensP:
                f = self.coords(self.act(D, e))
                lam = np.vdot(self.R[:, i], f) / np.vdot(self.R[:, i], self.R[:, i])
                v.append(int(round(np.angle(lam) / (2 * np.pi / 3))) % 3)
            self.deg.append(tuple(v))
        w4 = self.alpha[:, :4]
        X = np.concatenate([w4.real, w4.imag], 1)
        self.X = X / np.sqrt((X[0] @ X[0]) / 2)
        self.Gram = self.X @ self.X.T

    def coords(self, e):
        return np.concatenate([self.Slp @ e[0].ravel(), e[1], e[2]])

    def elem(self, c):
        return ((self.Sl @ c[:80]).reshape(9, 9), c[80:164], c[164:])

    @staticmethod
    def act(U, e, anti=False):
        A, x, k = e
        if anti:
            A, x, k = A.conj(), x.conj(), k.conj()
        Uc = U.conj()
        return (U @ A @ U.conj().T, E.sorted_c(np.einsum("ai,bj,ck,ijk->abc", U, U, U, E.full(x))),
                E.sorted_c(np.einsum("ai,bj,ck,ijk->abc", Uc, Uc, Uc, E.full(k))))

    def Ad(self, U, anti=False):
        return np.array([self.coords(self.act(U, b, anti)) for b in self.basis]).T

    def components(self, idx):
        idx = list(idx)
        n = len(idx)
        comp = -np.ones(n, int)
        c = 0
        for s in range(n):
            if comp[s] < 0:
                stack = [s]
                comp[s] = c
                while stack:
                    a = stack.pop()
                    for b in range(n):
                        if comp[b] < 0 and abs(self.Gram[idx[a], idx[b]]) > 1e-6:
                            comp[b] = c
                            stack.append(b)
                c += 1
        return sorted(np.bincount(comp).tolist(), reverse=True) if n else []


def pass11687(d):
    out = {}
    cases = {"point (Z on qutrit 1)": span([(0, 1, 0, 0)]),
             "hyperplane p^perp": perp(span([(0, 1, 0, 0)])),
             "Lagrangian line <Z1,Z2>": span([(0, 1, 0, 0), (0, 0, 0, 1)]),
             "qutrit-1 Paulis (tensor factor)": span([(1, 0, 0, 0), (0, 1, 0, 0)])}
    for name, S in cases.items():
        Sp = perp(S)
        idx = [i for i in range(240) if d.deg[i] in Sp and d.deg[i] != (0, 0, 0, 0)]
        out[name] = dict(roots=len(idx), dim=8 + len(idx), components=d.components(idx))
    # triality for the standard factorisation
    Hp = {v for v in itertools.product(range(3), repeat=4) if v[0] == 0 and v[1] == 0}
    Hq = {v for v in itertools.product(range(3), repeat=4) if v[2] == 0 and v[3] == 0}
    D = [i for i in range(240) if (d.deg[i] in Hp or d.deg[i] in Hq)]
    mixed = [i for i in range(240) if i not in D]
    B = []
    for i in D:
        if np.linalg.matrix_rank(np.array(B + [d.X[i]])) > len(B):
            B.append(d.X[i])
        if len(B) == 8:
            break
    B = np.array(B).T

    def key(x):
        c = np.linalg.solve(B, x)
        return tuple(int(t) for t in np.round((c - np.floor(c + 1e-9)) * 2) % 2)
    keys = Counter(key(d.X[i]) for i in mixed)
    by = {}
    for i in mixed:
        by.setdefault(d.deg[i], []).append(key(d.X[i]))
    w4 = d.alpha[:, :4]

    def rot(i):
        t = W3 * w4[i]
        return int(np.argmin(np.abs(w4 - t).sum(1)))
    cyc = Counter((key(d.X[i]), key(d.X[rot(i)])) for i in mixed)
    out["triality"] = dict(D4xD4_roots=len(D), mixed_roots=len(mixed), coset_sizes=sorted(keys.values()),
                           mixed_charges_with_three_distinct_cosets=sum(len(set(v)) == 3 for v in by.values()),
                           mixed_charges=len(by), omega_coset_map=sorted(cyc.values()),
                           omega_cycles_three_cosets=len(cyc) == 3 and len({a for a, _ in cyc}) == 3
                           and all(a != b for a, b in cyc))
    return out


def pass11688(d):
    z9 = np.exp(2j * np.pi / 9)
    out = {}
    for name, U in (("Z(x)I", np.kron(np.diag([1, W3, W3 * W3]), np.eye(3))),
                    ("T(x)I", np.kron(np.diag([1, z9, z9 ** -1]), np.eye(3)))):
        ev = np.linalg.eigvals(d.Ad(U))
        out[name] = dict(fixed_dim=int(np.sum(np.abs(ev - 1) < 1e-8)),
                         eigenphase_multiplicities_units_2pi_over_9={
                             str(k): v for k, v in sorted(Counter(round(np.angle(e) / (2 * np.pi / 9)) % 9 for e in ev).items())})
    # root systems w.r.t. the diagonal Cartan of sl9
    roots = []
    for i in range(9):
        for j in range(9):
            if i != j:
                v = np.zeros(9)
                v[i], v[j] = 1, -1
                roots.append(v)
    for T in itertools.combinations(range(9), 3):
        v = np.zeros(9)
        v[list(T)] = 1
        v -= 1 / 3
        roots += [v, -v]
    roots = np.array(roots)
    for name, expo, mod in (("Z(x)I", np.array([0, 0, 0, 1, 1, 1, 2, 2, 2]), 3), ("T(x)I", np.array([0, 0, 0, 1, 1, 1, -1, -1, -1]), 9)):
        R = np.array([r for r in roots if abs(round(r @ expo) - r @ expo) < 1e-9 and round(r @ expo) % mod == 0])
        G = R @ R.T
        n = len(R)
        comp = -np.ones(n, int)
        c = 0
        for s in range(n):
            if comp[s] < 0:
                stack = [s]
                comp[s] = c
                while stack:
                    a = stack.pop()
                    for b in range(n):
                        if comp[b] < 0 and abs(G[a, b]) > 1e-9:
                            comp[b] = c
                            stack.append(b)
                c += 1
        out[name]["fixed_roots"] = n
        out[name]["root_components"] = sorted(np.bincount(comp).tolist(), reverse=True)
    return out


def pass11689(d):
    Zq = np.diag([1, W3, W3 * W3])
    Fq = np.array([[W3 ** (a * b) for b in range(3)] for a in range(3)]) / np.sqrt(3)
    P = np.kron(Zq, np.eye(3))
    ev, V = np.linalg.eig(d.Ad(P))
    Vw, Vw2 = V[:, np.abs(ev - W3) < 1e-8], V[:, np.abs(ev - W3 * W3) < 1e-8]

    def lands(U, anti):
        imgs = np.array([d.coords(d.act(U, d.elem(Vw[:, i]), anti)) for i in range(Vw.shape[1])]).T
        if np.linalg.norm(imgs - Vw @ np.linalg.lstsq(Vw, imgs, rcond=None)[0]) < 1e-6:
            return "preserves (27,3)"
        if np.linalg.norm(imgs - Vw2 @ np.linalg.lstsq(Vw2, imgs, rcond=None)[0]) < 1e-6:
            return "swaps to (27bar,3bar)"
        return "neither"
    F2 = np.kron(Fq @ Fq, np.eye(3))
    tests = {"eps=+1 unitary (identity)": (np.eye(9), False, +1),
             "eps=-1 unitary (F^2 on qutrit 1)": (F2, False, -1),
             "eps=-1 antiunitary (K)": (np.eye(9), True, +1),
             "eps=+1 antiunitary (F^2 K)": (F2, True, -1)}
    out = {name: dict(result=lands(U, anti), eps_times_tau=et) for name, (U, anti, et) in tests.items()}
    out["character_is_eps_times_tau"] = all((v["result"] == "preserves (27,3)") == (v["eps_times_tau"] == 1)
                                            for v in out.values() if isinstance(v, dict))
    return out


def pass11690(d):
    import w33_pass11651_n_qutrit_hesse_space as H
    _, _, _, _, wg = H.setup(2)
    w4 = d.alpha[:, :4]
    root = {}
    for i in range(240):
        root.setdefault(proj(d.deg[i]), w4[i] / np.linalg.norm(w4[i]))
    P40 = sorted(root)
    oddb = np.array([(np.eye(9)[E.IDX[u]] - np.eye(9)[E.IDX[tuple((-x) % 3 for x in u)]]) / np.sqrt(2) for u in E.DIRS]).T
    tau = W3 ** 2
    cod, ranks = {}, []
    for v in P40:
        Dv = E.pauli(v) * tau ** ((v[0] * v[1] + v[2] * v[3]) % 3)
        Lv = (np.eye(9) + Dv + Dv.conj().T) / 3
        O = oddb.conj().T @ Lv @ oddb
        e_, V_ = np.linalg.eigh(O)
        ranks.append(int((e_ > 0.5).sum()))
        cod[v] = V_[:, np.argmax(e_)]
    C = np.array([cod[v] for v in P40])
    out = dict(odd_ranks=sorted(set(ranks)),
               codex_ray_overlaps=sorted(set(np.round((np.abs(C.conj() @ C.T) ** 2)[~np.eye(40, dtype=bool)], 6).tolist())))
    Hc = np.array(d.hcoef).T
    Hc = Hc / np.linalg.norm(Hc, axis=0)
    act3 = lambda g, c: E.sorted_c(np.einsum("ai,bj,ck,ijk->abc", g, g, g, E.full(c)))  # noqa: E731
    Rg = [Hc.conj().T @ np.array([act3(g, Hc[:, j]) for j in range(4)]).T for g in wg.values()]
    Og = [oddb.conj().T @ g @ oddb for g in wg.values()]

    def nullspace(A, tol=1e-8):
        _, s, Vh = np.linalg.svd(A)
        return Vh[int((s > tol).sum()):].conj().T
    res = {}
    for anti in (True, False):
        sols = [np.eye(16, dtype=complex)]
        for Rm, Om in zip(Rg, Og):
            Ot = Om.conj() if anti else Om
            cands = {complex(np.round(a / b, 8)) for a in np.linalg.eigvals(Rm) for b in np.linalg.eigvals(Ot)}
            new = []
            for S in sols:
                for c in cands:
                    N = nullspace((np.kron(Rm, np.eye(4)) - c * np.kron(np.eye(4), Ot.T)) @ S)
                    if N.shape[1]:
                        new.append(S @ N)
            sols = new
        res["antilinear" if anti else "linear"] = [S.shape[1] for S in sols]
        if anti and len(sols) == 1 and sols[0].shape[1] == 1:
            Mm = sols[0][:, 0].reshape(4, 4)
            Mm = Mm / np.sqrt(abs(np.trace(Mm @ Mm.conj().T)) / 4)
            out["intertwiner_unitary"] = bool(np.allclose(Mm @ Mm.conj().T, np.eye(4), atol=1e-6))
            perm = {}
            for v in P40:
                x = Mm @ cod[v].conj()
                x = x / np.linalg.norm(x)
                hit = [q for q in P40 if abs(abs(np.vdot(root[q], x)) - 1) < 1e-6]
                if len(hit) == 1:
                    perm[v] = hit[0]
            out["codex_rays_onto_root_rays"] = len(perm)
            out["label_map_is_xz_swap"] = int(sum(perm.get(v) == proj((v[1], v[0], v[3], v[2])) for v in P40))
    out["intertwiner_solution_space_dims"] = res
    return out


def pass11691():
    return dict(rule="Lambda^3 V x Lambda^3 V -> Lambda^6 V = Lambda^(n-6) V*; equals Lambda^3 V* iff n - 6 = 3",
                closing_dimensions=[n for n in range(3, 40) if n - 6 == 3],
                two_qutrit_dimension=9)


def main():
    d = E8Data()
    res = dict(pass_ids=[11687, 11688, 11689, 11690, 11691])
    res["11687"] = pass11687(d)
    print("11687", res["11687"], flush=True)
    res["11688"] = pass11688(d)
    print("11688", res["11688"], flush=True)
    res["11689"] = pass11689(d)
    print("11689", res["11689"], flush=True)
    res["11690"] = pass11690(d)
    print("11690", res["11690"], flush=True)
    res["11691"] = pass11691()
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
