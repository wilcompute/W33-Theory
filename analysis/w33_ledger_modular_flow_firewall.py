#!/usr/bin/env python3
"""Finite-geometry firewall for continuous modular flow.

The folded Tomita conjugation lands exactly on a W33 anti-symplectic mirror.
Continuous modular flow is different: unless the faithful state is tracial, it
cannot remain inside the finite projective Pauli/W33 automorphism group on any
time interval.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np

OUT=Path("data/PART_LEDGER_MODULAR_FLOW_FIREWALL.json")

def phase_distance(A,B):
    d=A.shape[0]
    ov=abs(np.trace(B.conj().T@A))
    return float(np.sqrt(max(0.0,2*d-2*ov)))

def main():
    q=3
    omega=np.exp(2j*np.pi/q)
    X=np.roll(np.eye(q,dtype=complex),1,axis=0)
    Z=np.diag([omega**j for j in range(q)])
    rho=np.diag(np.array([1.,2.,4.])/7.)
    logs=np.log(np.diag(rho))
    paulis=[]
    for a,b in itertools.product(range(q),repeat=2):
        if a==0 and b==0:continue
        paulis.append(np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b))
    rows=[]
    for t in [0.07,0.19,0.37,0.83]:
        U=np.diag(np.exp(1j*t*logs))
        A=U@X@U.conj().T
        rows.append({"t":t,"min_projective_pauli_distance":min(phase_distance(A,P) for P in paulis)})
    checks={
      "state_nontracial":float(np.ptp(np.diag(rho)))>0.1,
      "generic_modular_flow_exits_pauli_rays":all(r["min_projective_pauli_distance"]>1e-3 for r in rows),
    }
    assert all(checks.values()),checks
    out={
      "schema":"w33.ledger.modular-flow-firewall.v1",
      "status":"NO_GO_NONTRIVIAL_CONTINUOUS_MODULAR_FLOW_INSIDE_W33_AUTOMORPHISMS",
      "theorem":[
        "Let rho be faithful and sigma_t(P)=rho^(it) P rho^(-it). If sigma_t maps every projective Pauli ray into the finite W33 Pauli-ray set for all t in an interval, continuity forces the induced permutation to be constant.",
        "At t=0 that permutation is the identity, so sigma_t(P)=c_P(t)P for every Pauli P.",
        "For qutrit Paulis P^3=I. Hence c_P(t)^3=1; continuity and c_P(0)=1 force c_P(t)=1.",
        "Therefore rho commutes with the full Pauli algebra, so rho is scalar. The only continuous modular flow living entirely inside W33 automorphisms is the trivial tracial flow."
      ],
      "physics_boundary":"The folded Tomita J can be a discrete W33 mirror, but Ledger modular time cannot literally be continuous motion in the finite W33 automorphism group. A continuum/enlarged operator algebra must carry the nontrivial flow while W33 remains a discrete skeleton.",
      "numerical_nontracial_witness":rows,
      "checks":checks
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
    return out
if __name__=="__main__":main()
