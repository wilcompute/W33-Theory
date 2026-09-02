#!/usr/bin/env python3
"""Decide whether the old 81-dimensional clique-Hodge sector is Steinberg.

The W33 flag building has H1 dimension 81 and the new exact certificate proves
its character is irreducible.  Independently, the W33 clique complex on the
40-point collinearity graph has chain dimensions

    C0=40, C1=240, C2=160, C3=40

and rational homology b0=1,b1=81,b2=b3=0.

The repo has long called the 81 harmonic edge modes 'Steinberg', but older
spectral scripts established only the dimension.  This script settles the
representation identity without relying on a character-table label.

For each of all 25,920 PSp4(3) elements it computes the *oriented* simplicial
chain characters (a fixed simplex contributes the sign of the induced vertex
permutation).  Lefschetz/Euler in the representation ring gives

 chi_H1(clique) = 1 - chi_C0 + chi_C1 - chi_C2 + chi_C3.

It compares this element-by-element with the W33 Levi-building H1 character

 chi_H1(building) = #fixed chambers - #fixed points - #fixed lines + 1.

Equality on every element is an exact ordinary-character certificate that the
rational clique H1/Hodge harmonic module is the degree-81 Steinberg module.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import w33_20260901_packet48_bt796_crossid as shell

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260901_CLIQUE_H1_EQUALS_BUILDING_STEINBERG.json'


def parity_of_image(simplex, p):
    """Sign of induced permutation if simplex set is fixed; else zero."""
    S=tuple(sorted(simplex)); image=tuple(p[x] for x in S)
    if set(image)!=set(S): return 0
    pos={x:i for i,x in enumerate(S)}
    q=[pos[x] for x in image]
    inv=sum(q[i]>q[j] for i in range(len(q)) for j in range(i+1,len(q)))
    return -1 if inv%2 else 1


def ip(a,b):
    s=sum(x*y for x,y in zip(a,b)); assert s%len(a)==0
    return s//len(a)


def main():
    D=shell.build(); pts,wlines,G=D['pts'],D['wlines'],D['G']
    assert len(pts)==len(wlines)==40 and len(G)==25920
    li={frozenset(L):i for i,L in enumerate(wlines)}
    line_sets=[set(L) for L in wlines]
    edges=sorted({tuple(sorted((a,b))) for L in wlines for a,b in itertools.combinations(L,2)})
    tris=sorted({tuple(sorted(t)) for L in wlines for t in itertools.combinations(L,3)})
    tets=sorted(tuple(sorted(L)) for L in wlines)
    assert (len(edges),len(tris),len(tets))==(240,160,40)

    def line_perm(p): return tuple(li[frozenset(p[x] for x in L)] for L in wlines)

    clique=[]; building=[]; profiles=Counter(); mismatches=[]
    for gi,(p40,_p45,_p27) in enumerate(G):
        lp=line_perm(p40)
        c0=sum(p40[i]==i for i in range(40))
        c1=sum(parity_of_image(e,p40) for e in edges)
        c2=sum(parity_of_image(t,p40) for t in tris)
        c3=sum(parity_of_image(T,p40) for T in tets)
        hcl=1-c0+c1-c2+c3
        fc=sum(p40[p]==p and lp[ell]==ell for ell,L in enumerate(wlines) for p in L)
        hbu=fc-c0-sum(lp[i]==i for i in range(40))+1
        clique.append(hcl); building.append(hbu)
        profiles[(hcl,hbu)]+=1
        if hcl!=hbu and len(mismatches)<20: mismatches.append({'elementIndex':gi,'clique':hcl,'building':hbu})

    equal=(clique==building)
    assert equal, mismatches[:3]
    norm=ip(clique,clique); assert norm==1
    # Identity is the unique element fixing all 40 vertices.
    ids=[i for i,(p40,_a,_b) in enumerate(G) if all(p40[x]==x for x in range(40))]
    assert len(ids)==1 and clique[ids[0]]==81

    out={
      'schema':'w33.20260901.clique-h1-equals-building-steinberg.v1','status':'PASS','groupOrder':25920,
      'cliqueComplex':{'C0':40,'C1':240,'C2':160,'C3':40,'rationalBetti':[1,81,0,0]},
      'buildingLevi':{'points':40,'lines':40,'chambers':160,'H1Degree':81},
      'elementwiseCharacterEquality':True,'checkedElements':25920,'characterNorm':norm,
      'characterValueProfile':{str(k):v for k,v in sorted(Counter(clique).items())},
      'theorem':('The rational 81-dimensional H1 of the W33 clique complex and the 81-dimensional H1 of the W33 rank-two Levi building have identical PSp4(3) characters on all 25,920 elements. Since this character has norm one, the old clique-Hodge harmonic edge sector is exactly the irreducible degree-81 Steinberg representation in characteristic zero, not merely an equal-dimensional space.'),
      'codeBoundary':('The characteristic-zero harmonic/H1 module is now identified. The ternary CSS logical quotient has the same dimension 81 but modular equivalence in characteristic 3 is a separate statement and is not inferred solely from this ordinary-character calculation.'),
      'physicsBoundary':('This corrects/validates a representation-theoretic label only. It does not establish a matter-field, particle-generation, or continuum-physics interpretation of the 81 modes.')
    }
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','equal':equal,'degree':clique[ids[0]],'norm':norm,'values':dict(sorted(Counter(clique).items()))},sort_keys=True))

if __name__=='__main__': main()
