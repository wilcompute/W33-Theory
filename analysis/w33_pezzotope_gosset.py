"""Are the 432 E6 pezzotopes (Pass 12634 addendum: S5-pentads of W(3,3) lines) the 432 four-simplex faces of the Gosset polytope 2_21
(vertices = the 27 lines of a cubic surface, edges = skew pairs; a 4-simplex = 5 mutually skew lines; 2_21 f-vector
(27, 216, 720, 1080, 648 = 432 simplices + 216 orthoplexes, 99))?
Model: E8 roots in doubled coordinates; E6 = roots orthogonal to an A2 = <a1, a2>; the 27 = E8 roots r with (r.a1, r.a2) equal to a
fixed nonzero class, projected to the E6 span.  Lines meet / are skew by the projected inner product.  For each pentad (T_1..T_5;
roots r_ab with r_ab in T_i iff i not in {a, b}), look for a canonical set of lines: those orthogonal to all 10 roots, those in the
"(1,1,1) part" of each T, etc., and test whether the map pentad -> line set is a W(E6)-equivariant bijection onto skew 5-sets
(or onto the 72 sixes x 6).
usage: py -3 analysis/w33_pezzotope_gosset.py"""
import itertools
import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_pass12634_naruki_fan.py"), encoding="utf-8").read().split("# --- Check 1")[0]
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pass12634_naruki_fan.py")}
exec(src, g)
E8, a1, a2, POS, IP, T3, roots_of, np = (g[k] for k in ("E8", "a1", "a2", "POS", "IP", "T3", "roots_of", "np"))

# the 27: E8 roots with a fixed nonzero inner-product class against (a1, a2)
classes = Counter((int(r @ a1), int(r @ a2)) for r in E8)
cls = next(c for c, n in classes.items() if n == 27)
B = np.array([a1, a2], dtype=float)
proj = lambda v: v - B.T @ np.linalg.solve(B @ B.T, B @ v)
L27 = np.array([proj(r.astype(float)) for r in E8 if (int(r @ a1), int(r @ a2)) == cls])
assert len(L27) == 27
G = L27 @ L27.T
vals = sorted(Counter(np.round(G[np.triu_indices(27, 1)], 6)).items())
print("line-line inner products (value: pairs):", vals)
# meeting pairs: 135 (each line meets 10); skew: 216 (each skew to 16)
v_meet = next(v for v, n in vals if n == 135)
v_skew = next(v for v, n in vals if n == 216)
skew = lambda i, j: abs(G[i, j] - v_skew) < 1e-6
sk5 = [S for S in itertools.combinations(range(27), 5) if all(skew(i, j) for i, j in itertools.combinations(S, 2))]
sk6 = [S for S in itertools.combinations(range(27), 6) if all(skew(i, j) for i, j in itertools.combinations(S, 2))]
print("skew 5-sets (4-simplices of 2_21):", len(sk5), "| sixes:", len(sk6))
# root-line inner products in the same normalisation
RL = POS.astype(float) @ L27.T
print("root.line values:", sorted(Counter(np.round(RL.ravel(), 6)).items()))

# rebuild the 432 pentads
n = 40
share = [[len(roots_of[s] & roots_of[t]) for t in range(n)] for s in range(n)]
cl = []
def ext(c, cand):
    if len(c) == 5:
        cl.append(tuple(c)); return
    for i, v in enumerate(cand):
        ext(c + [v], [w_ for w_ in cand[i + 1:] if share[v][w_] == 3])
ext([], list(range(n)))
pents = []
for C in cl:
    r = {}
    good = True
    for trip in itertools.combinations(range(5), 3):
        com = roots_of[C[trip[0]]] & roots_of[C[trip[1]]] & roots_of[C[trip[2]]]
        if len(com) != 1:
            good = False; break
        r[tuple(sorted(set(range(5)) - set(trip)))] = next(iter(com))
    if good and len(set(r.values())) == 10:
        pents.append((C, r))
assert len(pents) == 432

# candidate canonical line sets for a pentad
def candidates(C, r):
    R = sorted(r.values())
    zero_all = [l for l in range(27) if all(abs(RL[x, l]) < 1e-6 for x in R)]
    # line pattern vector against the 10 roots (0 / nonzero)
    pat = Counter(tuple(int(abs(RL[x, l]) > 1e-6) for x in R) for l in range(27))
    return zero_all, pat
zs = Counter()
maps = []
for C, r in pents:
    z, pat = candidates(C, r)
    zs[len(z)] += 1
    maps.append(frozenset(z))
print("lines orthogonal to all 10 pentad roots: count per pentad:", dict(zs))
res = dict(line_inner_products=[(float(v), n) for v, n in vals], n_skew5=len(sk5), n_sixes=len(sk6), orth_lines_per_pentad=dict(zs))
if set(zs) == {5}:
    imgs = set(maps)
    res["image_is_skew5"] = all(all(skew(i, j) for i, j in itertools.combinations(sorted(S), 2)) for S in imgs)
    res["bijective_onto_skew5"] = len(imgs) == 432 and imgs == {frozenset(S) for S in sk5}
    print("image pairwise skew:", res["image_is_skew5"], "| bijective onto the 432 4-simplices:", res["bijective_onto_skew5"])
else:
    # report the pattern of how lines sit against the 10 roots for one pentad
    C, r = pents[0]
    R = [r[k] for k in sorted(r)]
    pat = Counter(tuple(int(round(RL[x, l] / abs(v_skew if v_skew else 1)) if False else int(abs(RL[x, l]) > 1e-6)) for x in R) for l in range(27))
    res["pattern_counts_first_pentad"] = {str(k): v for k, v in pat.items()}
    print("line patterns vs the 10 roots (first pentad):", dict(Counter(sum(k) for k in pat.elements())))
json.dump(res, open(os.path.join(ROOT, "data", "w33_pezzotope_gosset.json"), "w"), indent=1, default=str)

# --- the 12 + 15 split: is the 12 a double-six, are the 5-root patterns Hamiltonian 5-cycles of K5, and do the two sixes = the two
#     A5-orbits of 5-cycles?  And the 15: their 4-root patterns. Checked on all 432 pentads.
def is_ham_cycle(edges):
    if len(edges) != 5:
        return False
    deg = Counter(x for e in edges for x in e)
    if set(deg.values()) != {2} or len(deg) != 5:
        return False
    adj = {v: [u for e in edges for u in e if v in e and u != v] for v in deg}
    seen, cur, prev = {0}, 0, None
    for _ in range(4):
        nxt = [u for u in adj[cur] if u != prev][0] if prev is not None else adj[cur][0]
        prev, cur = cur, nxt
        seen.add(cur)
    return len(seen) == 5
def cyc_parity(edges):
    # orientation class of a 5-cycle under A5: canonical cyclic sequence starting at 0, compare with its reverse via permutation parity
    adj = {v: sorted(u for e in edges for u in e if v in e and u != v) for v in range(5)}
    seq = [0, adj[0][0]]
    while len(seq) < 5:
        seq.append([u for u in adj[seq[-1]] if u != seq[-2]][0])
    # parity of the permutation seq (as a map i -> seq[i]); reversal-invariant class: min over seq and reversed rotation
    def parity(p):
        p = list(p); s = 0
        for i in range(5):
            while p[i] != i:
                j = p[i]; p[i], p[j] = p[j], p[i]; s += 1
        return s % 2
    return parity(seq)
summ = Counter()
for C, r in pents:
    keys = sorted(r)
    R = [r[k] for k in keys]
    nz = {l: [keys[x] for x in range(10) if abs(RL[R[x], l]) > 1e-6] for l in range(27)}
    twelve = [l for l in range(27) if len(nz[l]) == 5]
    fifteen = [l for l in range(27) if len(nz[l]) == 4]
    # double-six: 12 lines splitting into two pairwise-skew sixes, each line of one six meeting all but one of the other
    sixes_here = [S for S in itertools.combinations(twelve, 6) if all(skew(i, j) for i, j in itertools.combinations(S, 2))]
    ds = len(sixes_here) == 2 and set(sixes_here[0]) | set(sixes_here[1]) == set(twelve)
    ham = all(is_ham_cycle(nz[l]) for l in twelve)
    split_ok = None
    if ds and ham:
        par = [{cyc_parity(nz[l]) for l in S} for S in sixes_here]
        split_ok = all(len(p) == 1 for p in par) and par[0] != par[1]
    # 15 lines: their 4 roots = which edge pattern? classify by degree sequence of the 4-edge graph on 5 vertices
    pat15 = Counter(tuple(sorted(Counter(x for e in nz[l] for x in e).values())) for l in fifteen)
    summ[(len(twelve), ds, ham, split_ok, tuple(sorted(pat15.items())))] += 1
print("per-pentad summary (|12|, double-six, all Hamiltonian 5-cycles, sixes = the two A5 orbits, 15-line edge patterns): count")
for k, v in summ.items():
    print("  ", k, v)
ds_of = Counter()
for C, r in pents:
    keys = sorted(r); R = [r[k] for k in keys]
    twelve = frozenset(l for l in range(27) if sum(abs(RL[R[x], l]) > 1e-6 for x in range(10)) == 5)
    ds_of[twelve] += 1
res["pentad_summary"] = {str(k): v for k, v in summ.items()}
res["distinct_double_sixes"] = len(ds_of)
res["pentads_per_double_six"] = sorted(set(ds_of.values()))
print("distinct double-sixes hit:", len(ds_of), "| pentads per double-six:", sorted(set(ds_of.values())))
json.dump(res, open(os.path.join(ROOT, "data", "w33_pezzotope_gosset.json"), "w"), indent=1, default=str)

# --- the 5 cube facets as a synthematic total of the double-six (corpus P12523: 216 codewords = totals of 36 double-sixes) ---------
meet = lambda i, j: abs(G[i, j] - v_meet) < 1e-6
tot_map = Counter()
total_ok = Counter()
for C, r in pents:
    keys = sorted(r); R = [r[k] for k in keys]
    nz = {l: [keys[x] for x in range(10) if abs(RL[R[x], l]) > 1e-6] for l in range(27)}
    twelve = [l for l in range(27) if len(nz[l]) == 5]
    fifteen = [l for l in range(27) if len(nz[l]) == 4]
    sixes_here = [S for S in itertools.combinations(twelve, 6) if all(skew(i, j) for i, j in itertools.combinations(S, 2))]
    six = sorted(sixes_here[0])
    duad = {l: frozenset(six.index(a) for a in six if meet(l, a)) for l in fifteen}
    groups = {}
    for l in fifteen:
        miss = (set(range(5)) - {x for e in nz[l] for x in e}).pop()
        groups.setdefault(miss, []).append(duad[l])
    synthemes_ok = all(len(gp) == 3 and all(len(d) == 2 for d in gp) and len(frozenset().union(*gp)) == 6 for gp in groups.values())
    all_duads = [d for gp in groups.values() for d in gp]
    total = synthemes_ok and len(set(all_duads)) == 15
    total_ok[total] += 1
    # key: (double-six as a set of 12 lines, the total as a set of synthemes in terms of LINE labels, which is six-independent)
    tot_lines = frozenset(frozenset(l for l in fifteen if (set(range(5)) - {x for e in nz[l] for x in e}).pop() == m) for m in range(5))
    tot_map[(frozenset(twelve), tot_lines)] += 1
res["cubes_form_synthematic_total"] = dict(total_ok)
res["distinct_double_six_total_pairs"] = len(tot_map)
res["pentads_per_pair"] = sorted(set(tot_map.values()))
print("5 cube facets form a synthematic total:", dict(total_ok), "| distinct (double-six, total):", len(tot_map), "| pentads per pair:", res["pentads_per_pair"])
json.dump(res, open(os.path.join(ROOT, "data", "w33_pezzotope_gosset.json"), "w"), indent=1, default=str)
