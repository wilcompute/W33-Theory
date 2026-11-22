#!/usr/bin/env python3
"""Construct a 9-dimensional exact code for the restricted H27 Weyl error set.

The 27D E6 fundamental is an H27 isotypic module C9 tensor C3. This
construction gives an explicit syndrome/gauge factor and 9D logical code.
The full E6 group error set has a separate no-go by irreducible multiplicity 1.
"""
import json
from pathlib import Path
import numpy as np
import toe_20261122_e6_132_constructive_embedding as E
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_round7_h27_subsystem_code.json'

def build():
    w=np.exp(2j*np.pi/3); e=np.eye(3,dtype=complex);X=np.roll(e,1,axis=0);Z=np.diag([1,w,w*w]);
    x=E.blocks(E.tensor(X.conj(),e),E.tensor(e,X),E.tensor(X,X.conj()))
    y=E.blocks(E.tensor(Z.conj(),e),E.tensor(e,Z.conj()),E.tensor(Z,Z))
    assert np.max(abs(x@y@x.conj().T@y.conj().T-w*np.eye(27)))<1e-12
    ids=np.flatnonzero(abs(np.diag(y)-1)<1e-12)
    assert len(ids)==9
    F=np.eye(27,dtype=complex)[:,ids]
    U=np.column_stack([np.linalg.matrix_power(x,k)@F[:,j] for j in range(9) for k in range(3)])
    return x,y,U,w

def verify():
    x,y,U,w=build();I9=np.eye(9);I3=np.eye(3)
    X=np.roll(I3,1,axis=0);Zinv=np.diag([1,np.conj(w),w])
    residual={
      'unitarity':float(np.max(abs(U.conj().T@U-np.eye(27)))),
      'x_tensor':float(np.max(abs(U.conj().T@x@U-np.kron(I9,X)))),
      'y_tensor':float(np.max(abs(U.conj().T@y@U-np.kron(I9,Zinv)))),
    }
    assert max(residual.values())<1e-12,residual
    C=U[:,np.arange(0,27,3)]
    assert np.max(abs(C.conj().T@C-I9))<1e-12
    errors=[np.linalg.matrix_power(x,a)@np.linalg.matrix_power(y,b) for a in range(3) for b in range(3)]
    errmax=0;coefficients=[]
    for a,A in enumerate(errors):
      for b,B in enumerate(errors):
        compressed=C.conj().T@A.conj().T@B@C
        coeff=np.trace(compressed)/9
        errmax=max(errmax,float(np.max(abs(compressed-coeff*I9))))
        coefficients.append([a,b,round(float(coeff.real),10),round(float(coeff.imag),10)])
    assert errmax<1e-12
    # Concrete recovery of a randomized nine-dimensional logical pure state
    # after an arbitrary convex mixture of the nine Weyl errors.
    rng=np.random.default_rng(20261122)
    logical=rng.normal(size=9)+1j*rng.normal(size=9);logical/=np.linalg.norm(logical)
    psi=C@logical;rho0=np.outer(psi,psi.conj())
    prob=rng.random(9);prob/=prob.sum()
    damaged=sum(float(p)*err@rho0@err.conj().T for p,err in zip(prob,errors))
    recovered=np.zeros((27,27),complex)
    for a in range(3):
      sector=U[:,np.arange(a,27,3)]
      proj=sector@sector.conj().T
      inverse_shift=np.linalg.matrix_power(x,(3-a)%3)
      recovered+=inverse_shift@proj@damaged@proj@inverse_shift.conj().T
    recovery_error=float(np.max(abs(recovered-rho0)))
    assert recovery_error<2e-12
    # Channel acts as I9 on the logical subsystem and Weyl on gauge;
    # a simple syndrome measurement in k determines shift a, then undo.
    output=dict(status='PASS_RESTRICTED_H27_9D_QUANTUM_ERROR_CORRECTING_SUBSPACE',
      E6_host_irrep='27 fundamental', H27_isotypic_factorization='C^9 logical tensor C^3 gauge',
      isometry_shape=[27,27],logical_code_dimension=9,physical_dimension=27,
      H27_projective_errors=9,
      representation_weyl_relation='X Y X^-1 Y^-1 = omega I_27',
      tensor_residuals=residual,
      KL_max_abs_residual=errmax,
      nine_error_mixture_recovered_density_max_abs_residual=recovery_error,
      KL_coefficient_matrix=coefficients,
      recovery='Measure the three orthogonal Weyl-X syndrome sectors k=0,1,2 and undo X^k; Weyl-Z phases are scalar on the encoded gauge-k=0 state. This corrects the span of all nine X^aY^b errors.',
      restricted_error_scope='Noise generated exclusively by the chosen H27 subgroup acting in E6 27, not arbitrary E6 group errors, cross-sector leakage, full E6 gauge dynamics or physical energy-decoherence rate.',
      full_E6_no_go='The 132D multiplicity-free 78 + 27 + anti27 has full compact E6 error algebra End(78) direct-sum End(27) direct-sum End(anti27). For any code dimension >=2, compression of a rank-one projector supported on a nonzero irrep block has rank at most 1 but KL requires scalar identity; hence no nontrivial code corrects that full algebra. A restricted physical error algebra is essential.' )
    return output

if __name__=='__main__':
 d=verify();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print({k:v for k,v in d.items() if k not in ['KL_coefficient_matrix']})
