#!/usr/bin/env python3
"""Conditional S3 closure of the doubled determinant-phase sector.

Inputs already certified elsewhere:
  * the quartic H1 invariant det(X), with candidate phase omega^(r det X), r=1,2;
  * the multiplier-minus-one Suzuki outer action, which swaps r=1 <-> r=2.

On the doubled central-character label define
    D_f = diag(omega^f, omega^(-f)),  f in F3,
    S   = [[0,1],[1,0]].
Then S D_f S = D_f^{-1}.  For f != 0, D_f has order 3 and S has order 2,
so <D_f,S> is exactly C3:C2 ~= S3.  For f=0 the C3 factor collapses.

The finite group closure is exact.  Calling D_f a physical gate remains
conditional on the still-open H1-to-register coupling.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_det_phase_outer_s3_closure.json'


def key(M):
    return tuple(np.round(M.real,12).ravel())+tuple(np.round(M.imag,12).ravel())


def closure(gens):
    I=np.eye(gens[0].shape[0],dtype=complex); seen={key(I):I}; stack=[I]
    while stack:
        A=stack.pop()
        for g in gens:
            B=A@g; k=key(B)
            if k not in seen: seen[k]=B; stack.append(B)
    return list(seen.values())


def main(write=True):
    w=np.exp(2j*np.pi/3)
    S=np.array([[0,1],[1,0]],dtype=complex)
    rows={}
    for f in (0,1,2):
        D=np.diag([w**f,w**(-f)])
        assert np.allclose(S@S,np.eye(2))
        assert np.allclose(S@D@S,np.linalg.inv(D))
        G=closure([D,S])
        expected=2 if f==0 else 6
        assert len(G)==expected
        if f:
            assert np.allclose(np.linalg.matrix_power(D,3),np.eye(2))
        rows[str(f)]={'group_order':len(G),'group':'C2' if f==0 else 'S3','D_order':1 if f==0 else 3}
    out={
      'schema':'w33.det_phase_outer_s3_closure.v1','status':'PASS_CONDITIONAL_ON_DET_PHASE_COUPLING',
      'headline':'On the doubled r=1 plus r=2 central-character sector, the candidate determinant phase D_f=diag(omega^f,omega^-f) and the certified outer sector swap S obey S D_f S=D_f^-1. For det(X)=f=1 or 2 they generate exactly C3:C2 ~= S3; for f=0 only the C2 swap remains. Thus the determinant phase and Suzuki outer inversion are algebraically compatible and close the noncentral ternary/binary hinge left open in Pass5732, conditional on a physical H1-to-register determinant-phase coupling.',
      'relations':{'S2':'1','D3':'1 for f != 0','SDS':'D^-1','presentation':'<D,S | D^3=S^2=1, SDS=D^-1> ~= S3'},
      'fiber_census':rows,
      'inputs':[
        'w33_h1_adjoint_nonlinear_invariants.py: det(X) is first new pointwise quartic invariant; omega^(r det X) is a candidate phase, not a certified gate',
        'w33_suzuki_outer_heisenberg_sector_swap.py: multiplier-minus-one outer swaps r=1 and r=2',
        'Pass5725-5732: a noncentral C3:C2 route requires qutrit inversion; Chinese-remainder packaging alone is insufficient'
      ],
      'cross_repo_note':'Holotrade requires an even-order ingredient beyond the order-three GUT twist. The S3 closure supplies an exact finite algebraic C2 extension of the ternary phase sector, but no heterotic orbifold embedding is certified.',
      'boundary':'The S3 presentation and matrix closure are exact. The determinant phase remains conditional because the H1 controller variable has not yet been coupled to the six-qutrit register as a physical nonlinear gate.',
      'checks':{'f0_C2':True,'f1_S3':True,'f2_S3':True,'outer_inverts_phase':True}
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2)); return out

if __name__=='__main__': main(True)
