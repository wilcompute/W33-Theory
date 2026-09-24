#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, sys
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_hermitian_3p1_spread_bridge.json"

from analysis.w33_20260924_history_bigcell_q43_compactification import (
    all_points, all_lagrangian_lines, wedge5, q43, canon,
)

P=3

def qh(v):
    a,c,x,y=v
    return (a*c-x*x-y*y)%3

def phi(v):
    a,c,x,y=v
    return canon((a,x,y,-x,-c))
def projective4():
    return sorted({
        canon(v) for v in itertools.product(range(3),repeat=4) if any(v)
    })

def projective5():
    return sorted({
        canon(v) for v in itertools.product(range(3),repeat=5) if any(v)
    })

def hyperplane_points(h,qpts):
    return [
        x for x in qpts
        if sum(h[i]*x[i] for i in range(5))%3==0
    ]

def skew_spread(lines):
    return (
        len(lines)==10
        and all(not(set(A)&set(B)) for A,B in itertools.combinations(lines,2))
        and len(set().union(*(set(L) for L in lines)))==40
    )

def enumerate_spreads(lines,pts):
    pidx={p:i for i,p in enumerate(pts)}
    lids_by_point={i:[] for i in range(40)}
    masks=[]
    for li,L in enumerate(lines):
        mask=0
        for p in L:
            j=pidx[p]
            mask|=1<<j
            lids_by_point[j].append(li)
        masks.append(mask)
    full=(1<<40)-1
    out=set()

    def rec(covered,chosen):
        if covered==full:
            out.add(tuple(sorted(chosen)))
            return
        p=next(i for i in range(40) if not (covered>>i)&1)
        for li in lids_by_point[p]:
            if masks[li]&covered:
                continue
            rec(covered|masks[li],chosen+[li])

    rec(0,[])
    return sorted(out)

def no_compatible_complex_structure():
    B=np.array([
        [0,1,0,0],
        [1,0,0,0],
        [0,0,1,0],
        [0,0,0,1],
    ],dtype=int)%3
    good=[]
    for z in itertools.product(range(3),repeat=6):
        K=np.zeros((4,4),dtype=int)
        k=0
        for i in range(4):
            for j in range(i+1,4):
                K[i,j]=z[k]
                K[j,i]=(-z[k])%3
                k+=1
        # K represents the alternating form Omega; J=-B*K because
        # Omega(x,y)=B(Jx,y) has matrix J^T B = K.
        J=(-B@K)%3
        if np.array_equal((J@J)%3,2*np.eye(4,dtype=int)%3):
            good.append(J.tolist())
    return B,good

def main():
    vecs=list(itertools.product(range(3),repeat=4))
    affine_hist=Counter(qh(v) for v in vecs)
    assert affine_hist==Counter({0:21,1:30,2:30})

    p4=projective4()
    proj_hist=Counter(qh(v) for v in p4)
    assert proj_hist==Counter({0:10,1:15,2:15})

    lines=all_lagrangian_lines()
    pts=all_points()
    coords={wedge5(L):L for L in lines}
    assert len(lines)==len(coords)==40
    qpts=sorted(coords)
    assert all(q43(x)==0 for x in qpts)

    H=(0,1,0,1,0)
    section=hyperplane_points(H,qpts)
    assert len(section)==10
    assert all((x[1]+x[3])%3==0 for x in section)

    herm_null={phi(v) for v in p4 if qh(v)==0}
    assert herm_null==set(section)
    for v in p4:
        assert q43(phi(v))==(-qh(v))%3

    spread_lines=[coords[x] for x in section]
    assert skew_spread(spread_lines)

    all_hyp=projective5()
    sec_hist=Counter()
    elliptic=[]
    for h in all_hyp:
        s=hyperplane_points(h,qpts)
        sec_hist[len(s)]+=1
        if len(s)==10:
            elliptic.append((h,s))
    assert sec_hist==Counter({16:45,13:40,10:36})
    section_spreads=set()
    lidx={L:i for i,L in enumerate(lines)}
    for h,s in elliptic:
        SL=[coords[x] for x in s]
        assert skew_spread(SL)
        section_spreads.add(tuple(sorted(lidx[L] for L in SL)))
    assert len(section_spreads)==36

    spreads=enumerate_spreads(lines,pts)
    assert len(spreads)==36
    assert set(spreads)==section_spreads

    B,goodJ=no_compatible_complex_structure()
    assert len(goodJ)==0
    detB=int(round(np.linalg.det(B)))%3
    assert detB==2

    out={
      "schema":"w33.20260924.hermitian_3p1_spread_bridge.v1",
      "status":"PASS_HERMITIAN_3P1_ELLIPTIC_SECTION_SPREAD_WITH_J_NOGO",
      "hermitian_space":{
        "field_model":"F9=F3[u]/(u^2+1), u^2=-1",
        "matrix":"[[a,z],[conj(z),c]], z=x+u*y",
        "determinant":"Q_H(a,c,x,y)=a*c-x^2-y^2",
        "affine_event_count":81,
        "affine_norm_counts":{str(k):v for k,v in sorted(affine_hist.items())},
        "projective_direction_count":40,
        "projective_norm_counts":{str(k):v for k,v in sorted(proj_hist.items())},
      },
      "q43_embedding":{
        "Q43":"x0*x4-x1*x3+x2^2=0",
        "elliptic_hyperplane":"x1+x3=0",
        "map":"Phi(a,c,x,y)=[a,x,y,-x,-c]",
        "identity":"Q43(Phi(v))=-Q_H(v)",
        "null_projective_points":10,
        "hyperplane_section_census":{
          "elliptic_10":sec_hist[10],
          "tangent_13":sec_hist[13],
          "hyperbolic_16":sec_hist[16],
        },
      },
      "spread_bridge":{
        "representative_section_hyperplane":list(H),
        "representative_spread_line_indices":sorted(lidx[L] for L in spread_lines),
        "pairwise_skew":True,
        "covered_W33_points":40,
        "elliptic_sections":len(section_spreads),
        "independent_exact_cover_spreads":len(spreads),
        "section_spreads_equal_all_W33_spreads":True,
      },
      "complex_structure_nogo":{
        "polarization_matrix":B.tolist(),
        "polarization_determinant_mod3":detB,
        "candidate_space_size":3**6,
        "conditions":["J^2=-I","Omega(x,y)=B(Jx,y) alternating"],
        "solutions":len(goodJ),
        "conclusion":(
          "The direct compatibility ansatz Omega=B(J.,.) has no solution. "
          "The causal and symplectic geometries meet instead through the "
          "elliptic-section/Q43/W33-line duality."
        ),
      },
      "theorem":(
        "Herm_2(F9) is a four-dimensional F3 quadratic space with 81 affine "
        "events split 21+30+30 by determinant. Its ten projective null directions "
        "embed explicitly as the elliptic hyperplane section x1+x3=0 of the "
        "already-certified Q(4,3) Lagrangian compactification. Under the Plucker "
        "dictionary those ten Q43 points are ten pairwise-skew W33 lines covering "
        "all forty W33 points, hence a spread. All 36 elliptic sections reproduce "
        "exactly all 36 W33 spreads. The stronger single-complex-structure ansatz "
        "Omega=B(J.,.) is impossible: exhaustive search of all 729 B-skew "
        "candidates finds no J with J^2=-I."
      ),
      "boundary":(
        "The spread bridge is exact finite geometry. It does not by itself turn "
        "the determinant classes into continuum timelike/spacelike sectors or "
        "supply a measured Lorentzian spacetime."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "affine":out["hermitian_space"]["affine_norm_counts"],
      "projective":out["hermitian_space"]["projective_norm_counts"],
      "hyperplanes":out["q43_embedding"]["hyperplane_section_census"],
      "spreads":out["spread_bridge"]["elliptic_sections"],
      "J_solutions":out["complex_structure_nogo"]["solutions"],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
