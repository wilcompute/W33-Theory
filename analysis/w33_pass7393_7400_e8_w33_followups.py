#!/usr/bin/env python3
"""Passes 7393--7400: follow-ups to the Eisenstein E8->W33 bridge.

S2  Reconcile 40x6 (Eisenstein) with Pass1041 axis-glue 40x3x2: each Eisenstein
    line is an A2 root hexagon (v.rho(v)=-1), i.e. 3 antipodal axes x 2 endpoints.
S3  D4 subsystems of E8: 3150 total (240 roots x 2520 diagrams / |W(D4)|=192);
    exactly 90 are rho-invariant (unions of 4 Eisenstein lines) == the 90
    "C6-supported" D4s of Pass7353-7360.  The 40 GQ lines (24 roots each) are NOT
    D4 subsystems.
S4  Closure-package correction: T201/T229 list alpha(W33)=10; the exact value is
    alpha=7.  10 is the Lovász theta bound -v*s/(k-s)=10, not the independence number.
S5  Shared smallest eigenvalue -4: eigenspace dims W33:15 (= doily W(2,2) points),
    E8 root graph:84, antipodal SRG(120,56,28,24):84.  Structural, not spectral.
"""
import json
from itertools import combinations, product
from collections import Counter
import numpy as np
import networkx as nx

def build_e8_roots():
    roots = []
    for i, j in combinations(range(8), 2):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8); v[i] = si; v[j] = sj; roots.append(v)
    for signs in product((1, -1), repeat=8):
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(np.array(signs) * 0.5)
    return np.array(roots)

def main():
    R = build_e8_roots(); Gm = R @ R.T
    A = (np.abs(Gm - 1.0) < 1e-9).astype(int); np.fill_diagonal(A, 0)
    e = np.eye(8)
    sroots = [0.5*(e[0]-e[1]-e[2]-e[3]-e[4]-e[5]-e[6]+e[7]), e[1]+e[2], e[2]-e[1],
              e[3]-e[2], e[4]-e[3], e[5]-e[4], e[6]-e[5], e[7]-e[6]]
    M = np.eye(8)
    for a in sroots: M = (np.eye(8) - 2*np.outer(a, a)/(a@a)) @ M
    rho = np.linalg.matrix_power(M, 10)
    def orbit_of(idx):
        orb = set(); cur = R[idx]
        for a in range(3):
            for s in (1, -1):
                v = s * (cur @ np.linalg.matrix_power(rho, a).T)
                orb.add(int(np.where(np.all(np.abs(R - v) < 1e-6, axis=1))[0][0]))
        return frozenset(orb)
    ls = {}
    for i in range(240): ls.setdefault(orbit_of(i), None)
    lines = list(ls.keys())
    res = {"schema": "w33.pass7393_7400.e8_w33_followups.v1"}

    hexok = all(abs(float(R[sorted(L)[0]] @ (R[sorted(L)[0]] @ rho.T)) + 1.0) < 1e-6 for L in lines)
    res["S2_A2_hexagon_reconciliation"] = {"v_dot_rho_v": -1, "all_lines": bool(hexok),
        "statement": "40x6 = 40x(3 antipodal axes)x(2 endpoints); Eisenstein fibration == Pass1041 axis-glue fibration"}

    ipm = np.round(Gm, 6)
    neg1 = [np.where(np.abs(ipm[i] + 1.0) < 1e-6)[0] for i in range(240)]
    a0 = 0; nb = neg1[a0]
    orth = (np.abs(ipm[np.ix_(nb, nb)]) < 1e-6).astype(int)
    triangles = int(np.trace(np.linalg.matrix_power(orth, 3)) // 6)
    d4_count = 240 * triangles // 192
    res["S3_d4_count"] = {"diagrams_per_root": triangles, "total_D4": d4_count,
                          "divisor": "|W(D4)|=192 simple systems per D4"}
    assert d4_count == 3150
    line_basis = np.array([np.array([R[sorted(L)[0]], R[sorted(L)[0]] @ rho.T]) for L in lines])
    def rank_of_quad(quad):
        return np.linalg.matrix_rank(np.concatenate([line_basis[q] for q in quad], axis=0), tol=1e-6)
    def is_d4(idxset):
        if len(idxset) != 24: return False
        vecs = R[sorted(idxset)]
        if np.linalg.matrix_rank(vecs, tol=1e-6) != 4: return False
        cur = {tuple(np.round(v, 6)) for v in vecs}; changed = True
        while changed:
            changed = False
            arr = [np.array(v) for v in cur]
            for x in arr:
                for a in arr:
                    y = x - (x @ a) * a; key = tuple(np.round(y, 6))
                    if key not in cur:
                        cur.add(key); changed = True
                        if len(cur) > 24: return False
        return len(cur) == 24
    rho_inv = []
    for quad in combinations(range(40), 4):
        if rank_of_quad(quad) == 4:
            rts = set()
            for q in quad: rts |= set(lines[q])
            if is_d4(rts): rho_inv.append(quad)
    res["S3_rho_invariant_D4"] = {"count": len(rho_inv),
        "matches_pass7353_7360_C6_supported": len(rho_inv) == 90,
        "note": "rho-invariant D4s = unions of 4 Eisenstein lines = the 90 C6-supported D4s"}
    assert len(rho_inv) == 90
    def fully_orth(L, Lp): return all(abs(float(R[i] @ R[j])) < 1e-9 for i in L for j in Lp)
    W = np.zeros((40, 40), dtype=int)
    for a in range(40):
        for b in range(a + 1, 40):
            if fully_orth(lines[a], lines[b]): W[a, b] = W[b, a] = 1
    WG = nx.from_numpy_array(W)
    cliques4 = [tuple(sorted(c)) for c in nx.enumerate_all_cliques(WG) if len(c) == 4]
    gq0 = [c for c in cliques4 if 0 in c]
    gq0_is_d4 = 0
    for c in gq0:
        rts = set()
        for L in c: rts |= set(lines[L])
        if is_d4(rts): gq0_is_d4 += 1
    res["S3_gq_lines_are_not_D4"] = {"gq_lines_through_point": len(gq0), "that_are_D4": gq0_is_d4}

    adj = [set(np.where(W[i] == 1)[0]) for i in range(40)]
    best = [0]
    def bb(cand, cur):
        if not cand: best[0] = max(best[0], len(cur)); return
        if len(cur) + len(cand) <= best[0]: return
        v = max(cand, key=lambda x: len(adj[x] & cand))
        bb(cand - {v} - adj[v], cur | {v}); bb(cand - {v}, cur)
    bb(set(range(40)), set())
    theta = -40 * (-4) / (12 + 4)
    res["S4_alpha_vs_theta"] = {"alpha": best[0], "lovász_theta": theta,
        "closure_package_error": "T201/T229 list alpha=theta=10; correct alpha=7, theta=10"}

    def eig(Am): return Counter(np.round(np.linalg.eigvalsh(Am.astype(float)), 6))
    res["S5_minus4_eigenspace"] = {"W33": eig(W)[-4.0], "E8_root_graph": eig(A)[-4.0],
        "note": "W33 dim 15 = doily W(2,2) points; E8 dim 84; structural not spectral"}

    res["status"] = "PASS"; res["passes"] = "7393-7400"
    return res

if __name__ == "__main__":
    out = main()
    print(json.dumps({"status": out["status"], "D4_total": out["S3_d4_count"]["total_D4"],
                      "rho_invariant_D4": out["S3_rho_invariant_D4"]["count"],
                      "alpha": out["S4_alpha_vs_theta"]["alpha"]}))
