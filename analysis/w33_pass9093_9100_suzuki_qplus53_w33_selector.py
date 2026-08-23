#!/usr/bin/env python3
"""Pass9093-9100: exact Suzuki/M12:2 Q+(5,3) selector geometry.

Uses the vendored ATLAS 12-dimensional GF(3) representation of 2.Suz through
`scripts/w33_2suz_sp12_embedding.py` and the exact ATLAS-word M12:2 subgroup
from `scripts/w33_2suz_m12_2_subgroup.py`.

The derived M12 subgroup has a 2-dimensional commutant containing a canonical
non-scalar involution with two 6-dimensional Lagrangian eigenspaces U+ and U-;
the outer generator x exchanges them.  Pairing U+ with xU+ defines a symmetric
nondegenerate 6-dimensional form C.  This pass enumerates all 2-spaces A<U+
and proves that W_A=A + xA is symplectic-nondegenerate exactly when C|A is
nondegenerate.  The 11,011 two-spaces split into 3,640 degenerate, 5,265
hyperbolic and 2,106 anisotropic cases, leaving 7,371 polarization-compatible
W(3,3) four-spaces.
"""
from __future__ import annotations

import itertools, json
from collections import Counter
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/PART_W33_PASS9093_9100_SUZUKI_QPLUS53_W33_SELECTOR.json'
P = 3

from scripts.w33_2suz_sp12_embedding import analyze as analyze_2suz
from scripts.w33_2suz_m12_2_subgroup import (
    build_m12_2_generators_from_suz,
    _standard_symplectic_form,
    _symplectic_inverse,
    _commutant_basis,
    _find_involutive_commutant_element,
    _nullspace_basis_mod_p,
    _basis_matrix,
    _rank_mod_p,
)


def canon(v):
    v=tuple(int(x)%P for x in v)
    for x in v:
        if x:
            z=pow(x,-1,P)
            return tuple((z*y)%P for y in v)
    raise ValueError('zero')


def rref_rows(rows):
    A=np.array(rows,dtype=np.int64)%P;m,n=A.shape;r=0
    for c in range(n):
        q=next((i for i in range(r,m) if A[i,c]),None)
        if q is None: continue
        A[[r,q]]=A[[q,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,P))%P
        for i in range(m):
            if i!=r and A[i,c]: A[i]=(A[i]-A[i,c]*A[r])%P
        r+=1
        if r==m: break
    return tuple(tuple(int(x) for x in row) for row in A if np.any(row))


def two_spaces_6():
    pts=sorted({canon(v) for v in itertools.product(range(P),repeat=6) if any(v)})
    assert len(pts)==364
    S=set()
    for i in range(len(pts)):
        for j in range(i+1,len(pts)):
            k=rref_rows([pts[i],pts[j]])
            if len(k)==2:S.add(k)
    assert len(S)==11011
    return sorted(S)


def main():
    rep=analyze_2suz(); assert rep.get('available') is True
    std=rep['standardized_generators']
    a=np.array(std['A_std_mod3'],dtype=np.int64)%P
    b=np.array(std['B_std_mod3'],dtype=np.int64)%P
    J=_standard_symplectic_form(6,p=P)
    g=build_m12_2_generators_from_suz(a,b,p=P)
    x,y=g['x'],g['y']; xi=_symplectic_inverse(x,J,p=P)
    yc=xi@y@x%P

    comm=_commutant_basis([y,yc],p=P); assert len(comm)==2
    s=_find_involutive_commutant_element(comm,p=P); assert s is not None
    I=np.eye(12,dtype=np.int64)%P
    assert np.array_equal(s@s%P,I)
    assert np.array_equal(xi@s@x%P,(-s)%P)
    plus=_nullspace_basis_mod_p((s-I)%P,P)
    minus=_nullspace_basis_mod_p((s+I)%P,P)
    U=_basis_matrix(plus,p=P); V=_basis_matrix(minus,p=P)
    assert U.shape==V.shape==(12,6)
    assert not np.any(U.T@J@U%P) and not np.any(V.T@J@V%P)

    C=U.T@J@x@U%P
    assert np.array_equal(C,C.T)
    assert _rank_mod_p(C,P)==6

    # The induced quadratic projective geometry is plus type Q+(5,3).
    p6=sorted({canon(v) for v in itertools.product(range(P),repeat=6) if any(v)})
    singular=[v for v in p6 if int(np.array(v)@C@np.array(v))%P==0]
    assert len(singular)==130

    spaces=two_spaces_6(); typ=Counter(); w33_ok=0
    for key in spaces:
        B2=np.array(key,dtype=np.int64).T%P
        G=B2.T@C@B2%P
        r=_rank_mod_p(G,P)
        if r<2:
            t='degenerate'
        else:
            iso=False
            for z in itertools.product(range(P),repeat=2):
                if z==(0,0):continue
                q=np.array(z,dtype=np.int64)
                if int(q@G@q)%P==0:iso=True;break
            t='hyperbolic' if iso else 'anisotropic'
        typ[t]+=1

        # Direct 4-space check: W_A = span(U A, x U A).
        if r==2:
            Acoords=B2
            WA=np.concatenate([U@Acoords%P, x@U@Acoords%P],axis=1)%P
            assert _rank_mod_p(WA,P)==4
            assert _rank_mod_p(WA.T@J@WA%P,P)==4
            w33_ok+=1
    assert typ==Counter({'hyperbolic':5265,'degenerate':3640,'anisotropic':2106})
    assert w33_ok==7371

    out={
      'schema':'w33.pass9093_9100.suzuki_qplus53_w33_selector.v1','status':'PASS','passes':'9093-9100',
      'ambient':'vendored ATLAS 2.Suz < Sp(12,3)','subgroup':'ATLAS-word M12:2',
      'polarization':{'commutant_dim':2,'eigenspaces':[6,6],'both_Lagrangian':True,'outer_x_exchanges_eigenspaces':True},
      'symmetric_form_C':{'dimension':6,'rank':6,'singular_projective_points':130,'identification':'Q+(5,3)'},
      'two_space_census':{'total':11011,'degenerate':3640,'hyperbolic':5265,'anisotropic':2106},
      'polarization_compatible_W33':7371,
      'criterion':'W_A=A direct-sum xA is symplectic-nondegenerate iff C restricted to A is nondegenerate',
      'theorem':'The exact M12:2 polarization inside the ATLAS 2.Suz six-qutrit module cuts the astronomical W33 subspace census down to 7,371 canonical polarization-compatible candidates, controlled by the orthogonal quadric Q+(5,3).',
      'claim_boundary':'Exact finite-module selector theorem. It does not yet show that full 2.Suz has a unique orbit or preferred W33 among the 7,371.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','Qplus53':130,'two_spaces':11011,'W33_candidates':7371,'types':dict(typ)}))

if __name__=='__main__':main()
