#!/usr/bin/env python3
"""Pass4877 — the 120 maximum cuts are not the 120 Steiner triangles as PGSp G-sets.

Pass4867 found exactly 120 maximum cuts of the double-six graph, while the
Steiner layer has exactly 120 maximal triangles.  Equal cardinality is tested,
not promoted.

A maximum cut is constructed from the marked-double-six K6 chart: its duad
part is a Hamilton C6 and exactly two triad completions attain weight 216.
The full PGSp orbit has size 120.  Both maximum cuts and Steiner triangles
therefore have stabilizer order 432.  The stabilizers are nevertheless
nonconjugate: the maximum-cut stabilizer fixes no Steiner triangle and contains
order-8 elements, whereas a Steiner stabilizer fixes one Steiner triangle and
contains no order-8 elements.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,deque
from pathlib import Path
import numpy as np,networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4877_MAXCUT_STEINER_NONBIJECTION.json'

def Q6(v):
    a,c,d,e,f,g=v;return (a*c+d*e+f+f*g+g)&1
def add2(a,b):return tuple(x^y for x,y in zip(a,b))
def polar(a,b):return Q6(add2(a,b))^Q6(a)^Q6(b)
def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def closure(gens,n):
    I=tuple(range(n));S={I};D=deque([I])
    while D:
        a=D.popleft()
        for g in gens:
            z=comp(g,a)
            if z not in S:S.add(z);D.append(z)
    return S
def porder(p):
    seen=set();o=1
    for i in range(len(p)):
        if i in seen:continue
        j=i;l=0
        while j not in seen:seen.add(j);l+=1;j=p[j]
        o=math.lcm(o,l)
    return o

def main()->int:
    vecs=[v for v in itertools.product((0,1),repeat=6) if any(v)]
    sing=[v for v in vecs if Q6(v)==0];nons=[v for v in vecs if Q6(v)==1];si={v:i for i,v in enumerate(sing)}
    trans=[]
    for v in nons:
        p=[]
        for x in sing:p.append(si[add2(x,v) if polar(x,v) else x])
        trans.append(tuple(p))
    gf=[];FULL={tuple(range(27))}
    for g in trans:
        T=closure(gf+[g],27)
        if len(T)>len(FULL):gf.append(g);FULL=T
        if len(FULL)==51840:break
    assert len(FULL)==51840

    qp=[sum(bit<<i for i,bit in enumerate(v)) for v in sing]
    pts=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp})
    lines=[tuple(i for i,P in enumerate(pts) if x in P) for x in qp]
    G=nx.Graph();G.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if set(lines[i])&set(lines[j]):G.add_edge(i,j)
    C6=[frozenset(c) for c in nx.find_cliques(nx.complement(G)) if len(c)==6]
    DS=set()
    for A,B in itertools.combinations(C6,2):
        if A&B:continue
        H=G.subgraph(A|B)
        if len(A|B)==12 and H.number_of_edges()==30 and set(dict(H.degree()).values())=={5} and nx.is_bipartite(H):DS.add(frozenset(A|B))
    DS=sorted(DS,key=lambda x:tuple(sorted(x)));assert len(DS)==36
    H36=nx.Graph();H36.add_nodes_from(range(36))
    for i,j in itertools.combinations(range(36),2):
        if len(DS[i]&DS[j])==6:H36.add_edge(i,j)
    E=sorted(tuple(sorted(e)) for e in H36.edges());assert len(E)==360

    tri=[t for t in itertools.combinations(range(36),3) if all(H36.has_edge(*e) for e in itertools.combinations(t,2))]
    steiner=sorted(t for t in tri if len(DS[t[0]]&DS[t[1]]&DS[t[2]])==0);assert len(steiner)==120
    di={S:i for i,S in enumerate(DS)};sti={t:i for i,t in enumerate(steiner)}
    def p36(g):return tuple(di[frozenset(g[x] for x in S)] for S in DS)
    def stperm(p):return tuple(sti[tuple(sorted(p[i] for i in t))] for t in steiner)

    # marked-double-six chart around vertex 0
    base=0;D0=DS[base];J0=G.subgraph(D0);A0,B0=nx.algorithms.bipartite.sets(J0);A0=sorted(A0);B0=set(B0)
    columns=[]
    for a in A0:
        miss=[b for b in B0 if not G.has_edge(a,b)];assert len(miss)==1;columns.append((a,miss[0]))
    N=sorted(H36.neighbors(base));F=sorted(set(range(36))-{base}-set(N));assert (len(F),len(N))==(15,20)
    def pattern(S):return tuple((1 if a in S else 0)+(2 if b in S else 0) for a,b in columns)
    duad={};triad={}
    for j in F:
        p=pattern(DS[j]&D0);duad[j]=tuple(i for i,z in enumerate(p) if z==3)
    for j in N:
        p=pattern(DS[j]&D0);triad[j]=tuple(i for i,z in enumerate(p) if z==1)
    d_to_v={s:v for v,s in duad.items()}
    cycle=[tuple(sorted(e)) for e in ((0,1),(1,2),(2,3),(3,4),(4,5),(5,0))]
    Dsel={d_to_v[e] for e in cycle};Nlist=sorted(N);npos={v:i for i,v in enumerate(Nlist)}

    # Exactly two triad completions of this C6 reach the maximum 216.
    fixed=sum((a in Dsel)!=(b in Dsel) for a,b in E)
    lin=np.zeros(20,dtype=np.int16)
    for i,nv in enumerate(Nlist):
        for x in H36.neighbors(nv):
            if x==base or x in F:lin[i]+=(-1 if x in Dsel else 1)
    nbr=[]
    for nv in Nlist:
        m=0
        for w in H36.neighbors(nv):
            if w in npos:m|=1<<npos[w]
        nbr.append(m)
    size=1<<20;cutN=np.zeros(size,dtype=np.int16)
    for m in range(1,size):
        lb=m&-m;i=lb.bit_length()-1;prev=m^lb
        cutN[m]=cutN[prev]+10-2*((prev&nbr[i]).bit_count())
    masks=np.arange(size,dtype=np.uint32)
    bits=((masks[:,None]>>np.arange(20,dtype=np.uint32))&1).astype(np.int8)
    weights=fixed+bits@lin+cutN
    completions=np.flatnonzero(weights==216);assert len(completions)==2 and int(weights.max())==216
    m=int(completions[0]);Tsel={Nlist[i] for i in range(20) if (m>>i)&1};Smax=set(Dsel)|Tsel
    def cutword(S):return frozenset(i for i,(a,b) in enumerate(E) if ((a in S)!=(b in S)))
    cw=cutword(Smax);assert len(cw)==216

    # orbit of the cut word under generator actions
    eidx={e:i for i,e in enumerate(E)};edgegens=[]
    for g in gf:
        p=p36(g);edgegens.append(tuple(eidx[tuple(sorted((p[a],p[b])))] for a,b in E))
    O={cw};Dq=deque([cw])
    while Dq:
        x=Dq.popleft()
        for p in edgegens:
            y=frozenset(p[i] for i in x)
            if y not in O:O.add(y);Dq.append(y)
    assert len(O)==120

    # compare full stabilizers inside PGSp
    cut_stab=[];steiner_stab=[]
    for g in FULL:
        p=p36(g);op=stperm(p)
        if cutword({p[x] for x in Smax})==cw:cut_stab.append((p,op))
        if op[0]==0:steiner_stab.append((p,op))
    assert len(cut_stab)==len(steiner_stab)==432
    cut_fixed=[i for i in range(120) if all(op[i]==i for _,op in cut_stab)]
    st_fixed=[i for i in range(120) if all(op[i]==i for _,op in steiner_stab)]
    assert cut_fixed==[] and st_fixed==[0]
    cut_census=Counter(porder(p) for p,_ in cut_stab);st_census=Counter(porder(p) for p,_ in steiner_stab)
    assert cut_census==Counter({1:1,2:45,3:26,4:54,6:90,8:108,12:108})
    assert st_census==Counter({1:1,2:87,3:26,4:72,6:210,12:36})

    out={
      'pass':4877,
      'maximum_cuts':{'count':120,'weight':216,'PGSp_orbit_size':120,'stabilizer_order':432,
        'marked_chart_certificate':'duad state C6 has exactly two triad completions at weight 216',
        'stabilizer_fixed_Steiner_triangles':0,
        'stabilizer_order_census':{str(k):v for k,v in sorted(cut_census.items())}},
      'Steiner_triangles':{'count':120,'PGSp_orbit_size':120,'stabilizer_order':432,
        'stabilizer_fixed_Steiner_triangles':1,
        'stabilizer_order_census':{str(k):v for k,v in sorted(st_census.items())}},
      'nonbijection':{
        'same_cardinality':True,'same_stabilizer_order':True,'stabilizers_conjugate':False,
        'PGSp_equivariant_bijection_exists':False,
        'certificates':['maximum-cut stabilizer fixes no Steiner triangle; every conjugate of a Steiner stabilizer fixes one','maximum-cut stabilizer has 108 order-8 elements; Steiner stabilizer has none','complete element-order censuses differ']},
      'theorem':'The 120 maximum cuts of the double-six graph and the 120 Steiner triangles are distinct transitive PGSp(4,3) G-sets. Both have stabilizer order 432, but the stabilizers are nonconjugate and have different element-order spectra: the maximum-cut stabilizer has 108 elements of order 8 and fixes no Steiner triangle, whereas a Steiner stabilizer has no order-8 elements and fixes exactly its defining triangle. Therefore no PGSp-equivariant bijection exists between the two 120-sets. The equality of counts is not an identification.',
      'boundary':'Finite G-set obstruction. This rules out a canonical PGSp-equivariant identification; it does not rule out arbitrary coordinate-dependent bijections.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
