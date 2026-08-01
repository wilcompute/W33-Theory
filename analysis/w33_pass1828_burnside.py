#!/usr/bin/env python3
from __future__ import annotations
import sys, collections, json, hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from w33_pass1801_1805_common import build_geometry
D=build_geometry(); gens=[tuple(a[4]) for a in D['acts']]; I=tuple(range(45))
def comp(p,q): return tuple(p[q[i]] for i in range(45))
seen={I}; queue=[I]
for x in queue:
    for g in gens:
        y=comp(g,x)
        if y not in seen: seen.add(y); queue.append(y)
assert len(seen)==25920
def ctype(p):
    done=[False]*45; lengths=[]
    for i in range(45):
        if done[i]: continue
        j=i; n=0
        while not done[j]: done[j]=True; n+=1; j=p[j]
        lengths.append(n)
    return tuple(sorted(lengths))
ct=collections.Counter(ctype(g) for g in seen); sums=[0]*46
for typ,mul in ct.items():
    poly=[1]+[0]*45
    for L in typ:
        for k in range(45,L-1,-1): poly[k]+=poly[k-L]
    for k in range(46): sums[k]+=mul*poly[k]
assert all(x%25920==0 for x in sums)
orbits=[x//25920 for x in sums]
res={'group_order':25920,'cycle_type_count':len(ct),'subset_orbit_counts':orbits,
     'total_subset_orbits':sum(orbits),'middle_orbits':orbits[22],
     'symmetry':all(orbits[k]==orbits[45-k] for k in range(46)),
     'cycle_index':[{'cycle_lengths':list(t),'multiplicity':m} for t,m in sorted(ct.items())]}
raw=json.dumps(res,sort_keys=True,separators=(',',':'))
res['sha256']=hashlib.sha256(raw.encode()).hexdigest()
(ROOT/'data'/'w33_pass1828_burnside.json').write_text(json.dumps(res,sort_keys=True,separators=(',',':'))+'\n')
print(json.dumps(res,indent=2))
