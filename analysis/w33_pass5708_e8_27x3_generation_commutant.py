#!/usr/bin/env python3
"""Pass5708: what the E8 (27,3) really proves about a generation multiplicity space.

The standard branching used throughout the repo is
  248=(78,1)+(1,8)+(27,3)+(27bar,3bar)
under E6 x SU(3). The 81-dimensional (27,3) is an outer tensor product.

Schur's lemma gives the decisive distinction:
  * under E6 alone, 27 x C^3 is three equivalent copies and End_E6 = M3(C);
  * a central Z3 acting as omega I_3 leaves that M3 untouched;
  * under the full E6 x SU(3) action, 27 x 3 is irreducible and its commutant is C.

So there really is a 3-dimensional multiplicity space relative to E6 alone, but
there are not three independently invariant generations under an unbroken family
SU(3). Selecting a generation basis/hierarchy requires breaking/reducing that
family action or supplying extra structure. This is distinct from Pass5698's
vertical regular Z3, whose three Fourier sectors are inequivalent charges.

The new affine su(3) of Pass5686/5696 has the right abstract A2 type and an 8D
adjoint, but no explicit intertwiner has yet identified it with the (1,8) family
factor in this E8 branching. This pass refuses that identification by dimension.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5708_E8_27x3_GENERATION_COMMUTANT.json'

def commutant_dim(gens,n,tol=1e-9):
    if not gens:return n*n
    A=np.vstack([np.kron(G.T,np.eye(n))-np.kron(np.eye(n),G) for G in gens])
    return n*n-int(np.linalg.matrix_rank(A,tol))

def main():
    # Small model for the multiplicity factor only. E6 irreducibility means any
    # E6-commuting operator on 27xC3 is I_27 tensor M, so it suffices to compute
    # which 3x3 M commute with the family action.
    w=np.exp(2j*np.pi/3)
    Zcenter=w*np.eye(3)
    # Two standard generators of the irreducible 3 of SU3: a diagonal torus
    # element with distinct weights and a 3-cycle permutation (both det=1).
    T=np.diag([1,w,w*w])
    C=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
    assert abs(np.linalg.det(T)-1)<1e-8 and abs(np.linalg.det(C)-1)<1e-8
    dims={
      'E6_only':commutant_dim([],3),
      'E6_x_center_Z3':commutant_dim([Zcenter],3),
      'E6_x_maximal_torus_sample':commutant_dim([T],3),
      'E6_x_SU3_generated_by_T_and_C':commutant_dim([T,C],3)
    }
    assert dims=={'E6_only':9,'E6_x_center_Z3':9,'E6_x_maximal_torus_sample':3,'E6_x_SU3_generated_by_T_and_C':1}
    out={
      'pass':5708,'status':'E8_27x3_HAS_GENUINE_M3_MULTIPLICITY_RELATIVE_TO_E6_ONLY__FULL_FAMILY_SU3_COLLAPSES_COMMUTANT_TO_C',
      'branching':'248=(78,1)+(1,8)+(27,3)+(27bar,3bar) under E6 x SU3_family',
      'matter_carrier':'W=27 tensor C^3, dimension81',
      'commutant_dimensions':dims,
      'commutant_algebras':{'E6_only':'M3(C)','E6_x_center_Z3':'M3(C)','E6_x_generic_torus':'C^3','E6_x_full_SU3_family':'C'},
      'generation_result':'The factor C^3 is an honest multiplicity space for the irreducible E6 27. Thus three equivalent E6 copies are representation-theoretically real. But full unbroken SU3_family rotates those copies irreducibly, so no individual generation or mass hierarchy is invariant under the maximal product symmetry.',
      'comparison_with_vertical_Z3':'Pass5698 used the regular C[Z3] fiber representation, which splits into three inequivalent characters and destroys M3. Here the center of the fundamental SU3 acts as scalar omega I3, so a central Z3 alone does NOT distinguish the three multiplicity directions.',
      'affine_su3_boundary':'The Pass5686/5696 affine su3 is abstractly type A2 with adjoint dimension8, matching the dimension of the E8 (1,8) factor. No common 81D action or intertwiner has been constructed, so these su3 objects are not identified here.',
      'physics_boundary':'This establishes a representation multiplicity conditional on which symmetry is treated as unbroken. It does not derive the observed three fermion generations, their hierarchy, Yukawa matrices, or family-symmetry breaking.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
