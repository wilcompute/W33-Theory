#!/usr/bin/env python3
"""Pass5727 and bonkers Pass5730: exact qutrit Heisenberg bridge for affine torsion."""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT7=ROOT/'data/PART_W33_PASS5727_TORSION_E8_FAMILY_HEISENBERG_INTERTWINER.json'
OUT30=ROOT/'data/PART_W33_PASS5730_HEISENBERG_QUTRIT_GL23_EXTENDED_CLIFFORD.json'

def key(A):return tuple(np.round(A.real,10).ravel())+tuple(np.round(A.imag,10).ravel())
def closure(gens):
 I=np.eye(gens[0].shape[0],dtype=complex);seen={key(I):I};todo=[I]
 while todo:
  A=todo.pop()
  for G in gens:
   B=A@G;k=key(B)
   if k not in seen:seen[k]=B;todo.append(B)
 return list(seen.values())
def phase_res(A,B):
 ij=np.argwhere(np.abs(B)>1e-9)[0];i,j=map(int,ij);p=A[i,j]/B[i,j]
 return p,float(np.linalg.norm(A-p*B))
def commutant_dim(gens,n=3,tol=1e-9):
 if not gens:return n*n
 A=np.vstack([np.kron(G.T,np.eye(n))-np.kron(np.eye(n),G) for G in gens])
 return n*n-int(np.linalg.matrix_rank(A,tol))

def main():
 w=np.exp(2j*np.pi/3)
 Z=np.diag([1,w,w*w])
 X=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
 H=closure([X,Z]);assert len(H)==27
 center=[A for A in H if np.linalg.norm(A@X-X@A)<1e-8 and np.linalg.norm(A@Z-Z@A)<1e-8]
 assert len(center)==3 and commutant_dim([X,Z])==1
 comm=Z@X@np.linalg.inv(Z)@np.linalg.inv(X);p,r=phase_res(comm,np.eye(3));assert r<1e-8 and abs(p-w)<1e-8
 F=np.array([[w**(j*k) for k in range(3)] for j in range(3)],complex)/math.sqrt(3)
 P=np.diag([1,1,w])
 checks={}
 for name,A,B in [
  ('F_X_to_Z',F@X@F.conj().T,Z),('F_Z_to_Xinv',F@Z@F.conj().T,np.linalg.matrix_power(X,2)),
  ('P_X_to_XZ',P@X@P.conj().T,X@Z),('P_Z_to_Z',P@Z@P.conj().T,Z)]:
  _,rr=phase_res(A,B);assert rr<1e-8;checks[name]=rr
 kx=float(np.linalg.norm(X.conj()-X));kz=float(np.linalg.norm(Z.conj()-np.linalg.matrix_power(Z,2)))
 assert kx<1e-8 and kz<1e-8
 out7={
  'pass':5727,'status':'FINITE_TORSION_TO_E8_FAMILY_INTERTWINER_CONSTRUCTED_VIA_HEISENBERG_EXTENSION__LIE_SU3_IDENTIFICATION_REMAINS_OPEN',
  'correction_to_pass5708':{
   'old_generators':'T=diag(1,omega,omega^2)=Z and C=3-cycle=X','generated_group_order':27,
   'exact_group':'qutrit Heisenberg H3, not full SU(3)','commutant_dimension':1,
   'why_old_scalar_commutant_survives':'The 3D Schrödinger representation of H3 is irreducible, so its commutant is already C. Full irreducible SU(3) also has scalar commutant, but the old T,C finite test did not generate full SU(3).'},
  'intertwiner':{
   'torsion_quotient':'H3/Z(H3)=F3^2, matching H1(X;Z)=(Z/3)^2',
   'basis_map':'after choosing a torsion basis, e1 -> projective X and e2 -> projective Z',
   'family_target':'the same C^3 multiplicity factor used in the E8 (27,3) branch',
   'linear_intertwiner_after_basis_choice':'identity on C^3 between the qutrit Schrödinger model and Pass5708 X,Z matrices',
   'ambiguity':'torsion basis/orientation/central-character choice; full GL(2,3) is semilinear rather than purely unitary'},
  'remaining_no_go':'This proves a finite Heisenberg/projective torsion action on the E8 family multiplicity factor. It does NOT identify the affine Lie su(3) of Pass5686/5696 with the E8 family SU(3) Lie algebra.',
  'physics_boundary':'No physical generation, color, Yukawa, or particle assignment follows.'}
 out30={
  'pass':5730,'status':'BONKERS_HEISENBERG_QUTRIT_BRIDGE_CLOSES__GL23_REQUIRES_EXTENDED_UNITARY_ANTIUNITARY_CLIFFORD',
  'Heisenberg_group':{'order':27,'center_order':3,'quotient':'F3^2','commutation':'Z X = omega X Z','irreducible_dimension':3,'commutant_dimension':1},
  'SL23_normalizer':{'Fourier_action':'X->Z, Z->X^-1','quadratic_phase_action':'X->XZ, Z->Z','projective_residuals':checks},
  'GL23_extension':{'det_minus_one_generator':'complex conjugation K','action':'X->X, Z->Z^-1','antiunitary':True,'K_X_residual':kx,'K_Zinverse_residual':kz,
   'consequence':'determinant +1 quotient actions are unitary Clifford; determinant -1 requires the extended Clifford antiunitary coset'},
  'orientation_character':'The alternating form on F3^2 is preserved by SL(2,3) and reversed by determinant -1; the same determinant bit distinguishes unitary from antiunitary normalizers.',
  'physics_boundary':'Finite qutrit/projective representation theorem only.'}
 OUT7.write_text(json.dumps(out7,indent=2,sort_keys=True)+'\n');OUT30.write_text(json.dumps(out30,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'5727':out7,'5730':out30},indent=2,sort_keys=True))
if __name__=='__main__':main()
