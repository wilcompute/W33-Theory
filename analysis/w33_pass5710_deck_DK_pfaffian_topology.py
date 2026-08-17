#!/usr/bin/env python3
"""Pass5710 bonkers: Pfaffian/Z2 test of the magnetic DK duality.

Each flat-bond ray is a gapped purely imaginary Hermitian H=iS with S real skew,
so ordinary conjugation K is a particle-hole operation with K^2=+1. In a fixed
Majorana basis the finite 0D class-D diagnostic is the Pfaffian parity of S.

Pass5692 gives S2=-D S1 D with D diagonal, D^2=1 and eight negative entries, so
det(D)=+1. For a 16x16 skew matrix,
  Pf(S2)=Pf(-D S1 D)=(-1)^8 det(D) Pf(S1)=Pf(S1).
Thus DK does not separate the two rays by Pfaffian parity. Moreover D neither
commutes nor anticommutes with one ray: DK is a duality between H1 and H2, not a
chiral or antiunitary symmetry of a single Hamiltonian. No new protected Z2
phase distinction appears from D.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import w33_pass5630_deck_bdg_commutant_mass_ratio_unprotected as core
import w33_pass5692_deck16_flatray_duality as dual
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5710_DECK_DK_PFAFFIAN_TOPOLOGY.json'

def pfaffian(A,tol=1e-12):
    A=np.array(A,dtype=float,copy=True);n=A.shape[0];assert n%2==0 and np.max(abs(A+A.T))<1e-8
    pf=1.0
    for k in range(0,n-1,2):
      j=max(range(k+1,n),key=lambda q:abs(A[k,q]))
      if abs(A[k,j])<tol:return 0.0
      if j!=k+1:
        A[[k+1,j],:]=A[[j,k+1],:];A[:,[k+1,j]]=A[:,[j,k+1]];pf*=-1
      a=A[k,k+1];pf*=a
      for i in range(k+2,n):
        for j2 in range(i+1,n):
          A[i,j2]-=(A[k,i]*A[k+1,j2]-A[k,j2]*A[k+1,i])/a
          A[j2,i]=-A[i,j2]
    return float(pf)

def main():
    pairs,Rs,H=core.build();_S0,rays,nz=dual.flat_rays(pairs,H)
    S1=rays[0][1];S2=rays[1][1]
    d=np.array([1]*4+[-1]*8+[1]*4,float);D=np.diag(d)
    target=-D@S1@D
    if np.linalg.norm(S2-target)>np.linalg.norm(-S2-target):S2=-S2
    assert np.max(abs(S2-target))<1e-7 and round(np.linalg.det(D))==1
    p1=pfaffian(S1);p2=pfaffian(S2)
    assert abs(p1)>1e-7 and abs(p2)>1e-7
    assert np.sign(p1)==np.sign(p2) and abs(abs(p1)-abs(p2))<1e-5
    detres1=abs(np.linalg.det(S1)-p1*p1);detres2=abs(np.linalg.det(S2)-p2*p2)
    assert detres1<1e-4 and detres2<1e-4
    H1=1j*S1;H2=1j*S2
    phs=float(np.linalg.norm(H1.conj()+H1));assert phs<1e-9
    comm=float(np.linalg.norm(D@H1-H1@D));anti=float(np.linalg.norm(D@H1+H1@D))
    assert comm>1e-6 and anti>1e-6
    dk_map=float(np.linalg.norm(H2-D@H1.conj()@D));assert dk_map<1e-7
    ev=np.linalg.eigvalsh(H1);gap=float(min(abs(ev)));assert gap>1e-6
    out={
      'pass':5710,'status':'DK_DUAL_FLAT_RAYS_HAVE_IDENTICAL_PFAFFIAN_PARITY__NO_D_PROTECTED_TOPOLOGICAL_SPLIT',
      'single_ray_structure':{'H':'i S with S real skew','K_particle_hole_residual':phs,'K_squared':'+1','finite_gap':gap},
      'D':{'negative_diagonal_entries':8,'determinant':1,'commutator_norm_with_H1':comm,'anticommutator_norm_with_H1':anti},
      'DK_duality_residual':dk_map,
      'pfaffians':{'ray1':p1,'ray2':p2,'same_sign_in_canonical_basis':True,'det_minus_pf2_residual_ray1':detres1,'det_minus_pf2_residual_ray2':detres2},
      'exact_reason':'S2=-D S1 D, dimension16 gives Pf(-A)=(-1)^8 Pf(A)=Pf(A), and det(D)=+1 gives Pf(D A D)=Pf(A). Therefore the two rays have identical Pfaffian parity.',
      'topology_result':'D is not a chiral symmetry of H1 and DK does not preserve H1; it exchanges H1 and H2. Hence D/DK supplies a duality orbit, not a protected topological distinction between the two magnetic rays.',
      'basis_boundary':'An absolute Pfaffian sign depends on orientation of the chosen Majorana basis; the relative equality under the orientation-preserving D is invariant for this comparison.',
      'physics_boundary':'Calling the finite carrier a physical BdG system or assigning an Altland-Zirnbauer topological phase still requires a fermionic/Majorana realization. This pass establishes only the finite skew-Hamiltonian diagnostic.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
