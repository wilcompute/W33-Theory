#!/usr/bin/env python3
"""Pass7653-7660: the mixed Leech quotient has a canonical dual PG(3,3) interface.

Dependency: Pass7645 proves C=coker(1-g)=(Z/3)^2 x (Z/9)^2 for the fixed-point-
free order-nine Leech automorphism.  For any automorphism g of an integral
unimodular lattice with 1-g nonsingular, the discriminant/linking form

    b([x],[y]) = <(1-g)^(-1)x,y> mod Z

is perfect.  If g is an isometry then b is skew modulo Z; on odd-primary
C it is alternating.  Consequently b induces a perfect F3-bilinear duality

    (C/3C) x C[3] -> (1/3 Z)/Z ~= F3.

Both spaces have dimension four.  Projectivizing therefore gives 40 points on
each side, and orthogonality is the point-hyperplane incidence design of PG(3,3):
a symmetric 2-(40,13,4) design.  This is a canonical 40+40 interface, but it is
not yet a W(3,3) polarity because the two 40-sets are dual spaces, not canonically
identified copies of one symplectic space.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/PART_W33_PASS7645_7652_LEECH_ORDER9_MIXED_TORSION_DUAL40.json'
OUT=ROOT/'data/PART_W33_PASS7653_7660_LEECH_LINKING_DUAL_PG33.json'

def norm(v):
    v=tuple(int(x)%3 for x in v)
    i=next(i for i,x in enumerate(v) if x)
    a=pow(v[i],-1,3)
    return tuple((a*x)%3 for x in v)

def main():
    src=json.loads(SRC.read_text());assert src['status']=='PASS' and src['nontrivial_smith_invariants']=={'3':2,'9':2}
    # Standard model for any perfect duality F3^4 x (F3^4)^*: all such pairings
    # are equivalent under GL(4,3), so these finite incidence parameters are basis-free.
    pts=sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    assert len(pts)==40
    N=np.zeros((40,40),dtype=np.int8)
    for i,x in enumerate(pts):
        for j,y in enumerate(pts):
            if sum(a*b for a,b in zip(x,y))%3==0:N[i,j]=1
    assert set(map(int,N.sum(0)))==set(map(int,N.sum(1)))=={13}
    G=N@N.T
    assert set(map(int,np.diag(G)))=={13}
    assert {int(G[i,j]) for i,j in itertools.combinations(range(40),2)}=={4}
    assert np.array_equal(G,9*np.eye(40,dtype=np.int16)+4*np.ones((40,40),dtype=np.int16))
    sv=np.linalg.svd(N.astype(float),compute_uv=False)
    vals=sorted(round(float(x),8) for x in sv)
    assert vals==[3.0]*39+[13.0]
    # Counts in the canonical 3-adic filtration of C.
    filtration={'3C':(2,4),'C[3]':(4,40),'C[3]/3C':(2,4),'C/3C':(4,40)}
    out={
      'schema':'w33.pass7653_7660.leech_linking_dual_pg33.v1','status':'PASS','passes':'7653-7660',
      'dependency':'Pass7645-7652: C=(Z/3)^2 x (Z/9)^2 for the fixed-point-free Leech order-9 element',
      'linking_form':'b([x],[y])=< (1-g)^(-1)x, y > mod Z; unimodularity gives perfectness and g-isometry gives b(y,x)=-b(x,y) mod Z, hence alternating on odd 3-primary torsion',
      'induced_duality':'(C/3C) x C[3] -> F3 is perfect because (C[3])^perp=3C',
      'filtration':{k:{'F3_dimension':d,'projective_points':p} for k,(d,p) in filtration.items()},
      'projective_interface':{'left':'P(C/3C)','right':'P(C[3])','sizes':[40,40],'incidence':'linking-orthogonality','design':'symmetric 2-(40,13,4)','degree_each_side':13,'incidences':520,'common_duals_for_two_left_points':4,'incidence_singular_values':'13^1 + 3^39'},
      'projective_space_identification':'up to independent projective coordinates the interface is point-hyperplane incidence of PG(3,3)',
      'W33_boundary':'W(3,3) also has 40 points in PG(3,3), but requires a nondegenerate alternating polarity identifying point and dual spaces. Pass7653 does not produce such an identification; the exact output is the dual 40+40 PG(3,3) interface.',
      'theorem':'The corrected non-elementary Leech order-9 quotient canonically retains two 40-point projective boundary layers, paired by the unimodular linking form as PG(3,3) points and hyperplanes.',
      'claim_boundary':'Finite lattice/discriminant-form theorem only.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','design':'2-(40,13,4)','shells':[40,40],'singular_values':[13,3]}))
if __name__=='__main__':main()
