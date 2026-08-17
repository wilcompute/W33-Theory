#!/usr/bin/env python3
"""Pass5729: exact Herm(3) commutants for natural finite family actions."""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS5729_FAMILY_SYMMETRY_BREAKING_LATTICE.json'

def hb():
 B=[]
 for i in range(3):H=np.zeros((3,3),complex);H[i,i]=1;B.append(H)
 for i in range(3):
  for j in range(i+1,3):
   H=np.zeros((3,3),complex);H[i,j]=H[j,i]=1;B.append(H)
   K=np.zeros((3,3),complex);K[i,j]=1j;K[j,i]=-1j;B.append(K)
 return B
def hdim(gens):
 B=hb()
 if not gens:return 9
 rows=[]
 for G in gens:
  for i in range(3):
   for j in range(3):
    z=[(H@G-G@H)[i,j] for H in B];rows.append([q.real for q in z]);rows.append([q.imag for q in z])
 return 9-int(np.linalg.matrix_rank(np.array(rows,float),1e-9))
def Pmat(p):
 P=np.zeros((3,3),complex)
 for j,i in enumerate(p):P[i,j]=1
 return P

def main():
 w=np.exp(2j*np.pi/3);I=np.eye(3,dtype=complex);Z=np.diag([1,w,w*w]);X=Pmat((1,2,0));swap=Pmat((1,0,2));S3=[Pmat(p) for p in itertools.permutations(range(3))]
 dims={'trivial':hdim([]),'center_Z3_scalar':hdim([w*I]),'cyclic_X':hdim([X]),'cyclic_Z':hdim([Z]),'C2_swap':hdim([swap]),'S3_permutation':hdim(S3),'Heisenberg_H3_XZ':hdim([X,Z])}
 assert dims=={'trivial':9,'center_Z3_scalar':9,'cyclic_X':3,'cyclic_Z':3,'C2_swap':5,'S3_permutation':2,'Heisenberg_H3_XZ':1}
 Mz=np.diag([1.,2.,4.]);Mx=2*I+.31*(X+X.conj().T)+.23j*(X-X.conj().T)
 ez=np.linalg.eigvalsh(Mz);ex=np.linalg.eigvalsh(Mx);assert min(np.diff(np.sort(ez)))>1e-6 and min(np.diff(np.sort(ex)))>1e-6
 F=np.array([[w**(j*k) for k in range(3)] for j in range(3)],complex)/math.sqrt(3);assert np.max(np.abs(np.abs(F)-1/math.sqrt(3)))<1e-8
 J=np.ones((3,3),complex);es3=np.linalg.eigvalsh(1.7*I+.4*J);assert abs(es3[0]-es3[1])<1e-8
 out={'pass':5729,'status':'FINITE_FAMILY_BREAKING_LATTICE_CLASSIFIED__SINGLE_C3_ALLOWS_THREE_LEVELS_BUT_MIXING_REQUIRES_RELATIVE_AXIS_MISMATCH',
  'Hermitian_commutant_real_dimensions':dims,'nondegenerate_examples':{'Z_axis_eigenvalues':[float(x) for x in ez],'X_axis_eigenvalues':[float(x) for x in ex]},
  'selection_rules':{'center_Z3':'scalar center imposes no family texture','single_C3':'3-real-dimensional commutant; generic three distinct eigenvalues allowed','C2_swap':'Herm(2) plus one singlet, dimension5; generic three levels allowed','S3':'1+2 permutation decomposition; invariant Hermitian operators force a doublet degeneracy','H3_or_full_irreducible_SU3':'scalar commutant; exact degeneracy'},
  'mixing_refinement':'X- and Z-cyclic axes are Fourier conjugate with all overlap magnitudes 1/sqrt(3). A single residual C3 selects a basis; mixing becomes invariant only as a relative mismatch between independently selected residual axes in two operator/species sectors. Requiring both X and Z on one operator regenerates H3 and collapses the commutant to scalars.',
  'fourier_overlap_abs':1/math.sqrt(3),'physics_boundary':'Finite texture/commutant classification only; no observed mass or CKM/PMNS prediction.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
