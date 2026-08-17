#!/usr/bin/env python3
"""Pass5692: resolve the two flat-bond deck16 rays by an exact carrier-centralizer duality.

Pass5685 leaves two projective stabilizer-equivariant K-odd Hamiltonian rays after
imposing the magnetic support and flat nonzero bond magnitude.  This pass finds an
exact diagonal involution D on the 4x4 Segre carrier,

    D = diag(+,+,+,+,-,-,-,-,-,-,-,-,+,+,+,+),

which commutes with every element of the 96-element signed vector stabilizer but is
not itself in that group.  On P1(F3)xP1(F3), D depends only on the first coordinate
u=(u0,u1): d(u)=+1 when u0^2+u1^2=1 mod3 and -1 when it equals 2.

After normalizing the two flat-bond rays to unit nonzero bond magnitude,

    H_2 = - D H_1 D.

Because ordinary conjugation K is particle-hole on these purely imaginary
Hamiltonians, the antiunitary D K sends H_1 to H_2.  Thus the two rays are an exact
centralizer/PHS dual pair, not two unrelated spectra.  If this kinematic duality is
included in the equivalence relation, the flat-bond ratio-two orbit is unique.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import w33_pass5630_deck_bdg_commutant_mass_ratio_unprotected as prev
import w33_pass5675_deck16_equivariant_bdg_normal_form as nf
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5692_DECK16_FLATRAY_DUALITY.json'

def flat_rays(pairs,H):
    basis=nf.skew_commutant_basis(pairs);S=(-1j*H).real
    zeros=[];nz=[]
    for i in range(16):
      for j in range(i+1,16):
        (zeros if abs(S[i,j])<1e-8 else nz).append((i,j))
    Z=np.array([[B[i,j] for B in basis] for i,j in zeros],float)
    _u,s,vh=np.linalg.svd(Z);r=int(np.sum(s>1e-8));assert r==2
    coeff=vh[r:].T;L=[sum(coeff[j,k]*basis[j] for j in range(4)) for k in range(2)]
    ab=np.array([[L[0][i,j],L[1][i,j]] for i,j in nz]);a0,b0=ab[0]
    cands=[]
    for a,b in ab[1:]:
      for sg in (1,-1):
        den=b-sg*b0;num=sg*a0-a
        if abs(den)>1e-10:cands.append(float(num/den))
    raymap={}
    for t in cands:
      vals=ab[:,0]+t*ab[:,1];m=np.abs(vals)
      if m.min()>1e-8 and m.max()-m.min()<1e-7:
        signs=np.sign(vals).astype(int);key=tuple(signs);neg=tuple(-signs);canon=min(key,neg)
        if canon not in raymap:
          X=L[0]+t*L[1]; X=X/np.max(np.abs([X[i,j] for i,j in nz]))
          corr=abs(np.vdot(X.ravel(),S.ravel()))/(np.linalg.norm(X)*np.linalg.norm(S))
          raymap[canon]=(corr,X)
    rays=sorted(raymap.values(),reverse=True,key=lambda z:z[0]);assert len(rays)==2
    return S/np.max(np.abs([S[i,j] for i,j in nz])),rays,nz

def main():
    pairs,Rs,H=prev.build();S0,rays,nz=flat_rays(pairs,H)
    assert rays[0][0]>0.999999 and abs(rays[1][0]-0.6)<1e-6
    S1=rays[0][1]
    if np.vdot(S1,S0).real<0:S1=-S1
    S2=rays[1][1]

    d=np.array([1]*4+[-1]*8+[1]*4,dtype=int);D=np.diag(d)
    assert np.array_equal(D@D,np.eye(16,dtype=int))
    assert max(np.max(abs(D@R-R@D)) for R in Rs)==0
    idperm=tuple(range(16));dpair=(idperm,tuple(int(x) for x in d))
    assert dpair not in set(pairs)
    enlarged=prev.pair_closure(list(pairs)+[dpair]);assert len(enlarged)==192

    target=-D@S1@D
    if np.linalg.norm(S2-target)>np.linalg.norm(-S2-target):S2=-S2
    assert np.max(abs(S2-target))<1e-7
    H1=1j*S1;H2=1j*S2
    # Antiunitary A=D K acts by A H A^-1 = D conj(H) D.
    assert np.max(abs(H2-D@H1.conj()@D))<1e-7
    ev1=np.linalg.eigvalsh(H1);ev2=np.linalg.eigvalsh(H2)
    assert np.max(abs(ev1-ev2))<1e-7
    # The projective sign disagreement remains 12/60 up to global sign.
    a=np.sign([S1[i,j] for i,j in nz]);b=np.sign([S2[i,j] for i,j in nz])
    dis=int(np.sum(a!=b));dis=min(dis,60-dis);assert dis==12

    P=prev.core.p1()
    row_sign=[]
    for u in P:
      q=(u[0]*u[0]+u[1]*u[1])%3
      row_sign.append(1 if q==1 else -1)
    assert row_sign==[1,-1,-1,1]

    out={
      'pass':5692,'status':'TWO_FLAT_BOND_RAYS_ARE_EXACT_CENTRALIZER_PARTICLE_HOLE_DUALS',
      'centralizer_involution':{
        'D_diagonal':d.tolist(),'D_squared':'I_16','commutes_with_all_signed_stabilizer_elements':True,
        'D_in_signed_stabilizer':False,'group_order_after_adjoining_D':192,
        'P1_row_rule':'d(u)=+1 if u0^2+u1^2=1 mod3, -1 if u0^2+u1^2=2 mod3',
        'P1_row_signs':row_sign
      },
      'ray_identity':'after unit flat-bond normalization, H2 = - D H1 D',
      'antiunitary_identity':'with K=ordinary conjugation, (D K) H1 (D K)^-1 = H2',
      'bond_sign_disagreements_up_to_global_sign':dis,
      'shared_spectrum':[float(x) for x in ev1],
      'conclusion':'The discrete two-ray ambiguity left by Pass5685 is an exact kinematic duality orbit. Modulo the carrier-centralizer involution together with particle-hole conjugation, there is one flat-bond ratio-two class.',
      'physics_boundary':'D is an exact carrier centralizer that maps one Hamiltonian to the other; this does not by itself make D a physical gauge symmetry, select a Standard Model particle assignment, or fix the overall energy scale.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
