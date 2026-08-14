#!/usr/bin/env python3
"""Pass5075: q=4 local-minimum chart rigidity for the apartment code.

Assume every active opposite-pair chart is a minimum 1|4 cut of K5.
Fix apartment 0 by transitivity.  Its four charts each have two possible
singleton roots, hence 16 seeds.  Exact constraint propagation/DFS shows
8 seeds are satisfiable and they are precisely the 8 chamber stars through
apartment 0; the other 8 are inconsistent.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from analysis.w33_pass5056_q4_theta_apartment_code import build_geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS5075_Q4_LOCAL_CUT_RIGIDITY.json'
ALL=(1<<6)-1  # state bit 0=inactive, bits 1..5=singleton roots 0..4

def states(mask):
    if mask&1: yield -1
    for r in range(5):
        if mask&(1<<(r+1)): yield r

def sel(s,pair): return s>=0 and s in pair

def restrict_bool(mask,pair,b):
    z=0
    for s in states(mask):
        if sel(s,pair)==b: z |= 1 if s<0 else 1<<(s+1)
    return z

def poss(mask,pair): return {sel(s,pair) for s in states(mask)}

def build_charts(G):
    n=len(G['apartments']);occ=[[] for _ in range(n)];chart_apts=[]
    for p,q,common in G['opposite_point_pairs']:
        c=len(chart_apts);loc=[]
        for i,j in itertools.combinations(range(5),2):
            a=G['apt_index_by_points'][frozenset((p,q,common[i],common[j]))]
            loc.append((a,(i,j)));occ[a].append((c,(i,j)))
        chart_apts.append(loc)
    for l,m,common in G['opposite_line_pairs']:
        c=len(chart_apts);loc=[]
        for i,j in itertools.combinations(range(5),2):
            a=G['apt_index_by_lines'][frozenset((l,m,common[i],common[j]))]
            loc.append((a,(i,j)));occ[a].append((c,(i,j)))
        chart_apts.append(loc)
    assert len(chart_apts)==5440 and all(len(x)==10 for x in chart_apts)
    assert all(len(x)==4 for x in occ)
    return chart_apts,occ

def propagate(dom,occ):
    changed=True
    while changed:
        changed=False
        for os in occ:
            allowed={False,True}
            for c,pair in os: allowed &= poss(dom[c],pair)
            if not allowed:return None
            if len(allowed)==1:
                b=next(iter(allowed))
                for c,pair in os:
                    z=restrict_bool(dom[c],pair,b)
                    if not z:return None
                    if z!=dom[c]:dom[c]=z;changed=True
    return dom

def solve(dom,occ,nodes):
    nodes[0]+=1;dom=propagate(dom[:],occ)
    if dom is None:return None
    cand=[(m.bit_count(),i) for i,m in enumerate(dom) if m.bit_count()>1]
    if not cand:return dom
    _,c=min(cand)
    for s in states(dom[c]):
        d=dom[:];d[c]=1 if s<0 else 1<<(s+1)
        z=solve(d,occ,nodes)
        if z is not None:return z
    return None

def support(dom,occ):
    out=set()
    for a,os in enumerate(occ):
        vals={sel(next(states(dom[c])),pair) for c,pair in os}
        assert len(vals)==1
        if next(iter(vals)):out.add(a)
    return frozenset(out)

def main():
    G=build_geometry();chart_apts,occ=build_charts(G);base=0
    base_occ=occ[base];assert len(base_occ)==4
    rows=G['apartment_cycle_rows'];base_flags=[i for i in range(425) if (rows[base]>>i)&1]
    assert len(base_flags)==8
    stars={frozenset(i for i,row in enumerate(rows) if (row>>f)&1):f for f in base_flags}
    assert len(stars)==8 and {len(s) for s in stars}=={256}
    records=[];sat=0
    for bits in itertools.product((0,1),repeat=4):
        dom=[ALL]*len(chart_apts)
        for k,(c,pair) in enumerate(base_occ):
            r=pair[bits[k]];dom[c]=1<<(r+1)
        nodes=[0];z=solve(dom,occ,nodes)
        if z is None:
            records.append({'seed':''.join(map(str,bits)),'status':'UNSAT','nodes':nodes[0]})
        else:
            S=support(z,occ);f=stars.get(S);assert f is not None and len(S)==256
            sat+=1;records.append({'seed':''.join(map(str,bits)),'status':'SAT_CHAMBER_STAR','flag':f,'weight':256,'nodes':nodes[0]})
    assert sat==8 and sum(r['status']=='UNSAT' for r in records)==8
    result={'pass':5075,'status':'PASS','q':4,'assumption':'every active chart is a minimum 1|4 cut','fixed_apartment':0,'seeds':16,'sat_chamber_stars':8,'unsat':8,'base_chamber_stars':8,'records':records,'theorem':'Under the local-minimum-cut assumption, every nonzero codeword containing apartment 0 is one of the eight chamber stars through apartment 0.','remaining_shell':'A hypothetical non-chamber weight-256 word must contain at least one heavier 2|3 chart.','weight256_heavy_chart_parameterization':'If A2=2t counts 2|3 charts, then A1=256-3t and total active charts=256-t.'}
    OUT.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
