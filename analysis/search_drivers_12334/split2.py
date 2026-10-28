"""12334b (corrected rule): the e6 translation lies in the centralizer only of sectors whose twist fixes torus 3 (even Z6 power n);
odd-n sectors are localised on torus 3 (no e6 phase, no momentum tower).  Rule: brother = parent's odd-n states + parent's even-n states
with V_h.lam even; the brother's half-integer-momentum tower = parent's even-n states with V_h.lam odd.  Compared without U(1) charges
(the engine's U(1) bases differ between parent and brother).  The rule was read off the 12334 sector table (post hoc); this checks it
on the full field multiset of every lineage variant."""
import collections, json, sys
exec(open('split.py').read().split('res = {}')[0])
from mirage import read
res = {}
for v in ('v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v13', 'v17'):
    base = '../search_drivers_12281/bro/' if v in ('v9', 'v4') else '../search_drivers_12302/bro/'
    import os
    if not os.path.exists(base + f'Z6II_60_SM_20260917_810_{v}__ctrl.nsoq'):
        base = '../search_drivers_12281/bro/'
    _, prow = read(base + f'Z6II_60_SM_20260917_810_{v}__ctrl.txt'); _, brow = read(base + f'Z6II_60_SM_20260917_810_{v}__w6odd.txt')
    lam = brow[8]
    V0l, V1l = dot(prow[0], lam), dot(prow[1], lam); Wl = [dot(prow[3 + k], lam) for k in range(6)]
    par = fields(base + f'Z6II_60_SM_20260917_810_{v}__ctrl.nsoq'); bro = fields(base + f'Z6II_60_SM_20260917_810_{v}__w6odd.nsoq')
    vhl = lambda f: f['mm'] * V0l + f['n'] * V1l + sum(f['lat'][k] * Wl[k] for k in range(6))
    k5 = lambda f: f['key'][:5]
    keep = collections.Counter(k5(f) for f in par if f['n'] % 2 == 1 or vhl(f) % 2 == 0)
    half = [f for f in par if f['n'] % 2 == 0 and vhl(f) % 2 != 0]
    bk = collections.Counter(k5(f) for f in bro)
    kinds = collections.Counter('tachyon' if f['m'] in (21, 22, 23, 24) else ('fermion' if f['m'] in (19, 20) else 'boson') for f in half)
    res[v] = dict(rule_matches_brother=(keep == bk), only_rule=sum((keep - bk).values()), only_brother=sum((bk - keep).values()),
                  half_tower=dict(kinds))
    print(v, res[v])
json.dump(res, open('split2.json', 'w'), indent=1)
