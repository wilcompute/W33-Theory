#!/usr/bin/env python3
"""Pass 4603 -- the 135 apartment fibers carry an imprimitive 5-class association scheme.

Pass4577 attached to each pair of distinct 12-apartment fibers the number n2 of
cross-fiber apartment pairs sharing exactly two W33 lines. The possible values
are 0,2,6,12,48. This pass treats those five values as five binary relations and
checks every intersection number p_ij^k exhaustively over all 135 points.
They form a symmetric five-class association scheme, with nontrivial valencies
24,12,32,64,2 for n2=0,2,6,12,48 respectively.

The valency-two n2=48 relation is 45 disjoint K3s. Quotient by those 45 triples.
Every pair of quotient triples has one of exactly two cross-patterns:
  6*(n2=12)+3*(n2=6), occurring on 720 pairs;
  6*(n2=0)+3*(n2=2), occurring on 270 pairs.
Joining the first type gives SRG(45,32,22,24), exactly the 45-object parameter
set already present in the repository. This pass proves the quotient from the
apartment-fiber scheme itself; identification with any separately constructed
45-carrier still requires an action intertwiner.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict,deque
from pathlib import Path
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4603_APARTMENT_FIBER_FIVE_CLASS_SCHEME.json'
VALS=[0,2,6,12,48]
def q8(m):return (int(m).bit_count()//4)&1
def srg(adj):
    d={len(x) for x in adj};aa=set();nn=set()
    for i,j in itertools.combinations(range(len(adj)),2):
        c=len(adj[i]&adj[j]);(aa if j in adj[i] else nn).add(c)
    return [len(adj),next(iter(d)),next(iter(aa)),next(iter(nn))]
def main():
    pts,pidx,lines,A,apartments,apmasks,H=geometry();fib=defaultdict(list)
    for ai,ap in enumerate(apartments):
        b=np.zeros(40,dtype=np.uint8);b[list(ap)]=1;y=(A@b)%2
        m=sum(int(z)<<i for i,z in enumerate(y));fib[m].append(ai)
    keys=sorted(fib);assert len(keys)==135 and set(map(len,fib.values()))=={12}
    R=np.zeros((135,135),dtype=np.uint8);idx={v:i+1 for i,v in enumerate(VALS)}
    for i,j in itertools.combinations(range(135),2):
        n2=sum(1 for a in fib[keys[i]] for b in fib[keys[j]] if (apmasks[a]&apmasks[b]).bit_count()==2)
        assert n2 in idx;R[i,j]=R[j,i]=idx[n2]
    vals=[int(np.sum(R[0]==r)) for r in range(6)]
    assert [set(np.sum(R==r,axis=1).tolist()) for r in range(6)]==[{1},{24},{12},{32},{64},{2}]
    # Full association-scheme intersection constants.
    P={}
    for k in range(6):
        pairs=[(x,y) for x in range(135) for y in range(135) if R[x,y]==k]
        mat=[]
        for i in range(6):
            row=[]
            for j in range(6):
                counts={sum(1 for z in range(135) if R[x,z]==i and R[z,y]==j) for x,y in pairs}
                assert len(counts)==1;row.append(next(iter(counts)))
            mat.append(row)
        P[str(k)]=mat
    # Imprimitivity classes from relation n2=48 (relation 5).
    seen=set();classes=[]
    for x in range(135):
        if x in seen:continue
        C={x}|{y for y in range(135) if R[x,y]==5};assert len(C)==3
        assert all(R[a,b]==5 for a,b in itertools.combinations(C,2));classes.append(sorted(C));seen|=C
    assert len(classes)==45 and len(seen)==135
    patterns=Counter();adj=[set() for _ in range(45)]
    for a,b in itertools.combinations(range(45),2):
        c=Counter(int(R[i,j]) for i in classes[a] for j in classes[b]);patterns[tuple(sorted(c.items()))]+=1
        if c==Counter({4:6,3:3}):adj[a].add(b);adj[b].add(a)
    assert patterns==Counter({((3,3),(4,6)):720,((1,6),(2,3)):270})
    qp=srg(adj);assert qp==[45,32,22,24]
    out={'pass':4603,'points':135,'relation_labels':{'0':'diagonal','1':'n2=0','2':'n2=2','3':'n2=6','4':'n2=12','5':'n2=48'},'valencies':[1,24,12,32,64,2],'association_scheme_verified':True,'intersection_matrices_pij_by_relation_k':P,'imprimitive_relation':{'relation':'n2=48','components':45,'component_graph':'K3','component_size':3},'quotient45':{'cross_patterns':{'6*n2=12 + 3*n2=6':720,'6*n2=0 + 3*n2=2':270},'first_pattern_graph_srg':qp},'theorem':'The five apartment-fiber n2 relations form a symmetric 5-class association scheme; its n2=48 imprimitivity quotient is SRG(45,32,22,24).','boundary':'Exact finite association geometry. Equality of quotient SRG parameters with another 45-carrier is not an identification without an explicit equivariant map.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='intersection_matrices_pij_by_relation_k'},indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
