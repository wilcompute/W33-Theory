#!/usr/bin/env python3
"""Pass8101-8108: identify one 36-Lagrangian Leech component as an H27:GL2(3) coset graph.

Dependencies:
- Pass7885: 144 mixed Leech Lagrangians, three lifts of 48 affine/Hesse lines.
- Pass7957: full 148-Lagrangian sheet controller.

This verifier rebuilds the 144 mixed Lagrangians in C=(Z/9)^2 x (Z/3)^2,
forms the intersection-9 graph, and proves it has four connected 36-vertex
components.  For one component it enumerates the full graph automorphism group
with NetworkX and gets order 1296.  The canonical 12 fibres are the three lifts
of the 12 affine lines in one AG(2,3); the induced quotient is AGL2(3), order 432,
with central sheet kernel C3.

Independently it constructs H27:GL2(3), chooses the order-36 lift of an affine-line
stabilizer, and forms its 36-coset action.  The union of stabilizer suborbits 2+9
is graph-isomorphic to the Leech component.  The preimage of the translation
C3^2 is order 27, exponent 3, nonabelian, with center=derived=C3, hence H27.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS8101_8108_LEECH_H27_GL23_LAGRANGIAN_CONTROLLER.json'
E=[(a,b,c,d) for a in range(9) for b in range(9) for c in range(3) for d in range(3)]
Z=(0,0,0,0)

def add(x,y):return ((x[0]+y[0])%9,(x[1]+y[1])%9,(x[2]+y[2])%3,(x[3]+y[3])%3)
def smul(n,x):return ((n*x[0])%9,(n*x[1])%9,(n*x[2])%3,(n*x[3])%3)
def order(x):
    for n in (1,3,9):
        if smul(n,x)==Z:return n
    raise AssertionError
def pair(x,y):return (x[0]*y[1]-x[1]*y[0]+3*(x[2]*y[3]-x[3]*y[2]))%9

def canon(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:
            s=1 if x==1 else 2
            return tuple((s*y)%3 for y in v)
    raise ValueError
def top(x):return (x[0]%3,x[1]%3,x[2]%3,x[3]%3)
def proj(H):return frozenset(canon(top(x)) for x in H if any(top(x)))
def qdir(u):return canon((u[0],u[1],0,0))[:2]

def lagrangians():
    o9=[x for x in E if order(x)==9];o3=[x for x in E if order(x)==3];M=set()
    for x in o9:
        X={smul(a,x) for a in range(9)}
        for y in o3:
            if y in X or pair(x,y):continue
            H=frozenset(add(u,smul(b,y)) for u in X for b in range(3))
            if len(H)==27:M.add(H)
    assert len(M)==144
    return sorted(M,key=lambda H:tuple(sorted(H)))

def comps(A):
    seen=set();C=[]
    for s in range(len(A)):
        if s in seen:continue
        X={s};q=[s];seen.add(s)
        while q:
            u=q.pop()
            for v in np.flatnonzero(A[u]):
                v=int(v)
                if v not in X:X.add(v);seen.add(v);q.append(v)
        C.append(sorted(X))
    return C

def comp_perm(p,q):return tuple(p[q[i]] for i in range(len(q)))
def inv_perm(p):
    z=[0]*len(p)
    for i,j in enumerate(p):z[j]=i
    return tuple(z)
def ord_perm(p):
    e=tuple(range(len(p)));x=e
    for n in range(1,100):
        x=comp_perm(p,x)
        if x==e:return n
    raise AssertionError

def detu(u,v):return (u[0]*v[1]-u[1]*v[0])%3
def detA(A):return (A[0][0]*A[1][1]-A[0][1]*A[1][0])%3
def mm(A,B):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2))%3 for j in range(2)) for i in range(2))
def mv(A,u):return tuple(sum(A[i][k]*u[k] for k in range(2))%3 for i in range(2))
def hmul(h,k):
    u,z=h;v,w=k
    return (((u[0]+v[0])%3,(u[1]+v[1])%3),(z+w+detu(u,v))%3)
def phi(A,h):
    u,z=h;return (mv(A,u),detA(A)*z%3)
def gmul(g,h):
    u,z,A=g;v,w,B=h;uv,zz=hmul((u,z),phi(A,(v,w)))
    return (uv,zz,mm(A,B))

def main():
    L=lagrangians();A=np.zeros((144,144),dtype=np.int8)
    for i,j in itertools.combinations(range(144),2):
        if len(L[i]&L[j])==9:A[i,j]=A[j,i]=1
    assert set(map(int,A.sum(1)))=={11}
    CC=comps(A);assert list(map(len,CC))==[36,36,36,36]
    C=CC[0];A36=A[np.ix_(C,C)];GX=nx.from_numpy_array(A36)
    autos=[tuple(m[i] for i in range(36)) for m in nx.algorithms.isomorphism.GraphMatcher(GX,GX).isomorphisms_iter()]
    assert len(autos)==1296

    # Canonical 12 three-sheet fibres over one AG(2,3).
    fibres=defaultdict(list)
    for loc,g in enumerate(C):fibres[proj(L[g])].append(loc)
    assert len(fibres)==12 and set(map(len,fibres.values()))=={3}
    lines=sorted(fibres,key=lambda S:tuple(sorted(S)));F=[frozenset(fibres[S]) for S in lines];fi={x:i for i,x in enumerate(F)}
    dirs={qdir(next(u for u in S if (u[0],u[1])!=(0,0))) for S in lines};assert len(dirs)==1
    bperms=[]
    for p in autos:
        b=tuple(fi[frozenset(p[x] for x in f)] for f in F);bperms.append(b)
    assert len(set(bperms))==432
    kernel=[p for p,b in zip(autos,bperms) if b==tuple(range(12))];assert len(kernel)==3

    # Recover the affine 9-point line geometry and its translation C3^2.
    traces=[]
    for S in lines:
        traces.append(frozenset((u[2],u[3]) for u in S if (u[0],u[1])!=(0,0)))
    pts=sorted(set().union(*map(set,traces)));assert len(pts)==9
    def pointmap(b):
        z={}
        for x in pts:
            inc=[i for i,T in enumerate(traces) if x in T]
            for i,j in itertools.combinations(inc,2):
                q=traces[b[i]]&traces[b[j]]
                if len(q)==1:z[x]=next(iter(q));break
        return z
    trans=set()
    for b in set(bperms):
        z=pointmap(b);v=np.array(z[(0,0)],int)
        e1=(np.array(z[(1,0)],int)-v)%3;e2=(np.array(z[(0,1)],int)-v)%3;M=np.column_stack([e1,e2])%3
        assert all(tuple(map(int,(M@np.array(x)+v)%3))==z[x] for x in pts)
        if np.array_equal(M,np.eye(2,dtype=int)%3):trans.add(b)
    assert len(trans)==9
    H27=[p for p,b in zip(autos,bperms) if b in trans];assert len(H27)==27
    assert Counter(ord_perm(p) for p in H27)==Counter({3:26,1:1})
    Hset=set(H27);assert all(comp_perm(p,q) in Hset for p in H27 for q in H27)
    center=[p for p in H27 if all(comp_perm(p,q)==comp_perm(q,p) for q in H27)];assert len(center)==3
    comm=set()
    for p in H27:
      for q in H27:comm.add(comp_perm(comp_perm(comp_perm(inv_perm(p),inv_perm(q)),p),q))
    assert len(comm)==3 and set(comm)==set(center)

    # Independent H27:GL2(3) coset model.
    GL=[]
    for a,b,c,d in itertools.product(range(3),repeat=4):
        M=((a,b),(c,d))
        if detA(M):GL.append(M)
    I=((1,0),(0,1));G=[(u,z,M) for u in itertools.product(range(3),repeat=2) for z in range(3) for M in GL]
    K=[((t,0),0,M) for t in range(3) for M in GL if M[1][0]==0];assert len(K)==36
    unseen=set(G);cos=[];ci={}
    while unseen:
        g=next(iter(unseen));Q=frozenset(gmul(g,k) for k in K);j=len(cos);cos.append(Q)
        for x in Q:ci[x]=j
        unseen-=set(Q)
    assert len(cos)==36;reps=[next(iter(Q)) for Q in cos]
    def act(g):return tuple(ci[gmul(g,r)] for r in reps)
    base=ci[((0,0),0,I)];Kp=[act(k) for k in K]
    OO=[];seen=set()
    for s in range(36):
        if s in seen:continue
        X={s};q=[s];seen.add(s)
        while q:
            x=q.pop()
            for p in Kp:
                y=p[x]
                if y not in X:X.add(y);seen.add(y);q.append(y)
        OO.append(sorted(X))
    assert sorted(map(len,OO))==[1,2,6,9,18]
    N=set(next(o for o in OO if len(o)==2)+next(o for o in OO if len(o)==9));Ar=np.zeros((36,36),dtype=np.int8)
    rg=[None]*36
    for g in G:
        p=act(g);v=p[base]
        if rg[v] is None:rg[v]=g
    for v,g in enumerate(rg):
        p=act(g)
        for x in N:Ar[v,p[x]]=1
    assert np.array_equal(Ar,Ar.T) and set(map(int,Ar.sum(1)))=={11}
    assert nx.is_isomorphic(nx.from_numpy_array(Ar),GX)

    out={'schema':'w33.pass8101_8108.leech_h27_gl23_lagrangian_controller.v1','status':'PASS','passes':'8101-8108',
      'Leech_component':{'vertices':36,'components_total':4,'degree':11,'spectrum':'11^1 + 2^20 + (-1)^3 + (-4)^12','full_automorphism_order':1296,'three_sheet_fibres':12,'base_action_order':432,'base':'AGL2(3) on 12 affine lines','sheet_kernel':'C3'},
      'translation_preimage':{'order':27,'element_orders':'1^1+3^26','center_order':3,'derived_order':3,'identification':'extraspecial Heisenberg H27'},
      'coset_model':{'group':'H27:GL2(3)','group_order':1296,'stabilizer_order':36,'subdegrees':[1,2,6,9,18],'graph_orbit_union':[2,9],'isomorphic_to_Leech_component':True},
      'theorem':'Each 36-object mixed-Lagrangian component is exactly a coset graph of H27:GL2(3). Its 12-line quotient is AGL2(3); the central C3 supplies the three sheets, and the preimage of affine translations is the nonabelian extraspecial H27.',
      'claim_boundary':'Exact finite-group/Leech-linking theorem. No physical Heisenberg dynamics is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','Aut':1296,'controller':'H27:GL2(3)','translation_preimage':'H27'}))
if __name__=='__main__':main()
