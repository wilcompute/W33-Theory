#!/usr/bin/env python3
"""Pass5211 (bonkers): the odd-q P-component graph is the classical NO_5^+(q).

Let V be the 4D symplectic module with form omega.  For odd q, the quotient

  M = Lambda^2 V / <omega>

is 5-dimensional and carries the standard nondegenerate orthogonal form coming
from the exterior-square/Pfaffian quadratic form.  This is the classical
exceptional identification PSp4(q) ~= P Omega5(q).

A non-isotropic projective line H=<x,y> in PG(V) determines the decomposable
bivector x wedge y.  If H^perp is its symplectic polar line, then after choosing
compatible area forms one has

  [wedge(H^perp)] = -[wedge(H)] in M,

because their sum is the symplectic form omega.  Therefore the unordered polar
pair {H,H^perp}, exactly a P component by Pass5187, determines one projective
nonisotropic point of M.  The relevant norm class is the plus class.  Conversely
a plus-type nonisotropic projective point lifts to such a nondegenerate 2-space,
so this is a bijection.

Under this bijection, the Pass5203 relation 'dual grids meet in two W-points'
is the standard nonorthogonality relation on the plus-type nonisotropic points.
Thus the P-component block graph is NO_5^+(q).  Its standard rank-3 parameters
are exactly the Pass5203 formulas.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5211_ODDQ_PBLOCK_NO5PLUS.json'

def params(q):
    return {'vertices':q*q*(q*q+1)//2,'degree':(q+1)*(q*q-1),
      'lambda':3*q*q-q-2,'mu':2*q*(q+1),
      'eigenvalues':[ (q+1)*(q*q-1), q*q-2*q-1, -(q+1)]}

def main():
    assert params(5)=={'vertices':325,'degree':144,'lambda':68,'mu':60,
                       'eigenvalues':[144,14,-6]}
    out={'pass':5211,'status':'THEOREM_ODDQ_P_COMPONENT_GRAPH_IS_NO5PLUS',
      'domain':'odd prime powers q',
      'orthogonal_module':'M=Lambda^2(F_q^4)/<omega>, dimension 5, with the exterior-square quadratic form.',
      'exceptional_identification':'PSp4(q) acts on M as P Omega5(q).',
      'vertex_map':'A P component {H,H^perp} maps to the projective class of wedge(H); wedge(H^perp) is its negative modulo omega, so the polar pair is one orthogonal point.',
      'vertex_class':'plus-type nonisotropic projective points of M',
      'adjacency':'Two P components intersect in two W-points iff the corresponding plus-type orthogonal points are in the standard NO_5^+(q) nonorthogonality relation.',
      'graph':'NO_5^+(q)',
      'parameters':'SRG(q^2(q^2+1)/2,(q+1)(q^2-1),3q^2-q-2,2q(q+1))',
      'q5':params(5),
      'connection':'The 325-coordinate q5 footprint code is therefore a binary code on a classical orthogonal rank-3 graph, opening the orthogonal-module/code literature to the d=25 problem.',
      'boundary':'Odd characteristic theorem; no even-q identification is asserted in this quotient form, and the graph identification alone does not prove footprint d=25.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
