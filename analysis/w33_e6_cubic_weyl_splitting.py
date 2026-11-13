"""Pass 12655: does the monomial symmetry group M = 2^6.W(E6) of the signed cubic (w33_e6_cubic_integral_structure.py) SPLIT, i.e.
does W(E6) lift to a subgroup of signed permutations preserving N?  Exact finite test: take six reflections (involutions with 15
fixed coordinates) forming an E6 Coxeter system; each has 2^6 sign lifts; a splitting exists iff lifts r_1..r_6 can be chosen with
r_i^2 = 1 and (r_i r_j)^{m_ij} = 1 (Coxeter presentation of W(E6)).  Exhaustive CSP over the 64^6 choices by pairwise filtering.
Control: the A2 parabolic alone (two adjacent reflections) -- reports its number of compatible lift pairs.
usage: py -3 analysis/w33_e6_cubic_weyl_splitting.py"""
import itertools, json, os
import numpy as np, networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_e6_cubic_integral_structure.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_e6_cubic_integral_structure.py")}
exec(src[: src.index("GM = nx.algorithms")], g)
G, triads, tidx, slog, solve, ker = g["G"], g["triads"], g["tidx"], g["slog"], g["solve"], g["ker"]
# reflections: automorphisms that are involutions with 15 fixed points
GM = nx.algorithms.isomorphism.GraphMatcher(G, G); refl = []
for iso in GM.isomorphisms_iter():
    pi = tuple(iso[i] for i in range(27))
    if all(pi[pi[i]] == i for i in range(27)) and sum(1 for i in range(27) if pi[i] == i) == 15: refl.append(pi)
    if len(refl) == 36: break
assert len(refl) == 36
comp = lambda p, q: tuple(p[q[i]] for i in range(27))  # p after q
def order(p):
    q = p; k = 1
    while q != tuple(range(27)): q = comp(p, q); k += 1
    return k
m = {(i, j): order(comp(refl[i], refl[j])) for i in range(36) for j in range(36) if i != j}
# find an E6 simple system: path 0-1-2-3-4 with node 5 attached to node 2; adjacent = order 3, non-adjacent = order 2
edges = {(0, 1), (1, 2), (2, 3), (3, 4), (2, 5)}
def want(a, b): return 3 if (a, b) in edges or (b, a) in edges else 2
simple = None
def rec(ch):
    global simple
    if simple: return
    if len(ch) == 6: simple = list(ch); return
    for r in range(36):
        if r in ch: continue
        if all(m[(ch[a], r)] == want(a, len(ch)) for a in range(len(ch))): rec(ch + [r])
rec([])
assert simple is not None
# signed permutations: (pi, eps): x'_{pi(i)} = (-1)^{eps_i} x_i ; composition (p,e)*(q,f): i -> p(q(i)), sign f_i + e_{q(i)}
def lifts(pi):
    img = [tidx[tuple(sorted(pi[i] for i in t))] for t in triads]
    e0 = solve((slog + slog[img]) % 2); assert e0 is not None
    out = []
    for mask in range(1 << len(ker)):
        e = e0.copy()
        for j in range(len(ker)):
            if mask >> j & 1: e ^= ker[j]
        out.append((pi, tuple(int(x) for x in e)))
    return out
def mul(A, B):
    (p, e), (q, f) = A, B
    return (tuple(p[q[i]] for i in range(27)), tuple((f[i] + e[q[i]]) % 2 for i in range(27)))
ID = (tuple(range(27)), (0,) * 27)
def power_is_id(A, k):
    X = ID
    for _ in range(k): X = mul(A, X)
    return X == ID
L = [[A for A in lifts(refl[s]) if power_is_id(A, 2)] for s in simple]
n_inv_lifts = [len(x) for x in L]
ok = {}
for a, b in itertools.combinations(range(6), 2):
    ok[(a, b)] = {(i, j) for i, A in enumerate(L[a]) for j, B in enumerate(L[b]) if power_is_id(mul(A, B), want(a, b))}
sols = []
def rec2(ch):
    if len(sols) >= 1 and len(ch) < 6 and False: return
    if len(ch) == 6: sols.append(tuple(ch)); return
    b = len(ch)
    for j in range(len(L[b])):
        if all((ch[a], j) in ok[(a, b)] for a in range(b)): rec2(ch + [j])
rec2([])
res = dict(simple_system_found=True, involutive_lifts_per_simple_reflection=n_inv_lifts,
           compatible_pairs={f"{a}-{b}": len(v) for (a, b), v in ok.items()}, n_splittings_for_this_simple_system=len(sols), splits=bool(sols))
if sols:
    # verify: generated group has order 51840 (acts faithfully via pi) and is sign-closed: check the group generated is a complement
    gens = [L[a][sols[0][a]] for a in range(6)]
    seen = {ID}; fr = [ID]
    while fr:
        nx_ = []
        for X in fr:
            for s in gens:
                Y = mul(s, X)
                if Y not in seen: seen.add(Y); nx_.append(Y)
        fr = nx_
        if len(seen) > 60000: break
    res["generated_group_order"] = len(seen)
print(res)
json.dump(res, open(os.path.join(ROOT, "data", "w33_e6_cubic_weyl_splitting.json"), "w"), indent=1)
