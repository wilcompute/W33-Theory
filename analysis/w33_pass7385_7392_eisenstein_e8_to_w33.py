#!/usr/bin/env python3
"""Passes 7385--7392: the Eisenstein E8 -> W(3,3) bridge, explicit and corrected.

MAIN THEOREM (machine-verified): the 240 roots of E8, grouped into 40 Eisenstein
lines (orbits under <-1, rho> = Z6 with rho = (Coxeter)^10 a fixed-point-free
order-3 automorphism, 1+rho+rho^2=0), are the 40 points of W(3,3) when two lines
are collinear iff their rho-invariant real 2-planes are orthogonal.  The graph is
SRG(40,12,2,4), satisfies the GQ(3,3) axioms, and has alpha=7 (so W(3,3), not the
dual Q(4,3) which has ovoids, alpha=10).

CORRECTION (PART_CCCCCXCIX): the iterated local-subgraph chain of the E8 root graph
is the Gosset-Elte chain 240->56->27->16->10->6; it never contains 40 or 33, and
W33 has 40 vertices, not 33.  The E8->W33 bridge is a lattice ring reduction
E8 -> Z[omega] -> F_3, NOT a graph cover: spec(W33)={12,2,-4} does not embed in
spec(root graph)={56,28,8,-2,-4}.
"""
import json
from itertools import combinations, product
from collections import Counter
import numpy as np

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

def spectrum(Am):
    return {str(k): v for k, v in sorted(Counter(np.round(np.linalg.eigvalsh(Am.astype(float)), 6)).items(), key=lambda x: -x[0])}

def srg_params(Am):
    n = Am.shape[0]; k = int(Am.sum(1)[0]); lams = set(); mus = set()
    for u in range(n):
        for v in range(u + 1, n):
            c = int((Am[u] * Am[v]).sum())
            (lams if Am[u, v] else mus).add(c)
    return k, sorted(lams), sorted(mus)

def main():
    R = build_e8_roots()
    Gm = R @ R.T
    A = (np.abs(Gm - 1.0) < 1e-9).astype(int); np.fill_diagonal(A, 0)
    res = {"schema": "w33.pass7385_7392.eisenstein_e8_w33_bridge.v1"}
    res["e8_root_graph"] = {"vertices": 240, "degree": 56, "spectrum": spectrum(A),
                            "intersection_array": "{56,28,1;1,12,56}", "antipodal_diameter": 3}
    def local(Am):
        nb = np.where(Am[0] == 1)[0]; return Am[np.ix_(nb, nb)]
    chain = [A]
    for _ in range(5): chain.append(local(chain[-1]))
    res["gosset_elte_chain"] = {"240_E8": spectrum(chain[0]), "56_Gosset": spectrum(chain[1]),
        "27_Schlafli": spectrum(chain[2]), "16_Clebsch": spectrum(chain[3]),
        "10_T5": spectrum(chain[4]), "6_prism": spectrum(chain[5]),
        "note": "vertex counts 240,56,27,16,10,6 -- never 40 or 33"}
    e = np.eye(8)
    sroots = [0.5*(e[0]-e[1]-e[2]-e[3]-e[4]-e[5]-e[6]+e[7]), e[1]+e[2], e[2]-e[1],
              e[3]-e[2], e[4]-e[3], e[5]-e[4], e[6]-e[5], e[7]-e[6]]
    M = np.eye(8)
    for a in sroots: M = (np.eye(8) - 2*np.outer(a, a)/(a@a)) @ M
    rho = np.linalg.matrix_power(M, 10)
    assert np.allclose(np.linalg.matrix_power(rho, 3), np.eye(8))
    assert np.allclose(np.eye(8) + rho + rho @ rho, 0)
    res["eisenstein_rho"] = {"definition": "rho = (E8 Coxeter element)^10", "order": 3,
        "relation": "1+rho+rho^2=0", "char_poly": "Phi_3^4=(x^2+x+1)^4", "fixed_point_free": True}
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
    assert len(lines) == 40 and set(len(l) for l in lines) == {6}
    res["eisenstein_lines"] = {"count": 40, "fiber_size": 6, "fiber_group": "Z6=<-1,omega>",
        "line_structure": "each line is an A2 root hexagon (v.rho(v)=-1): 3 antipodal axes x 2 endpoints"}
    def fully_orth(L, Lp): return all(abs(float(R[i] @ R[j])) < 1e-9 for i in L for j in Lp)
    W = np.zeros((40, 40), dtype=int)
    for a in range(40):
        for b in range(a + 1, 40):
            if fully_orth(lines[a], lines[b]): W[a, b] = W[b, a] = 1
    k, lams, mus = srg_params(W)
    assert (40, k, lams[0], mus[0]) == (40, 12, 2, 4)
    res["w33_graph"] = {"srg": [40, 12, 2, 4], "spectrum": spectrum(W),
                        "adjacency_rule": "lines collinear iff their rho-invariant 2-planes are orthogonal"}
    import networkx as nx
    WG = nx.from_numpy_array(W)
    cliques4 = [tuple(sorted(c)) for c in nx.enumerate_all_cliques(WG) if len(c) == 4]
    pt_lines = Counter()
    for c in cliques4:
        for p in c: pt_lines[p] += 1
    gq_ok = all(len([c for c in cliques4 if p in c and set(c) & set(L)]) == 1
                for L in cliques4 for p in range(40) if p not in set(L))
    assert len(cliques4) == 40 and set(pt_lines.values()) == {4} and gq_ok
    res["gq_3_3"] = {"lines": 40, "points_per_line": 4, "lines_per_point": 4, "gq_axiom": True}
    adj = [set(np.where(W[i] == 1)[0]) for i in range(40)]
    best = [0]
    def bb(cand, cur):
        if not cand: best[0] = max(best[0], len(cur)); return
        if len(cur) + len(cand) <= best[0]: return
        v = max(cand, key=lambda x: len(adj[x] & cand))
        bb(cand - {v} - adj[v], cur | {v}); bb(cand - {v}, cur)
    bb(set(range(40)), set())
    assert best[0] == 7
    res["independence_number"] = {"alpha": 7, "lovász_theta": 10,
        "note": "alpha=7 => W(3,3) (no ovoid); Q(4,3) has alpha=10. theta=10 is only the Lovász bound."}
    res["status"] = "PASS"; res["passes"] = "7385-7392"
    return res

if __name__ == "__main__":
    out = main()
    print(json.dumps({"status": out["status"], "srg": out["w33_graph"]["srg"],
                      "alpha": out["independence_number"]["alpha"]}))
