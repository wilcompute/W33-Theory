#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_20260924_bell_shell_quadratic_history_intertwiner.json"
MOD = 3


def mkey(A):
    return tuple(int(x) for x in np.asarray(A).reshape(-1))


def canon(v):
    for x in v:
        if x % MOD:
            s = 1 if x % MOD == 1 else 2
            return tuple((s*y) % MOD for y in v)
    raise ValueError


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def inv_mod(A):
    A = np.array(A, dtype=int) % MOD
    n = A.shape[0]
    aug = np.concatenate([A, np.eye(n, dtype=int)], axis=1) % MOD
    r = 0
    for c in range(n):
        pivots = [i for i in range(r, n) if aug[i, c] % MOD]
        if not pivots:
            raise ValueError("singular")
        piv = pivots[0]
        aug[[r, piv]] = aug[[piv, r]]
        aug[r] = (aug[r] * pow(int(aug[r, c]), -1, MOD)) % MOD
        for i in range(n):
            if i != r and aug[i, c] % MOD:
                aug[i] = (aug[i] - aug[i, c] * aug[r]) % MOD
        r += 1
    return aug[:, n:] % MOD


def build_w33():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})
    pidx = {p:i for i,p in enumerate(pts)}

    def symp(x, y):
        return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1]) % MOD

    adj = [[False]*40 for _ in range(40)]
    for i,j in combinations(range(40), 2):
        adj[i][j] = adj[j][i] = (symp(pts[i], pts[j]) == 0)
    lines = [frozenset(q) for q in combinations(range(40), 4)
             if all(adj[i][j] for i,j in combinations(q, 2))]
    assert len(lines) == 40
    lidx = {L:i for i,L in enumerate(lines)}

    def transvection(v):
        out = []
        for x in pts:
            w = symp(x, v)
            y = tuple((x[t] + w*v[t]) % MOD for t in range(4))
            out.append(pidx[canon(y)])
        return tuple(out)


    gens = [transvection(v) for v in pts]
    ident = tuple(range(40))
    group = {ident}
    frontier = [ident]
    while frontier:
        g = frontier.pop()
        for h in gens:
            y = compose(h, g)
            if y not in group:
                group.add(y)
                frontier.append(y)
    assert len(group) == 25920

    def line_perm(g):
        return tuple(lidx[frozenset(g[x] for x in L)] for L in lines)

    lperms = {g: line_perm(g) for g in group}
    return lines, ident, list(group), lperms


def inverse_perm(g):
    inv = [0]*len(g)
    for i,j in enumerate(g):
        inv[j] = i
    return tuple(inv)


def bell_parabolic_module(lines, ident, group, lperms):
    L0 = 0
    base = lines[L0]
    stab = [g for g in group if frozenset(g[x] for x in base) == base]
    assert len(stab) == 648

    O3 = [g for g in stab if all(g[x] == x for x in base)]
    assert len(O3) == 27

    basis = []
    span = {ident}
    for g in sorted(O3):
        if g in span:
            continue
        basis.append(g)
        new = set()
        for x in span:
            cur = x
            for _ in range(3):
                new.add(cur)
                cur = compose(g, cur)
        span = new
        if len(span) == 27:
            break
    assert len(basis) == 3


    coords = {}
    a,b,c = basis
    ai = ident
    for i in range(3):
        bj = ai
        for j in range(3):
            ck = bj
            for k in range(3):
                coords[ck] = (i,j,k)
                ck = compose(c, ck)
            bj = compose(b, bj)
        ai = compose(a, ai)
    assert len(coords) == 27

    image = {}
    for h in stab:
        hi = inverse_perm(h)
        cols = []
        for g in basis:
            cg = compose(compose(h, g), hi)
            cols.append(coords[cg])
        M = np.array(cols, dtype=int).T % MOD
        image[mkey(M)] = M
    assert len(image) == 24


    shell = [m for m in range(40) if m != L0 and not (set(lines[m]) & set(base))]
    assert len(shell) == 27
    M0 = shell[0]
    addr = {}
    for g in O3:
        addr[lperms[g][M0]] = coords[g]
    assert len(addr) == 27
    return stab, O3, image, shell, addr


def sym2_pgl_module():
    basisS = [
        np.array([[1,0],[0,0]], dtype=int),
        np.array([[0,1],[1,0]], dtype=int),
        np.array([[0,0],[0,1]], dtype=int),
    ]

    def coordsS(S):
        return np.array([S[0,0], S[0,1], S[1,1]], dtype=int) % MOD

    image = {}
    for z in product(range(3), repeat=4):
        G = np.array(z, dtype=int).reshape(2,2)
        if int(round(np.linalg.det(G))) % MOD == 0:
            continue

        cols = [coordsS((G @ S @ G.T) % MOD) for S in basisS]
        M = np.column_stack(cols) % MOD
        image[mkey(M)] = M
    assert len(image) == 24
    return image


def gl3():
    for z in product(range(3), repeat=9):
        Q = np.array(z, dtype=int).reshape(3,3)
        try:
            Qi = inv_mod(Q)
        except ValueError:
            continue
        yield Q % MOD, Qi


def find_conjugacy(G1, G2):
    target = set(G2)
    for Q, Qi in gl3():
        conj = {mkey((Q @ A @ Qi) % MOD) for A in G1.values()}
        if conj == target:
            return Q, Qi
    raise AssertionError("modules are not conjugate")


def quadratic_type(v):
    a,b,c = map(int, v)
    if (a,b,c) == (0,0,0):
        return "zero"

    det = (a*c - b*b) % MOD
    if det == 0:
        return "rank1"
    return "invertible_det1" if det == 1 else "invertible_det2"


def main():
    lines, ident, group, lperms = build_w33()
    stab, O3, wmod, shell, addr = bell_parabolic_module(lines, ident, group, lperms)
    qmod = sym2_pgl_module()
    Q, Qi = find_conjugacy(wmod, qmod)

    history = {}
    census = Counter()
    for m, v in sorted(addr.items()):
        svec = tuple(int(x) for x in (Q @ np.array(v, dtype=int)) % MOD)
        typ = quadratic_type(svec)
        census[typ] += 1
        a,b,c = svec
        history[str(m)] = {
            "torsor_address": list(v),
            "symmetric_matrix_coordinates": list(svec),
            "symmetric_matrix": [[a,b],[b,c]],
            "quadratic_type": typ,
        }

    expected = Counter({"zero":1, "rank1":8, "invertible_det1":6, "invertible_det2":12})
    assert census == expected


    all_vecs = [np.array(v, dtype=int) for v in product(range(3), repeat=3)]
    for A in qmod.values():
        assert all(
            quadratic_type(v) == quadratic_type((A @ v) % MOD)
            for v in all_vecs
        )

    out = {
        "schema": "w33.20260924.bell_shell_quadratic_history_intertwiner.v1",
        "status": "PASS_BELL_SHELL_QUADRATIC_HISTORY_INTERTWINER",
        "bell_line_parabolic": {
            "order": len(stab),
            "structure": "3^3:S4",
            "translation_kernel_order": len(O3),
            "translation_kernel": "F3^3",
            "shell_size": len(shell),
            "repo_parents": [
                "analysis/bt858_heisenberg_shell_torsors.py",
                "analysis/bt860_bell_shell_register_arithmetic.py",
                "analysis/w33_pass196_kernel_flat_shell.py",
            ],
        },
        "quadratic_action_space": {
            "space": "Sym_2(F3)",
            "dimension_over_F3": 3,
            "size": 27,
            "quotient_group": "PGL(2,3)=S4",
            "action": "S -> G S G^T",
            "orbit_types": dict(census),
        },

        "intertwiner": {
            "Q_torsor_to_sym2": Q.astype(int).tolist(),
            "Q_inverse": Qi.astype(int).tolist(),
            "conjugacy": "Q * S4_Bell * Q^-1 = PGL2(3) on Sym_2(F3)",
            "exact": True,
        },
        "histories": history,
        "checks": {
            "PSp43_order": len(group),
            "Bell_stabilizer_order": len(stab),
            "translation_kernel_order": len(O3),
            "Bell_shell_size": len(shell),
            "Bell_S4_image_order": len(wmod),
            "PGL2_sym2_image_order": len(qmod),
            "orbit_census_1_8_6_12": [
                census["zero"],
                census["rank1"],
                census["invertible_det1"],
                census["invertible_det2"],
            ],
        },
        "interpretation": (
            "After choosing one Bell-shell context as affine origin, the actual "
            "S4 quotient module of the 27 skew contexts is GL(3,3)-conjugate to "
            "the congruence action on Sym_2(F3). Each context therefore has an "
            "equivariant symmetric quadratic generating-function label."
        ),
        "boundary": (
            "Exact finite-geometry/module theorem. Physical temporal histories "
            "still require a process-tensor implementation and an orientation rule."
        ),
    }

    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "intertwiner": out["intertwiner"]["Q_torsor_to_sym2"],
        "orbit_census": dict(census),
    }, indent=2))


if __name__ == "__main__":
    main()
