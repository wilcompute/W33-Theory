#!/usr/bin/env python3
"""H27 automorphisms and the four projective torsion-gerbe clock directions.

Finite arithmetic is exact over F3. This constructs abstract H27/torsion
module symmetries, not a diffeomorphism, metric or physical time operator.
"""
import itertools
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import toe_20261119_h27_integral_torsion_gerbes as source

F=range(3)
MATRICES=[(a,b,c,d) for a,b,c,d in itertools.product(F,repeat=4)
          if (a*d-b*c)%3!=0]
def determinant(M):
    a,b,c,d=M
    return (a*d-b*c)%3
SL2=[M for M in MATRICES if determinant(M)==1]
GL2=[M for M in MATRICES if determinant(M)!=0]

def transform(M,g):
    """Center-scaled Heisenberg automorphism, Weyl-symmetric coordinates."""
    a,b,c=g
    u,v=(M[0]*a+M[1]*b)%3,(M[2]*a+M[3]*b)%3
    det=determinant(M)
    t=(c-2*a*b)%3
    return (u,v,(det*t+2*u*v)%3)

def ray(v):
    assert v!=(0,0)
    return min(v,((-v[0])%3,(-v[1])%3))

RAYS=sorted({ray((a,b)) for a,b in itertools.product(F,repeat=2)
             if (a,b)!=(0,0)})
INDEX={v:i for i,v in enumerate(RAYS)}

def dual_action(M,v):
    """Pullback on H1 base; H3 torsion also carries a determinant twist."""
    x,y=v
    return ((M[0]*x+M[2]*y)%3,(M[1]*x+M[3]*y)%3)

def torsion_action(M,v):
    """H3 torsion cup classes transform by det(M) times the H1 pullback.
    Because a cup b=3*eta, eta picks up the determinant sign.
    """
    x,y=dual_action(M,v)
    d=determinant(M)
    return (d*x%3,d*y%3)

def ray_permutation(M):
    return tuple(INDEX[ray(torsion_action(M,v))] for v in RAYS)

def sign(perm):
    n=sum(perm[i]>perm[j] for i in range(len(perm))
          for j in range(i+1,len(perm)))
    return (-1)**n

def certify():
    assert len(GL2)==48 and len(SL2)==24
    assert len(RAYS)==4
    identity=(1,0,0,1)
    minus=(2,0,0,2)
    assert ray_permutation(identity)==tuple(range(4))
    assert ray_permutation(minus)==tuple(range(4))
    for M in GL2:
        assert transform(M,source.C)==(0,0,determinant(M))
        for g in source.GROUP:
            for h in source.GROUP:
                assert transform(M,source.multiply(g,h))==source.multiply(
                    transform(M,g),transform(M,h))
    all_actions={ray_permutation(M) for M in GL2}
    even_actions={ray_permutation(M) for M in SL2}
    assert len(all_actions)==24 and len(even_actions)==12
    assert all(sign(ray_permutation(M))==(1 if determinant(M)==1 else -1)
               for M in GL2)
    assert {ray(dual_action(M,RAYS[0])) for M in SL2}==set(RAYS)
    gl_kernel=[M for M in GL2 if ray_permutation(M)==tuple(range(4))]
    sl_kernel=[M for M in SL2 if ray_permutation(M)==tuple(range(4))]
    assert set(gl_kernel)=={identity,minus}
    assert set(sl_kernel)=={identity,minus}
    return dict(status="PASS",
                source_torsion_H3="(Z/3)^2",
                nonzero_torsion_classes=8,
                projective_torsion_rays=[list(v) for v in RAYS],
                projective_correspondence="P1(F3): four Hesse/MUB clock labels",
                exact_H27_automorphisms=len(GL2),
                center_preserving_automorphisms=len(SL2),
                center_inverting_automorphisms=len(GL2)-len(SL2),
                center_preserving_projective_image="A4, order 12",
                full_projective_image="S4, order 24",
                central_projective_kernel=["+I","-I"],
                SL2_orbit_on_four_rays=4,
                determinant_to_permutation_parity="det=1 even; det=2 odd",
                H3_torsion_linear_action="det(M) * M^T on (F3)^2",
                scope=["abstract group automorphisms and cohomology module only",
                       "not a canonical choice of a clock or an isometry of Y7",
                       "opposite torsion classes need not be physically equivalent",
                       "no time evolution, field equations, or chiral spectrum derived"])

def main():
    result=certify()
    out=HERE.parents[0]/"data"/"toe_20261119_h27_clifford_torsion_clock.json"
    out.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps({"status":result["status"],"GL2":result["exact_H27_automorphisms"],
                      "A4":result["center_preserving_projective_image"],
                      "S4":result["full_projective_image"],"output":str(out)}))
if __name__=="__main__":
    main()
