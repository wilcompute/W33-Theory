#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20260924_bell_shell_clifford_cyclotomic_lift.json"
D=3
TOL=3e-12
omega=np.exp(2j*np.pi/3)
zeta9=np.exp(2j*np.pi/9)


def phase_distance(A,B):
    z=np.vdot(B.reshape(-1),A.reshape(-1))
    if abs(z)==0:
        return float("inf")
    q=z/abs(z)
    return float(np.linalg.norm(A-q*B))


def paulis():
    X=np.zeros((D,D),complex)
    for j in range(D):
        X[(j+1)%D,j]=1
    Z=np.diag([omega**j for j in range(D)])
    I=np.eye(D)

    return X,Z,np.kron(X,I),np.kron(Z,I),np.kron(I,X),np.kron(I,Z)


def quadratic_gate(a,b,c):
    vals=[]
    for y0 in range(3):
        for y1 in range(3):
            q=(2*(a*y0*y0+2*b*y0*y1+c*y1*y1))%3
            vals.append(omega**q)
    return np.diag(vals)


def identify_pauli(A):
    _x,_z,X1,Z1,X2,Z2=paulis()
    for a,b,c,d in itertools.product(range(3),repeat=4):
        P=(np.linalg.matrix_power(X1,a) @ np.linalg.matrix_power(Z1,b)
           @ np.linalg.matrix_power(X2,c) @ np.linalg.matrix_power(Z2,d))
        if phase_distance(A,P)<TOL:
            return (a,b,c,d)
    return None


def is_clifford(U):
    _x,_z,X1,Z1,X2,Z2=paulis()
    Ud=U.conj().T
    images=[]
    for P in (X1,Z1,X2,Z2):
        images.append(identify_pauli(U@P@Ud))
    return all(x is not None for x in images),images


def main():
    gates={}
    images={}
    for a,b,c in itertools.product(range(3),repeat=3):
        U=quadratic_gate(a,b,c)
        ok,img=is_clifford(U)
        assert ok
        gates[(a,b,c)]=U
        images[str((a,b,c))]=img
    assert len(gates)==27
    I9=np.eye(9)

    for s,U in gates.items():
        assert np.linalg.norm(np.linalg.matrix_power(U,3)-I9)<TOL
        for t,V in gates.items():
            st=tuple((s[i]+t[i])%3 for i in range(3))
            assert phase_distance(U@V,gates[st])<TOL

    T=np.diag([1,zeta9,zeta9**-1])
    T1=np.kron(T,np.eye(3))
    tok,timg=is_clifford(T1)
    assert not tok
    _x,_z,_X1,Z1,_X2,_Z2=paulis()
    assert phase_distance(np.linalg.matrix_power(T1,3),Z1)<TOL

    nearest=min(phase_distance(T1,U) for U in gates.values())
    assert nearest>1e-6

    out={
      "schema":"w33.20260924.bell_shell_clifford_cyclotomic_lift.v1",
      "status":"PASS_BELL_SHELL_IS_QUADRATIC_CLIFFORD_AND_T_IS_MU9_LIFT",
      "bell_shell_quadratic_group":{
        "coordinate_space":"Sym_2(F3) ~= F3^3",
        "order":27,
        "law":"U_S U_T = U_(S+T) projectively",
        "exponent":3,
        "phase_field":"mu_3",
        "all_27_normalize_two_qutrit_paulis":True,
      },

      "nonclifford_lift":{
        "gate":"T1 = diag(1,zeta9,zeta9^-1) tensor I3",
        "zeta9_order":9,
        "T1_cubed":"Z1 projectively",
        "T1_is_Clifford":False,
        "nearest_quadratic_history_projective_distance":nearest,
        "phase_quotient":"mu_9/mu_3 ~= C3",
      },
      "universality_reading":(
        "The 27 quadratic histories form a finite diagonal Clifford group. "
        "The ADQC analyzer can carry the required basis-dependent ninth-root "
        "phase profile instead of demanding another finite W33 gate."
      ),

      "relation_to_prior_repo_no_go":(
        "A scalar ninth root is conjugation-trivial. The required resource "
        "is the nonuniform computational-basis phase profile of qutrit T."
      ),
      "boundary":(
        "Exact ideal gate algebra; no protected optical analyzer threshold "
        "or laboratory error budget is claimed."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "quadratic_group_order":27,
      "T_is_Clifford":False,
      "nearest_distance":nearest,
    },indent=2))


if __name__=="__main__":
    main()
