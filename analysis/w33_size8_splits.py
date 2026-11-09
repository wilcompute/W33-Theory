"""Item 1: the 135 size-8 maximal partial spreads of W(3,3) (weakly unextendible 8-MUB sets, Pass 12636) vs the 45 tensor splits.
Chain: size-8 set -> its orthogonal root frame (multiplicity-6 roots, Pass 12636) -> the D4 the frame spans -> the split (Pass 12635
dictionary, D4 <-> split via the 16/24 meeting partition).  Test: 3-to-1 onto the 45 splits; and how the 8 lines sit against the split
{b, b-perp}: how many of the 8 lines meet b and b-perp (expected: the 8 = the 24 lines missing b u b-perp, minus 16?).
usage: py -3 analysis/w33_size8_splits.py"""
import itertools, json, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ns = {"__name__": "x", "__file__": os.path.join(HERE, "w33_split_bridge.py")}
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(HERE, "w33_split_bridge.py"), encoding="utf-8").read(), ns)
phi, lines, roots_of, IP, D4s, splits, match2 = (ns[k] for k in ("phi", "lines", "roots_of", "IP", "D4s", "splits", "match2"))
inv = {v: k for k, v in phi.items()}
disj = [[not (lines[a] & lines[b]) for b in range(40)] for a in range(40)]
eight = []
def bk(R, Pc, X):
    if not Pc and not X:
        if len(R) == 8: eight.append(frozenset(R))
        return
    for v in list(Pc):
        bk(R | {v}, {u for u in Pc if disj[v][u]}, {u for u in X if disj[v][u]}); Pc = Pc - {v}; X = X | {v}
bk(set(), set(range(40)), set())
d4_of_root_set = {}
for i, D in enumerate(D4s):
    d4_of_root_set[i] = D
split_of_d4 = {i: m[0] for i, m in enumerate(match2)}
img = Counter(); rel = Counter()
for S in eight:
    cnt = Counter(r for l in S for r in roots_of[inv[l]])
    F = frozenset(r for r in range(36) if cnt.get(r, 0) == 6)
    d = next(i for i, D in d4_of_root_set.items() if F <= D)
    s = split_of_d4[d]
    img[s] += 1
    b, bp = splits[s]
    rel[tuple(sorted(Counter((len(lines[l] & b), len(lines[l] & bp)) for l in S).items()))] += 1
res = dict(n_eight=len(eight), splits_hit=len(img), multiplicity=sorted(set(img.values())), line_vs_split_profile={str(k): v for k, v in rel.items()})
print(res)
json.dump(res, open(os.path.join(ROOT, "data", "w33_size8_splits.json"), "w"), indent=1)
# partition check: for each split, the three size-8 sets are disjoint and cover the 24 lines missing b u b-perp (P11143's entangled lines)
by_split = {}
for S in eight:
    cnt = Counter(r for l in S for r in roots_of[inv[l]])
    F = frozenset(r for r in range(36) if cnt.get(r, 0) == 6)
    d = next(i for i, D in d4_of_root_set.items() if F <= D)
    by_split.setdefault(split_of_d4[d], []).append(S)
part = Counter()
for s, Ss in by_split.items():
    b, bp = splits[s]
    missing = frozenset(l for l in range(40) if not (lines[l] & (b | bp)))
    product = frozenset(l for l in range(40) if (lines[l] & b) and (lines[l] & bp))
    disjoint_sets = all(not (A & B) for A, B in itertools.combinations(Ss, 2))
    part[(len(missing), len(product), len(Ss), disjoint_sets, frozenset().union(*Ss) == missing)] += 1
    # product lines: do the 16 form anything maximal? count maximal partial spreads inside the product lines
res["partition_check"] = {str(k): v for k, v in part.items()}
print("per split (entangled lines, product lines, # 8-sets, pairwise disjoint, cover the entangled lines):", dict(part))
json.dump(res, open(os.path.join(ROOT, "data", "w33_size8_splits.json"), "w"), indent=1)
