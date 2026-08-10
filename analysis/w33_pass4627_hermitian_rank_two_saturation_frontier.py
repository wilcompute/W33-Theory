#!/usr/bin/env python3
"""Pass 4627 -- rational rank closes; the all-q binary problem is 2-saturation.

For Q^-(5,q)=GQ(q,q^2), let N be point-line incidence.  The point graph has
parameters v=(q+1)(q^3+1), k=q(q^2+1), eigenvalues q-1 and -(q^2+1), and
multiplicity q(q^2-q+1) on the negative eigenspace.  Since
NN^T=(q^2+1)I+A, the rational kernel of N^T is exactly that negative eigenspace.
Therefore rank_Q N=q^4+q^2+1 for every prime-power q.

For odd q the remaining conjecture rank_F2 N=rank_Q N is equivalent to a purely
integral statement: the nonzero Smith invariant factors of N are all odd, i.e.
the incidence image lattice is 2-saturated.  Exact q=3,5,7 anchors prove this
locally but no all-q proof is claimed.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4627_HERMITIAN_RANK_TWO_SATURATION_FRONTIER.json'

def main()->int:
    q=sp.symbols('q', positive=True, integer=True)
    v=(q+1)*(q**3+1);k=q*(q**2+1);r=q-1;s=-(q**2+1)
    ms=sp.factor((-k-r*(v-1))/(s-r));mr=sp.factor(v-1-ms)
    rq=sp.factor(v-ms)
    assert sp.expand(ms-q*(q**2-q+1))==0
    assert sp.expand(mr-q**2*(q**2+1))==0
    assert sp.expand(rq-(q**4+q**2+1))==0
    old=json.loads((ROOT/'data/PART_W33_PASS4620_QMINUS_HERMITIAN_BINARY_RANK_REFORMULATION.json').read_text())
    anchors=old['exact_anchors'];assert [x['q'] for x in anchors]==[3,5,7]
    for a in anchors:
        z=a['q'];assert a['candidate_rank_N']==z**4+z**2+1
    out={
      'pass':4627,
      'generalized_quadrangle':{'type':'Q^-(5,q)=GQ(q,q^2), dual to H(3,q^2)','point_count':'(q+1)(q^3+1)','point_graph_degree':'q(q^2+1)','point_graph_eigenvalues':['q-1','-(q^2+1)'],'multiplicities':{'q-1':'q^2(q^2+1)','-(q^2+1)':'q(q^2-q+1)'}},
      'rational_theorem':{'gram':'N N^T=(q^2+1)I+A_point','kernel_Q':'the -(q^2+1) eigenspace','kernel_dimension':'q(q^2-q+1)','rank_Q':'q^4+q^2+1'},
      'binary_equivalences_for_odd_q':['rank_F2(N)=q^4+q^2+1','rank_F2(N)=rank_Q(N)','no nonzero Smith invariant factor of N is even','coker(N) has no 2-primary torsion in its torsion subgroup','the incidence image lattice is 2-saturated'],
      'exact_anchors':anchors,
      'status':'OPEN: prove 2-saturation of the Q^-(5,q)/H(3,q^2) incidence image for every odd q.',
      'literature_boundary':['Arslan--Sin (arXiv:0908.3035) develops defining-characteristic p-rank/module methods for orthogonal and Hermitian incidence geometries; it does not provide this cross-characteristic binary 2-saturation theorem.','De Boeck--Vandendriessche (arXiv:1601.00443) studies the dual code of Hermitian points/generators and small weights, not this binary rank formula.','Sin (arXiv:1401.8210) surveys Smith-normal-form methods and motivates the integral formulation, but no directly applicable all-q Hermitian 2-SNF formula was found in the targeted audit.'],
      'theorem':'The proposed binary rank is not a guessed polynomial: q^4+q^2+1 is the exact rational rank for every q. The only remaining all-odd-q issue is whether reduction modulo two creates extra kernel, equivalently whether the incidence lattice is 2-saturated.',
      'boundary':'Exact symbolic rational theorem plus exact q=3,5,7 binary anchors. The all-q binary equality remains conjectural.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
