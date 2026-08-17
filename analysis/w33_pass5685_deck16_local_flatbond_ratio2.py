#!/usr/bin/env python3
"""Pass5685: intersect the deck16 BdG cone with the actual magnetic support geometry.

Pass5675 leaves a four-real-dimensional equivariant K-odd cone (Herm_2 on the
multiplicity space), hence one continuous level ratio after scale.  Here we add two
constraints already present in the intrinsic magnetic carrier rather than inventing
a new group:

  (1) geometric locality: preserve the zero/nonzero support pattern of H_mag;
  (2) flat bond magnitude: every nonzero real-skew bond has the same |S_ij|.

The zero-pattern constraint cuts the 4D cone to dimension 2.  In that projective
line, the equal-magnitude equations have exactly two real rays.  Both have fourfold
levels +/-a and +/-2a.  Thus locality + flat magnetic bond strength discretely pins
the absolute ratio 2, while leaving a two-ray chirality/sign-pattern ambiguity.

Projective rays are deduplicated by their 60-bond sign pattern modulo global sign,
not by a floating coordinate.  This makes the certificate stable across NumPy/SVD
versions where one algebraic root can appear as multiple nearby floats.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import w33_pass5630_deck_bdg_commutant_mass_ratio_unprotected as prev
import w33_pass5675_deck16_equivariant_bdg_normal_form as nf
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5685_DECK16_LOCAL_FLATBOND_RATIO2.json'

def cluster(ev,tol=1e-7):
    out=[]
    for x in ev:
        if not out or abs(x-out[-1][0])>tol:out.append([float(x),1])
        else:out[-1][1]+=1
    return out

def main():
    pairs,Rs,H=prev.build();basis=nf.skew_commutant_basis(pairs)
    assert len(basis)==4
    S=(-1j*H).real
    zeros=[];nz=[]
    for i in range(16):
        for j in range(i+1,16):
            (zeros if abs(S[i,j])<1e-8 else nz).append((i,j))
    assert (len(zeros),len(nz))==(60,60)
    Z=np.array([[B[i,j] for B in basis] for i,j in zeros],float)
    _u,s,vh=np.linalg.svd(Z);r=int(np.sum(s>1e-8));assert r==2
    coeff=vh[r:].T;assert coeff.shape==(4,2)
    L=[sum(coeff[j,k]*basis[j] for j in range(4)) for k in range(2)]
    ab=np.array([[L[0][i,j],L[1][i,j]] for i,j in nz])
    a0,b0=ab[0];cands=[]
    for a,b in ab[1:]:
        for sg in (1,-1):
            den=b-sg*b0;num=sg*a0-a
            if abs(den)>1e-10:cands.append(float(num/den))

    raymap={}
    s0=np.sign([S[i,j] for i,j in nz]).astype(int)
    for t in cands:
        vals=ab[:,0]+t*ab[:,1];m=np.abs(vals)
        if m.min()>1e-8 and m.max()-m.min()<1e-7:
            sx=np.sign(vals).astype(int)
            key=tuple(int(x) for x in sx); neg=tuple(-int(x) for x in sx)
            canon=min(key,neg)
            if canon in raymap: continue
            Sx=L[0]+t*L[1];ev=np.linalg.eigvalsh(1j*Sx);cl=cluster(ev)
            assert len(cl)==4 and [z[1] for z in cl]==[4,4,4,4]
            pos=sorted(abs(z[0]) for z in cl if z[0]>0)
            ratio=pos[1]/pos[0]
            corr=abs(np.vdot(Sx.ravel(),S.ravel()))/(np.linalg.norm(Sx)*np.linalg.norm(S))
            disagree=int(np.sum(sx!=s0));disagree=min(disagree,60-disagree)
            raymap[canon]={'t':t,'ratio':float(ratio),'correlation_with_Hmag_ray':float(corr),'bond_sign_disagreements_up_to_global_sign':disagree,'levels':cl}
    sols=sorted(raymap.values(),key=lambda x:x['correlation_with_Hmag_ray'],reverse=True)
    assert len(sols)==2
    assert all(abs(x['ratio']-2)<1e-7 for x in sols)
    assert sols[0]['correlation_with_Hmag_ray']>0.999999
    assert abs(sols[1]['correlation_with_Hmag_ray']-0.6)<1e-6
    out={
      'pass':5685,'status':'LOCAL_SUPPORT_PLUS_FLAT_BONDS_DISCRETELY_PIN_RATIO_TWO_WITH_TWO_RAYS',
      'starting_equivariant_Kodd_dimension':4,
      'magnetic_support':{'zero_undirected_pairs':60,'nonzero_undirected_pairs':60,'nonzero_magnitude':float(np.max(abs(S)))},
      'support_preserving_subspace_dimension':2,
      'projective_flat_bond_rays':sols,
      'ray_deduplication':'canonical 60-bond sign pattern modulo global sign',
      'theorem':'Among stabilizer-equivariant K-odd Hamiltonians, preserving the intrinsic magnetic support and requiring constant nonzero bond magnitude leaves exactly two real projective rays; both have absolute level ratio 2.',
      'interpretation':'The second ray differs from the magnetic sign pattern on 12 of 60 bonds up to global sign. The ratio is geometric-flatness protected, but the discrete ray/chirality choice is not resolved here.',
      'physics_boundary':'This fixes a dimensionless spectral ratio inside the finite carrier model. It does not assign either level to a Standard Model particle, derive the energy scale, or show that flat bond magnitude is the unique microscopic Hamiltonian principle.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
