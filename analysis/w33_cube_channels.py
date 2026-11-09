"""Item 3: the cube (cusp) facets.  Each cusp facet of a pezzotope is a cube = a product of three two-point amplitudes; its 6 neighbouring
roots come in 3 opposite pairs (never in a common vertex).  Test on all 432 x 5 cusp facets: the 6 neighbours are 2 roots from each
of the 3 A2 factors of the cusp's A2^3, and each opposite pair = one A2 factor (so the 3 two-point channels = the 3 A2 factors of the
context = its 3 Steiner trihedral pairs).
usage: py -3 analysis/w33_cube_channels.py"""
import itertools, json, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
gz = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pezzotope_gosset.py")}
exec(open(os.path.join(HERE, "w33_pezzotope_gosset.py"), encoding="utf-8").read().split("# candidate canonical line sets")[0], gz)
pents, IP, T3 = gz["pents"], gz["IP"], gz["T3"]
st = Counter()
for C, r in pents:
    ra = set(r.values())
    for t in C:
        factors = sorted(T3[t], key=min)
        nb = [x for A in factors for x in A if x in ra]
        per_factor = tuple(sorted(len(set(A) & ra) for A in factors))
        verts = [frozenset(p) for p in itertools.product(*[sorted(set(A) & ra) for A in factors])]
        opp = [frozenset(pr) for pr in itertools.combinations(nb, 2) if not any(set(pr) <= v for v in verts)]
        opp_is_factor = all(any(pr <= set(A) for A in factors) for pr in opp)
        st[(per_factor, len(verts), len(opp), opp_is_factor)] += 1
res = {str(k): v for k, v in st.items()}
print("(neighbour roots per A2 factor, vertices, opposite pairs, each opposite pair = one A2 factor): count", res)
json.dump(res, open(os.path.join(ROOT, "data", "w33_cube_channels.json"), "w"), indent=1)
