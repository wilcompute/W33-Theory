#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1793_payne_bt1788_alignment_matrix.json'
F=range(3)
def rep(v):
    v=tuple(x%3 for x in v)
    for x in v:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%3 for y in v)
    raise ValueError('zero')
def form(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%3
def projective_points(): return sorted({rep(v) for v in product(F, repeat=4) if any(v)})
def projective_line(u,v): return frozenset(rep(tuple((a*u[i]+b*v[i])%3 for i in range(4))) for a,b in product(F,F) if a or b)
def shell_coord(v):
    if v[2]==2: v=tuple((2*x)%3 for x in v)
    assert v[2]==1
    return (v[0],v[1],v[3])
def h27_support():
    P=projective_points(); anchor=rep((1,0,0,0)); shell=set(p for p in P if p!=anchor and form(anchor,p)!=0)
    lines=sorted({projective_line(u,v) for u,v in combinations(P,2) if form(u,v)==0}, key=lambda L: sorted(L))
    old=[]
    for L in lines:
        if anchor in L: continue
        sh=tuple(sorted(shell_coord(x) for x in L if x in shell)); assert len(sh)==3
        old.append(sh)
    new=[tuple((a,b,d) for a in F) for b,d in product(F,F)]
    return [tuple(sorted(L)) for L in old+new]
def affine_maps():
    mats=[]
    for a,b,c,d in product(F, repeat=4):
        if (a*d-b*c)%3: mats.append(((a,b),(c,d)))
    out=[]
    for M in mats:
        for t in product(F, repeat=2):
            out.append((M,t,lambda x,y,M=M,t=t: ((M[0][0]*x+M[0][1]*y+t[0])%3,(M[1][0]*x+M[1][1]*y+t[1])%3)))
    return out
def table_triple(i,j,s,f0,f1,f2):
    b0,d0=f0(i,j); b1,d1=f1(i,s); b2,d2=f2(j,s)
    return tuple(sorted([(0,b0,d0),(1,b1,d1),(2,b2,d2)]))
def main():
    support=h27_support(); support_set=set(support)
    identity=lambda x,y:(x%3,y%3)
    def eval_pair(f1,f2):
        non=con=cnt=0; rows=[]
        for i,j,s in product(F,F,F):
            tri=table_triple(i,j,s,identity,f1,f2)
            if tri in support_set:
                c=(s==(j-i)%3); cnt+=1; con+=int(c); non+=int(not c)
                rows.append({'i':i,'j':j,'s':s,'concurrent':c,'triple':[list(p) for p in tri]})
        return non,cnt,con,rows
    default_non,default_cnt,default_con,default_rows=eval_pair(identity,identity)
    best=None; best_records=[]; maps=affine_maps()
    for idx1,(M1,t1,f1) in enumerate(maps):
        for idx2,(M2,t2,f2) in enumerate(maps):
            non,cnt,con,rows=eval_pair(f1,f2)
            key=(non,cnt,-con)
            rec=(idx1,idx2,M1,t1,M2,t2,non,cnt,con,rows)
            if best is None or key>best:
                best=key; best_records=[rec]
            elif key==best:
                best_records.append(rec)
    idx1,idx2,M1,t1,M2,t2,non,cnt,con,rows=best_records[0]
    payload={
        'bt':'BT1793',
        'title':'Payne-BT1788 alignment matrix',
        'table_model':'BT1788 table (Ri,Cj,Ds) maps to three pair-frontier points RC(i,j), RD(i,s), CD(j,s); concurrent iff s=(j-i) mod 3.',
        'h27_target':'45 Payne/H27 support triples = 36 old W33 shell triples + 9 central fibres.',
        'default_alignment':{'nonconcurrent_hits':default_non,'total_support_hits':default_cnt,'concurrent_hits':default_con,'support_hit_rows':default_rows},
        'best_RC_fixed_affine_alignment':{'search_space':'RC identity; RD and CD independently affine GL(2,3) semidirect F3^2; 432^2 cases','max_nonconcurrent_hits':non,'total_support_hits':cnt,'concurrent_hits':con,'number_of_tied_optima':len(best_records),'RD_matrix':M1,'RD_translation':t1,'CD_matrix':M2,'CD_translation':t2,'support_hit_rows':rows},
        'conclusion':'The 18 nonconcurrent ternary tables are not merely 18 renamed H27 support lines. Naively only 2/18 nonconcurrent table triples land on the H27 support; even the best RC-fixed affine pair-frontier alignment lands on only 12/18. The missing BT1781 materialization is a real projection/transport map, not a coordinate relabeling.'
    }
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'default':[default_non,default_cnt,default_con],'best_RC_fixed':[non,cnt,con],'tied_optima':len(best_records)},indent=2,sort_keys=True))
if __name__=='__main__': main()
