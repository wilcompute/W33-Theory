#!/usr/bin/env python3
"""Pass10789-10796: the order-2 half of C13:C6 produces a 32-dimensional defect.

Let n be Wilson's explicit order-6 normalizer element with g8^n=g8^4 and let
k=n^3.  Then k has order 2 and conjugates g8 to g8^{-1}.

On V2=F4^6, k fixes exactly 64 vectors = 4^3, hence the permutation module
F2[V2] has (4096+64)/2 = 2080 invariant orbit-sums.

On the H(4) Levi graph, k fixes 21 points, 25 lines and 45 flags.  The fixed
subgraph is a tree.  The quotient graph has 1388 vertex orbits and 3435 edge
orbits, so its cycle rank is 2048.  Direct invariant-chain elimination over F2
shows H1^k has this same dimension 2048.

Thus after the C3 stable repair, the order-2 extension faces a new exact defect
  2080 - 2048 = 32.
This is characteristic-2 information: Maschke semisimplicity is unavailable for
C2, so Brauer characters alone cannot repair it.
"""
from __future__ import annotations
from collections import Counter,deque
import itertools,json
from pathlib import Path
import numpy as np
import w33_pass10477_10484_h4_normalizer_27state_quotient as Q
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10789_10796_ORDER2_NORMALIZER_DEFECT.json'

def build_generators():
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
    k=Q.pw(n,3)
    assert Q.order(g8)==13 and Q.order(n)==6 and Q.order(k)==2
    assert np.array_equal(Q.conj(g8,k),Q.pw(g8,-1))
    return g1,g2,k

def orbits(p):
    seen=[False]*len(p);out=[]
    for s in range(len(p)):
      if seen[s]:continue
      C=[];x=s
      while not seen[x]:seen[x]=True;C.append(x);x=int(p[x])
      out.append(C)
    return out

def bitrank(cols):
    basis={};r=0
    for x in cols:
      y=x
      while y:
        p=y.bit_length()-1
        if p in basis:y^=basis[p]
        else:basis[p]=y;r+=1;break
    return r

def main():
    g1,g2,k=build_generators()
    vecs=[tuple(v) for v in itertools.product(range(4),repeat=6)];vi={v:i for i,v in enumerate(vecs)}
    vk=np.array([vi[tuple(map(int,Q.mv(k,v)))] for v in vecs],dtype=np.int32)
    vo=orbits(vk);assert Counter(map(len,vo))==Counter({2:2016,1:64})
    v_inv=len(vo);assert v_inv==2080

    pts=[];seen=set()
    for v in vecs[1:]:
      p=Q.norm(v)
      if p not in seen:seen.add(p);pts.append(p)
    pi={p:i for i,p in enumerate(pts)};assert len(pts)==1365
    def pp(A):return np.array([pi[Q.norm(Q.mv(A,p))] for p in pts],dtype=np.int32)
    pg1,pg2,pk=map(pp,(g1,g2,k))
    po=orbits(pk);assert Counter(map(len,po))==Counter({2:672,1:21}) and len(po)==693

    seed=tuple(sorted(pi[p] for p in [(0,0,0,0,0,1),(0,1,3,0,0,0),(0,1,3,0,0,1),(0,1,3,0,0,2),(0,1,3,0,0,3)]))
    lines={seed};D=deque([seed])
    while D:
      L=D.popleft()
      for p in (pg1,pg2):
        M=tuple(sorted(int(p[x]) for x in L))
        if M not in lines:lines.add(M);D.append(M)
    line_list=sorted(lines);li={L:i for i,L in enumerate(line_list)};assert len(line_list)==1365
    lk=np.array([li[tuple(sorted(int(pk[x]) for x in L))] for L in line_list],dtype=np.int32)
    lo=orbits(lk);assert Counter(map(len,lo))==Counter({2:670,1:25}) and len(lo)==695

    flags=[(x,j) for j,L in enumerate(line_list) for x in L];fi={f:i for i,f in enumerate(flags)}
    fk=np.array([fi[(int(pk[x]),int(lk[j]))] for x,j in flags],dtype=np.int32)
    fo=orbits(fk);assert Counter(map(len,fo))==Counter({2:3390,1:45}) and len(fo)==3435

    fp=[x for x in range(1365) if pk[x]==x];fl=[j for j in range(1365) if lk[j]==j]
    ff=[(x,j) for j in fl for x in line_list[j] if pk[x]==x]
    assert (len(fp),len(fl),len(ff))==(21,25,45)
    adj={('p',x):[] for x in fp};adj.update({('l',j):[] for j in fl})
    for x,j in ff:adj[('p',x)].append(('l',j));adj[('l',j)].append(('p',x))
    seen_nodes=set();cc=0
    for s in adj:
      if s in seen_nodes:continue
      cc+=1;dq=deque([s]);seen_nodes.add(s)
      while dq:
        u=dq.popleft()
        for v in adj[u]:
          if v not in seen_nodes:seen_nodes.add(v);dq.append(v)
    assert cc==1 and len(ff)-len(adj)+cc==0
    assert Counter(len(adj[('p',x)]) for x in fp)==Counter({1:15,5:6})
    assert Counter(len(adj[('l',j)]) for j in fl)==Counter({1:20,5:5})

    # Invariant chain complex.  One basis vector per edge orbit and vertex orbit.
    point_oid={x:i for i,C in enumerate(po) for x in C};line_oid={j:len(po)+i for i,C in enumerate(lo) for j in C}
    cols=[]
    for C in fo:
      support=set()
      for ei in C:
        x,j=flags[ei]
        for v in (x,1365+j):
          if v in support:support.remove(v)
          else:support.add(v)
      # support is invariant; collapse each full vertex orbit to one coefficient.
      oids=set(point_oid[v] if v<1365 else line_oid[v-1365] for v in support)
      mask=0
      for r in oids:mask|=(1<<r)
      cols.append(mask)
    rank=bitrank(cols);assert rank==len(po)+len(lo)-1==1387
    h_inv=len(fo)-rank;assert h_inv==2048
    quotient_beta=len(fo)-len(po)-len(lo)+1;assert quotient_beta==2048
    defect=v_inv-h_inv;assert defect==32

    out={
      'schema':'w33.pass10789_10796.order2_normalizer_defect.v1','status':'PASS','passes':'10789-10796',
      'involution':{'k':'n^3','order':2,'action_on_C13':'inversion'},
      'V2_action':{'fixed_vectors':64,'fixed_F4_dimension':3,'orbit_lengths':{'1':64,'2':2016},'permutation_module_invariant_dimension':v_inv},
      'H4_action':{
        'point_orbits':{'1':21,'2':672,'total':len(po)},'line_orbits':{'1':25,'2':670,'total':len(lo)},'flag_orbits':{'1':45,'2':3390,'total':len(fo)},
        'fixed_subgraph':{'vertices':46,'edges':45,'components':1,'beta1':0,'shape':'tree','point_degrees':{'1':15,'5':6},'line_degrees':{'1':20,'5':5}},
        'quotient_Levi':{'vertices':len(po)+len(lo),'edges':len(fo),'beta1':quotient_beta},
        'invariant_boundary_rank':rank,'H1_invariant_dimension':h_inv},
      'defect':{'F2V2_invariants_minus_H1_invariants':defect,'value':32},
      'theorem':'The order-2 half of the explicit 13:6 normalizer creates a new characteristic-2 obstruction. Its fixed space on V2 is F4^3 with 64 vectors, giving 2080 permutation-orbit invariants, while the H(4) Levi quotient has beta1=2048 and the invariant cycle space has dimension 2048. The exact defect is 32.',
      'boundary':'Exact explicit F4 permutation and invariant-chain computation. Because characteristic 2 divides the involution order, this defect is not controlled by semisimple Brauer-character arithmetic and is not repaired by the C13:C3 stable theorem alone.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','V2_inv':v_inv,'H1_inv':h_inv,'defect':defect,'fixed_subgraph':'tree'}))
if __name__=='__main__':main()
