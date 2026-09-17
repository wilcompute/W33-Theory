#!/usr/bin/env python3
"""Logical-qubit structure of the doubled r=1 plus r=2 Heisenberg sectors.

On V_1 direct-sum V_2, the Heisenberg centre z has eigenvalues omega,omega^2
and the Suzuki outer operation swaps the sectors.  This produces an exact
2-level central-character factor.  The theorem is representation-theoretic;
physical coherence between the two sectors remains an implementation condition.
"""
import json,cmath,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_doubled_central_character_logical_qubit.json'

def close(gens):
    def key(M):return tuple(np.round(M.real,12).ravel())+tuple(np.round(M.imag,12).ravel())
    I=np.eye(2,dtype=complex); seen={key(I):I}; q=[I]
    while q:
        A=q.pop()
        for g in gens:
            B=A@g;k=key(B)
            if k not in seen:seen[k]=B;q.append(B)
    return list(seen.values())

def main(write=True):
    w=np.exp(2j*np.pi/3); z=np.diag([w,w*w]); X=np.array([[0,1],[1,0]],complex); I=np.eye(2,dtype=complex)
    Z=(z-np.linalg.inv(z))/(1j*np.sqrt(3))
    assert np.allclose(Z,np.diag([1,-1])) and np.allclose(X@Z,-Z@X)
    assert np.allclose(X@z@X,np.linalg.inv(z)) and np.allclose(np.linalg.matrix_power(z,3),I) and np.allclose(X@X,I)
    G=close([z,X]); assert len(G)==6
    # z is not a logical Clifford: it does not normalize {+/-X,+/-Y,+/-Z}.
    Y=1j*X@Z; zxz=z@X@np.linalg.inv(z)
    paulis=[X,Y,Z,-X,-Y,-Z]
    assert not any(np.allclose(zxz,P) for P in paulis)
    # If an ambient center-trivial sector is present, this polynomial is 0 there and 1 on r=1,2.
    code_eval={'r0':float(np.real((2-1-1)/3)),'r1':float(np.real((2-w-w*w)/3)),'r2':float(np.real((2-w*w-w)/3))}
    assert abs(code_eval['r0'])<1e-9 and abs(code_eval['r1']-1)<1e-9 and abs(code_eval['r2']-1)<1e-9
    # Conditional universality test: adjoining logical Hadamard makes H*z infinite order.
    H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2)
    U=1j*H@z  # determinant one representative
    tr=float(np.real_if_close(np.trace(U)))
    # tr = -sqrt(3/2), which is not an algebraic integer (minimal polynomial 2x^2-3).
    assert abs(tr+np.sqrt(3/2))<1e-10
    out={
      'schema':'w33.doubled_central_character_logical_qubit.v1','status':'PASS',
      'code_space':{'sectors':['r=1','r=2'],'dimension_total':1458,'formal_factor':'C^2 sector label x C^729 after choosing conjugate bases'},
      'logical_paulis':{'Z_L':'(z-z^-1)/(i sqrt(3)) = diag(1,-1)','X_L':'outer sector swap','anticommute':True},
      'finite_control':{'center_gate':'z=exp(2 pi i Z_L/3)','outer_gate':'X_L','group':'S3 = C3:C2','order':len(G),'universal_alone':False},
      'non_clifford_relative_to_logical_pauli':{'center_gate_normalizes_logical_Pauli':False,'conjugated_X':'-1/2 X + sqrt(3)/2 Y (up to orientation convention)'},
      'leakage_syndrome':{'projector':'P_code=(2I-z-z^-1)/3','eigenvalues':code_eval,'use':'detects centre-trivial r=0 leakage without distinguishing r=1 from r=2'},
      'conditional_dense_extension':{'extra_gate':'logical Hadamard H_L','trace_of_SU2_representative_Hz':'-sqrt(3/2)','trace_is_algebraic_integer':False,'product_has_finite_order':False,'consequence':'if H_L is physically available, <H_L,z> is not a finite Clifford-like subgroup; with nonparallel axes its closure is SU(2)'},
      'realification':'V_1 plus V_2=conjugate(V_1) is the complexification pattern of a real 1458-dimensional carrier; the antiunitary outer action on one sector becomes a complex-linear swap on the doubled space.',
      'fault_tolerance_boundary':'P_code is a genuine symmetry-based leakage check. Z_L itself is logical information, so measuring r=1 versus r=2 is not a stabilizer syndrome. No distance or threshold claim is made.',
      'universality_boundary':'S3 alone is finite. A certified logical basis-changing gate such as H_L, or another independent sector operation, is still required before the doubled sector supplies universal control.',
      'physical_boundary':'All statements assume coherent access to V_1 direct-sum V_2. If central character is a strict superselection charge, the logical qubit and relative center phase are not operational.'}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
