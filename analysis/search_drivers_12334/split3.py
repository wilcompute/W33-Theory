"""12334c: the full rule on all 15 lineage variants, comparing physical classes (boson / fermion; the engine lists each CPT pair in
both members, so L/R and phi/phi* labels are not physical).  Rule (bicharacter, S = {e6}):
  even-n sectors: e6 lies in the centralizer; brother keeps the parent states with V_h.lam even, the odd ones move to half-integer
    e6 momentum (the brother's massive tower);
  odd-n sectors: localised on torus 3; at fixed points with odd label f6, B(w, h) = -(1/2) f6 V0.lam = 1/2 flips the Witten projection:
    bosons <-> fermions; elsewhere unchanged."""
import collections, json, os
exec(open('split.py').read().split('res = {}')[0])
from mirage import read
cls = lambda m: 'B' if m in ('13', '14', '15', '16', '17', '18', '8', '9') else ('F' if m in ('19', '20') else 'T' + m)
res = {}
for v in ('v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v13', 'v17'):
    base = '../search_drivers_12302/bro/'
    if not os.path.exists(base + f'Z6II_60_SM_20260917_810_{v}__ctrl.nsoq'):
        base = '../search_drivers_12281/bro/'
    _, prow = read(base + f'Z6II_60_SM_20260917_810_{v}__ctrl.txt'); _, brow = read(base + f'Z6II_60_SM_20260917_810_{v}__w6odd.txt')
    lam = brow[8]
    V0l, V1l = dot(prow[0], lam), dot(prow[1], lam); Wl = [dot(prow[3 + k], lam) for k in range(6)]
    par = fields(base + f'Z6II_60_SM_20260917_810_{v}__ctrl.nsoq'); bro = fields(base + f'Z6II_60_SM_20260917_810_{v}__w6odd.nsoq')
    vhl = lambda f: f['mm'] * V0l + f['n'] * V1l + sum(f['lat'][k] * Wl[k] for k in range(6))
    pred = collections.Counter(); half = collections.Counter()
    for f in par:
        c = cls(f['key'][0]); key = (f['key'][1], f['key'][2], f['key'][3], f['key'][4])
        if f['n'] % 2 == 0:
            if vhl(f) % 2 == 0:
                pred[(c,) + key] += 1
            else:
                half['tachyon' if c.startswith('T') else c] += 1
        else:
            if f['lat'][5] % 2 == 1 and c in ('B', 'F'):
                c = {'B': 'F', 'F': 'B'}[c]
            pred[(c,) + key] += 1
    bk = collections.Counter((cls(f['key'][0]), f['key'][1], f['key'][2], f['key'][3], f['key'][4]) for f in bro)
    res[v] = dict(rule_matches=(pred == bk), mismatch=sum((pred - bk).values()) + sum((bk - pred).values()), half_tower=dict(half))
    print(v, res[v])
json.dump(res, open('split3.json', 'w'), indent=1)
