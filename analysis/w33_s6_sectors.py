"""Item 4: unify the doily-S6 proof (Pass 12639) with the other track's nine 5D centre-of-mass sectors (7332f3b48).
Sectors: Sym^2(C^9) basis |z,w> + |w,z>, z, w in F3^2 (computational labels), grouped by s = z + w (9 sectors of dim 5).
Test: do the five sentinel swap operators S_k (and the 15 doily transpositions) preserve every sector?  If so, the S6 acts on each 5D
sector, and its character there should be the standard (5,1): trace 3 on a transposition, 2 on a 3-cycle.
usage: py -3 analysis/w33_s6_sectors.py"""
import itertools, json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
si = {"__name__": "x", "__file__": os.path.join(HERE, "w33_sentinel_identity.py")}
src = open(os.path.join(HERE, "w33_sentinel_identity.py"), encoding="utf-8").read().split("# --- Jucys-Murphy test")[0]
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, si)
Ss, d = si["Ss"], 9
lab = [(a, b) for a in range(3) for b in range(3)]  # computational basis index i <-> z = (i // 3, i % 3)
sectors = {}
for i in range(9):
    for j in range(i, 9):
        s = ((lab[i][0] + lab[j][0]) % 3, (lab[i][1] + lab[j][1]) % 3)
        v = np.zeros(81)
        if i == j: v[i * 9 + i] = 1
        else: v[i * 9 + j] = v[j * 9 + i] = 1 / np.sqrt(2)
        sectors.setdefault(s, []).append(v)
sectors = {s: np.array(V).T for s, V in sectors.items()}
assert len(sectors) == 9 and all(V.shape[1] == 5 for V in sectors.values())
pres = []
tr = []
for S in Ss:
    ok = True
    for s, V in sectors.items():
        img = S @ V
        P = V @ V.T
        if not np.allclose(P @ img, img, atol=1e-8): ok = False
    pres.append(ok)
V0 = sectors[(0, 0)]
Sr = [V0.T @ S @ V0 for S in Ss]
res = dict(sentinel_swaps_preserve_all_sectors=all(pres), per_swap=pres)
if all(pres):
    res.update(trace_transposition=float(np.trace(Sr[0]).real), trace_3cycle=float(np.trace(Sr[0] @ Sr[1]).real))
print(res)
json.dump(res, open(os.path.join(ROOT, "data", "w33_s6_sectors.json"), "w"), indent=1, default=str)
