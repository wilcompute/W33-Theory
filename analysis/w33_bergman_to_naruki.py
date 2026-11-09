"""Item 1 of Pass 12634's next steps: the Naruki fan's rays are the images of the 750 rays of the E6 Bergman fan Berg(E6) under a
40x36 matrix (Ren-Shaw-Sturmfels, arXiv:1402.5651, citing Hacking-Keel-Tevelev Thm 6.1).  Rays of Berg(E6) = proper connected flats
F of the E6 root arrangement = irreducible closed root subsystems (A1 36, A2 120, A3 270, A4 216, D4 45, A5 36, D5 27 = 750), with
ray e_F = indicator of the positive roots in F (mod R.1).
Hypothesis: the matrix is the root / A2^3 incidence M[T, r] = 1 iff r in T (each row has 9 ones).  Test: the images M e_F, taken
modulo R.1 and positive scaling, must be exactly 76 distinct nonzero rays, 36 of type (a) and 40 of type (b) as reconstructed in
Pass 12634.  Control: a random 0/1 matrix with 9 ones per row must not give 76.
usage: py -3 analysis/w33_bergman_to_naruki.py"""
import itertools
import json
import os
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_pass12634_naruki_fan.py"), encoding="utf-8").read().split("# --- Check 1")[0]
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pass12634_naruki_fan.py")}
exec(src, g)
POS, IP, T3, roots_of = g["POS"], g["IP"], g["T3"], g["roots_of"]
N = 36

# flats: subsets F of positive roots with F = (positive roots in span F); connected = the inner-product graph on F is connected
def closure(S):
    M = POS[sorted(S)].astype(float)
    P = M.T @ np.linalg.pinv(M.T)
    return frozenset(i for i in range(N) if np.allclose(P @ POS[i], POS[i], atol=1e-9))

flats = {1: {frozenset((i,)) for i in range(N)}}
for r in range(2, 6):
    flats[r] = {closure(F | {i}) for F in flats[r - 1] for i in range(N) if i not in F}
    flats[r] = {F for F in flats[r] if np.linalg.matrix_rank(POS[sorted(F)].astype(float)) == r}

def connected(F):
    F = sorted(F)
    seen, todo = {F[0]}, [F[0]]
    while todo:
        x = todo.pop()
        for y in F:
            if y not in seen and IP[x, y] != 0:
                seen.add(y); todo.append(y)
    return len(seen) == len(F)

conn = [F for r in flats for F in flats[r] if connected(F)]
size_type = Counter(len(F) for F in conn)  # A1:1 A2:3 A3:6 A4:10 D4:12 A5:15 D5:20
print("connected proper flats:", len(conn), dict(sorted(size_type.items())))

def rays_from(M):
    out = set()
    for F in conn:
        e = np.zeros(N); e[sorted(F)] = 1
        v = M @ e
        v = v - v.min()
        if not v.any():
            continue
        v = v / np.gcd.reduce(v.astype(int))
        out.add(tuple(int(x) for x in v))
    return out

M = np.zeros((40, N), dtype=int)
for t in range(40):
    M[t, sorted(roots_of[t])] = 1
R = rays_from(M)
# type (b) ray of T in R^40 mod 1: what does the image of an A2 flat look like?
img_type = defaultdict(set)
for F in conn:
    e = np.zeros(N); e[sorted(F)] = 1
    v = M @ e; v = v - v.min()
    if v.any():
        v = v / np.gcd.reduce(v.astype(int))
    img_type[len(F)].add(tuple(int(x) for x in v))
rng = np.random.default_rng(3)
Mr = np.zeros((40, N), dtype=int)
for t in range(40):
    Mr[t, rng.choice(N, 9, replace=False)] = 1
Rc = rays_from(Mr)
res = dict(n_connected_flats=len(conn), flat_sizes=dict(size_type), n_image_rays_incidence=len(R), n_image_rays_random_control=len(Rc),
           distinct_images_by_flat_size={k: len(v) for k, v in img_type.items()})
print("image rays under incidence matrix:", len(R), "| random control:", len(Rc))
print("distinct images by flat size (1=A1,3=A2,6=A3,10=A4,12=D4,15=A5,20=D5):", res["distinct_images_by_flat_size"])
json.dump(res, open(os.path.join(ROOT, "data", "w33_bergman_to_naruki.json"), "w"), indent=1)

# --- Does every image lie in a cone of the reconstructed Naruki fan (mod R.1)? ------------------------------------------------
from scipy.optimize import nnls
A_ray = {}
for i in range(N):
    e = np.zeros(N); e[i] = 1; A_ray[("a", i)] = M @ e
for t in range(40):
    A2f = sorted(T3[t], key=min)[0]
    e = np.zeros(N); e[sorted(A2f)] = 1; A_ray[("b", t)] = M @ e
orth_sets4 = []
def ext(S, start):
    if len(S) == 4:
        orth_sets4.append(tuple(S)); return
    for k in range(start, N):
        if all(IP[k, x] == 0 for x in S):
            ext(S + [k], k + 1)
ext([], 0)
cones = [[("a", i) for i in S] for S in orth_sets4]
for t in range(40):
    for pick in itertools.product(*[sorted(x) for x in sorted(T3[t], key=min)]):
        cones.append([("b", t)] + [("a", p) for p in pick])
assert len(cones) == 1215
one = np.ones(40)
def in_fan(v):
    best = None
    for C in cones:
        B = np.column_stack([A_ray[c] for c in C] + [one, -one])
        lam, r = nnls(B, v)
        if r < 1e-8:
            used = tuple(sorted(c for c, l in zip(C, lam[:len(C)]) if l > 1e-9))
            return used
    return None
where = Counter()
fails = 0
for F in conn:
    e = np.zeros(N); e[sorted(F)] = 1
    u = in_fan(M @ e)
    if u is None:
        fails += 1; continue
    where[(len(F), "".join(sorted(x[0] for x in u)))] += 1
res["images_outside_fan"] = fails
res["image_support_by_flat_size"] = {f"{k[0]}:{k[1] or 'zero'}": v for k, v in sorted(where.items())}
print("images outside the reconstructed fan:", fails)
print("support type of each image (flat size: rays used):", res["image_support_by_flat_size"])
json.dump(res, open(os.path.join(ROOT, "data", "w33_bergman_to_naruki.json"), "w"), indent=1)
