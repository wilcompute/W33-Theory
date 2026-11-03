"""12533 follow-ups (ideas 1 and 5): the W(3,3) objects as colour patterns on 6 strands.  (a) the 40 points by colour-class sizes; (b) does a strand permutation preserving parity classes preserve the form?  (c) which perfect matchings of the 6 strands give Lagrangians (lines); (d) how many of those matching lines lie in a minimal codeword; which colour types a codeword covers.  usage: py -3 colour_patterns.py"""
import collections
import itertools
import json

src = open("fox_w33.py", encoding="utf-8").read().split('caps = {to4(c) for c in ALL')[0]
exec(src)
out = {}
ns = g
lines_ = [frozenset(L) for L in lines]
inv = {}
for v in nz:
    inv.setdefault(pt_of(v), []).append(from4(v))
assert len(inv) == 40 and all(len(x) == 2 for x in inv.values())
def csize(c):
    return tuple(sorted(collections.Counter(c).values(), reverse=True))
def ctype(c):
    n = collections.Counter(c)
    return (tuple(sorted(n.values(), reverse=True)),)
types = {p: csize(inv[p][0]) for p in inv}
out["points_by_colour_class_sizes"] = {str(k): v for k, v in collections.Counter(types.values()).items()}
# strand permutations preserving the alternating sum
odd, even = (0, 2, 4), (1, 3, 5)
def perm_ok(perm):
    pmap = {}
    for p in inv:
        c = inv[p][0]
        d = tuple(c[perm[i]] for i in range(6))
        if alt(d) != 0:
            return None
        pmap[p] = pt_of(to4(d))
    return all((om(to4(inv[a][0]), to4(inv[b][0])) == 0) == (om(to4(tuple(inv[a][0][perm[i]] for i in range(6))), to4(tuple(inv[b][0][perm[i]] for i in range(6)))) == 0) for a in inv for b in inv)
res = collections.Counter()
for po in itertools.permutations(odd):
    for pe in itertools.permutations(even):
        perm = [0] * 6
        for a, b in zip(odd, po):
            perm[a] = b
        for a, b in zip(even, pe):
            perm[a] = b
        res[str(perm_ok(perm))] += 1
out["parity_preserving_strand_perms_preserve_commutation"] = dict(res)
# matchings
matchings = []
def pm(items):
    if not items:
        yield []
        return
    a = items[0]
    for i in range(1, len(items)):
        for r in pm(items[1:i] + items[i + 1:]):
            yield [(a, items[i])] + r
all_pm = list(pm(list(range(6))))
rec = []
for M in all_pm:
    basis_ = []
    for (a_, b_) in M:
        c = [0] * 6
        c[a_] = c[b_] = 1
        basis_.append(tuple(c))
    bip = all((a_ + b_) % 2 == 1 for a_, b_ in M)
    if not bip:
        rec.append(dict(M=M, bipartite=False))
        continue
    cover = {tuple(sum(s[i] * basis_[i][k] for i in range(3)) % 3 for k in range(6)) for s in itertools.product(range(3), repeat=3)}
    P = {pt_of(to4(c)) for c in cover if any(to4(c))}
    noncross = all(not (a_ < x < b_ < y or x < a_ < y < b_) for (a_, b_), (x, y) in itertools.combinations(M, 2))
    rec.append(dict(M=M, bipartite=True, noncrossing=noncross, is_a_line=frozenset(P) in lines_, points=len(P)))
out["matchings"] = dict(total=len(all_pm), bipartite=sum(r["bipartite"] for r in rec), bipartite_are_lines=sum(1 for r in rec if r.get("is_a_line")), bipartite_noncrossing=sum(1 for r in rec if r.get("noncrossing")))
mlines = [frozenset({pt_of(to4(tuple(sum(s[i] * ([1 if k in pair else 0 for k in range(6)])[k2] for i, pair in enumerate(r["M"])) % 3 for k2 in range(6)))) for s in itertools.product(range(3), repeat=3) if any(to4(tuple(sum(s[i] * ([1 if k in pair else 0 for k in range(6)])[k2] for i, pair in enumerate(r["M"])) % 3 for k2 in range(6))))}) for r in rec if r.get("is_a_line")]
lid = {L: j for j, L in enumerate(lines_)}
ids = {lid[L] for L in mlines}
rs = {}
exec(open("braid_codewords.py", encoding="utf-8").read().split("codewords = list(orb)")[0].split("# induced path")[1].split("gens = [T(pts[p]) for p in path]")[0] if False else "", rs)
import runpy
bc = runpy.run_path("braid_codewords.py")
cw = bc["codewords"]
assert bc["pts"] == pts or list(map(tuple, bc["pts"])) == list(map(tuple, pts))
out["codewords_by_number_of_matching_lines"] = {str(k): v for k, v in sorted(collections.Counter(len(set(S) & ids) for S in cw).items())}
cov = collections.Counter()
for S in cw[:216]:
    C = set().union(*(set(bc["lines"][j]) for j in S))
    cov[tuple(sorted(collections.Counter(types[p] for p in C).items()))] += 1
out["covered_points_colour_profiles"] = {str(k): v for k, v in cov.items()}
print(json.dumps(out, default=str))
json.dump(out, open("colour_patterns.json", "w"), indent=1, default=str)
