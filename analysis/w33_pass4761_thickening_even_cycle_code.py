#!/usr/bin/env python3
"""Pass 4761 -- support-12 thickenings generate the even cycle code of the dual W33 line graph.

For every W33 apartment A, Pass4703 defines the 12-line corner-star thickening
T(A).  Here a thickening is sent to the 28 edges induced by T(A) in the 40-line
intersection graph X (the point graph of the dual GQ(4,3)).  The 1620 resulting
240-bit vectors generate exactly the even-weight hyperplane in Z_1(X;F2).

The theorem is therefore intrinsic:

  C_thick = Z_1(X;F2) cap {even edge weight} = [240,200,4]_2,
  C_thick^perp = Cut(X) + <1_E>                 = [240,40,12]_2.

The dual distance uses the exact edge-connectivity 12 and the SRG least-eigenvalue
max-cut bound: maxcut(X)<=160, so the all-edge cut coset has weight >=80.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4761_THICKENING_EVEN_CYCLE_CODE.json'

def rank2(rows):
    piv={}
    for x in rows:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)

def main()->int:
    pts,pidx,lines,A,apartments,_,_=geometry();A=np.asarray(A,dtype=np.uint8)
    edges=[(i,j) for i,j in itertools.combinations(range(40),2) if A[i,j]];eidx={e:k for k,e in enumerate(edges)}
    assert len(edges)==240 and set(map(int,A.sum(axis=1)))=={12}
    # verify SRG(40,12,2,4)
    adj=[];non=[]
    for i,j in itertools.combinations(range(40),2):
        c=int(np.dot(A[i],A[j]));(adj if A[i,j] else non).append(c)
    assert set(adj)=={2} and set(non)=={4}
    through=[set() for _ in range(40)]
    for li,L in enumerate(lines):
        for p in L:through[p].add(li)
    thick=[];emasks=[]
    for ap in apartments:
        corners=set()
        for i,j in itertools.combinations(ap,2):
            z=lines[i]&lines[j]
            if z:corners|=set(z)
        assert len(corners)==4
        T=set()
        for p in corners:T|=through[p]
        assert len(T)==12;T=frozenset(T);thick.append(T)
        m=0;degs=Counter()
        for i,j in itertools.combinations(sorted(T),2):
            if A[i,j]:
                m|=1<<eidx[(i,j)];degs[i]+=1;degs[j]+=1
        assert m.bit_count()==28 and all(v%2==0 for v in degs.values())
        emasks.append(m)
    assert len(set(thick))==1620 and len(set(emasks))==1620
    colw=Counter()
    for m in emasks:
        x=m
        while x:
            b=x&-x;colw[b.bit_length()-1]+=1;x^=b
    assert set(colw.values())=={189}
    r=rank2(emasks);assert r==200

    X=nx.Graph();X.add_nodes_from(range(40));X.add_edges_from(edges)
    assert nx.is_connected(X) and nx.edge_connectivity(X)==12
    cycle_dim=len(edges)-40+1;assert cycle_dim==201
    # An apartment is a 4-cycle, so even-cycle distance <=4; nonzero even Eulerian
    # edge sets cannot have weight 1,2,3 in a simple graph.
    assert any(len(ap)==4 for ap in apartments)
    primal_d=4
    # C^perp = cut space + <all edges>.  X contains triangles, so 1_E is not a cut.
    cut_dim=39;dual_dim=cut_dim+1;assert dual_dim==40
    # SRG eigenvalues 12,2,-4; Hoffman max-cut bound m/2 - n*lambda_min/4.
    maxcut_bound=240//2-40*(-4)//4;assert maxcut_bound==160
    complement_cut_lower=240-maxcut_bound;assert complement_cut_lower==80
    dual_d=12
    out={'pass':4761,'carrier':{'graph':'W33 line-intersection graph = dual GQ(4,3) point graph','vertices':40,'edges':240,'SRG':[40,12,2,4]},
      'thickening_edge_incidence':{'rows':1620,'columns':240,'row_weight':28,'column_weight':189,'binary_rank':r,'all_rows_eulerian':True,'all_rows_even_weight':True},
      'cycle_space':{'dimension':cycle_dim,'even_cycle_hyperplane_dimension':200,'row_code_equals_even_cycle_hyperplane':True},
      'code':{'parameters':'[240,200,4]_2','dual_parameters':'[240,40,12]_2','dual_description':'Cut(X)+<1_E>','cut_space_dimension':cut_dim,'edge_connectivity':12,'all_edge_coset_min_lower_bound':complement_cut_lower},
      'theorem':'The 1620 support-12 apartment thickenings, read as their 28 induced edges in the dual W33 line graph, generate exactly the even-weight cycle hyperplane [240,200,4]_2. Its dual is Cut(X)+<1_E>, a [240,40,12]_2 code.',
      'boundary':'Exact binary graph-code theorem on the dual line graph. This coordinate carrier is not identified with the point-edge CSS carrier by dimension or length alone.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
