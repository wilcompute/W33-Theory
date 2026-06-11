#!/usr/bin/env python3
"""
BT823 - The Closure: exact KS maximum, deep magic = polar pair, and the
        self-loop fixed point.  The W(3,3) universal computer, sealed.

  T1. EXACT Kochen-Specker maximum by branch-and-bound over all 2^40
      markings: the true maximum number of contexts satisfiable
      exactly-once (BT818 found >= 36; 40 is impossible = ovoid).
  T2. DEEP MAGIC = POLAR GEOMETRY.  Map the 8 deep-magic rays
      (F = (2+sqrt3)/6, BT822) through the Witting -> W(3,3) isomorphism
      and test whether they form the point set of a hyperbolic polar
      pair {L, L^perp} - the [8,32] orbit of the index-45 maximal
      (BT810/811).  If yes: the magic metallurgy is the vacuum
      geography - the 24-cell vacuum marks the deepest fuel.
  T3. THE SELF-LOOP FIXED POINT (CTC-lite).  The photon's past
      configures its future via teleportation.  WITHOUT the 2-trit
      classical feedforward, the loop channel is
          Phi(rho) = (1/9) sum_ab D_ab U rho U^dag D_ab^dag
      = the completely depolarizing channel: unique fixed point I/q -
      exactly the Bell marginal (BT820).  WITH the 2 trits, the loop is
      unitary.  The machine's arrow of time = the price of forgetting
      its own measurement record: 2 trits per cycle = log3(q^2) = the
      stabilizer order of the Bell line.
"""
from __future__ import annotations

from itertools import combinations, product
import json

import numpy as np


def witting_rays():
    w = np.exp(2j * np.pi / 3.0)
    s3 = np.sqrt(3.0)
    rays = []
    for i in range(4):
        e = np.zeros(4, dtype=complex)
        e[i] = 1.0
        rays.append(e)
    for mu, nu in product(range(3), repeat=2):
        rays.append(np.array([0, 1, -(w**mu), w**nu]) / s3)
        rays.append(np.array([1, 0, -(w**mu), -(w**nu)]) / s3)
        rays.append(np.array([1, -(w**mu), 0, w**nu]) / s3)
        rays.append(np.array([1, w**mu, w**nu, 0]) / s3)
    return rays


def main():
    rays = witting_rays()
    n = 40
    orth = [[abs(np.vdot(rays[i], rays[j])) < 1e-9 for j in range(n)]
            for i in range(n)]
    contexts = [c for c in combinations(range(n), 4)
                if all(orth[i][j] for i, j in combinations(c, 2))]
    assert len(contexts) == 40

    # ---- T1: exact KS maximum by branch and bound -----------------------
    ctx_of = [[] for _ in range(n)]
    for ci, c in enumerate(contexts):
        for r in c:
            ctx_of[r].append(ci)

    best = [36]   # BT818 witness

    cnt = [0] * 40        # marks per context
    decided = [0] * 40    # rays decided per context

    def bound_ok(depth):
        # broken contexts: cnt >= 2, or fully decided with cnt == 0
        broken = 0
        for ci in range(40):
            if cnt[ci] >= 2 or (decided[ci] == 4 and cnt[ci] == 0):
                broken += 1
        return 40 - broken

    def dfs(r):
        ub = bound_ok(r)
        if ub <= best[0]:
            return
        if r == n:
            sat = sum(1 for ci in range(40)
                      if cnt[ci] == 1)
            if sat > best[0]:
                best[0] = sat
            return
        # branch: mark r
        good = True
        for ci in ctx_of[r]:
            cnt[ci] += 1
            decided[ci] += 1
        dfs(r + 1)
        for ci in ctx_of[r]:
            cnt[ci] -= 1
        # branch: don't mark
        dfs(r + 1)
        for ci in ctx_of[r]:
            decided[ci] -= 1

    dfs(0)
    ks_max = best[0]
    print(f"T1 EXACT Kochen-Specker maximum = {ks_max}/40")
    print(f"   contextual deficit = {40 - ks_max} contexts; contextual")
    print(f"   fraction = {(40 - ks_max)}/40")

    # ---- T2: deep magic = polar pair? ------------------------------------
    # deep rays: stabilizer fidelity (2+sqrt3)/6 - recompute grades quickly
    I2 = np.eye(2)
    Xq = np.array([[0, 1], [1, 0]], dtype=complex)
    Zq = np.diag([1, -1]).astype(complex)
    paulis = {}
    for a, b in product(range(2), repeat=2):
        for c, d in product(range(2), repeat=2):
            if (a, b, c, d) == (0, 0, 0, 0):
                continue
            paulis[(a, b, c, d)] = np.kron(
                np.linalg.matrix_power(Xq, a) @ np.linalg.matrix_power(Zq, b),
                np.linalg.matrix_power(Xq, c) @ np.linalg.matrix_power(Zq, d))
    keys = list(paulis)
    triples = set()
    for u, v in combinations(keys, 2):
        if np.allclose(paulis[u] @ paulis[v], paulis[v] @ paulis[u]):
            wk = tuple((u[i] + v[i]) % 2 for i in range(4))
            triples.add(frozenset((u, v, wk)))
    rng = np.random.default_rng(3)
    stab = []
    for T in triples:
        M = sum((rng.normal() + 1j * rng.normal()) * paulis[k] for k in T)
        _, vecs = np.linalg.eig(M)
        for k in range(4):
            psi = vecs[:, k] / np.linalg.norm(vecs[:, k])
            if not any(abs(np.vdot(psi, s))**2 > 1 - 1e-9 for s in stab):
                stab.append(psi)
    deepF = round((2 + np.sqrt(3)) / 6, 6)
    deep_rays = [i for i in range(4, 40)
                 if round(max(abs(np.vdot(rays[i], s))**2
                              for s in stab), 6) == deepF]
    assert len(deep_rays) == 8
    # Witting -> symplectic iso
    import networkx as nx

    def canon(v):
        for x in v:
            if x % 3:
                c = 1 if x % 3 == 1 else 2
                return tuple((c * y) % 3 for y in v)
        raise ValueError

    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})

    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    GW = nx.Graph()
    GW.add_nodes_from(range(n))
    for i, j in combinations(range(n), 2):
        if orth[i][j]:
            GW.add_edge(i, j)
    GS = nx.Graph()
    GS.add_nodes_from(range(40))
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            GS.add_edge(i, j)
    gm = nx.algorithms.isomorphism.GraphMatcher(GW, GS)
    assert gm.is_isomorphic()
    f = gm.mapping
    deep_pts = [pts[f[i]] for i in deep_rays]
    # are they two projective lines of PG(3,3), mutually perp,
    # both non-isotropic?
    found = False
    for quad in combinations(range(8), 4):
        A = [deep_pts[i] for i in quad]
        B = [deep_pts[i] for i in range(8) if i not in quad]
        # A is a projective line iff all points lie in a 2-dim subspace
        M = np.array(A[0]).reshape(1, 4)

        def rank3(vecs):
            arr = np.array(vecs) % 3
            # GF(3) rank
            arr = arr.astype(int).tolist()
            r = 0
            cols = 4
            mat = [row[:] for row in arr]
            for c in range(cols):
                piv = None
                for i in range(r, len(mat)):
                    if mat[i][c] % 3:
                        piv = i
                        break
                if piv is None:
                    continue
                mat[r], mat[piv] = mat[piv], mat[r]
                inv = 1 if mat[r][c] % 3 == 1 else 2
                mat[r] = [(x * inv) % 3 for x in mat[r]]
                for i in range(len(mat)):
                    if i != r and mat[i][c] % 3:
                        fct = mat[i][c]
                        mat[i] = [(x - fct * y) % 3
                                  for x, y in zip(mat[i], mat[r])]
                r += 1
            return r

        if rank3(A) == 2 and rank3(B) == 2:
            # mutual perpendicularity: every a in A perp every b in B
            if all(symp(a, b) == 0 for a in A for b in B):
                # non-isotropic: some pair within A non-perp
                na = any(symp(x, y) != 0 for x, y in combinations(A, 2))
                nb = any(symp(x, y) != 0 for x, y in combinations(B, 2))
                if na and nb:
                    found = True
                    break
    print(f"\nT2 deep-magic 8 rays = hyperbolic polar pair (L, L^perp): "
          f"{found}")

    # ---- T3: self-loop fixed point -----------------------------------------
    w3 = np.exp(2j * np.pi / 3)
    X3 = np.zeros((3, 3), dtype=complex)
    for j in range(3):
        X3[(j + 1) % 3, j] = 1
    Z3 = np.diag([1, w3, w3**2])
    rngu = np.random.default_rng(11)
    A_ = rngu.normal(size=(3, 3)) + 1j * rngu.normal(size=(3, 3))
    U, _ = np.linalg.qr(A_)

    def loop_channel(rho):
        out = np.zeros((3, 3), dtype=complex)
        for a in range(3):
            for b in range(3):
                Dab = (np.linalg.matrix_power(X3, a)
                       @ np.linalg.matrix_power(Z3, b))
                K = Dab @ U
                out += K @ rho @ K.conj().T
        return out / 9

    rho = np.diag([1.0, 0, 0]).astype(complex)
    for _ in range(60):
        rho = loop_channel(rho)
    print(f"T3 self-loop WITHOUT feedforward: fixed point eigenvalues "
          f"{[round(float(x), 6) for x in np.linalg.eigvalsh(rho).real]}")
    assert np.allclose(rho, np.eye(3) / 3, atol=1e-8)
    print("   = I/q exactly: the Bell marginal.  The machine's arrow of")
    print("   time = the cost of discarding its own 2-trit record;")
    print("   with feedforward the loop is unitary (BT821 T3).")

    out = {
        "theorem": "BT823 the closure",
        "ks_exact_max": ks_max,
        "contextual_deficit": 40 - ks_max,
        "deep8_is_polar_pair": bool(found),
        "selfloop_fixed_point": "I/3 (depolarizing without feedforward)",
    }
    with open("data/bt823_the_closure.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt823_the_closure.json")


if __name__ == "__main__":
    main()
