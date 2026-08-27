#!/usr/bin/env python3
"""Pass10709-10716: the C13 chain intertwiner does not extend to the order-3 normalizer complement.

Use the explicit Wilson F4^6 matrices from Pass10477.  Let n have order 6 and
normalize g8 by g8^n=g8^4.  Then h=n^2 has order3.

On V2=F4^6, h has vector-set orbit structure 1^16 3^1360, hence the fixed
space of the permutation module F2[V2] has dimension 1376.

On the H(4) Levi graph, h has:
  465 point orbits = 1^15 3^450,
  463 line orbits  = 1^12 3^451,
  2295 flag/edge orbits = 1^30 3^2265.
The quotient Levi graph is connected, so beta1=2295-465-463+1=1368.
Because char(F2)=2 does not divide 3, taking C3-invariants is exact (Maschke),
thus dim H1^<h> = 1368.

The fixed dimensions 1376 and1368 differ, proving that the explicit C13-module
isomorphism/chain blueprint cannot extend to C13:C3, hence not to C13:C6.
"""
from __future__ import annotations
from collections import Counter,deque
import itertools,json
from pathlib import Path
import numpy as np
import w33_pass10477_10484_h4_normalizer_27state_quotient as Q
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10709_10716_NORMALIZER_CHAIN_EXTENSION_NOGO.json'

def orbits(p):
    seen=[False]*len(p);out=[]
    for s in range(len(p)):
      if seen[s]:continue
      C=[];x=s
      while not seen[x]:seen[x]=True;C.append(x);x=int(p[x])
      out.append(C)
    return out

def main():
    g1=np.array([[3,0,0,1,2,0],[3,3,2,0,1,2],[2,0,0,0,0,2],[1,2,2,3,2,3],[2,0,1,2,0,0],[1,2,2,1,3,0]],dtype=np.uint8)
    g2=np.array([[3,1,2,2,1,1],[2,1,1,3,0,0],[2,3,1,0,3,0],[3,3,1,1,1,1],[3,2,1,1,2,1],[3,2,2,0,2,3]],dtype=np.uint8)
    g3=Q.pw(Q.mm(Q.pw(g1,4),g2),4)
    X=Q.pw(Q.mm(Q.mm(Q.mm(g1,g2),g1),Q.pw(g2,2)),3);g4=Q.conj(X,Q.pw(g2,4))
    A=Q.pw(Q.mm(Q.pw(Q.mm(g3,g4),3),g4),3)
    B=Q.pw(Q.mm(g3,g4),4);B=Q.mm(B,g4);B=Q.mm(B,g3);B=Q.mm(B,g4);B=Q.mm(B,Q.pw(Q.mm(g3,Q.pw(g4,2)),2))
    g5=Q.mm(Q.mm(A,Q.pw(B,3)),Q.invm(A))
    Y=Q.mm(Q.mm(Q.mm(g3,g4),g3),Q.pw(g4,2))
    g6=Q.mm(Q.pw(Y,-2),Q.mm(Q.pw(Q.mm(Q.mm(g3,g4),Q.pw(Y,2)),5),Q.pw(Y,2)))
    g7=Q.conj(g6,Q.mm(g5,Q.pw(g6,2)));g8=Q.mm(Q.mm(Q.mm(g5,g7),g5),Q.pw(g7,2));n=Q.mm(g5,g7)
    h=Q.pw(n,2);assert Q.order(g8)==13 and Q.order(n)==6 and Q.order(h)==3

    vecs=[tuple(v) for v in itertools.product(range(4),repeat=6)];vi={v:i for i,v in enumerate(vecs)}
    vp=np.array([vi[tuple(map(int,Q.mv(h,v)))] for v in vecs],dtype=np.int32)
    vo=orbits(vp);assert Counter(map(len,vo))==Counter({3:1360,1:16});vfix=len(vo);assert vfix==1376

    pts=[];seen=set()
    for v in vecs[1:]:
      p=Q.norm(v)
      if p not in seen:seen.add(p);pts.append(p)
    pi={p:i for i,p in enumerate(pts)};assert len(pts)==1365
    def pp(A):return np.array([pi[Q.norm(Q.mv(A,p))] for p in pts],dtype=np.int32)
    pg1,pg2,ph=map(pp,(g1,g2,h))
    po=orbits(ph);assert Counter(map(len,po))==Counter({3:450,1:15}) and len(po)==465

    seed=tuple(sorted(pi[p] for p in [(0,0,0,0,0,1),(0,1,3,0,0,0),(0,1,3,0,0,1),(0,1,3,0,0,2),(0,1,3,0,0,3)]))
    lines={seed};D=deque([seed])
    while D:
      L=D.popleft()
      for p in (pg1,pg2):
        M=tuple(sorted(int(p[x]) for x in L))
        if M not in lines:lines.add(M);D.append(M)
    line_list=sorted(lines);li={L:i for i,L in enumerate(line_list)};assert len(line_list)==1365
    lh=np.array([li[tuple(sorted(int(ph[x]) for x in L))] for L in line_list],dtype=np.int32)
    lo=orbits(lh);assert Counter(map(len,lo))==Counter({3:451,1:12}) and len(lo)==463

    flags=[(x,j) for j,L in enumerate(line_list) for x in L];fi={f:i for i,f in enumerate(flags)}
    fh=np.array([fi[(int(ph[x]),int(lh[j]))] for x,j in flags],dtype=np.int32)
    fo=orbits(fh);assert Counter(map(len,fo))==Counter({3:2265,1:30}) and len(fo)==2295
    beta=len(fo)-len(po)-len(lo)+1;assert beta==1368
    assert beta!=vfix

    out={
      'schema':'w33.pass10709_10716.normalizer_chain_extension_nogo.v1','status':'PASS','passes':'10709-10716',
      'element':{'h':'n^2','order':3,'normalizer':'<g8,n> = C13:C6','subgroup_tested':'C13:C3'},
      'V2_vector_action':{'orbit_lengths':{'1':16,'3':1360},'permutation_module_fixed_dimension':vfix},
      'H4_Levi_action':{'point_orbits':{'1':15,'3':450,'total':465},'line_orbits':{'1':12,'3':451,'total':463},'flag_orbits':{'1':30,'3':2265,'total':2295},'quotient_beta1':beta,'H1_fixed_dimension':beta},
      'Maschke_reason':'3 is invertible in F2, so invariant functor is exact and H1^C3 equals H1 of the quotient chain complex',
      'extension_to_C13_colon_C3':False,'extension_to_C13_colon_C6':False,'fixed_dimension_defect':vfix-beta,
      'theorem':'The explicit C13 chain-level H(4)-homology/F2[V2] bridge is genuinely C13-only. The order-3 normalizer complement has fixed dimensions 1368 on H1(Levi H4;F2) and 1376 on F2[V2], an exact eight-dimensional defect, so no C13:C3- or C13:C6-equivariant extension exists.',
      'boundary':'Exact finite F4 orbit census and graph-quotient homology calculation. It rules out the natural normalizer extension; it does not rule out unrelated eight-dimensional corrections or enlarged modules.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','fixed_dims':[1368,1376],'defect':8,'extends':False}))
if __name__=='__main__':main()
