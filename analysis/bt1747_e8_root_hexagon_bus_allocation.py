#!/usr/bin/env python3
"""BT1747: root-level E8 hexagon allocation into atlas buses.

This upgrades BT1742 from count allocation to a reproducible root-level allocation.
The E8 roots are partitioned by C^5 into 40 Coxeter hexagons.  The 40 hexagons
are assigned whole-hexagon-wise into five 48-root buses: one 48-root atlas bus
and four 48-root framed-flag buses, totaling 48 + 192 = 240.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1747_e8_root_hexagon_bus_allocation.json'
def e8_roots_doubled():
    roots=[]
    for i,j in itertools.combinations(range(8),2):
        for si in (2,-2):
            for sj in (2,-2):
                v=[0]*8; v[i]=si; v[j]=sj; roots.append(tuple(v))
    for signs in itertools.product((1,-1), repeat=8):
        if signs.count(-1)%2==0: roots.append(tuple(signs))
    return roots
def main():
    roots=e8_roots_doubled(); R=set(roots); idx={r:i for i,r in enumerate(roots)}
    def dot(v,a): return sum(x*y for x,y in zip(v,a))//4
    def basis(i,s=2):
        v=[0]*8; v[i]=s; return tuple(v)
    def sub(a,b): return tuple(x-y for x,y in zip(a,b))
    def add(a,b): return tuple(x+y for x,y in zip(a,b))
    A=[(1,-1,-1,-1,-1,-1,-1,1), add(basis(0),basis(1)), sub(basis(1),basis(0)), sub(basis(2),basis(1)), sub(basis(3),basis(2)), sub(basis(4),basis(3)), sub(basis(5),basis(4)), sub(basis(6),basis(5))]
    def refl(alpha):
        def s(v):
            c=dot(v,alpha); return tuple(v[i]-c*alpha[i] for i in range(8))
        return s
    S=[refl(a) for a in A]
    assert all(all(s(r) in R for r in roots) for s in S)
    def cox(v):
        for s in S: v=s(v)
        return v
    perm=[idx[cox(r)] for r in roots]
    def power(p,k):
        out=list(range(len(p)))
        for _ in range(k): out=[p[out[i]] for i in range(len(p))]
        return out
    c5=power(perm,5)
    seen=set(); hexagons=[]
    for i in range(240):
        if i in seen: continue
        orb=[]; j=i
        while j not in seen:
            seen.add(j); orb.append(j); j=c5[j]
        hexagons.append(orb)
    hexagons=sorted(hexagons,key=lambda o:min(o))
    buses={f'grade_bus_{g}':[] for g in range(5)}
    for h,orb in enumerate(hexagons):
        buses[f'grade_bus_{h//8}'].extend(orb)
    atlas_bus='grade_bus_0'
    framed=[f'grade_bus_{g}' for g in range(1,5)]
    checks={
      'roots_240':len(roots)==240,
      'hexagons_40_size6':len(hexagons)==40 and all(len(o)==6 for o in hexagons),
      'five_buses_48_each':all(len(v)==48 for v in buses.values()),
      'whole_hexagons_per_bus_8':all(len(buses[f'grade_bus_{g}'])==8*6 for g in range(5)),
      'atlas_48_framed_192':len(buses[atlas_bus])==48 and sum(len(buses[b]) for b in framed)==192,
      'partition_240':len(set().union(*[set(v) for v in buses.values()]))==240,
    }
    payload={'theorem':'BT1747 E8 Root-Hexagon Bus Allocation','verified':all(checks.values()),'summary':'The 240 E8 roots are partitioned into 40 Coxeter C^5 hexagons of size 6. Assigning eight whole hexagons to each of five Clifford-grade buses gives five 48-root buses. One bus is the local atlas incidence bus (48); the other four are framed flag buses (192). This realizes 240 = 48 + 192 at root level while preserving whole Witting/Eisenstein hexagons.', 'hexagon_count':len(hexagons),'roots_per_hexagon':6,'bus_sizes':{k:len(v) for k,v in buses.items()},'atlas_bus':atlas_bus,'framed_flag_buses':framed,'hexagon_to_bus':{str(h):f'grade_bus_{h//8}' for h in range(40)},'root_index_buses':buses,'checks':checks,'boundary':'The bus assignment is canonical by sorted orbit order, not yet canonical under the full E8 Weyl group. It is a root-level allocation, not a unique physical identification.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'bus_sizes':payload['bus_sizes']},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
