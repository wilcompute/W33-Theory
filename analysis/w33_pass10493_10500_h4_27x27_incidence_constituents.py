#!/usr/bin/env python3
"""Pass10493-10500: the full H(4)/(13:6) Levi quotient is a 27|27 incidence transport.

The explicit Wilson 13:6 acts on the 1365 points, 1365 lines and 6825 flags of
H(4).  It has 27 point orbits and 27 line orbits.  The equitable point-to-line
incidence quotient M has row degree 5 and rank 21.  If R is the weighted point
adjacency quotient from Pass10477-10484, then exactly

    M M^vee = 5 I + R,

where M^vee is the reverse line-to-point quotient.  Therefore the squared
singular spectrum is 25^1,12^8,4^12,0^6 and the bipartite 54-state quotient has
spectrum +/-5, +/-sqrt(12)^8, +/-2^12, 0^12.

The old E6 cubic-line/double-six incidence intertwiner (Pass4545/4549) also has
rank 21 and a 6-dimensional kernel, but RR^T spectrum 192^1,12^20,0^6.  Thus
the new incidence transport preserves the 1|6 outer constituent dimensions
while refining the old transmitted 20 as 8+12.  H27 independently has
nontrivial eigenspace dimensions 12,8,6.  This is recorded as a constituent
fingerprint, NOT an objectwise E6/H27 intertwiner.
"""
from __future__ import annotations
from collections import Counter,deque
import itertools,json
from pathlib import Path
import numpy as np
import importlib

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10493_10500_H4_27X27_INCIDENCE_CONSTITUENTS.json'
Q=importlib.import_module('w33_pass10477_10484_h4_normalizer_27state_quotient')

def orbits(N,perms):
    seen=[False]*N;out=[]
    for s in range(N):
      if seen[s]:continue
      C=[];D=deque([s]);seen[s]=True
      while D:
        x=D.popleft();C.append(x)
        for p in perms:
          y=int(p[x])
          if not seen[y]:seen[y]=True;D.append(y)
      out.append(C)
    return out

def rankq(A):
    import sympy as sp
    return int(sp.Matrix(np.asarray(A).tolist()).rank())

def main():
    # Rebuild the explicit F4 group/normalizer using the already certified formulas.
    g1=np.array([[3,0,0,1,2,0],[3,3,2,0,1,2],[2,0,0,0,0,2],[1,2,2,3,2,3],[2,0,1,2,0,0],[1,2,2,1,3,0]],dtype=np.uint8)
    g2=np.array([[3,1,2,2,1,1],[2,1,1,3,0,0],[2,3,1,0,3,0],[3,3,1,1,1,1],[3,2,1,1,2,1],[3,2,2,0,2,3]],dtype=np.uint8)
    g3=Q.pw(Q.mm(Q.pw(g1,4),g2),4);X=Q.pw(Q.mm(Q.mm(Q.mm(g1,g2),g1),Q.pw(g2,2)),3);g4=Q.conj(X,Q.pw(g2,4))
    A=Q.pw(Q.mm(Q.pw(Q.mm(g3,g4),3),g4),3);B0=Q.pw(Q.mm(g3,g4),4);B0=Q.mm(B0,g4);B0=Q.mm(B0,g3);B0=Q.mm(B0,g4);B0=Q.mm(B0,Q.pw(Q.mm(g3,Q.pw(g4,2)),2));g5=Q.mm(Q.mm(A,Q.pw(B0,3)),Q.invm(A))
    Y=Q.mm(Q.mm(Q.mm(g3,g4),g3),Q.pw(g4,2));g6=Q.mm(Q.pw(Y,-2),Q.mm(Q.pw(Q.mm(Q.mm(g3,g4),Q.pw(Y,2)),5),Q.pw(Y,2)));g7=Q.conj(g6,Q.mm(g5,Q.pw(g6,2)));g8=Q.mm(Q.mm(Q.mm(g5,g7),g5),Q.pw(g7,2));n=Q.mm(g5,g7)
    assert Q.order(g8)==13 and Q.order(n)==6

    pts=[];seen=set()
    for v in itertools.product(range(4),repeat=6):
      if any(v):
        p=Q.norm(v)
        if p not in seen:seen.add(p);pts.append(p)
    pi={p:i for i,p in enumerate(pts)};assert len(pts)==1365
    def perm(A):return np.array([pi[Q.norm(Q.mv(A,p))] for p in pts],dtype=np.int32)
    pg1,pg2,pg8,pn=map(perm,(g1,g2,g8,n))
    seed=tuple(sorted(pi[p] for p in [(0,0,0,0,0,1),(0,1,3,0,0,0),(0,1,3,0,0,1),(0,1,3,0,0,2),(0,1,3,0,0,3)]))
    lines={seed};D=deque([seed])
    while D:
      L=D.popleft()
      for p in (pg1,pg2):
        M=tuple(sorted(int(p[x]) for x in L))
        if M not in lines:lines.add(M);D.append(M)
    line_list=sorted(lines);li={L:i for i,L in enumerate(line_list)};assert len(line_list)==1365
    def lp(pp):return np.array([li[tuple(sorted(int(pp[x]) for x in L))] for L in line_list],dtype=np.int32)
    lg8,ln=lp(pg8),lp(pn)
    pO=orbits(1365,[pg8,pn]);lO=orbits(1365,[lg8,ln])
    assert len(pO)==len(lO)==27
    assert Counter(map(len,pO))==Counter({78:12,39:6,26:6,13:3})
    assert Counter(map(len,lO))==Counter({78:12,39:7,26:4,13:4})
    po={x:i for i,C in enumerate(pO) for x in C};lo={x:i for i,C in enumerate(lO) for x in C}
    inc=[[] for _ in pts]
    for j,L in enumerate(line_list):
      for x in L:inc[x].append(j)
    M=np.zeros((27,27),dtype=np.int64);N=np.zeros((27,27),dtype=np.int64)
    for i,C in enumerate(pO):
      x=C[0]
      for j in inc[x]:M[i,lo[j]]+=1
    for j,C in enumerate(lO):
      z=C[0]
      for x in line_list[z]:N[j,po[x]]+=1
    assert set(map(int,M.sum(1)))==set(map(int,N.sum(1)))=={5}
    assert rankq(M)==rankq(N)==21
    assert np.array_equal(np.array(list(map(len,pO)))[:,None]*M,(np.array(list(map(len,lO)))[:,None]*N).T)

    R=M@N-5*np.eye(27,dtype=np.int64)
    assert set(map(int,R.sum(1)))=={20}
    assert rankq(M@N)==21
    I=np.eye(27,dtype=np.int64);prod=M@N
    Z=(prod-25*I)@(prod-12*I)@(prod-4*I)@prod;assert not np.any(Z)
    mult={str(l):27-rankq(prod-l*I) for l in (25,12,4,0)}
    assert mult=={'25':1,'12':8,'4':12,'0':6}

    # Flag orbits give the actual edge-orbits of the quotient Levi multigraph.
    flags=[(x,j) for j,L in enumerate(line_list) for x in L];fi={f:i for i,f in enumerate(flags)}
    f8=np.array([fi[(int(pg8[x]),int(lg8[j]))] for x,j in flags],dtype=np.int32);fn=np.array([fi[(int(pn[x]),int(ln[j]))] for x,j in flags],dtype=np.int32)
    fO=orbits(len(flags),[f8,fn]);assert len(fO)==107
    assert Counter(map(len,fO))==Counter({78:76,39:13,26:12,13:6})
    beta=107-54+1;assert beta==54

    old=json.loads((ROOT/'data/PART_W33_PASS4545_4549_SCHLAFLI_DOUBLE_SIX_INTERTWINER.json').read_text())
    h27=json.loads((ROOT/'data/PART_W33_PASS7629_7636_SCHLAEFLI_H27_STEINBERG_COMPLEMENT.json').read_text())
    assert old['incidence']['rank_over_Q']==21 and old['rational_constituents']['R_kills_on_27_side']==6
    assert h27['H27']['spectrum']=={'-4':6,'-1':8,'2':12,'8':1}
    out={
      'schema':'w33.pass10493_10500.h4_27x27_incidence_constituents.v1','status':'PASS','passes':'10493-10500',
      'normalizer_orbits':{'point_orbits':27,'point_sizes':dict(Counter(map(len,pO))),'line_orbits':27,'line_sizes':dict(Counter(map(len,lO))),'flag_orbits':107,'flag_sizes':dict(Counter(map(len,fO)))},
      'incidence_quotient':{'shape':[27,27],'point_row_sum':5,'line_row_sum':5,'rank':21,'identity':'M M^vee = 5 I + R_point','squared_singular_spectrum':mult,'bipartite_spectrum':'(+/-5)^1, (+/-2sqrt3)^8, (+/-2)^12, 0^12','quotient_Levi_beta1':beta},
      'E6_comparison':{'Pass4545_4549_rank':21,'Pass4545_4549_kernel_dimension':6,'Pass4545_4549_RRt_spectrum':'192^1,12^20,0^6','new_kernel_dimension':6,'new_transmitted_refinement':'20 = 8 + 12'},
      'H27_comparison':{'H27_eigenspace_dimensions':'1 + 12 + 8 + 6','new_incidence_constituent_dimensions':'1 + 8 + 12 + 6','interpretation':'same four constituent dimensions as an exact spectral fingerprint; no common intertwiner has yet been constructed'},
      'theorem':'The full H(4) Levi geometry modulo the explicit 13:6 normalizer is naturally a 27-point-state by 27-line-state incidence transport of rank 21. Its kernel has dimension 6, exactly as in the repo E6 cubic-line/double-six incidence intertwiner, while its transmitted 20-dimensional sector refines as 8+12. H27 independently carries the same nontrivial constituent dimensions 12,8,6. This is a precise spectral-constituent bridge, not yet an objectwise E6 intertwiner.',
      'boundary':'All orbit/incidence/rank/spectrum statements are exact. Equality of constituent dimensions does not by itself identify the representations; an explicit intertwiner remains open.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','shape':[27,27],'rank':21,'spectrum':mult,'beta1':beta}))
if __name__=='__main__':main()
