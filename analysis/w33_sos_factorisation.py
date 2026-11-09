"""Item 3 (explanation): the degree-4 certificate operator H on Sym^2(C^9) has spectrum {1/9 (36), 16/9 (9)} for pentads and
{4/9 (36), 16/9 (9)} for size-8 sets.  Sym^2(C^3 (x) C^3) = Sym^2 (x) Sym^2 (36) + Lambda^2 (x) Lambda^2 (9) for a tensor factorisation.
For each of the 45 splits {b, b-perp}, S_b = (1/3) sum_{u in <b>} W_u (x) W_u^dag swaps the first tensor factors between the copies; the
split's Lambda^2 (x) Lambda^2 is the -1 eigenspace of S_b inside Sym^2.  Test: is the 9-dim (16/9) eigenspace of H equal to the
Lambda^2 (x) Lambda^2 of some split, and which (how many) splits?  For size-8 sets: is it their own split?  For pentads: which splits?
usage: py -3 analysis/w33_sos_factorisation.py"""
import itertools, json, os
from collections import Counter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
import contextlib, io
ns = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pentad_umub.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(HERE, "w33_pentad_umub.py"), encoding="utf-8").read().split("# --- (3)")[0], ns)
P, lines, maxsets, disj, pauli, bases = ns["P"], ns["lines"], ns["maxsets"], ns["disj"], ns["pauli"], ns["bases"]
sb = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pass12635_burkhardt_fan.py")}
exec(open(os.path.join(HERE, "w33_pass12635_burkhardt_fan.py"), encoding="utf-8").read().split("res = dict(")[0], sb)
splits, Pb = sb["splits"], sb["P"]
assert Pb == P
d = 9
S = []
for i in range(d):
    for j in range(i, d):
        v = np.zeros(d * d, complex)
        if i == j: v[i * d + i] = 1
        else: v[i * d + j] = v[j * d + i] = 1 / np.sqrt(2)
        S.append(v)
S = np.array(S).T
def H_of(Ls):
    M = np.zeros((81, 81), complex)
    for L in Ls:
        for e in bases[L].T:
            A = np.outer(e, e.conj()) - np.eye(d) / d
            M += np.kron(A, A)
    H = S.conj().T @ M @ S
    return (H + H.conj().T) / 2
def top_space(H, k=9):
    w, V = np.linalg.eigh(H)
    return V[:, -k:]
def split_space(b):
    vecs = set()
    pts = [P[i] for i in b]
    for a in range(3):
        for c in range(3):
            vecs.add(tuple((a * pts[0][k] + c * next(p for p in pts if not all((p[t] - x * pts[0][t]) % 3 == 0 for t in range(4) for x in [0]) or True)[k]) % 3 for k in range(4)))
    # span of the 2-dim isotropy-free plane b: all F3 combinations of two independent points
    u = pts[0]; v = next(p for p in pts[1:] if not any(all((p[t] - x * u[t]) % 3 == 0 for t in range(4)) for x in range(3)))
    span = {tuple((a * u[k] + c * v[k]) % 3 for k in range(4)) for a in range(3) for c in range(3)}
    Sb = sum(np.kron(pauli(x), pauli(x).conj().T) for x in span) / 3
    Hs = S.conj().T @ Sb @ S
    w, V = np.linalg.eigh((Hs + Hs.conj().T) / 2)
    return V[:, np.abs(w + 1) < 1e-6]
split_spaces = [split_space(b) for b, bp in splits]
def match(V):
    hits = []
    for s, U in enumerate(split_spaces):
        if U.shape[1] != V.shape[1]:
            continue
        # equal subspaces iff the projectors agree
        if np.allclose(V @ V.conj().T, U @ U.conj().T, atol=1e-8):
            hits.append(s)
    return hits
res = {}
dims = Counter(U.shape[1] for U in split_spaces)
print("dimension of Lambda^2 (x) Lambda^2 per split (expect 9):", dict(dims))
pent = sorted(maxsets[0])
Hp = H_of(pent)
res["pentad_top_space_matches_splits"] = match(top_space(Hp))
eights = []
def bk(R, Pc, X):
    if len(eights) >= 2: return
    if not Pc and not X:
        if len(R) == 8: eights.append(sorted(R))
        return
    for v in list(Pc):
        bk(R | {v}, {u for u in Pc if disj[v][u]}, {u for u in X if disj[v][u]}); Pc = Pc - {v}; X = X | {v}
bk(set(), set(range(40)), set())
for k, E8 in enumerate(eights):
    hits = match(top_space(H_of(E8)))
    own = [s for s, (b, bp) in enumerate(splits) if all(not (lines[L] & (b | bp)) for L in E8)]
    res[f"size8_{k}"] = dict(top_space_matches=hits, own_split=own)
print(res)
json.dump(res, open(os.path.join(ROOT, "data", "w33_sos_factorisation.json"), "w"), indent=1)
