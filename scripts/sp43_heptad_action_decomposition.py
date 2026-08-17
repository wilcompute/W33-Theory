"""Pass6001-6012: Sp(4,3) heptad action — full group-level decomposition.

# PRODUCER: Sp(4,3) built from 8 transvections (vectorized BFS, |G|=51840);
# orbit, stabilizer, permutation character, and stabilizer-orbit count all
# computed from the built group. Runtime ~25s total.

FIREWALL: finite group theory over F_3 only.
"""
import numpy as np
from itertools import product
from collections import deque, Counter
import time

F3 = [0, 1, 2]
def m3(x): return x % 3
def sp3(u, v): return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2]) % 3

def canon_proj(v):
    for s in (1, 2):
        w = tuple(m3(s*x) for x in v)
        if any(w):
            for x in w:
                if x != 0: return w if x == 1 else None
proj_pts = sorted({c for v in product(F3, repeat=4) if any(v)
                   for c in [canon_proj(v)] if c is not None})
assert len(proj_pts) == 40
pidx = {p: i for i, p in enumerate(proj_pts)}

coll = {i: set() for i in range(40)}
for i in range(40):
    for j in range(40):
        if i != j and sp3(proj_pts[i], proj_pts[j]) == 0:
            coll[i].add(j)
noncoll = {i: set(range(40)) - {i} - coll[i] for i in range(40)}

# seed heptad + swap-BFS closure
def find_heptad():
    import random
    random.seed(1)
    order = sorted(range(40), key=lambda x: random.random())
    for start in order:
        stack = [([start], sorted(noncoll[start]))]
        while stack:
            cur, cand = stack.pop()
            if len(cur) == 7: return frozenset(cur)
            if len(cur)+len(cand) < 7: continue
            v = cand[0]
            stack.append((cur, cand[1:]))
            stack.append((cur+[v], [x for x in cand if x in noncoll[v]]))
H0 = find_heptad()
def neighbors(H):
    out = []
    for p in H:
        rest = H - {p}
        cand = set(range(40)) - H
        for r in rest: cand &= noncoll[r]
        for q in cand: out.append(frozenset(rest | {q}))
    return out
seen = {H0}; qq = deque([H0])
while qq:
    H = qq.popleft()
    for H2 in neighbors(H):
        if H2 not in seen: seen.add(H2); qq.append(H2)
heptads = list(seen)
assert len(heptads) == 2880

# Sp(4,3) build
def transvection_matrix(a):
    a = np.array(a, dtype=np.int64)
    T = np.eye(4, dtype=np.int64)
    for j in range(4):
        e = np.zeros(4, dtype=np.int64); e[j] = 1
        T[:, j] = (e + sp3(tuple(e), tuple(a))*a) % 3
    return T
J3 = np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]], dtype=np.int64) % 3
e = [tuple(1 if i == k else 0 for i in range(4)) for k in range(4)]
dirs = [e[0], e[1], e[2], e[3],
        tuple((np.array(e[0])+np.array(e[3])) % 3), tuple((np.array(e[1])+np.array(e[2])) % 3),
        tuple((np.array(e[0])+np.array(e[2])) % 3), tuple((np.array(e[1])+np.array(e[3])) % 3)]
gens = [transvection_matrix(d) for d in dirs]
for T in gens:
    assert np.array_equal((T.T @ J3 @ T) % 3, J3)
def mat_key(M): return tuple(M.flatten().tolist())
I4 = np.eye(4, dtype=np.int64)
group = {mat_key(I4): I4}
frontier = [I4]
gen_stack = np.stack(gens)
while frontier:
    F = np.stack(frontier)
    prods = np.einsum('nij,gjk->ngik', F, gen_stack) % 3
    new_frontier = []
    for M in prods.reshape(-1, 4, 4):
        k = mat_key(M)
        if k not in group: group[k] = M; new_frontier.append(M)
    frontier = new_frontier
assert len(group) == 51840                                   # PRODUCER

# permutations of the 40 points
P = np.array(proj_pts, dtype=np.int64)
def canon_arr(W):
    out = []
    for w in W:
        cw = None
        for s in (1, 2):
            ww = tuple((s*w) % 3)
            for x in ww:
                if x != 0:
                    cw = ww if x == 1 else None
                    break
            if cw is not None: break
        out.append(pidx[cw])
    return out
group_list = list(group.values())
perms = [tuple(canon_arr((P @ M.T) % 3)) for M in group_list]

# orbit + stabilizer
H0s = sorted(H0)
orbit = set(frozenset(perm[i] for i in H0s) for perm in perms)
assert orbit == set(heptads)                                 # PRODUCER: transitivity
stab_idx = [k for k, perm in enumerate(perms) if frozenset(perm[i] for i in H0s) == H0]
stab = [group_list[k] for k in stab_idx]
stab_perms = [perms[k] for k in stab_idx]
assert len(stab) == 18                                       # PRODUCER

def mat_order(M):
    M = np.array(M); cur = np.eye(4, dtype=np.int64); o = 0
    while True:
        cur = (cur @ M) % 3; o += 1
        if np.array_equal(cur, np.eye(4, dtype=np.int64)): return o
        if o > 100: return -1
assert Counter(mat_order(M) for M in stab) == Counter({1:1, 2:1, 3:8, 6:8})  # C3 x C6
assert all(np.array_equal((A @ B) % 3, (B @ A) % 3) for A in stab for B in stab)  # abelian

# permutation character
H_mat = np.zeros((2880, 40), dtype=np.int8)
for i, H in enumerate(heptads):
    for p in H: H_mat[i, p] = 1
chi = np.zeros(51840, dtype=np.int64)
for k, perm in enumerate(perms):
    parr = np.array(perm)
    chi[k] = (H_mat[:, parr] == H_mat).all(axis=1).sum()
assert chi[0] == 2880
assert chi.sum() == 51840                                    # <chi,1> = 1
assert int((chi.astype(np.int64)**2).sum()) == 392*51840     # <chi,chi> = 392
assert Counter(int(c) for c in chi) == Counter({0:50238, 12:960, 24:480, 144:160, 2880:2})

# direct stabilizer-orbit count on heptads
hep_idx = {h: i for i, h in enumerate(heptads)}
assigned = np.zeros(2880, dtype=bool)
n_orbits = 0
sizes = []
for i in range(2880):
    if assigned[i]: continue
    orb = set()
    for sp in stab_perms:
        orb.add(hep_idx[frozenset(sp[p] for p in heptads[i])])
    for j in orb: assigned[j] = True
    n_orbits += 1; sizes.append(len(orb))
assert n_orbits == 392                                       # PRODUCER
assert Counter(sizes) == Counter({1: 12, 3: 92, 9: 288})

# 40-point character anchor
chi40 = np.array([sum(1 for p in range(40) if perm[p] == p) for perm in perms])
assert chi40.sum() == 51840                                  # <chi40,1> = 1
assert int((chi40.astype(np.int64)**2).sum()) == 3*51840     # rank 3
A40 = np.zeros((40, 40), dtype=np.int8)
for i in range(40):
    for j in coll[i]: A40[i, j] = 1
spec40 = Counter(round(float(x), 4) for x in np.linalg.eigvalsh(A40.astype(float)))
assert spec40[12.0] == 1 and spec40[2.0] == 24 and spec40[-4.0] == 15

if __name__ == '__main__':
    print('Pass6001-6012: all assertions PASS')
    print('|Sp(4,3)| = 51840; heptad orbit = 2880 = swap closure')
    print('Stab = C3 x C6 (abelian, spectrum verified); point image (Z/3)^2')
    print('perm character values {2880:2, 144:160, 24:480, 12:960, 0:50238}')
    print('rank = 392 = 12x1 + 92x3 + 288x9 stabilizer orbits (direct count)')
    print('40-point rep = 1 + 15 + 24 (rank 3, spectrum-anchored)')
