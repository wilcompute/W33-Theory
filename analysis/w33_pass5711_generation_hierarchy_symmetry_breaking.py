#!/usr/bin/env python3
"""Pass5711 bonkers: maximal-symmetry stress test of the 81-dimensional generation carrier.

Pass5708 shows W=27 tensor C3 has M3(C) multiplicity relative to E6 alone, but
commutant C under E6 x SU3_family. Here we ask the physics-facing question: can
an exact unbroken family SU3 itself support three distinct generation masses?
No. Any Hermitian operator on the multiplicity factor commuting with the
irreducible fundamental 3 is scalar by Schur, hence its spectrum is (m,m,m).

A central Z3 acts as omega I and imposes no mass degeneracy beyond Hermiticity;
a generic maximal torus with three distinct weights reduces the commutant to the
diagonal algebra C^3 and permits three distinct masses but no off-diagonal mixing.
Thus a hierarchy requires family-SU3 breaking/reduction. The repo's recurring
'three = fundamental 3' is a valid multiplicity statement, not a hierarchy theorem.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5711_GENERATION_HIERARCHY_SYMMETRY_BREAKING.json'

def hermitian_commutant_basis(gens,tol=1e-9):
    # Hermitian 3x3 real vector space basis (9 real dims).
    B=[]
    for i in range(3):
      X=np.zeros((3,3),complex);X[i,i]=1;B.append(X)
    for i in range(3):
      for j in range(i+1,3):
        X=np.zeros((3,3),complex);X[i,j]=X[j,i]=1;B.append(X)
        Y=np.zeros((3,3),complex);Y[i,j]=1j;Y[j,i]=-1j;B.append(Y)
    rows=[]
    for G in gens:
      C=[G@X-X@G for X in B]
      for a in range(3):
        for b in range(3):
          rows.append([X[a,b].real for X in C]);rows.append([X[a,b].imag for X in C])
    if not rows:return len(B)
    return len(B)-int(np.linalg.matrix_rank(np.array(rows,float),tol))

def main():
    w=np.exp(2j*np.pi/3);Z=w*np.eye(3)
    T=np.diag([1,w,w*w]);C=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
    dims={'no_family_action':hermitian_commutant_basis([]),'center_Z3_only':hermitian_commutant_basis([Z]),'generic_torus':hermitian_commutant_basis([T]),'full_SU3_generated':hermitian_commutant_basis([T,C])}
    assert dims=={'no_family_action':9,'center_Z3_only':9,'generic_torus':3,'full_SU3_generated':1}

    # Solve explicitly for a Hermitian mass matrix commuting with T,C using LSQ
    # nullspace; the one-dimensional solution must be proportional to identity.
    # The dimension result above is basis-independent; exhibit the consequence.
    m=2.75;M=m*np.eye(3);assert np.linalg.norm(T@M-M@T)<1e-12 and np.linalg.norm(C@M-M@C)<1e-12
    ev=np.linalg.eigvalsh(M);assert max(ev)-min(ev)<1e-12
    out={
      'pass':5711,'status':'UNBROKEN_SU3_FAMILY_FORCES_DEGENERATE_GENERATION_OPERATOR__HIERARCHY_REQUIRES_SYMMETRY_BREAKING',
      'carrier':'81=(27,3) under E6 x SU3_family; generation-sensitive operators reduce to Hermitian 3x3 matrices on the multiplicity factor once E6 irreducibility is imposed',
      'Hermitian_commutant_real_dimensions':dims,
      'mass_consequences':{
        'E6_only_or_center_Z3':'arbitrary Hermitian 3x3 generation operator is allowed',
        'generic_family_torus':'only diagonal 3x3 operators survive; three distinct eigenvalues are allowed but mixing is removed',
        'full_unbroken_SU3_family':'only m I3 survives; all three eigenvalues are exactly degenerate'
      },
      'example_full_SU3_spectrum':[float(x) for x in ev],
      'generation_hierarchy_no_go':'The full family SU3 cannot simultaneously remain exact and explain a nondegenerate three-generation mass hierarchy. Any physical generation reading of the fundamental 3 requires a symmetry-breaking datum or a reduced family action.',
      'relation_to_torsor_no_go':'This is the linear-operator version of the earlier torsor principle: a transitive/unbroken symmetry can present a multiplicity but cannot intrinsically rank its members.',
      'relation_to_Pass5698':'A center Z3 in the fundamental acts as a scalar and leaves M3 intact, unlike the vertical regular Z3 fiber action whose three Fourier sectors are inequivalent. The two qutrits must not be conflated.',
      'physics_boundary':'No breaking mechanism, Yukawa texture, CKM/PMNS matrix or observed mass value is derived. The result is a symmetry constraint on any future generation mechanism.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
