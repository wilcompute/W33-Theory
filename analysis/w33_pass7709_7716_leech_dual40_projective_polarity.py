#!/usr/bin/env python3
"""Pass7709-7716: the Leech mixed-torsion top/socle carry canonical PG(3,3) duality.

Pass7645 proves for the fixed order-9 Co0 witness that
    C = coker(1-g) = (Z/3)^2 x (Z/9)^2,
with top C/3C and socle C[3] both F3^4, while the standard odd-primary
lattice linking pairing is perfect and alternating.

For any perfect bilinear pairing on C, (3C)^perp=C[3] by inclusion plus order.
Hence the pairing descends to a perfect F3-valued pairing
    (C/3C) x C[3] -> F3.
Projectivizing gives the point-hyperplane design PG(3,3): 40+40 objects,
13 incidences per object, lambda=4.  If one additionally identifies top with
socle through a symplectic polarity, the 40x40 incidence matrix becomes
I + A(W(3,3)).  The existence of a *canonical Leech-induced* identification is
NOT asserted; it is isolated as the exact remaining obstruction.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS7709_7716_LEECH_DUAL40_PROJECTIVE_POLARITY.json'

def canon(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:
            u=1 if x==1 else 2
            return tuple((u*y)%3 for y in v)
    raise ValueError('zero vector')

def omega(a,b):
    return (a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2])%3

def main():
    # Pass7645 invariant-factor arithmetic.
    order_C=3**2*9**2;order_3C=3**2;order_socle=3**4;order_top=3**4
    assert order_C==729 and order_3C==9 and order_socle==order_top==81
    # Perfectness gives |H^perp|=|C|/|H|. Since C[3] annihilates 3C by
    # bilinearity and both sets have order 81, (3C)^perp=C[3]. Dually,
    # C[3]^perp=3C. Therefore top x socle is a perfect F3 pairing.
    assert order_C//order_3C==order_socle
    assert order_C//order_socle==order_3C

    P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    assert len(P)==40
    N=np.array([[omega(x,y)==0 for y in P] for x in P],dtype=np.int64)
    assert set(map(int,N.sum(1)))=={13} and set(map(int,N.sum(0)))=={13}
    NN=N@N.T
    assert set(map(int,np.diag(NN)))=={13}
    assert set(map(int,NN[np.triu_indices(40,1)]))=={4}

    # A symplectic polarity identifies the two projective 40-sets. Alternation
    # puts every point on its own polar hyperplane, so A=N-I is W(3,3).
    A=N-np.eye(40,dtype=np.int64)
    assert set(map(int,A.sum(1)))=={12}
    lam=set();mu=set()
    for i in range(40):
      for j in range(i+1,40):
        c=int(A[i]@A[j]);(lam if A[i,j] else mu).add(c)
    assert lam=={2} and mu=={4}

    # Exact spectra follow from the design identity NN^T=9I+4J and from the
    # SRG quadratic relation. We record them without floating-point dependence.
    out={
      'schema':'w33.pass7709_7716.leech_dual40_projective_polarity.v1','status':'PASS','passes':'7709-7716',
      'dependency':'Pass7645-7652: C=(Z/3)^2 x (Z/9)^2 with perfect odd-primary alternating lattice linking pairing',
      'cokernel_order':729,'threeC_order':9,'socle_order':81,'top_order':81,
      'annihilators':{'(3C)^perp':'C[3]','C[3]^perp':'3C'},
      'induced_pairing':'perfect F3 pairing (C/3C) x C[3] -> F3',
      'projective_shells':[40,40],
      'cross_design':{'name':'PG(3,3) point-hyperplane incidence','parameters':'symmetric 2-(40,13,4)','bipartite_vertices':80,'degree':13,'spectrum':'13^1 + 3^39 + (-3)^39 + (-13)^1'},
      'w33_polarity_test':{'after_symplectic_identification':'N = I + A_W33','srg':[40,12,2,4],'spectrum':'12^1 + 2^24 + (-4)^15'},
      'theorem':'The Leech order-9 cokernel canonically supplies two dual PG(3,3) 40-point shells via its linking pairing. Any symplectic polarity identification of top with socle converts the cross-incidence relation into the closed-neighborhood relation of W(3,3).',
      'remaining_obstruction':'Construct, or prove absent, a canonical Leech/Co0-equivariant identification C/3C -> C[3] whose transported cross-pairing is alternating. Without that datum the result is dual PG(3,3), not yet a canonical W(3,3).',
      'claim_boundary':'Exact finite-module/projective-geometry consequence of Pass7645 plus perfect pairing. No Monster or physical claim follows.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','design':'2-(40,13,4)','W33_if_polarity':[40,12,2,4]}))
if __name__=='__main__':main()
