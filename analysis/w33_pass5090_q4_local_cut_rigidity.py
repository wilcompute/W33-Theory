#!/usr/bin/env python3
"""Pass5090: exact q=4 rigidity in the all-local-minimum chart sector."""
from __future__ import annotations
import itertools,json
from pathlib import Path
from analysis.w33_pass5056_q4_theta_apartment_code import build_geometry
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS5090_Q4_LOCAL_CUT_RIGIDITY.json'
ALL=(1<<6)-1

def states(mask):
    if mask&1:yield -1
    for r in range(5):
        if mask&(1<<(r+1)):yield r

def selected(s,pair):return s>=0 and s in pair

def poss(mask,pair):return {selected(s,pair) for s in states(mask)}
def restrict_bool(mask,pair,b):
    z=0
    for s in states(mask):
        if selected(s,pair)==b:z|=1 if s<0 else 1<<(s+1)
    return z

def build_charts(G):
    occ=[[] for _ in G['apartments']];ca=[]
    for p,q,common in G['opposite_point_pairs']:
        c=len(ca);loc=[]
        for i,j in itertools.combinations(range(5),2):
            a=G['apt_index_by_points'][frozenset((p,q,common[i],common[j]))];loc.append(a);occ[a].append((c,(i,j)))
        ca.append(loc)
    for l,m,common in G['opposite_line_pairs']:
        c=len(ca);loc=[]
        for i,j in itertools.combinations(range(5),2):
            a=G['apt_index_by_lines'][frozenset((l,m,common[i],common[j]))];loc.append(a);occ[a].append((c,(i,j)))
        ca.append(loc)
    assert len(ca)==5440 and all(len(x)==10 for x in ca) and all(len(x)==4 for x in occ)
    return ca,occ

def propagate(dom,occ,ca):
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
                    z=restrict_bool(dom[c],pair,b)
                    if not z:return None
                    if z!=dom[c]:dom[c]=z;changed=True
    return dom

def solve(dom,occ,ca,nodes):
    nodes[0]+=1;dom=propagate(dom[:],occ,ca)
    if dom is None:return None
    cand=[(m.bit_count(),i) for i,m in enumerate(dom) if m.bit_count()>1]
    if not cand:return dom
    _,c=min(cand)
    for s in states(dom[c]):
        d=dom[:];d[c]=1 if s<0 else 1<<(s+1)
        z=solve(d,occ,ca,nodes)
        if z is not None:return z
    return None

def support(dom,occ):
    S=set()
    for a,os in enumerate(occ):
        vv={selected(next(states(dom[c])),pair) for c,pair in os};assert len(vv)==1
        if next(iter(vv)):S.add(a)
    return frozenset(S)

def main():
    G=build_geometry();ca,occ=build_charts(G);base=0;base_occ=occ[base];assert len(base_occ)==4
    rows=G['apartment_cycle_rows'];flags=[f for f in range(425) if (rows[base]>>f)&1];assert len(flags)==8
    stars={frozenset(i for i,r in enumerate(rows) if (r>>f)&1):f for f in flags};assert len(stars)==8
    rec=[]
    for bits in itertools.product((0,1),repeat=4):
        dom=[ALL]*len(ca)
        for k,(c,pair) in enumerate(base_occ):dom[c]=1<<(pair[bits[k]]+1)
        nodes=[0];z=solve(dom,occ,ca,nodes)
        if z is None:rec.append({'seed':''.join(map(str,bits)),'status':'UNSAT','nodes':nodes[0]})
        else:
            S=support(z,occ);assert S in stars and len(S)==256
            rec.append({'seed':''.join(map(str,bits)),'status':'SAT_CHAMBER_STAR','flag':stars[S],'nodes':nodes[0]})
    assert sum(r['status']=='SAT_CHAMBER_STAR' for r in rec)==8 and sum(r['status']=='UNSAT' for r in rec)==8
    out={'pass':5090,'status':'PASS','seeds':16,'sat':8,'unsat':8,'theorem':'Under the all-local-minimum 1|4-cut assumption, every word containing apartment 0 is one of the eight chamber stars through it.','remaining':'Any non-chamber weight-256 word must contain a 2|3 chart.','records':rec}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
