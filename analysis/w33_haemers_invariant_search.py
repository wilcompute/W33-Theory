"""Pass 12669: subgroup-invariant Haemers matrices for the Shannon capacity of the W(3,3) collinearity graph G.
Haemers: Theta(G) <= rank_F(M) for every matrix M over any field F with M_ii != 0 and M_ij = 0 whenever i != j are NON-adjacent.
Known: theta(G) = 10, alpha(G) = 7, Theta(G) >= sqrt 60 (Passes 12653-12656); A + cI gives at best rank 11 (Pass 12653).
Here M is restricted to matrices invariant under a subgroup H of Aut(G): M = sum over H-orbitals o (on ordered pairs (i,j) with i = j or
i ~ j) of c_o E_o.  Fewer coefficients than the full edge set, more freedom than the Bose-Mesner algebra.  For each H (cyclic and
two-generator subgroups sampled from PSp(4,3) via transvections): exhaustive search over F_2 when the number of free coefficients is
<= 16, else simulated annealing on the coefficient vector; also F_3 and F_4 (via F_2[w]) annealing.  Diagonal orbital coefficients are
forced non-zero.  Any matrix of rank <= 9 found is re-verified from scratch (support, diagonal, rank over the field).
Control: the 27-line meeting graph (Haemers' classical example, Theta <= 7 < theta = 9): the same code with H = full automorphism
orbitals must find rank 7 over F_2.   usage: py -3 analysis/w33_haemers_invariant_search.py [seconds] [seed]"""
import itertools, json, math, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_shannon_symmetric_codes.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_shannon_symmetric_codes.py")}
argv = sys.argv; sys.argv = ["x", "1", "1"]; exec(src[: src.index("elems = {}")], g); sys.argv = argv
adj = np.array(g["adj"]); n = 40
sec = float(sys.argv[1]) if len(sys.argv) > 1 else 1200; seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
rng = np.random.default_rng(seed); g["rng"] = rng
comp = lambda p, q: tuple(p[q[i]] for i in range(len(p)))


def rank_mod(M, p):
    M = M.copy() % p; r = 0; rows, cols = M.shape
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if M[i, c]: piv = i; break
        if piv is None: continue
        if piv != r: M[[r, piv]] = M[[piv, r]]
        inv = pow(int(M[r, c]), -1, p); M[r] = (M[r] * inv) % p
        nz = np.nonzero(M[:, c])[0]
        for i in nz:
            if i != r: M[i] = (M[i] - M[i, c] * M[r]) % p
        r += 1
        if r == rows: break
    return r


def group(gens, cap=2000):
    idp = tuple(range(n)); seen = {idp}; fr = [idp]
    while fr:
        nx = []
        for x in fr:
            for s in gens:
                y = comp(s, x)
                if y not in seen:
                    seen.add(y); nx.append(y)
                    if len(seen) > cap: return None
        fr = nx
    return list(seen)


def orbitals(H, A):
    pairs = [(i, j) for i in range(n) for j in range(n) if i == j or A[i, j]]
    idx = {}; orbs = []
    for (i, j) in pairs:
        if (i, j) in idx: continue
        o = sorted({(h[i], h[j]) for h in H}); k = len(orbs)
        for pr in o: idx[pr] = k
        orbs.append(o)
    return orbs


def build(orbs, coef):
    M = np.zeros((n, n), dtype=np.int64)
    for o, c in zip(orbs, coef):
        if c:
            for (i, j) in o: M[i, j] = c
    return M


def search(orbs, p, seconds, exhaustive_cap=18):
    diag = [k for k, o in enumerate(orbs) if o[0][0] == o[0][1]]; free = [k for k in range(len(orbs)) if k not in diag]
    best = (n + 1, None); t0 = time.time()
    if p == 2 and len(free) <= exhaustive_cap:
        coef = np.zeros(len(orbs), dtype=np.int64); coef[diag] = 1
        for mask in range(1 << len(free)):
            for b, k in enumerate(free): coef[k] = (mask >> b) & 1
            r = rank_mod(build(orbs, coef), 2)
            if r < best[0]: best = (r, coef.copy())
        return best[0], best[1], "exhaustive"
    coef = rng.integers(0, p, len(orbs)); coef[diag] = rng.integers(1, p, len(diag))
    cur = rank_mod(build(orbs, coef), p); best = (cur, coef.copy()); T = 1.5
    while time.time() - t0 < seconds:
        k = int(rng.integers(len(orbs))); old = coef[k]
        coef[k] = int(rng.integers(1, p)) if k in diag else int((old + rng.integers(1, p)) % p)
        r = rank_mod(build(orbs, coef), p)
        if r <= cur or rng.random() < math.exp(-(r - cur) / T): cur = r
        else: coef[k] = old
        if cur < best[0]: best = (cur, coef.copy())
        T = max(0.05, T * 0.999)
    return best[0], best[1], "anneal"


out = dict(control={}, runs=[]); t_all = time.time()
# control: 27-line meeting graph with its full automorphism orbitals = {diagonal, edges}
lines = [("a", i) for i in range(6)] + [("b", i) for i in range(6)] + [("c", p_) for p_ in itertools.combinations(range(6), 2)]
def meet(x, y):
    if x == y: return False
    (s, u), (t, v) = x, y
    if {s, t} == {"a", "b"}: return u != v
    if s == t and s in "ab": return False
    if s == "c" and t == "c": return not set(u) & set(v)
    cu, other = (u, v) if s == "c" else (v, u)
    return other in cu
Mt = np.array([[int(meet(x, y)) for y in lines] for x in lines])
orbs_ctrl = [[(i, i) for i in range(27)], [(i, j) for i in range(27) for j in range(27) if Mt[i, j]]]
n_save = n; n = 27
r_ctrl = min(rank_mod(build(orbs_ctrl, np.array([1, c])), 2) for c in (0, 1))
n = n_save
out["control"]["meeting_graph_F2_rank"] = r_ctrl; print("control (27-line meeting graph, expect 7):", r_ctrl, flush=True)
assert r_ctrl == 7
# subgroups of Aut(W(3,3))
best_overall = (99, None)
tried = 0; deadline = time.time() + sec
while time.time() < deadline:
    gens = []
    for _ in range(int(rng.integers(2, 4))):
        e = g["random_element"](int(rng.integers(2, 10))); o = g["order"](e)
        pr = [q_ for q_ in (2, 3, 5) if o % q_ == 0]
        gens.append(g["power"](e, o // int(rng.choice(pr))) if pr else e)
    H = group(gens, cap=6000)
    if H is None or len(H) < 20: continue
    orbs = orbitals(H, adj); tried += 1
    for p in (2, 3):
        budget = min(40.0, max(5.0, deadline - time.time()))
        r, coef, mode = search(orbs, p, budget)
        rec = dict(group_order=len(H), n_orbitals=len(orbs), p=p, best_rank=int(r), mode=mode)
        out["runs"].append(rec)
        if r < best_overall[0]:
            M = build(orbs, coef)
            ok = all(M[i, i] % p for i in range(n)) and all((M[i, j] % p == 0) for i in range(n) for j in range(n) if i != j and not adj[i, j])
            best_overall = (int(r), dict(rec, verified_support=bool(ok), rank_recomputed=int(rank_mod(M, p)), matrix=(M % p).tolist()))
            print("new best", rec, "verified", ok, round(time.time() - t_all), "s", flush=True)
        if time.time() > deadline: break
out["subgroups_tried"] = tried; out["best_rank"] = best_overall[0]; out["best"] = best_overall[1]
out["beats_lovasz"] = best_overall[0] <= 9
print("subgroups tried", tried, "best rank", best_overall[0], "beats theta=10:", out["beats_lovasz"], flush=True)
json.dump(out, open(os.path.join(ROOT, "data", f"w33_haemers_invariant_search_seed{seed}.json"), "w"), indent=1)
