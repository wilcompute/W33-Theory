#!/usr/bin/env python3
"""Pass7957-7964: full Aut(C,lambda) action on the 148 Leech order-9 Lagrangians.

Dependencies Pass7861 and Pass7885 established C=(Z/9)^2 x (Z/3)^2, the full
pairing-preserving order 1259712, and the 148 maximal isotropics.  Here we act on
those 148 objects and resolve the previously unnamed three-sheet controller above
the 48 Hesse lines.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from sympy.combinatorics import Permutation,PermutationGroup
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS7957_7964_LEECH_LAGRANGIAN_SHEET_CONTROLLER.json'
E=[(a,b,c,d) for a in range(9) for b in range(9) for c in range(3) for d in range(3)]
idx={x:i for i,x in enumerate(E)};zero=(0,0,0,0)
J=np.array([[0,1],[-1,0]],dtype=int)

def add(x,y):return ((x[0]+y[0])%9,(x[1]+y[1])%9,(x[2]+y[2])%3,(x[3]+y[3])%3)
def smul(n,x):return ((n*x[0])%9,(n*x[1])%9,(n*x[2])%3,(n*x[3])%3)
def order(x):
    for n in (1,3,9):
        if smul(n,x)==zero:return n
    raise AssertionError
def pair(x,y):return (x[0]*y[1]-x[1]*y[0]+3*(x[2]*y[3]-x[3]*y[2]))%9

def canon(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:return tuple(((1 if x==1 else 2)*y)%3 for y in v)
    raise ValueError
def top(x):return (x[0]%3,x[1]%3,x[2]%3,x[3]%3)
def proj(H):return frozenset(canon(top(x)) for x in H if any(top(x)))

def span3(gs):
    H=set()
    for cs in itertools.product(range(3),repeat=len(gs)):
        z=zero
        for a,g in zip(cs,gs):z=add(z,smul(a,g))
        H.add(z)
    return frozenset(H)

def lagrangians():
    o9=[x for x in E if order(x)==9];o3=[x for x in E if order(x)==3]
    mixed=set()
    for x in o9:
        X={smul(a,x) for a in range(9)}
        for y in o3:
            if y in X or pair(x,y):continue
            H=frozenset(add(u,smul(b,y)) for u in X for b in range(3))
            if len(H)==27:mixed.add(H)
    soc=[x for x in E if smul(3,x)==zero and x!=zero];elem=set()
    for gs in itertools.combinations(soc,3):
        if any(pair(gs[i],gs[j]) for i,j in itertools.combinations(range(3),2)):continue
        H=span3(gs)
        if len(H)==27:elem.add(H)
    assert len(mixed)==144 and len(elem)==4
    return sorted(mixed|elem,key=lambda H:tuple(sorted(H))),mixed,elem

def trans(A,D,C=None):
    A=np.array(A,dtype=int)%9;D=np.array(D,dtype=int)%3
    C=np.zeros((2,2),dtype=int) if C is None else np.array(C,dtype=int)%3
    if np.any(C):
        assert np.array_equal(A,np.eye(2,dtype=int)%9) and np.array_equal(D,np.eye(2,dtype=int)%3)
        B=(J@C.T@J)%3
    else:B=np.zeros((2,2),dtype=int)
    p=[]
    for x in E:
        u=np.array(x[:2],dtype=int);b=np.array(x[2:],dtype=int)
        up=(A@u+3*(B@b))%9;bp=(C@(u%3)+D@b)%3
        y=(int(up[0]),int(up[1]),int(bp[0]),int(bp[1]));p.append(idx[y])
    return tuple(p)

def normal(K):
    out=set()
    for n in itertools.product(range(3),repeat=3):
        if n==(0,0,0):continue
        if all(sum(n[i]*x[i] for i in range(3))%3==0 for x in K):out.add(canon(n))
    assert len(out)==1;return next(iter(out))

def rank3(rows):
    A=np.array(rows,dtype=int)%3;r=0
    for c in range(A.shape[1]):
        z=next((i for i in range(r,len(A)) if A[i,c]),None)
        if z is None:continue
        A[[r,z]]=A[[z,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,3))%3
        for i in range(len(A)):
            if i!=r and A[i,c]:A[i]=(A[i]-int(A[i,c])*A[r])%3
        r+=1
    return r

def main():
    L,mixed,elem=lagrangians();li={H:i for i,H in enumerate(L)}
    I2=np.eye(2,dtype=int);s1=np.array([[1,1],[0,1]]);s2=np.array([[0,-1],[1,0]])
    gens=[]
    for A in (s1,s2):gens.append(trans(A,I2))
    for D in (s1,s2):gens.append(trans(I2,D))
    for i in range(2):
      for j in range(2):
        C=np.zeros((2,2),dtype=int);C[i,j]=1;gens.append(trans(I2,I2,C))
    G729=PermutationGroup([Permutation(list(p)) for p in gens]);assert int(G729.order())==1259712
    lp=[]
    for p in gens:
        lp.append(tuple(li[frozenset(E[p[idx[x]]] for x in H)] for H in L))
    G=PermutationGroup([Permutation(list(p)) for p in lp]);assert int(G.order())==629856
    orbs=sorted(len(o) for o in G.orbits());assert orbs==[4,144]

    mixidx=[i for i,H in enumerate(L) if H in mixed];eidx=[i for i,H in enumerate(L) if H in elem]
    fibres=defaultdict(list)
    for i in mixidx:fibres[proj(L[i])].append(i)
    assert len(fibres)==48 and set(map(len,fibres.values()))=={3}
    lines=sorted(fibres,key=lambda S:tuple(sorted(S)));lpos={S:i for i,S in enumerate(lines)}
    baseperms=[]
    for p in lp:
        baseperms.append(tuple(lpos[proj(L[p[fibres[S][0]]])] for S in lines))
    GB=PermutationGroup([Permutation(list(p)) for p in baseperms]);assert int(GB.order())==23328
    assert int(G.order())//int(GB.order())==27

    # The 27 sheet transformations are the principal congruence kernel
    # A=I+3X, tr(X)=0.  Each 3-lift fibre sees one C3 quotient.
    Kacts=[]
    for a,b,c in itertools.product(range(3),repeat=3):
        X=np.array([[a,b],[c,(-a)%3]],dtype=int);A=(I2+3*X)%9;p=trans(A,I2)
        q=tuple(li[frozenset(E[p[idx[x]]] for x in H)] for H in L)
        Kacts.append(((a,b,c),q))
    assert len(Kacts)==27
    khist=Counter();kernels={}
    for S,F in fibres.items():
        ker=[]
        for coord,q in Kacts:
            if tuple(F.index(q[i]) for i in F)==(0,1,2):ker.append(coord)
        assert len(ker)==9;k=frozenset(ker);kernels[S]=k;khist[k]+=1
    assert len(khist)==4 and set(khist.values())=={12}
    normals=[normal(k) for k in khist]
    assert all(rank3([normals[i] for i in C])==3 for C in itertools.combinations(range(4),3))

    # Strict linking isometries act as A4 on the four elementary lifts.
    ep={i:j for j,i in enumerate(eidx)}
    eperms=[tuple(ep[p[i]] for i in eidx) for p in lp]
    GE=PermutationGroup([Permutation(list(p)) for p in eperms]);assert int(GE.order())==12

    mi=mixidx[0];ei=eidx[0]
    sm=G.stabilizer(mi);se=G.stabilizer(ei)
    assert sorted(len(o) for o in sm.orbits())==[1,1,1,1,3,6,9,9,9,27,81]
    assert sorted(len(o) for o in se.orbits())==[1,3,36,108]

    out={
      'schema':'w33.pass7957_7964.leech_lagrangian_sheet_controller.v1','status':'PASS','passes':'7957-7964',
      'Aut_C_lambda_order':1259712,'action_on_148_order':629856,'action_kernel':'central inversion {+-1}',
      'Lagrangian_orbits':[4,144],'mixed_top_lines':48,'mixed_lifts_per_line':3,
      'projected_48_line_action_order':23328,'three_sheet_kernel':{'order':27,'structure':'C3^3 = sl2(F3) additively'},
      'sheet_functionals':{'distinct_kernel_hyperplanes':4,'Hesse_lines_per_hyperplane':12,'dual_normals':normals,'projective_frame':'no three of the four normals are collinear in PG(2,3)'},
      'elementary_four_action':{'order':12,'identification':'A4 under strict linking isometries'},
      'mixed_stabilizer_subdegrees':[1,1,1,1,3,6,9,9,9,27,81],
      'elementary_stabilizer_subdegrees':[1,3,36,108],
      'theorem':'The 144 mixed Leech Lagrangians are not merely three lifts of 48 Hesse lines: the lift monodromy is a canonical C3^3 principal-congruence kernel. Its 48 fibre actions use exactly four order-9 kernel hyperplanes, 12 lines each, whose four dual points form a projective frame. The four exceptional elementary Lagrangians carry the matching A4 action.',
      'claim_boundary':'Exact finite linked-module action. The enlargement A4->S4 requires similitudes and is treated separately.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','action':629856,'orbits':orbs,'sheet_kernel':27,'four_frame':True}))
if __name__=='__main__':main()
