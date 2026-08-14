#!/usr/bin/env python3
"""Pass5089 (outside box): integral oriented-apartment presentation.

The theorem promoted with this certificate is the integral lift of Pass5066:
for a finite generalized quadrangle incidence graph Gamma, the free abelian
group on oriented apartments (orientation reversal = negation), modulo oriented
theta relations A_ij+A_jk-A_ik, is Z_1(Gamma;Z).

Proof mechanism: choose a base vertex and one geodesic to every vertex.  The fan
cycle attached to an oriented edge has reduced length <=8, hence by girth eight
is zero or an oriented apartment.  Summing fans around an integral cycle cancels
all chosen paths.  Changing a distance-four geodesic changes the fan by an
oriented theta relation, so the construction is a well-defined inverse to the
boundary map.  Therefore the quotient is torsion-free.  For W(3,q) its rank is
E-V+1=q^4.

The executable part builds q=2 with arbitrary canonical orientations, determines
the induced +- theta signs from integer apartment boundaries, and Smith-reduces
the relation matrix.  All 74 nonzero Smith invariants are 1, leaving Z^16.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import itertools,json
from pathlib import Path
import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5089_INTEGRAL_APARTMENT_PRESENTATION.json'

def oriented_boundaries(G):
    npnt=len(G['pts']);nf=len(G['flags']);cols=[]
    for edges in G['apt_edges']:
        vadj=defaultdict(list);eid={}
        for f in edges:
            p,l=G['flags'][f];u=p;v=npnt+l;vadj[u].append(v);vadj[v].append(u);eid[frozenset((u,v))]=f
        assert len(vadj)==8 and all(len(x)==2 for x in vadj.values())
        start=min(vadj);nxt=min(vadj[start]);cyc=[start,nxt];prev,cur=start,nxt
        while True:
            z=next(x for x in vadj[cur] if x!=prev)
            if z==start:break
            cyc.append(z);prev,cur=cur,z
        assert len(cyc)==8;v=np.zeros(nf,dtype=np.int8)
        for i,u in enumerate(cyc):
            w=cyc[(i+1)%8];f=eid[frozenset((u,w))];p,l=G['flags'][f]
            v[f]=1 if (u==p and w==npnt+l) else -1
        cols.append(v)
    return np.array(cols,dtype=np.int8).T

def main():
    G=build_W(2);D=oriented_boundaries(G);assert D.shape==(45,90)
    rows=[]
    for _,loc in G['charts']:
        for i,j,k in itertools.combinations(range(3),3):
            ids=[loc[tuple(sorted((i,j)))],loc[tuple(sorted((i,k)))],loc[tuple(sorted((j,k)))]]
            found=[]
            for sb in (1,-1):
                for sc in (1,-1):
                    if np.all(D[:,ids[0]]+sb*D[:,ids[1]]+sc*D[:,ids[2]]==0):found.append((1,sb,sc))
            assert len(found)==1;row=[0]*90
            for a,s in zip(ids,found[0]):row[a]=s
            rows.append(row)
    assert len(rows)==120
    R=sp.Matrix(rows);S=smith_normal_form(R,domain=sp.ZZ)
    diag=[abs(int(S[i,i])) for i in range(min(S.shape)) if S[i,i]!=0]
    assert len(diag)==74 and set(diag)=={1}
    out={'pass':5089,'status':'THEOREM_INTEGRAL_ALL_FINITE_GQ','statement':'Z[oriented apartments]/oriented theta ~= Z_1(Levi;Z)',
         'W3q_rank':'q^4','torsion':'none','oriented_theta':'A_ij + A_jk - A_ik = 0 for three oriented geodesic roots',
         'proof':'base-vertex geodesic fan decomposition over Z; girth 8 makes every reduced fan zero or one oriented apartment; path-choice changes are theta relations',
         'q2_smith_check':{'apartments':90,'relations':120,'relation_rank':74,'nonzero_smith_invariants':dict(Counter(diag)),'quotient_rank':16,'torsion_free':True},
         'boundary':'Integral graph-cycle theorem. It does not by itself prove the binary minimum-distance conjecture.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
