#!/usr/bin/env python3
"""Pass5610: turn the old s12/Klein cardinality bridge into an explicit gauge-chosen phase map.

The old exploration/w33_s12_klein_projective_bridge.py established the exact
cardinality chain 728/2=364=|PG(5,3)| and projective Golay weight counts, but it
did not construct a canonical Pluecker/Klein isometry selecting the W33 40-set.
Likewise scripts/s12_sl27_heisenberg_algebra.py explicitly says its nondegenerate
symplectic form on F3^6 is a choice on the systematic Golay labels.

Here we make the choice explicit. Embed W=F3^4 with
 B(x,y)=x0*y1-x1*y0+x2*y3-x3*y2
into the old three-qutrit phase space H=F3^6=(p1,p2,p3,q1,q2,q3) by
 E(x0,x1,x2,x3)=(x0,x2,0,-x1,-x3,0).
For the old convention <u,v>=q.p'-p.q', this is exactly symplectic:
 <E(x),E(y)>=B(x,y).

This is sufficient to place the Pass5609 magnetic phase inside the old s12
Heisenberg machinery without pretending that the embedding is canonical.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5610_S12_W33_SYMPLECTIC_EMBEDDING_FIREWALL.json'

def B(x,y): return (x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2])%3
def E(x): return (x[0]%3,x[2]%3,0,(-x[1])%3,(-x[3])%3,0)
def H(u,v):
    p=u[:3]; qq=u[3:]; p2=v[:3]; q2=v[3:]
    return sum(qq[i]*p2[i]-p[i]*q2[i] for i in range(3))%3

def rank_mod3(rows):
    A=[list(r) for r in rows]; m=len(A); n=len(A[0]); r=0
    for c in range(n):
      piv=next((i for i in range(r,m) if A[i][c]%3),None)
      if piv is None: continue
      A[r],A[piv]=A[piv],A[r]
      z=1 if A[r][c]%3==1 else 2; A[r]=[(z*x)%3 for x in A[r]]
      for i in range(m):
        if i!=r and A[i][c]%3:
          t=A[i][c]%3; A[i]=[(x-t*y)%3 for x,y in zip(A[i],A[r])]
      r+=1
    return r

def main():
    vecs=list(itertools.product(range(3),repeat=4))
    assert all(H(E(x),E(y))==B(x,y) for x in vecs for y in vecs)
    basis=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)]
    imgs=[E(x) for x in basis]; assert rank_mod3(imgs)==4
    radical=[x for x in vecs if all(B(x,y)==0 for y in vecs)]; assert radical==[(0,0,0,0)]
    out={
      'pass':5610,'status':'EXPLICIT_SYMPLECTIC_EMBEDDING_WITH_CANONICITY_FIREWALL',
      'W33_space':'F3^4','s12_Heisenberg_space':'F3^6=(p1,p2,p3,q1,q2,q3)',
      'embedding':'E(x0,x1,x2,x3)=(x0,x2,0,-x1,-x3,0)',
      'W33_form':'x0*y1-x1*y0+x2*y3-x3*y2 mod 3',
      's12_form':'q dot p_prime - p dot q_prime mod 3',
      'all_pair_checks':len(vecs)**2,'embedding_rank':4,'forms_match_exactly':True,
      'old_bridge_audit':{
        'supported':'The old s12 code really has 728 nonzero labels, 364 projective +/- lines, and projective weight counts 132+220+12.',
        'not_supported_by_cardinality_alone':'A canonical projective isometry from those 364 Golay lines to Pluecker PG(5,3), or a canonical identification of a 40-point W33 Klein slice.',
        'reason':'The old Heisenberg symplectic form is an extra nondegenerate choice on systematic F3^6 labels; the ternary Golay code by itself does not choose this particular W33 four-subspace.'
      },
      'bridge_to_5609':'Under E, the Pass5609 edge phase omega^{B(x,y)} is literally the restriction of the old s12 three-qutrit Weyl-Heisenberg phase omega^{<E(x),E(y)>}.',
      'physics_firewall':'This makes the phase dictionary explicit but gauge-chosen. Physical uniqueness would require an independent principle selecting this embedding/subspace.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
