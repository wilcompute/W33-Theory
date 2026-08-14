#!/usr/bin/env python3
"""Pass5129: all-q chamber apartment carrier = C2 maximal-unipotent root-coset controller.

The structural theorem is the standard rank-two building/Bruhat-cell statement:
a maximal unipotent U(q) fixes a chamber and acts regularly on apartments through
that chamber; the four positive-root directions cut the carrier into their right
cosets.  The executable certificate verifies the statement objectwise for
q=2,3,4,5, including the non-prime field GF(4).
"""
from __future__ import annotations
import functools,json
from collections import deque
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5129_ALLQ_INTRINSIC_UNIPOTENT_CONTROLLER.json'

class Fp:
    def __init__(self,q):self.q=q
    def add(self,a,b):return (a+b)%self.q
    def neg(self,a):return (-a)%self.q
    def mul(self,a,b):return (a*b)%self.q
    def inv(self,a):return pow(a,-1,self.q)
class GF4:
    q=4
    def add(self,a,b):return a^b
    def neg(self,a):return a
    def mul(self,a,b):
        a0,a1=a&1,(a>>1)&1;b0,b1=b&1,(b>>1)&1
        c0=a0*b0;c1=(a0*b1)^(a1*b0);c2=a1*b1
        return (c0^c2)|((c1^c2)<<1)
    def inv(self,a):return next(b for b in range(1,4) if self.mul(a,b)==1)
def FF(q):return GF4() if q==4 else Fp(q)
def I4():return tuple(tuple(int(i==j) for j in range(4)) for i in range(4))
def madd(A,B,F):return tuple(tuple(F.add(A[i][j],B[i][j]) for j in range(4)) for i in range(4))
def mscale(t,A,F):return tuple(tuple(F.mul(t,A[i][j]) for j in range(4)) for i in range(4))
def mm(A,B,F):
    return tuple(tuple(functools.reduce(F.add,(F.mul(A[i][k],B[k][j]) for k in range(4)),0) for j in range(4)) for i in range(4))
def mv(A,v,F):return tuple(functools.reduce(F.add,(F.mul(A[i][k],v[k]) for k in range(4)),0) for i in range(4))
def norm(v,F):
    for x in v:
        if x:
            z=F.inv(x);return tuple(F.mul(z,y) for y in v)
    raise ValueError
def E(i,j):
    M=[[0]*4 for _ in range(4)];M[i][j]=1;return tuple(map(tuple,M))
def roots(q):
    F=FF(q);I=I4();X=[]
    M=[list(r) for r in E(0,1)];M[3][2]=F.neg(1);X.append(tuple(map(tuple,M)))
    X.append(E(1,3));M=[list(r) for r in E(0,3)];M[1][2]=1;X.append(tuple(map(tuple,M)));X.append(E(0,2))
    H=[[madd(I,mscale(t,Z,F),F) for t in range(q)] for Z in X]
    gens=[z for h in H for z in h[1:]];U={I};Q=deque([I])
    while Q:
        a=Q.popleft()
        for g in gens:
            b=mm(a,g,F)
            if b not in U:U.add(b);Q.append(b)
    return sorted(U),H,F

def anchor(q):
    G=build_W(q);U,H,F=roots(q);assert len(U)==q**4;pidx={p:i for i,p in enumerate(G['pts'])}
    gens=[z for h in H for z in h[1:]]
    fp=[i for i,p in enumerate(G['pts']) if all(pidx[norm(mv(g,p,F),F)]==i for g in gens)]
    fl=[]
    for li,L in enumerate(G['lines']):
        if all(frozenset(pidx[norm(mv(g,G['pts'][p],F),F)] for p in L)==L for g in gens):fl.append(li)
    fixed=[(p,l) for p in fp for l in fl if p in G['lines'][l]];assert len(fixed)==1;fi=G['flags'].index(fixed[0])
    support=[a for a,es in enumerate(G['apt_edges']) if fi in es];assert len(support)==q**4
    lookup={G['apartments'][a]:a for a in support};base=G['apartments'][support[0]];u_to_a={}
    for ui,g in enumerate(U):
        A=frozenset(pidx[norm(mv(g,G['pts'][p],F),F)] for p in base);assert A in lookup;u_to_a[ui]=lookup[A]
    assert len(set(u_to_a.values()))==q**4;a_to_u={a:u for u,a in u_to_a.items()}
    active=set()
    S=set(support)
    for _,loc in G['charts']:
        T=S&set(loc.values())
        if T:active.add(frozenset(a_to_u[a] for a in T))
    idx={g:i for i,g in enumerate(U)};cosets=set()
    for h in H:
        for g in U:cosets.add(frozenset(idx[mm(g,z,F)] for z in h))
    assert active==cosets and len(active)==4*q**3 and {len(x) for x in active}=={q}
    return {'q':q,'U_order':len(U),'fixed_chamber_index':fi,'apartment_carrier':len(support),'active_charts':len(active),'root_cosets':len(cosets),'chart_size':q,'exact_hypergraph_match':True}

def main():
    A={str(q):anchor(q) for q in (2,3,4,5)}
    out={'pass':5129,'status':'THEOREM_ALL_FINITE_Q_INTRINSIC_C2_UNIPOTENT_CONTROLLER',
         'statement':'For W(3,q), after choosing a reconstructed chamber, its q^4 apartment carrier is a regular U(q)-torsor for the type-C2 maximal unipotent subgroup, and the 4q^3 active opposite-pair charts are exactly the right cosets of the four positive-root subgroups.',
         'building_proof':'The chamber is a Borel chamber; the opposite Bruhat cell is the maximal-unipotent torsor. A positive-root panel direction fixes one root parameter and its q-point fibers are precisely root-subgroup cosets.',
         'anchors':A,
         'intrinsic_upgrade':'Pass5112 reconstructs chambers/charts from the code itself, so this controller is determined by the apartment code up to code automorphism and the natural point-line orientation swap.',
         'boundary':'Exact finite code/building/group theorem, not a claim about optical-controller speed or noise performance.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
