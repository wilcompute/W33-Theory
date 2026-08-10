#!/usr/bin/env python3
"""Pass 4808 bonkers — first nonlocal logical sector has quotient lift distance six.

Pass4807 gives the canonical quotient
    C^perp / L  ~= H_1(Levi(GQ(4,2)); F3),
where L is the direct sum of the 27 local punctured ternary Golay G10 blocks.
This producer equips the quotient with the minimum triangle-lift metric.

For one K5 line, the 5x10 point/triangle incidence map has 81 possible
sum-zero syndromes. Exhaustion gives minimum local preimage costs
    cost 0: 1 state, cost 1: 20 states, cost 2: 60 states.
A global quotient vector is a choice of one local syndrome per GQ line whose
point sums cancel. An exact symmetry-broken MILP proves that no nonzero quotient
class has lift weight <=5. A weight-6 construction is supplied by every induced
K3,3 in the 27-line intersection graph: put opposite signs on the two parts and,
on each of the six lines, choose the triangle formed by its three intersections
with the opposite part.

The 27-line graph has exactly 360 induced K3,3 subgraphs. These furnish 360
canonical projective weight-6 witnesses. They are not asserted to exhaust the
full weight-6 quotient shell.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
import networkx as nx
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy import sparse
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4808_HOMOLOGY_DISTANCE_K33.json'

def Qm(v):
    x1,x2,x3,x4,x5,x6=v
    return (x1*x2+x3*x4+x5+x5*x6+x6)&1

def bits(x): return tuple((x>>i)&1 for i in range(6))

def build_geometry():
    qp=[x for x in range(1,64) if Qm(bits(x))==0];assert len(qp)==27
    ql=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if (a^b) in qp});assert len(ql)==45
    lines=[tuple(i for i,Q in enumerate(ql) if p in Q) for p in qp];assert len(set(lines))==27 and {len(L) for L in lines}=={5}
    inc={p:tuple(i for i,L in enumerate(lines) if p in L) for p in range(45)};assert {len(v) for v in inc.values()}=={3}
    G=nx.Graph();G.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if len(set(lines[i])&set(lines[j]))==1:G.add_edge(i,j)
    assert set(dict(G.degree()).values())=={10}
    return lines,inc,G

def local_states():
    triples=list(itertools.combinations(range(5),3));M=np.zeros((5,10),dtype=int)
    for j,T in enumerate(triples):M[list(T),j]=1
    best={};rep={}
    for x in itertools.product(range(3),repeat=10):
        a=np.array(x,dtype=int);z=tuple(int(v) for v in (M@a)%3);w=sum(bool(v) for v in x)
        if z not in best or w<best[z]:best[z]=w;rep[z]=tuple(x)
    assert len(best)==81 and Counter(best.values())==Counter({0:1,1:20,2:60})
    return triples,best,rep

def count_induced_k33(G):
    found=set()
    for S in itertools.combinations(range(27),6):
        H=G.subgraph(S)
        if H.number_of_edges()!=9 or set(dict(H.degree()).values())!={3} or not nx.is_bipartite(H):continue
        A,B=nx.algorithms.bipartite.sets(H)
        if len(A)==len(B)==3:
            found.add(tuple(sorted(S)))
    return sorted(found)

def k33_witness(lines,G,S):
    H=G.subgraph(S);A,B=nx.algorithms.bipartite.sets(H);A=set(A);B=set(B)
    assert len(A)==len(B)==3
    support=[];point_sum=Counter()
    for ell in sorted(S):
        opp=B if ell in A else A;sgn=1 if ell in A else 2
        pts=[]
        for m in opp:
            hit=set(lines[ell])&set(lines[m]);assert len(hit)==1;pts.extend(hit)
        assert len(set(pts))==3
        T=tuple(sorted(set(pts)));support.append((ell,sgn,T))
        for p in T:point_sum[p]=(point_sum[p]+sgn)%3
    assert all(v%3==0 for v in point_sum.values())
    assert len(support)==6
    return sorted(A),sorted(B),support

def no_weight_le5_milp(lines,best):
    # A nonzero quotient class of total lift cost <=5 either contains a cost-1
    # line state, or consists only of cost-2 states. The latter has weight 2 or 4;
    # Pass4802 proves every dual word of weight 4 is local (in L), while dual
    # distance is 4, so it cannot represent a nonzero quotient. We therefore fix
    # one cost-1 state by line/triangle transitivity and global scalar.
    states=sorted(best);cost=[best[z] for z in states];ns=len(states);zero=states.index((0,0,0,0,0))
    target=(0,0,1,1,1);assert target in best and best[target]==1
    # variables y_{ell,state} binary, plus integer q_p for mod-3 point equations.
    nY=27*ns;nQ=45;n=nY+nQ
    c=np.zeros(n);c[:nY]=np.repeat(cost,27).reshape(ns,27).T.ravel() if False else np.tile(np.array(cost,dtype=float),27)
    rows=[];lbs=[];ubs=[]
    # exactly one state per line
    for ell in range(27):
        row={ell*ns+s:1.0 for s in range(ns)};rows.append(row);lbs.append(1);ubs.append(1)
    # point conservation sum incident line-coordinate = 3 q_p
    pos={ell:{p:i for i,p in enumerate(lines[ell])} for ell in range(27)}
    for p in range(45):
        row={}
        for ell in range(27):
            if p not in pos[ell]:continue
            k=pos[ell][p]
            for s,z in enumerate(states):
                if z[k]:row[ell*ns+s]=float(z[k])
        row[nY+p]=-3.0;rows.append(row);lbs.append(0);ubs.append(0)
    # total cost <=5
    row={ell*ns+s:float(cost[s]) for ell in range(27) for s in range(ns) if cost[s]};rows.append(row);lbs.append(-np.inf);ubs.append(5)
    # symmetry break: line 0 is the chosen cost1 line and its local state is target.
    t=states.index(target);row={0*ns+t:1.0};rows.append(row);lbs.append(1);ubs.append(1)
    rr=[];cc=[];dd=[]
    for r,row in enumerate(rows):
        for j,v in row.items():rr.append(r);cc.append(j);dd.append(v)
    A=sparse.coo_matrix((dd,(rr,cc)),shape=(len(rows),n)).tocsr()
    lb=np.zeros(n);ub=np.ones(n);lb[nY:]=-10;ub[nY:]=10
    integ=np.ones(n)
    R=milp(c,integrality=integ,bounds=Bounds(lb,ub),constraints=LinearConstraint(A,np.array(lbs),np.array(ubs)),options={'presolve':True,'time_limit':300})
    assert R.status==2, (R.status,R.message)
    return {'status':int(R.status),'message':str(R.message),'symmetry_break':'line 0 carries normalized cost-1 state (0,0,1,1,1)','cost_bound':5}

def main()->int:
    lines,inc,G=build_geometry();triples,best,rep=local_states()
    K=count_induced_k33(G);assert len(K)==360
    A,B,wit=k33_witness(lines,G,K[0])
    proof=no_weight_le5_milp(lines,best)
    out={'pass':4808,'quotient':'C^perp / (direct_sum_27 G10) ~= H_1(Levi(GQ(4,2));F3)',
      'local_syndrome_state_count':81,'local_minimum_cost_distribution':{'0':1,'1':20,'2':60},
      'quotient_minimum_lift_weight':6,'no_nonzero_quotient_weight_le5':True,'milp_certificate':proof,
      'induced_K33_count':360,'projective_K33_witnesses':360,
      'representative_K33':{'left':A,'right':B,'signed_line_triangles':[(ell,sgn,list(T)) for ell,sgn,T in wit]},
      'theorem':'The first nonlocal/homological logical sector of the [[270,182,4]]_3 triangle CSS code appears at minimum triangle-lift weight 6. The overall distance-4 logicals are entirely local punctured-Golay operators. Every induced K3,3 in the 27-line intersection graph supplies a canonical projective weight-6 homology witness; there are 360 such K3,3 subgraphs.',
      'boundary':'The 360 K3,3 witnesses are a certified canonical family, not claimed to exhaust all projective weight-6 quotient classes. The distance is the minimum weight of a triangle-coordinate lift modulo the local Golay sum L.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
