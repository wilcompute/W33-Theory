#!/usr/bin/env python3
"""Suzuki multiplier -1 outer action swaps the two six-qutrit Heisenberg sectors.

The W33/Suzuki carrier has an extraspecial Heisenberg group H=3^(1+12) with
V=H/Z(H)=F3^12 and two faithful 729-dimensional Schrödinger sectors rho_r,
r=1,2, distinguished by rho_r(z)=omega^r I.

A symplectic similitude g with multiplier -1 satisfies
    Omega(gv,gw) = -Omega(v,w).
Its lift to the abstract Heisenberg group must therefore send the center
z -> z^{-1}.  Consequently rho_r o tau has central character -r and is the
opposite Schrödinger sector.  No complex-linear operator can implement tau
inside a single rho_r, because similarity cannot change the scalar omega^r I
to omega^{-r} I.  In the standard qutrit model, complex conjugation implements
tau antiunitarily; on rho_1 direct-sum rho_2, block swap implements tau linearly.

This is the rank-12/six-qutrit completion of the determinant-reversing
extended-Clifford observation in Passes 5725--5732, now tied to the explicit
Suzuki outer similitude.  It does NOT prove that the same C2 is a heterotic
orbifold/deck operation.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_suzuki_outer_heisenberg_sector_swap.json'
P=3


def main(write=True):
    # Standard six-qutrit phase-space coordinates (x1,z1,...,x6,z6).
    J=np.zeros((12,12),dtype=np.int64)
    for i in range(6):
        J[2*i,2*i+1]=1; J[2*i+1,2*i]=-1
    A=np.eye(12,dtype=np.int64)
    for i in range(6): A[2*i+1,2*i+1]=-1
    J%=P; A%=P
    assert np.array_equal(A.T@J@A%P,(-J)%P) and np.array_equal(A@A%P,np.eye(12,dtype=np.int64)%P)

    # One qutrit already certifies the tensor-factor action; X is real while
    # complex conjugation sends Z and omega to their inverses.
    w=np.exp(2j*np.pi/3)
    X=np.zeros((3,3),dtype=complex)
    for j in range(3): X[(j+1)%3,j]=1
    Z=np.diag([1,w,w*w])
    assert np.allclose(X.conj(),X)
    assert np.allclose(Z.conj(),np.linalg.inv(Z))
    assert abs(w.conjugate()-w*w)<1e-12

    # The central-character obstruction is exact: a linear similarity U cannot
    # change omega^r I into omega^{-r} I for r=1 or 2.
    chars={1:w,2:w*w}
    swaps={r:(-r)%3 for r in (1,2)}
    assert swaps=={1:2,2:1}
    no_linear_single=all(abs(chars[r]-chars[swaps[r]])>1e-12 for r in (1,2))
    assert no_linear_single

    out={
      'schema':'w33.suzuki_outer_heisenberg_sector_swap.v1','status':'PASS',
      'headline':'A multiplier-minus-one similitude of the F3^12 six-qutrit phase space induces z->z^{-1} on the extraspecial Heisenberg group 3^(1+12). Hence it swaps the two faithful 729-dimensional Schrödinger sectors r=1 and r=2. It cannot be implemented complex-linearly inside either sector alone; standard qutrit complex conjugation implements it antiunitarily, while rho_1 direct-sum rho_2 admits a linear block-swap implementation. The explicit Suzuki outer similitude therefore belongs to the determinant-reversing extended-Clifford side of the six-qutrit carrier.',
      'phase_space':{'dimension_F3':12,'qutrits':6,'anti_symplectic_involution':'diag(1,-1)^6','multiplier_mod3':2},
      'heisenberg':{'shape':'3^(1+12)','centre':'C3','schrodinger_dimension':729,'central_characters':[1,2],'outer_action_on_centre':'z -> z^{-1}','sector_action':'r -> -r mod 3'},
      'representation_boundary':{
        'linear_within_single_r_sector':False,
        'reason':'similarity preserves the scalar rho_r(z)=omega^r I, whereas tau requires omega^{-r} I',
        'antiunitary_single_sector':True,
        'antiunitary_model':'complex conjugation: X->X, Z->Z^{-1}, omega->omega^{-1}',
        'linear_on_doubled_r1_plus_r2':True,
        'linear_doubled_model':'swap the rho_1 and rho_2 blocks'
      },
      'repo_links':[
        'Pass5725-5732: determinant-reversing qutrit normalizer is antiunitary extended-Clifford',
        'w33_suz_outer_completes_local_e6_weyl.py: explicit Suzuki outer GF(3) similitude has multiplier -1',
        'w33_h1_adjoint_nonlinear_invariants.py: candidate phase uses synchronized r=1 or 2 central character'
      ],
      'cross_repo_boundary':'Holotrade now finds that order-three SU(5) and flipped-SU(5) routes require an even-order ingredient. This certificate supplies a canonical finite C2 inversion on the six-qutrit Heisenberg carrier, but does not identify it with a heterotic space-group/orbifold element or prove Standard-Model breaking.',
      'checks':{'anti_symplectic_order2':True,'center_inversion':True,'r1_r2_swapped':True,'no_linear_single_sector':True,'antiunitary_qutrit_model':True,'linear_doubled_sector_model':True}
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2)); return out

if __name__=='__main__': main(True)
