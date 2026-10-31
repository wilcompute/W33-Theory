"""12506: the 240 points covered by the q = 9 48-line even set, against the E8 root system.  The set's stabiliser contains the binary
icosahedral group 2I (McKay: 2I <-> E8; the 240 E8 roots are the icosians 2I u (golden conjugate)).  Here: (a) orbits on the 240
points of the stabiliser matrices (no swap: F9* . 2I, 480 matrices = 240 point permutations) and of its 2I part (SL(2,9) matrices);
(b) the collinearity graph on the 240 points (two points adjacent iff on a common W(3,9) line) and its spectrum, compared with the E8
root graph (<r,s> = 1: degree 56, eigenvalues 56, 28, 8, -4, -8 -- computed here from the E8 roots as a control).
usage: py -3 e8_icosian_probe.py"""
import json, itertools, collections
import numpy as np
exec(open("stab48.py", encoding="utf-8").read().split("perm_set =")[0])   # builds S, stab (matrices, swap flag, line maps), pts, ...

cov = sorted(set().union(*(sets[j] for j in S)))
covs = set(cov)
# point permutations of the non-swap stabiliser
def pmap(M):
    g = elem(M); return {p: g(p) for p in cov}
Ms = [M for M, sw, _ in stab if not sw]
maps = {tuple(sorted(pmap(M).items())) for M in Ms}
pm_list = [dict(m) for m in maps]
def orbits(perms, dom):
    seen, out = set(), []
    for p in dom:
        if p in seen: continue
        o = {p}; fr = [p]
        while fr:
            nx_ = []
            for t in fr:
                for P in perms:
                    u = P[t]
                    if u not in o: o.add(u); nx_.append(u)
            fr = nx_
        seen |= o; out.append(len(o))
    return sorted(out)
det = lambda M: add[mul[M[0][0]][M[1][1]]][neg[mul[M[0][1]][M[1][0]]]]
SLpart = [M for M in Ms if det(M) == 1]
sl_maps = [dict(m) for m in {tuple(sorted(pmap(M).items())) for M in SLpart}]
fixed = collections.Counter(sum(1 for p in cov if P[p] == p) for P in pm_list)
res = dict(covered=len(cov), point_permutations=len(pm_list), orbits_full=orbits(pm_list, cov),
           SL_matrices=len(SLpart), SL_point_perms=len(sl_maps), orbits_2I=orbits(sl_maps, cov),
           fixed_point_counts=dict(sorted(fixed.items())))
# collinearity graph on the 240 points
idx = {p: i for i, p in enumerate(cov)}; A = np.zeros((240, 240), dtype=int)
for L in lines:
    on = [idx[p] for p in L if p in covs]
    for a, b in itertools.combinations(on, 2): A[a, b] = A[b, a] = 1
ev = collections.Counter(np.round(np.linalg.eigvalsh(A), 3).tolist())
res["collinearity_degrees"] = sorted(set(A.sum(1).tolist())); res["collinearity_spectrum"] = dict(sorted(ev.items()))
# control: the E8 root graph
roots = []
for i, j in itertools.combinations(range(8), 2):
    for si in (1, -1):
        for sj in (1, -1):
            v = [0] * 8; v[i] = si; v[j] = sj; roots.append(v)
for signs in itertools.product((1, -1), repeat=8):
    if signs.count(-1) % 2 == 0: roots.append([s / 2 for s in signs])
R = np.array(roots); G = R @ R.T; E = (np.abs(G - 1) < 1e-9).astype(int)
res["E8_roots"] = len(roots); res["E8_root_graph_spectrum"] = dict(sorted(collections.Counter(np.round(np.linalg.eigvalsh(E), 3).tolist()).items()))
print(json.dumps(res, indent=1)); json.dump(res, open("e8_icosian_probe.json", "w"), indent=1)
