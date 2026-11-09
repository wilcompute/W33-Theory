"""Creative 3: is the chirality reflection s_alpha (Pass 12636) Pass 12523's Kramers reversal theta?  P12523: the outer coset of PSp(4,3)
in PGSp(4,3) has 576 involutions on the 40 points: 540 with 8 fixed points and 36 fixed-point-free (the Kramers reversals, one per
double-six).  Act with s_alpha on the 40 A2^3 (= W(3,3) lines) and on the 40 points (point = 4 pairwise root-disjoint A2^3 partitioning
the 36 roots, Pass 12635); count fixed points; s_alpha is theta iff fixed-point-free on points and an involution.
usage: py -3 analysis/w33_reflection_is_kramers.py"""
import itertools, json, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pass12634_naruki_fan.py")}
exec(open(os.path.join(HERE, "w33_pass12634_naruki_fan.py"), encoding="utf-8").read().split("# --- Check 1")[0], g)
POS, IP, PI, key, roots_of = g["POS"], g["IP"], g["PI"], g["key"], g["roots_of"]
Tindex = {roots_of[t]: t for t in range(40)}
def refl(a):
    al = POS[a]
    return [PI[key(POS[i] - (2 * (POS[i] @ al) // (al @ al)) * al)] for i in range(36)]
# points: 4-cliques of pairwise root-disjoint A2^3
disj = lambda s, t: not (roots_of[s] & roots_of[t])
points = [frozenset(c) for c in itertools.combinations(range(40), 4) if all(disj(a, b) for a, b in itertools.combinations(c, 2))]
assert len(points) == 40
pidx = {p: i for i, p in enumerate(points)}
st = Counter()
for a in range(36):
    s = refl(a)
    lineperm = [Tindex[frozenset(s[x] for x in roots_of[t])] for t in range(40)]
    ptperm = [pidx[frozenset(lineperm[t] for t in p)] for p in points]
    invol = all(ptperm[ptperm[i]] == i for i in range(40))
    st[(invol, sum(1 for i in range(40) if ptperm[i] == i), sum(1 for t in range(40) if lineperm[t] == t))] += 1
res = {str(k): v for k, v in st.items()}
print("(involution, fixed points, fixed lines): number of reflections", res)
json.dump(dict(stats=res, reflections_are_kramers=list(st) == [(True, 0, 4)] or all(k[0] and k[1] == 0 for k in st)), open(os.path.join(ROOT, "data", "w33_reflection_is_kramers.json"), "w"), indent=1)
