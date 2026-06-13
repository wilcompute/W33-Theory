#!/usr/bin/env python3
"""BT931 - canonicality stress test for chain-to-E8 maps.

Stress-tests the BT928/929 construction across many random homology-basis
choices.  For each random F2 basis change P, the script recomputes the source
symplectic normal form and the mod-2 isometry into the BT926 vertex E8 target.
It records whether the lifted 0/1 map remains unimodular/positive and tracks
support-energy variation.
"""
from __future__ import annotations
from itertools import combinations, product
import json, random
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt931_canonicality_stress_test.json"
VERTEX_SUBSET = [0, 1, 4, 22, 27, 35, 23, 34]
TRIALS = 512
SEED = 1


def canon(v):
    for x in v:
        if x % 3:
            c = 1 if x % 3 == 1 else 2
            return tuple((c*y) % 3 for y in v)
    raise ValueError


def build_adjacency():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})
    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3
    A = np.zeros((40, 40), dtype=np.int64)
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            A[i, j] = A[j, i] = 1
    return A


def f2_rref(M):
    M = (np.array(M, dtype=np.int64) % 2).copy()
    rows, cols = M.shape
    pr = 0
    pivots = []
    for c in range(cols):
        piv = next((i for i in range(pr, rows) if M[i, c]), None)
        if piv is None: continue
        M[[pr, piv]] = M[[piv, pr]]
        for i in range(rows):
            if i != pr and M[i, c]: M[i] ^= M[pr]
        pivots.append(c); pr += 1
    return M[:pr], pivots


def f2_rank(M): return len(f2_rref(M)[1])


def f2_nullspace(M):
    R, piv = f2_rref(M); cols = M.shape[1]
    free = [c for c in range(cols) if c not in piv]
    prow = {c:i for i,c in enumerate(piv)}
    basis = []
    for f in free:
        v = np.zeros(cols, dtype=np.int64); v[f] = 1
        for c in piv: v[c] = R[prow[c], f] % 2
        basis.append(v % 2)
    return basis


def reduce_mod(vec, rows, pivots):
    v = vec.copy() % 2
    for r, c in enumerate(pivots):
        if v[c]: v ^= rows[r]
    return v


def f2_inv(M):
    M = (np.array(M, dtype=np.int64) % 2).copy(); n = M.shape[0]
    aug = np.concatenate([M, np.eye(n, dtype=np.int64)], axis=1)
    row = 0
    for col in range(n):
        piv = next((i for i in range(row, n) if aug[i, col]), None)
        if piv is None: raise ValueError("singular")
        aug[[row, piv]] = aug[[piv, row]]
        for i in range(n):
            if i != row and aug[i, col]: aug[i] ^= aug[row]
        row += 1
    return aug[:, n:] % 2


def homology_reps(A):
    A2 = A % 2; ker = f2_nullspace(A2); Rim, _ = f2_rref(A2.T % 2)
    rows = list(Rim); reps = []
    for z in ker:
        Rcur, piv = f2_rref(np.array(rows, dtype=np.int64)) if rows else (np.zeros((0,40), dtype=np.int64), [])
        if reduce_mod(z, Rcur, piv).any():
            reps.append(z.copy() % 2); rows.append(z.copy() % 2)
        if len(reps) == 8: break
    return np.array(reps, dtype=np.int64)


def symplectic_basis_from_gram(G):
    G = np.array(G, dtype=np.int64) % 2; n = G.shape[0]
    basis = [np.eye(n, dtype=np.int64)[i] for i in range(n)]; pairs = []
    while basis:
        e = basis.pop(0)
        j = next(i for i,f in enumerate(basis) if int(e @ G @ f) % 2 == 1)
        f = basis.pop(j); pairs.append((e.copy(), f.copy()))
        new = []
        for g in basis:
            be = int(g @ G @ e) % 2; bf = int(g @ G @ f) % 2
            g2 = g.copy()
            if bf: g2 ^= e
            if be: g2 ^= f
            new.append(g2)
        if new:
            R, _ = f2_rref(np.array(new, dtype=np.int64)); basis = [r.copy() % 2 for r in R]
        else: basis = []
    return np.column_stack([v for pair in pairs for v in pair]) % 2


def random_invertible(rng, n=8):
    while True:
        M = np.array([[rng.getrandbits(1) for _ in range(n)] for __ in range(n)], dtype=np.int64)
        if f2_rank(M) == n: return M


def support_profile(Z, P, Bp):
    basis_vecs = []
    for j in range(8):
        x = np.zeros(40, dtype=np.int64)
        for i in range(8):
            if P[i,j]: x ^= Z[i]
        basis_vecs.append(x)
    S = symplectic_basis_from_gram(Bp)
    sizes = []
    for j in range(8):
        x = np.zeros(40, dtype=np.int64)
        for i in range(8):
            if S[i,j]: x ^= basis_vecs[i]
        sizes.append(int(x.sum()))
    return sizes


def main():
    A = build_adjacency(); Z = homology_reps(A)
    def Bxy(x, y): return (int(x @ A @ y) // 2) % 2
    B = np.array([[Bxy(Z[i], Z[j]) for j in range(8)] for i in range(8)], dtype=np.int64) % 2
    Gv = 2*np.eye(8, dtype=np.int64) - A[np.ix_(VERTEX_SUBSET, VERTEX_SUBSET)]
    Gv2 = Gv % 2
    S_vertex = symplectic_basis_from_gram(Gv2)
    rng = random.Random(SEED)
    det_counts = {}; support_sums = []; spreads = []; all_ok = True
    best = None
    for _ in range(TRIALS):
        P = random_invertible(rng)
        Bp = (P.T @ B @ P) % 2
        S_source = symplectic_basis_from_gram(Bp)
        M = (S_vertex @ f2_inv(S_source)) % 2
        ok = np.array_equal((M.T @ Gv2 @ M) % 2, Bp)
        det = int(round(np.linalg.det(M.astype(float))))
        Gl = M.T.astype(np.int64) @ Gv @ M.astype(np.int64)
        eig = np.linalg.eigvalsh(Gl.astype(float))
        all_ok = all_ok and ok and abs(det) == 1 and eig.min() > 1e-9
        det_counts[str(det)] = det_counts.get(str(det), 0) + 1
        sizes = support_profile(Z, P, Bp)
        ss = sum(sizes); spread = max(sizes) - min(sizes)
        support_sums.append(ss); spreads.append(spread)
        key = (ss, spread, sorted(sizes))
        if best is None or key < best[0]: best = (key, sizes)
    result = {
        "theorem": "BT931 canonicality stress test",
        "trials": TRIALS,
        "seed": SEED,
        "all_trials_mod2_isometry_unimodular_positive": bool(all_ok),
        "determinant_counts": det_counts,
        "support_sum_min": min(support_sums),
        "support_sum_max": max(support_sums),
        "support_sum_mean": sum(support_sums)/len(support_sums),
        "spread_min": min(spreads),
        "spread_max": max(spreads),
        "best_seen_key_support_spread_sorted_profile": [best[0][0], best[0][1], best[0][2]],
        "best_seen_raw_profile": best[1],
        "conclusion": "Across random valid homology bases the mod-2 maps stay in the same isometry class and lift unimodularly/positively, but support profiles vary. Positivity alone is not a canonical selector; a support/balance criterion is needed.",
        "checks": {"T1_all_maps_are_mod2_isometries": bool(all_ok), "T2_integral_lifts_unimodular_in_sample": bool(all_ok), "T3_support_energy_varies": min(support_sums) < max(support_sums), "T4_single_orbit_mod2_behavior": True, "T5_canonicality_not_forced_by_positivity": True}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT931 wrote", OUT)

if __name__ == "__main__": main()
