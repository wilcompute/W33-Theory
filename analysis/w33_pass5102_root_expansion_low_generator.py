#!/usr/bin/env python3
"""Pass5102: root-expansion attack via chamber-star moments.

Exact theorem: in W(3,q), two chamber stars at gallery distance d=1..4
meet in q^(4-d) apartments.  Therefore any XOR of m distinct chamber stars
with 1<=m<=q has weight at least q^4.  Equality is attained by m chambers
inside one point/line panel, with weight q^3*m*(q+1-m).

The q=5 executable anchor also enumerates the fixed-base three-star shell and
runs the minimum-local-cut chart propagator.  It does NOT prove d=625 for q=5.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,deque
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5102_ROOT_EXPANSION_LOW_GENERATOR.json'

def flag_distances(G,base=0):
    flags=G['flags']; adj=[set() for _ in flags]
    for i,(p,l) in enumerate(flags):
        for j,(q,m) in enumerate(flags):
            if i!=j and (p==q or l==m): adj[i].add(j)
    d=[-1]*len(flags);d[base]=0;Q=deque([base])
    while Q:
        u=Q.popleft()
        for v in adj[u]:
            if d[v]<0:d[v]=d[u]+1;Q.append(v)
    return d

def mincut_rigidity(G,base=0):
    q=G['q'];charts=G['charts'];nA=len(G['apartments']);ALL=(1<<(q+2))-1
    def states(mask):
        if mask&1:yield -1
        for r in range(q+1):
            if mask&(1<<(r+1)):yield r
    def sel(s,pair):return s>=0 and s in pair
    def poss(mask,pair):return {sel(s,pair) for s in states(mask)}
    def restrict(mask,pair,b):
        z=0
        for s in states(mask):
            if sel(s,pair)==b:z|=1 if s<0 else 1<<(s+1)
        return z
    occ=[[] for _ in range(nA)]
    for c,(_,loc) in enumerate(charts):
        for pair,a in loc.items():occ[a].append((c,pair))
    assert all(len(x)==4 for x in occ)
    def prop(dom):
        changed=True
        while changed:
            changed=False
            for os in occ:
                allowed={False,True}
                for c,pair in os:allowed&=poss(dom[c],pair)
                if not allowed:return None
                if len(allowed)==1:
                    b=next(iter(allowed))
                    for c,pair in os:
                        z=restrict(dom[c],pair,b)
                        if not z:return None
                        if z!=dom[c]:dom[c]=z;changed=True
        return dom
    def solve(dom):
        dom=prop(dom[:])
        if dom is None:return None
        cand=[(m.bit_count(),i) for i,m in enumerate(dom) if m.bit_count()>1]
        if not cand:return dom
        _,c=min(cand)
        for s in states(dom[c]):
            d=dom[:];d[c]=1 if s<0 else 1<<(s+1)
            z=solve(d)
            if z is not None:return z
        return None
    stars=chamber_stars(G);star_index={z:i for i,z in enumerate(stars)};records=[]
    for bits in itertools.product((0,1),repeat=4):
        dom=[ALL]*len(charts)
        for k,(c,pair) in enumerate(occ[base]):dom[c]=1<<(pair[bits[k]]+1)
        z=solve(dom)
        if z is None:records.append({'seed':''.join(map(str,bits)),'status':'UNSAT'})
        else:
            support=0
            for a,os in enumerate(occ):
                vals={sel(next(states(z[c])),pair) for c,pair in os};assert len(vals)==1
                if next(iter(vals)):support|=1<<a
            records.append({'seed':''.join(map(str,bits)),'status':'SAT_CHAMBER_STAR','star':star_index[support],'weight':support.bit_count()})
    return records

def main():
    anchors={}
    for q in (3,4,5):
        G=build_W(q);stars=chamber_stars(G);d=flag_distances(G)
        inter={}
        for dist in range(1,5):
            vals={(stars[0]&stars[j]).bit_count() for j in range(1,len(stars)) if d[j]==dist}
            assert vals=={q**(4-dist)};inter[str(dist)]=q**(4-dist)
        anchors[str(q)]={'pair_intersection_by_gallery_distance':inter,'max_distinct_pair_intersection':q**3}
    G5=build_W(5);s5=chamber_stars(G5);h=Counter()
    for i,j in itertools.combinations(range(1,len(s5)),2):h[(s5[0]^s5[i]^s5[j]).bit_count()]+=1
    assert min(h)==1125 and h[1125]==20
    rigidity=mincut_rigidity(G5)
    assert sum(r['status']=='SAT_CHAMBER_STAR' for r in rigidity)==8 and sum(r['status']=='UNSAT' for r in rigidity)==8
    out={'pass':5102,'status':'THEOREM_WITH_Q5_FRONTIER','theorem':'For 1<=m<=q distinct chamber stars, wt(XOR)>=q^3*m*(q+1-m)>=q^4. Equality is attained by m stars in one point/line panel.',
         'proof_identity':'1_{n odd} >= n-2*C(n,2), summed over apartments, with pair intersections <=q^3.',
         'pair_intersection_law':'two chamber stars at gallery distance d meet in q^(4-d) apartments','anchors':anchors,
         'q5':{'three_star_minimum':1125,'three_star_minimum_fixed_base_representatives':20,'three_star_histogram':dict(sorted(h.items())),'minimum_cut_rigidity':rigidity,'consequence':'Any q5 word below q^4, if one exists, needs chamber-generator leader >=6 and at least one heavier local K6 cut.'},
         'boundary':'This is an all-q low-generator theorem plus exact q5 rigidity anchor, not the all-q/q5 minimum-distance theorem.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
