#!/usr/bin/env python3
"""Exact q=2 parity obstruction to a three-load 16-apartment Levi cycle basis.

For W(3,2), 45 flags, 30 Levi vertices, 90 shortest octagons, cycle
dimension 16. Any 16 octagons require at least one flag to have load >=4,
even though the average lower bound is only ceil(128/45)=3.
A deterministic greedy GF(2) basis attains maximum load 4.
"""
from __future__ import annotations
import itertools
import json
from collections import Counter
from pathlib import Path

def pairing(a,b):
    return (a[0]*b[2]+a[2]*b[0]+a[1]*b[3]+a[3]*b[1])%2

def geometry():
    pts=sorted(v for v in itertools.product(range(2),repeat=4) if any(v))
    ix={v:i for i,v in enumerate(pts)}
    adjacent=[{j for j,v in enumerate(pts) if i!=j and pairing(u,v)==0} for i,u in enumerate(pts)]
    lines=set()
    for i,u in enumerate(pts):
        for j in adjacent[i]:
            if j<=i:continue
            v=pts[j]
            line=tuple(sorted(ix[tuple((a*u[k]+b*v[k])%2 for k in range(4))]
                              for a,b in [(1,0),(0,1),(1,1)]))
            lines.add(line)
    lines=sorted(lines)
    assert len(pts)==len(lines)==15
    pair={}
    for j,L in enumerate(lines):
        for a,b in itertools.combinations(L,2):pair[a,b]=pair[b,a]=j
    flags=sorted((p,j) for j,L in enumerate(lines) for p in L)
    assert len(flags)==45
    index={x:i for i,x in enumerate(flags)}
    cycles={}
    for p in range(15):
        for q in range(p+1,15):
            if q in adjacent[p]:continue
            common=sorted(adjacent[p]&adjacent[q])
            assert len(common)==3
            for a,b in itertools.combinations(common,2):
                walk=[p,15+pair[p,a],a,15+pair[a,q],q,15+pair[q,b],b,15+pair[b,p],p]
                support=tuple(sorted(index[(u,v-15)] if u<15 else index[(v,u-15)]
                                     for u,v in zip(walk,walk[1:])))
                cycles[support]=support
    supports=sorted(cycles)
    assert len(supports)==90 and all(len(s)==8 for s in supports)
    return flags,supports

def select(supports):
    loads=[0]*45
    pivots={}
    picked=[]
    for _ in range(16):
        order=sorted(range(len(supports)),key=lambda j:(
            max(loads[k]+1 for k in supports[j]),
            sum(loads[k] for k in supports[j]),
            sum((loads[k]+1)**2 for k in supports[j]),
            j))
        for j in order:
            mask=sum(1<<k for k in supports[j])
            for b in pivots.values():mask=min(mask,mask^b)
            if mask:
                pivots[mask.bit_length()-1]=mask
                picked.append(j)
                for k in supports[j]:loads[k]+=1
                break
        else:raise AssertionError("rank shortfall")
    return picked,loads

def verify():
    flags,supports=geometry()
    picked,loads=select(supports)
    # Parity obstruction: each Levi vertex has degree 3. Every cycle
    # contributes either 0 or 2 incident edges at each vertex, so the
    # sum of the three corresponding selected-cycle loads is even.
    # Assuming max load 3 forces at least one load<=2 at each of 30
    # vertices (3+3+3 is odd), hence >=15 low-load flags because
    # each flag is incident to two vertices. The total load would
    # then be <= 15*2 + 30*3=120 < 16*8=128.
    vertexflag=[[] for _ in range(30)]
    for j,(p,l) in enumerate(flags):
        vertexflag[p].append(j)
        vertexflag[15+l].append(j)
    assert all(len(v)==3 for v in vertexflag)
    assert all(sum(loads[e] for e in idx)%2==0 for idx in vertexflag)
    assert len(picked)==16 and sum(loads)==128 and max(loads)==4
    assert 15*2+30*3==120<128
    return {
      "status":"PASS_EXACT_Q2_PARITY_SHARP_LOAD_FOUR",
      "Levi_nodes":30,"flags":45,"apartments":90,"cycle_rank":16,
      "apartment_length":8,"selected_appearances":128,
      "naive_average_lower_bound":3,"parity_enhanced_lower_bound":4,
      "attained_maximum_flag_load":max(loads),
      "load_histogram":{str(k):v for k,v in sorted(Counter(loads).items())},
      "GF2_rank":len(picked),"selected_apartment_supports":[list(supports[j]) for j in picked],
      "obstruction":"Even degree-incidence at every trivalent Levi vertex forces >=15 flags with load<=2 if max load<=3. Therefore total load <=120, contradicting 16*8=128.",
      "scope":"Finite symplectic GQ(2,2) theorem; no physical continuum or q-selection."
    }

if __name__=="__main__":
    data=verify()
    out=Path(__file__).resolve().parents[1]/"data"/"2026_11_03_q2_parity_apartment_load.json"
    out.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(data["status"],data["load_histogram"])
