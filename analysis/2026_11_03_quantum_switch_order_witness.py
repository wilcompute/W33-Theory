#!/usr/bin/env python3
"""Alternative to geometry: exact controlled-order process / quantum switch.

Do not conflate operational quantum switch with causal inequality violation,
graviton dynamics, retrocausality or a physical superposition of geometries.
"""
from pathlib import Path
import json, numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"2026_11_03_quantum_switch_order_witness.json"
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Z=np.array([[1,0],[0,-1]],complex)
psi=np.array([1,0],complex)
def unitary_axis(t,pauli):
    return np.cos(t/2)*I-1j*np.sin(t/2)*pauli
def states(U,V):
    branch0=V@U@psi
    branch1=U@V@psi
    assert abs(np.linalg.norm(branch0)-1)<1e-11 and abs(np.linalg.norm(branch1)-1)<1e-11
    out=np.concatenate((branch0,branch1))/np.sqrt(2)
    assert abs(np.linalg.norm(out)-1)<1e-11
    minus=(branch0-branch1)/2
    plus=(branch0+branch1)/2
    prob=float(np.vdot(minus,minus).real)
    assert abs(np.vdot(plus,plus).real+prob-1)<1e-10
    return prob,branch0,branch1
def run():
    anti,b0,b1=states(X,Z)
    assert abs(anti-1)<1e-12
    assert abs(np.vdot(b0,b1)+1)<1e-12
    comm,b0,b1=states(X,I)
    assert comm<1e-12
    records=[]
    for theta in (0.,np.pi/6,np.pi/3,np.pi/2,np.pi):
        for phi in (0.,np.pi/6,np.pi/2,np.pi):
            U=unitary_axis(theta,X);V=unitary_axis(phi,Z)
            p,u,v=states(U,V)
            formula=float(np.sin(theta/2)**2*np.sin(phi/2)**2)
            assert abs(p-formula)<1e-11,(theta,phi,p,formula)
            comm_norm=np.linalg.norm((V@U-U@V)@psi)**2/4
            assert abs(p-comm_norm)<1e-11
            records.append({"theta":theta,"phi":phi,
                  "minus_outcome_coherent_switch":p,
                  "minus_outcome_incoherent_classical_order_mixture":0.5,
                  "analytic_commutator_formula":formula})
    # Incoherent mixture has maximally mixed control, regardless of U,V.
    # A control dephasing parameter eta interpolates p-=(1-eta)/2 +eta p_coherent.
    deco=[]
    for eta in (0.,.2,.5,.8,1.):
        for U,V,label in ((X,Z,"anticommuting"),(X,I,"commuting")):
            p,_u,_v=states(U,V)
            deco.append({"label":label,"visibility_eta":eta,
                         "minus_probability":(1-eta)/2+eta*p})
    out={
      "status":"PASS_COHERENT_QUANTUM_SWITCH_COMMUTATOR_NEGATIVE_CONTROLS",
      "pure_switch_definition":"|Psi>=(|0> VU|psi> + |1> UV|psi>)/sqrt(2), with control |+> and two unitary processes. Control measured in X basis.",
      "minus_probability_exact":"p(-)=||(VU-UV)|psi>||²/4",
      "pauli_X_Z_anticommuting_minus_probability":anti,
      "pauli_X_I_commuting_minus_probability":comm,
      "rotation_X_Z_formula":"for Rx(theta),Rz(phi), p(-)=sin²(theta/2) sin²(phi/2)",
      "angle_sweep":records,
      "dephasing_controls":deco,
      "operational_boundary":"Ideal circuit model of coherently controlled operation order. Quantum switch is causally nonseparable but cannot by itself violate ordinary causal inequalities using local laboratory statistics; does not demonstrate retrocausality. A process tensor for an open laboratory needs formal comb CP/trace constraints, which were already implemented elsewhere in this repo; this model is a new W33-independent control.",
      "physics_boundary":"No geometry, graviton, emergent time, local relativistic field theory or physical realization demonstrated.",
      "prior_repository":"analysis/PASS11042_INSTRUMENT_DEPENDENT_PROCESS_MEMORY.md already implements qutrit one-slot combs and instrument dependence; this adds a distinct two-unitary switch control, not a full replacement.",
      "literature":["https://doi.org/10.1103/9jss-yf1c","https://doi.org/10.1103/bnkn-4p3f","https://doi.org/10.1103/kmmy-3dy3"]
    }
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print("PROCESS SWITCH",{"X_Z":anti,"X_I":comm,"sweeps":len(records)},flush=True)
    return out
if __name__=="__main__":run()
