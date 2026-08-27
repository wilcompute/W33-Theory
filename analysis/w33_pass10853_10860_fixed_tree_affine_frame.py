#!/usr/bin/env python3
"""Pass10853-10860: the 2B-fixed H(4) tree selects an affine frame in PG(2,4).

Pass10789 found that k=n^3 fixes 21 H(4) points,25 H(4) lines and45 flags,
forming a tree.  Pass10845 identifies the 21 fixed projective points with
PG(Fix(k))=PG(2,4).

This pass refines the fixed tree exactly.

Among the 21 fixed points, six have fixed-tree degree5 and fifteen degree1.
Among the six degree5 points, five are collinear in PG(2,4); call their line
L_infty.  The sixth point c lies off L_infty.  Thus the point set splits

    PG(2,4) = {c} + L_infty(5) + 15 affine points.

The five fixed H(4) lines of degree5 are exactly the five PG(2,4) projective
lines through c.  Each contains c, one point of L_infty, and three of the
fifteen affine points.  The remaining20 fixed H(4) lines are degree-one leaves,
four attached to each point of L_infty.

So the fixed incidence tree is a treeification of an affine frame: origin c,
line at infinity L_infty, five radial directions, with four external H(4)
branches at each direction.
"""
from __future__ import annotations
from collections import Counter,deque
import itertools,json
from pathlib import Path
import numpy as np
import w33_pass10477_10484_h4_normalizer_27state_quotient as Q
import w33_pass10845_10852_normalizer_jordan_pg24 as J
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10853_10860_FIXED_TREE_AFFINE_FRAME.json'

def rank4(A): return J.rank4(A)

def nullspace4(A):
    A=np.array(A,dtype=np.uint8).copy();m,n=A.shape;r=0;piv=[]
    for c in range(n):
      q=next((i for i in range(r,m) if A[i,c]),None)
      if q is None:continue
      if q!=r:A[[r,q]]=A[[q,r]]
      u=Q.invs(int(A[r,c]));A[r]=np.array([Q.mul(int(x),u) for x in A[r]],dtype=np.uint8)
      for i in range(m):
        if i!=r and A[i,c]:
          t=int(A[i,c]);A[i]^=np.array([Q.mul(t,int(x)) for x in A[r]],dtype=np.uint8)
      piv.append(c);r+=1
    free=[c for c in range(n) if c not in piv];B=[]
    for f in free:
      v=np.zeros(n,dtype=np.uint8);v[f]=1
      for i,p in enumerate(piv):v[p]=A[i,f]
      B.append(v)
    return B

def solve(B,v):
    B=np.stack(B,axis=1)
    for c in itertools.product(range(4),repeat=B.shape[1]):
      z=np.zeros(B.shape[0],dtype=np.uint8)
      for j,a in enumerate(c):
        if a:z^=np.array([Q.mul(a,int(x)) for x in B[:,j]],dtype=np.uint8)
      if np.array_equal(z,v):return np.array(c,dtype=np.uint8)
    raise ValueError

def norm3(v):
    for x in v:
      if x:
        u=Q.invs(int(x));return tuple(Q.mul(u,int(y)) for y in v)
    raise ValueError

def span_line(u,v):
    S=set()
    for a,b in itertools.product(range(4),repeat=2):
      if a==b==0:continue
      w=np.array([Q.mul(a,int(x))^Q.mul(b,int(y)) for x,y in zip(u,v)],dtype=np.uint8)
      S.add(norm3(w))
    assert len(S)==5
    return frozenset(S)

def main():
    g8,n=J.build_normalizer();k=Q.pw(n,3);s=Q.pw(n,4);I=Q.eye(6)
    fix_basis=nullspace4(k^I);assert len(fix_basis)==3

    # Full PG(5,4) and H(4).
    def norm6(v):
      for x in v:
        if x:
          u=Q.invs(int(x));return tuple(Q.mul(u,int(y)) for y in v)
      raise ValueError
    pts=[];seen=set()
    for v in itertools.product(range(4),repeat=6):
      if any(v):
        p=norm6(v)
        if p not in seen:seen.add(p);pts.append(p)
    pi={p:i for i,p in enumerate(pts)};assert len(pts)==1365
    def pp(A):return np.array([pi[norm6(Q.mv(A,p))] for p in pts],dtype=np.int32)
    pg1=np.array([[3,0,0,1,2,0],[3,3,2,0,1,2],[2,0,0,0,0,2],[1,2,2,3,2,3],[2,0,1,2,0,0],[1,2,2,1,3,0]],dtype=np.uint8)
    pg2=np.array([[3,1,2,2,1,1],[2,1,1,3,0,0],[2,3,1,0,3,0],[3,3,1,1,1,1],[3,2,1,1,2,1],[3,2,2,0,2,3]],dtype=np.uint8)
    p1,p2,pk,ps=map(pp,(pg1,pg2,k,s))
    seed=tuple(sorted(pi[p] for p in [(0,0,0,0,0,1),(0,1,3,0,0,0),(0,1,3,0,0,1),(0,1,3,0,0,2),(0,1,3,0,0,3)]))
    lines={seed};D=deque([seed])
    while D:
      L=D.popleft()
      for p in (p1,p2):
        M=tuple(sorted(int(p[x]) for x in L))
        if M not in lines:lines.add(M);D.append(M)
    line_list=sorted(lines);li={L:i for i,L in enumerate(line_list)};assert len(line_list)==1365
    lk=np.array([li[tuple(sorted(int(pk[x]) for x in L))] for L in line_list],dtype=np.int32)
    ls=np.array([li[tuple(sorted(int(ps[x]) for x in L))] for L in line_list],dtype=np.int32)
    FP=[x for x in range(1365) if pk[x]==x];FL=[j for j in range(1365) if lk[j]==j]
    assert (len(FP),len(FL))==(21,25)
    adjP={x:[] for x in FP};adjL={j:[] for j in FL}
    for j in FL:
      for x in line_list[j]:
        if x in adjP:adjP[x].append(j);adjL[j].append(x)
    assert Counter(map(len,adjP.values()))==Counter({1:15,5:6})
    assert Counter(map(len,adjL.values()))==Counter({1:20,5:5})
    assert sum(map(len,adjP.values()))==45

    # Identify PG(2,4) coordinates inside Fix(k).
    coord={x:norm3(solve(fix_basis,np.array(pts[x],dtype=np.uint8))) for x in FP}
    highP=[x for x in FP if len(adjP[x])==5];highL=[j for j in FL if len(adjL[j])==5]
    assert (len(highP),len(highL))==(6,5)
    coredeg={x:sum(j in highL for j in adjP[x]) for x in highP}
    central=[x for x in highP if coredeg[x]==5];periph=[x for x in highP if coredeg[x]==1]
    assert len(central)==1 and len(periph)==5;c=central[0]
    Linf=span_line(coord[periph[0]],coord[periph[1]])
    assert {coord[x] for x in periph}==set(Linf)
    assert coord[c] not in Linf
    affine=[x for x in FP if x!=c and x not in periph];assert len(affine)==15

    # Each high H(4) line is literally the PG(2,4) radial line through c.
    for j in highL:
      fixed_on=[x for x in line_list[j] if x in adjP];assert len(fixed_on)==5
      inf=[x for x in fixed_on if x in periph];assert len(inf)==1 and c in fixed_on
      radial=span_line(coord[c],coord[inf[0]])
      assert {coord[x] for x in fixed_on}==set(radial)
    # Each infinity point has four dangling H4 fixed lines in addition to one radial line.
    assert all(sum(j not in highL for j in adjP[x])==4 for x in periph)
    assert all(len(adjP[x])==1 for x in affine)

    # C3 refinement of the selected affine frame.
    assert int(ps[c])==c and {int(ps[x]) for x in periph}==set(periph)
    def prof(p,S):
      S=set(S);seen=set();C=Counter()
      for x in S:
        if x in seen:continue
        y=x;n0=0
        while y not in seen:seen.add(y);n0+=1;y=int(p[y])
        C[n0]+=1
      return dict(sorted(C.items()))
    assert prof(ps,periph)=={1:2,3:1}
    assert prof(ps,affine)=={3:5}
    assert prof(ls,highL)=={1:2,3:1}

    out={
      'schema':'w33.pass10853_10860.fixed_tree_affine_frame.v1','status':'PASS','passes':'10853-10860',
      'fixed_geometry':{'projective_points':21,'H4_fixed_lines':25,'fixed_flags':45,'incidence':'connected tree','point_degree_profile':{'1':15,'5':6},'line_degree_profile':{'1':20,'5':5}},
      'PG24_affine_frame':{'space':'PG(Fix(k)) = PG(2,4)','central_origin_c':1,'line_at_infinity_points':5,'other_affine_points':15,'degree5_points':'{c} union L_infty','five_degree5_H4_lines':'exactly the five PG(2,4) radial lines through c'},
      'dangling_structure':{'per_infinity_point':4,'total_dangling_fixed_H4_lines':20,'affine_leaf_points_each_degree':1},
      'C3_action':{'c_fixed':True,'L_infty_orbits':{'1':2,'3':1},'other_affine_point_orbits':{'3':5},'radial_line_orbits':{'1':2,'3':1}},
      'theorem':'The 2B-fixed H(4) tree selects an affine frame in PG(2,4): a distinguished origin c and a distinguished line at infinity L_infty. The five non-leaf H(4) lines are exactly the five projective radial lines through c, while four additional H(4) leaf lines hang from each direction at infinity. Thus the fixed tree is a precise treeification of an affine-plane frame, not an anonymous 21-point fixed set.',
      'boundary':'Exact F4 coordinate and H(4) incidence computation. The 20 dangling H(4) lines are not identified with the remaining PG(2,4) projective lines; the two incidence structures differ and that distinction is part of the theorem.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','PG24':'1 origin + 5 infinity + 15 affine','fixed_tree':'5 radial + 20 dangling'}))
if __name__=='__main__':main()
