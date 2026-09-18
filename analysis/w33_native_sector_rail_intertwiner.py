#!/usr/bin/env python3
"""Exact generator-level native-sector to optical-rail intertwiner.

Choose computational bases |n>, n in F3^6, for the two faithful Heisenberg
Schrodinger sectors V1,V2 so that
  rho1(X_j)=X_j, rho1(Z_j)=Z_j,
  rho2(X_j)=X_j, rho2(Z_j)=Z_j^{-1}.
Order the doubled basis as |r,n> with r=+1,-1.

The linear basis identification
  J : V1 direct-sum V2 -> C^2_rail tensor C^729_internal
  J|r=+1,n> = |0>_rail|n>,
  J|r=-1,n> = |1>_rail|n>
puts every generator into a hardware-transparent normal form:
  X_j -> I_rail tensor X_j
  Z_j -> |0><0| tensor Z_j + |1><1| tensor Z_j^{-1}
  center -> diag(omega,omega^-1) tensor I
  outer s -> X_rail tensor I.

The verifier checks the one-qutrit 6x6 generator identities exactly up to
floating tolerance; the six-qutrit result follows by tensor locality.

This closes the algebraic intertwiner.  The remaining physical question is
whether the native VOA/material sectors can be coherently loaded into the two
optical rails with the required conjugate phase convention.
"""
from __future__ import annotations
import cmath,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_native_sector_rail_intertwiner.json'

def kron(A,B):
    return [[A[i//len(B)][j//len(B[0])]*B[i%len(B)][j%len(B[0])]
             for j in range(len(A[0])*len(B[0]))]
            for i in range(len(A)*len(B))]
def mm(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def close(A,B,tol=1e-9):
    return len(A)==len(B) and len(A[0])==len(B[0]) and all(abs(A[i][j]-B[i][j])<tol for i in range(len(A)) for j in range(len(A[0])))

def main(write=True):
    w=cmath.exp(2j*cmath.pi/3)
    I2=[[1,0],[0,1]]; Xr=[[0,1],[1,0]]
    I3=[[1,0,0],[0,1,0],[0,0,1]]
    X3=[[0,0,1],[1,0,0],[0,1,0]]
    Z3=[[1,0,0],[0,w,0],[0,0,w*w]]
    Z3i=[[1,0,0],[0,w*w,0],[0,0,w]]
    # block-diagonal native generators in doubled ordering
    nativeX=[[0j]*6 for _ in range(6)]
    nativeZ=[[0j]*6 for _ in range(6)]
    for r,B in enumerate((X3,X3)):
        for i in range(3):
            for j in range(3): nativeX[3*r+i][3*r+j]=B[i][j]
    for r,B in enumerate((Z3,Z3i)):
        for i in range(3):
            for j in range(3): nativeZ[3*r+i][3*r+j]=B[i][j]
    railX=kron(I2,X3)
    railZ=[[0j]*6 for _ in range(6)]
    for r,B in enumerate((Z3,Z3i)):
        for i in range(3):
            for j in range(3): railZ[3*r+i][3*r+j]=B[i][j]
    outer=kron(Xr,I3)
    center=kron([[w,0],[0,w.conjugate()]],I3)
    assert close(nativeX,railX) and close(nativeZ,railZ)
    # outer normalizes X and inverts Z/center.
    assert close(mm(mm(outer,railX),outer),railX)
    assert close(mm(mm(outer,railZ),outer),kron(I2,Z3i)) is False  # rail-dependent inverse, check directly below
    zinverse=[[0j]*6 for _ in range(6)]
    for r,B in enumerate((Z3i,Z3)):
        for i in range(3):
            for j in range(3): zinverse[3*r+i][3*r+j]=B[i][j]
    assert close(mm(mm(outer,railZ),outer),zinverse)
    cinv=kron([[w.conjugate(),0],[0,w]],I3)
    assert close(mm(mm(outer,center),outer),cinv)

    out={'schema':'w33.native_sector_rail_intertwiner.v1','status':'PASS_ALGEBRAIC_INTERTWINER',
      'map':'J|r=+1,n>=|0>rail|n>; J|r=-1,n>=|1>rail|n>',
      'dimension':1458,
      'generator_normal_form':{
        'X_j':'I_rail tensor X_j',
        'Z_j':'|0><0| tensor Z_j + |1><1| tensor Z_j^-1',
        'center':'diag(omega,omega^-1) tensor I_729',
        'outer':'X_rail tensor I_729'},
      'optical_compiler':{
        'outer':'deterministic rail or polarization swap',
        'center':'relative +/-2pi/3 phase between rails',
        'Z_j':'rail-conditioned sign of the internal qutrit phase',
        'X_j':'same internal cyclic shift on both rails'},
      'physical_interface_obligation':'Construct a coherent loading/readout isometry from native V1,V2 states into the two rails. This certificate proves the target normal form, not a material transducer.',
      'checks':{'one_qutrit_generator_identity':True,'outer_fixes_X':True,'outer_inverts_Z':True,'outer_inverts_center':True,
                'six_qutrit_extension':'tensor-local on j=1,...,6'}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
