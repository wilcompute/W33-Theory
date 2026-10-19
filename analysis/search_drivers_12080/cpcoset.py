import sys
from collections import Counter
import numpy as np
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12052_real_forms_on_forty_points import build
from w33_pass12053_gate_sets_and_real_forms import setup, sp43_from_ticks
R, C, fib, refl, perm = build()
Adj, invs, tick, _ = setup()
G = sp43_from_ticks(tick)
w = perm(np.load('w_invert.npy'))
Wp = perm(np.linalg.matrix_power(C, 10))
neg = perm(-np.eye(8))
ptof = np.empty(240, int)
for x in range(40):
    for i in fib[x]: ptof[i] = x
clocks = [s for k, s in invs if k == 'clock']
Pc = np.array(clocks)
cpt = []
for s in clocks:
    ev = {x for x in range(40) if not s[fib[x]].any()}
    cpt.append(next(x for x in range(40) if set(np.nonzero(Adj[x])[0]) == ev))
cpt = np.array(cpt)
print('omega fixes every clock:', all(np.array_equal(c[Wp], c) for c in clocks))
print('w preserves fibres:', all(len({ptof[w[i]] for i in fib[x]}) == 1 for x in range(40)))
idn = np.arange(240)
stats = Counter()
first = {}
for g in G:
    e = w[g]                     # composition: apply g then w (convention as in 12058: a[b])
    pp = np.array([ptof[e[fib[x][0]]] for x in range(40)])
    if not np.array_equal(pp[pp], np.arange(40)):
        continue
    fixed = np.where(pp == np.arange(40))[0]
    sq = e[e]
    sqt = 'e^2=1' if np.array_equal(sq, idn) else ('e^2=-1' if np.array_equal(sq, neg) else 'e^2 other')
    # clock action: clock c -> c o e^-1 ; preserved iff c[e] == c
    keep = [i for i in range(120) if np.array_equal(Pc[i][e], Pc[i])]
    kf = Counter(int(np.sum(cpt[keep] == x)) for x in fixed)
    stats[(len(fixed), sqt, len(keep), tuple(sorted(kf.items())))] += 1
for k, v in sorted(stats.items()): print(v, k)
# omega on clocks
cyc = all(len({cpt[i]} | {cpt[j] for j in range(120) if np.array_equal(Pc[i][Wp], Pc[j])}) == 1 for i in range(120))
orbit3 = all(not np.array_equal(Pc[i][Wp], Pc[i]) for i in range(120))
print('omega keeps each clock at its event and moves every clock (3-cycles at each event):', cyc, orbit3)
# CP fixed clocks on L leave su(2)^8 on L u L' (the CP's own fixed set)?
ok, n = True, 0
for g in G:
    e = w[g]
    pp = np.array([ptof[e[fib[x][0]]] for x in range(40)])
    if not np.array_equal(pp[pp], np.arange(40)): continue
    fixed = set(np.where(pp == np.arange(40))[0].tolist())
    if len(fixed) != 8: continue
    keep = [i for i in range(120) if np.array_equal(Pc[i][e], Pc[i])]
    comps = []
    for x in sorted(fixed):
        if not any(x in c for c in comps):
            comps.append({x} | {y for y in fixed if Adj[x, y]})
    L = sorted(comps[0])
    cl4 = [i for i in keep if cpt[i] in L]
    even = np.ones(240, bool)
    for i in cl4: even &= ~Pc[i]
    pts = {ptof[i] for i in np.nonzero(even)[0]}
    ok &= len(cl4) == 4 and even.sum() == 16 and pts == fixed
    n += 1
    if n >= 200: break
print('CP-compatible clocks on L leave su(2)^8 exactly on the CP fixed set L u L\' (200 CPs):', ok)
dbg = Counter()
n = 0
for g in G:
    e = w[g]
    pp = np.array([ptof[e[fib[x][0]]] for x in range(40)])
    if not np.array_equal(pp[pp], np.arange(40)): continue
    fixed = set(np.where(pp == np.arange(40))[0].tolist())
    if len(fixed) != 8: continue
    keep = [i for i in range(120) if np.array_equal(Pc[i][e], Pc[i])]
    comps = []
    for x in sorted(fixed):
        if not any(x in c for c in comps):
            comps.append({x} | {y for y in fixed if Adj[x, y]})
    L = sorted(comps[0])
    cl4 = [i for i in keep if cpt[i] in L]
    even = np.ones(240, bool)
    for i in cl4: even &= ~Pc[i]
    pts = {ptof[i] for i in np.nonzero(even)[0]}
    Lp = pts - set(L)
    dbg[(len(comps), len(cl4), int(even.sum()), len(pts & fixed), len(Lp & fixed))] += 1
    n += 1
    if n >= 200: break
print(dbg)
