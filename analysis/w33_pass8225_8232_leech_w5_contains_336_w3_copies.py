#!/usr/bin/env python3
"""Pass8225-8232: the Leech W(5,2) contains exactly 336 W(3,2) subgeometries.

Parallel Pass8022-8029 establishes the actual Leech qubit-halving tower
W(23,2)->W(11,2)->W(5,2).  E8 independently supplies W(3,2).  Here we ask the
precise containment question inside the three-qubit carrier F2^6.

A W(3,2) copy is the projectivization of a nondegenerate symplectic 4-subspace.
By orthogonal complement these are in bijection with nondegenerate 2-planes.
We enumerate all 336, audit their pairwise intersections, and compare with the
classical transitive Sp6(2) orbit-stabilizer formula.  Hence an E8 W(3,2) can be
embedded abstractly, but the Leech quotient alone does not select a canonical one.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS8225_8232_LEECH_W5_CONTAINS_336_W3_COPIES.json'
V=[tuple((n>>i)&1 for i in range(6)) for n in range(1,64)]

def om(a,b):return (a[0]*b[3]+a[1]*b[4]+a[2]*b[5]+a[3]*b[0]+a[4]*b[1]+a[5]*b[2])&1
def add(a,b):return tuple(x^y for x,y in zip(a,b))

def main():
    planes=set()
    for a,b in itertools.combinations(V,2):
        if om(a,b):planes.add(frozenset((a,b,add(a,b))))
    assert len(planes)==336
    copies=[]
    for P in planes:
        W=frozenset(v for v in V if all(om(v,u)==0 for u in P));assert len(W)==15;copies.append(W)
    assert len(set(copies))==336
    ih=Counter(len(A&B) for A,B in itertools.combinations(copies,2));assert ih==Counter({3:48720,7:7560})
    sp6=2**9*(2**2-1)*(2**4-1)*(2**6-1);sp4=2**4*(2**2-1)*(2**4-1);sp2=2*(2**2-1)
    assert sp6==1451520 and sp4==720 and sp2==6 and sp6//(sp4*sp2)==336
    out={'schema':'w33.pass8225_8232.leech_w5_contains_336_w3_copies.v1','status':'PASS','passes':'8225-8232',
      'dependency':'Parallel Pass8022-8029: actual Leech W(23,2)->W(11,2)->W(5,2) tower',
      'ambient':'W(5,2) on F2^6 / 63 projective points','subgeometry':'W(3,2) on a nondegenerate F2^4 / 15 points',
      'copies':336,'construction':'orthogonal complements of the 336 nondegenerate symplectic 2-planes in F2^6',
      'pairwise_point_intersections':{'3':48720,'7':7560},
      'Sp6_2_order':sp6,'stabilizer':'Sp4(2) x Sp2(2)','stabilizer_order':sp4*sp2,'orbit_index':336,
      'canonicality':'Sp6(2) is transitive on all 336 copies, so the bare Leech W(5,2) carrier selects no distinguished E8 W(3,2). An objectwise E8-in-Leech identification requires extra lattice/controller data.',
      'theorem':'The three-qubit Leech quotient contains exactly 336 two-qubit W(3,2) subgeometries, one Sp6(2) orbit. Thus E8 W(3,2) is abstractly embeddable but not canonically selected by the Leech symplectic quotient alone.',
      'claim_boundary':'Exact finite symplectic geometry; no specific E8 sublattice of the Leech lattice is asserted.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','W3_copies':336,'canonical':False}))
if __name__=='__main__':main()
