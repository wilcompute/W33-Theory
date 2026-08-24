#!/usr/bin/env python3
"""Pass10169-10176 outside-box: exact graph on the 16 Hermitian-isotropic W33 points.

Pass10105-10112 split the chamber-selected W33 points as 16|12|12 under the
projective U_2(3) centralizer.  This pass identifies the induced W33 collinearity
graph on the 16-point Hermitian-isotropic orbit.

It is the Cayley graph

  Gamma16 = Cay(C4 x C4, S),
  S={(0,1),(0,2),(0,3),(1,2),(2,2),(3,2)}.

Equivalently it consists of four K4 fibres (fixed first coordinate), with a
perfect antipodal matching between every pair of distinct fibres.  This form
makes the full automorphism group transparent:

* any S4 permutation of the four fibres is an automorphism;
* on the common four-point fibre coordinate, the allowed simultaneous
  permutations are exactly the centralizer of the antipodal involution
  tau=(0 2)(1 3), namely D8;
* the four K4 fibres are the ONLY 4-cliques, so every automorphism must permute
  them.  The kernel of this fibre action is at most C_{S4}(tau)=D8.

Hence Aut(Gamma16)=S4 x D8, order 192.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10169_10176_ISOTROPIC16_CAYLEY_GRAPH.json'
V=[(a,b) for a in range(4) for b in range(4)]
IDX={v:i for i,v in enumerate(V)}
S={(0,1),(0,2),(0,3),(1,2),(2,2),(3,2)}

def add(x,y):return ((x[0]+y[0])%4,(x[1]+y[1])%4)
def adj(x,y):return ((y[0]-x[0])%4,(y[1]-x[1])%4) in S

def matrix():
    A=sp.zeros(16)
    for i,x in enumerate(V):
        for j,y in enumerate(V):
            if i!=j and adj(x,y):A[i,j]=1
    return A

def cliques4(A):
    out=[]
    for C in itertools.combinations(range(16),4):
        if all(A[i,j]==1 for i,j in itertools.combinations(C,2)):out.append(C)
    return out

def centralizer_tau():
    tau={0:2,2:0,1:3,3:1}
    good=[]
    for p in itertools.permutations(range(4)):
        if all(p[tau[x]]==tau[p[x]] for x in range(4)):good.append(p)
    return good

def perm_fibre(pi,sigma,x):return (pi[x[0]],sigma[x[1]])

def main():
    A=matrix()
    assert all(sum(int(A[i,j]) for j in range(16))==6 for i in range(16))
    assert A==A.T

    # Exact spectrum.
    ev=A.eigenvals()
    spec={int(k):int(v) for k,v in ev.items()}
    assert spec=={6:1,2:4,0:6,-2:3,-4:2},spec

    # The only K4s are the four coordinate fibres.
    cs=cliques4(A)
    fibres=[tuple(IDX[(a,b)] for b in range(4)) for a in range(4)]
    assert set(map(tuple,cs))==set(fibres),cs

    # Between every two fibres: a perfect matching, always antipodal b -> b+2.
    matchings={}
    for a,c in itertools.combinations(range(4),2):
        pairs=[]
        for b in range(4):
            y=(c,(b+2)%4)
            assert adj((a,b),y)
            pairs.append(((a,b),y))
        assert sum(1 for b,d in itertools.product(range(4),repeat=2) if adj((a,b),(c,d)))==4
        matchings[f'{a}-{c}']=[[[*x],[*y]] for x,y in pairs]

    # Exhibit S4 x D8 automorphisms.
    D8=centralizer_tau();assert len(D8)==8
    autos=set()
    for pi in itertools.permutations(range(4)):
        for sig in D8:
            p=tuple(IDX[perm_fibre(pi,sig,x)] for x in V)
            assert all(int(A[i,j])==int(A[p[i],p[j]]) for i in range(16) for j in range(16))
            autos.add(p)
    assert len(autos)==192

    # Fullness proof by the clique system: any automorphism gives <=4! choices on
    # fibres and its fibre-kernel is <= C_S4(tau)=8, hence <=192.  We exhibit 192.
    upper=24*8;assert upper==192==len(autos)

    # Cayley translation subgroup C4 x C4 is visibly regular.
    translations=[]
    for t in V:
        p=tuple(IDX[add(x,t)] for x in V)
        assert all(int(A[i,j])==int(A[p[i],p[j]]) for i in range(16) for j in range(16))
        translations.append(p)
    assert len(set(translations))==16

    out={
      'schema':'w33.pass10169_10176.isotropic16_cayley_graph.v1','status':'PASS','passes':'10169-10176','outside_box':True,
      'graph':{'vertices':'C4 x C4','connection_set':sorted([list(x) for x in S]),'order':16,'degree':6,
               'spectrum':{str(k):v for k,v in sorted(spec.items())}},
      'fibre_structure':{'K4_count':4,'K4_fibres':[[list(V[i]) for i in C] for C in fibres],
                         'cross_fibre_relation':'for every two distinct fibres, the four cross edges are the perfect matching b -> b+2',
                         'matchings':matchings},
      'automorphisms':{'full_order':192,'structure':'S4 x D8','S4':'arbitrary permutation of four K4 fibres',
                       'D8':'centralizer in S4 of tau=(0 2)(1 3), acting simultaneously on all fibres',
                       'upper_bound_proof':'the four K4s are the only 4-cliques, so every automorphism permutes them; the fibre kernel is at most C_S4(tau)=D8, hence |Aut|<=24*8=192; 192 automorphisms are explicitly exhibited',
                       'regular_translation_subgroup':'C4 x C4, order 16'},
      'theorem':'The 16-point Hermitian-isotropic W33 residue graph is Cay(C4xC4,{(0,+/-1),(0,2),(+/-1,2),(2,2)}). It has spectrum 6^1,2^4,0^6,(-2)^3,(-4)^2, exactly four K4 fibres with antipodal perfect matchings between each pair, and full automorphism group S4 x D8 of order 192.',
      'bridge_target':'The repo independently found an S4 x D8 order-192 stabilizer for the 270 orbit of pairs of W33 spreads sharing four lines. Since four common spread lines contain 16 points, the next pass should test whether their induced W33 graph is this Gamma16 and whether the spread-pair stabilizer maps isomorphically onto Aut(Gamma16).',
      'boundary':'Exact finite graph calculation and group upper/lower bound. The spread-pair identification is the next objectwise test and is not claimed in this pass.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','spectrum':out['graph']['spectrum'],'Aut':192,'K4s':4}))
    return 0
if __name__=='__main__':raise SystemExit(main())
