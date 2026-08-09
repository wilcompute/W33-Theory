#!/usr/bin/env python3
"""Pass 4573 -- C8-alone apartment selection is not universal across thick GQs.

Pass 4548 proved a striking W33 statement: in GQ(3,3), the primitive length-eight
degree-four Walsh coefficient 712 occurs on exactly the 1620 apartments. This
pass tests whether that coefficient-selector phenomenon is a theorem of all
thick generalized quadrangles.

It is not. Exact nonbacktracking trace arithmetic gives a minimal counterexample:
for W(3,2)=GQ(2,2), every one of the 90 apartments has primitive C8 degree-four
coefficient 36, but so do 60 induced K_{1,3} supports in the line graph. Thus the
coefficient value alone does not select apartments.

The collision is not an automatic s=2 effect. In Q^-(5,2)=GQ(2,4), a certified
apartment has coefficient 60 while a K_{1,3} support has coefficient 36.

The universal statement that survives is Pass4523: primitive C6 degree two
reconstructs line adjacency for every thick GQ, after which apartments are the
induced line-graph C4s. W33's C8-alone selector is therefore a stronger special
sufficiency theorem, not a universal building axiom.
"""
from __future__ import annotations

import itertools,json
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4573_GENERAL_GQ_C8_SELECTOR_OBSTRUCTION.json'


def rankless_norm2(v):
    return tuple(int(x)&1 for x in v)


def symplectic_gq22():
    pts=[tuple(map(int,f'{x:04b}')) for x in range(1,16)]
    def B(x,y):return (x[0]*y[1]+x[1]*y[0]+x[2]*y[3]+x[3]*y[2])&1
    lines=set()
    for i,x in enumerate(pts):
        for y in pts[i+1:]:
            if B(x,y):continue
            z=tuple(a^b for a,b in zip(x,y));lines.add(frozenset((i,pts.index(z),pts.index(y))))
    return pts,sorted(lines,key=lambda L:sorted(L))


def qminus_gq24():
    vec=[tuple((x>>i)&1 for i in range(6)) for x in range(1,64)]
    def q(x):return (x[0]*x[1]+x[2]*x[3]+x[4]+x[4]*x[5]+x[5])&1
    pts=[x for x in vec if q(x)==0];idx={x:i for i,x in enumerate(pts)}
    def B(x,y):return q(tuple(a^b for a,b in zip(x,y)))^q(x)^q(y)
    lines=set()
    for i,x in enumerate(pts):
        for j in range(i+1,len(pts)):
            y=pts[j]
            if B(x,y):continue
            z=tuple(a^b for a,b in zip(x,y))
            if z in idx:lines.add(frozenset((i,j,idx[z])))
    return pts,sorted(lines,key=lambda L:sorted(L))


def point_graph(pts,lines):
    n=len(pts);adj=[set() for _ in range(n)];edge_line={}
    for li,L in enumerate(lines):
        for u,v in itertools.combinations(sorted(L),2):
            adj[u].add(v);adj[v].add(u);edge_line[(min(u,v),max(u,v))]=li
    return adj,edge_line


def line_graph(lines):
    n=len(lines);A=[[0]*n for _ in range(n)]
    for i,j in itertools.combinations(range(n),2):
        if lines[i]&lines[j]:A[i][j]=A[j][i]=1
    return A


def apartments(lines):
    A=line_graph(lines);out=[]
    for S in itertools.combinations(range(len(lines)),4):
        deg=[sum(A[i][j] for j in S if j!=i) for i in S]
        if sorted(deg)==[2,2,2,2]:out.append(S)
    return out


def stars(lines):
    A=line_graph(lines);out=[]
    for S in itertools.combinations(range(len(lines)),4):
        deg=sorted(sum(A[i][j] for j in S if j!=i) for i in S)
        if deg==[1,1,1,3]:out.append(S)
    return out


def nb_tables(pts,lines):
    adj,edge_line=point_graph(pts,lines);dedges=[];didx={}
    for u in range(len(pts)):
        for v in sorted(adj[u]):didx[(u,v)]=len(dedges);dedges.append((u,v))
    state_line=[edge_line[(min(u,v),max(u,v))] for u,v in dedges]
    nxt=[[] for _ in dedges]
    for i,(u,v) in enumerate(dedges):
        for w in adj[v]:
            if w!=u:
                j=didx[(v,w)];nxt[i].append((j,state_line[j]))
    rev=[[] for _ in dedges]
    for i,L in enumerate(nxt):
        for j,_ in L:rev[j].append((i,state_line[j]))
    return dedges,nxt,rev


def half(start,steps,trans):
    cur={(start,0):1}
    for _ in range(steps):
        z=defaultdict(int)
        for (st,m),c in cur.items():
            for j,li in trans[st]:z[(j,m^(1<<li))]+=c
        cur=z
    by=defaultdict(Counter)
    for (st,m),c in cur.items():by[st][m]+=c
    return by


def prepare_c8(pts,lines):
    dedges,nxt,rev=nb_tables(pts,lines);tables=[]
    for s in range(len(dedges)):tables.append((half(s,4,nxt),half(s,4,rev)))
    return tables


def primitive_c8_coeff(tables,target_mask):
    total=0
    for f,r in tables:
        for st in set(f)&set(r):
            rr=r[st]
            for m,c in f[st].items():total+=c*rr.get(m^target_mask,0)
    assert total%8==0
    return total//8


def mask(S):return sum(1<<i for i in S)


def main()->int:
    p22,l22=symplectic_gq22();assert (len(p22),len(l22))==(15,15)
    ap22=apartments(l22);st22=stars(l22);assert (len(ap22),len(st22))==(90,60)
    t22=prepare_c8(p22,l22)
    ca={primitive_c8_coeff(t22,mask(S)) for S in ap22}
    cs={primitive_c8_coeff(t22,mask(S)) for S in st22}
    assert ca=={36} and cs=={36}

    p24,l24=qminus_gq24();assert (len(p24),len(l24))==(27,45)
    ap24=apartments(l24);st24=stars(l24);assert ap24 and st24
    t24=prepare_c8(p24,l24)
    a0=primitive_c8_coeff(t24,mask(ap24[0]));s0=primitive_c8_coeff(t24,mask(st24[0]))
    assert (a0,s0)==(60,36)

    out={
      'pass':4573,
      'universal_C8_coefficient_selector':False,
      'counterexample':{
        'geometry':'W(3,2)=GQ(2,2)','points':15,'lines':15,'apartments':90,'induced_K13_supports':60,
        'primitive_C8_degree4_apartment_coefficient':36,
        'primitive_C8_degree4_K13_coefficient':36,
        'conclusion':'coefficient 36 contains both all apartments and 60 non-apartment stars'},
      'control':{
        'geometry':'Q^-(5,2)=GQ(2,4)','points':27,'lines':45,
        'sample_apartment_coefficient':60,'sample_K13_coefficient':36,
        'conclusion':'the GQ(2,2) collision is not forced merely by s=2'},
      'W33_special_case':{'geometry':'GQ(3,3)','apartment_coefficient':712,'apartments':1620,
                          'status':'Pass4548 exact: coefficient 712 singles out apartments'},
      'universal_replacement':'Pass4523 C6 degree-two reconstructs the line graph for every thick GQ; apartments are then its induced C4 building cycles',
      'boundary':'This refutes C8-coefficient-alone universality. It does not classify all (s,t) for which a unique C8 apartment coefficient exists.'}
    OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
