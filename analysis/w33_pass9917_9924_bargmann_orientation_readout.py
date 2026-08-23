#!/usr/bin/env python3
"""Pass9917-9924: gauge-invariant qutrit orientation readout for the Holonet.

The previous coherent-port stress test showed that line support and dark fraction
were robust but an absolute phase orientation tag failed first.  Replace the
absolute phase by the three-state Bargmann/Pancharatnam loop

 B=<psi0|psi1><psi1|psi2><psi2|psi0>.

B is exactly invariant under independent U(1) phase gauges psi_j -> e^{itheta_j}
psi_j and under any common U(3) mode rotation.  Complex conjugation sends B to
conjugate(B), so sign(Im B) is an orientation/chirality bit when Im B != 0.

The deterministic seeded stress test adds arbitrary local phases, a common Haar
U(3), independent small unitary mode errors at each port, and complex tomography
noise.  A naive absolute overlap phase is included as a control.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9917_9924_BARGMANN_ORIENTATION_READOUT.json'

BASE=[
 np.array([1,0,0],dtype=complex),
 np.array([1,1,0],dtype=complex)/np.sqrt(2),
 np.array([1,1j,1],dtype=complex)/np.sqrt(3),
]

def run_profile(seed,eps,noise,n=2000):
    rng=np.random.default_rng(seed)
    def haar_u3():
        Z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
        Q,R=np.linalg.qr(Z);d=np.diag(R)
        return Q*(d/np.abs(d)).conj()
    def small_u(e):
        H=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));H=(H+H.conj().T)/2
        w,V=np.linalg.eigh(H)
        return V@np.diag(np.exp(1j*e*w))@V.conj().T
    good_loop=0;good_naive=0
    for t in range(n):
        chir=1 if t%2==0 else -1
        states=[x.copy() if chir==1 else x.conj() for x in BASE]
        U=haar_u3();obs=[]
        for x in states:
            y=small_u(eps)@(U@x)
            y*=np.exp(1j*rng.uniform(0,2*np.pi))
            y+=noise*(rng.normal(size=3)+1j*rng.normal(size=3))
            y/=np.linalg.norm(y);obs.append(y)
        B=np.vdot(obs[0],obs[1])*np.vdot(obs[1],obs[2])*np.vdot(obs[2],obs[0])
        pred=1 if B.imag>=0 else -1
        good_loop+=int(pred==chir)
        A=np.vdot(obs[0],obs[1])
        pred0=1 if A.imag>=0 else -1
        good_naive+=int(pred0==chir)
    return {'trials':n,'bargmann_correct':good_loop,'bargmann_accuracy':good_loop/n,
            'naive_absolute_phase_correct':good_naive,'naive_accuracy':good_naive/n}

def main():
    # Ideal chirality pair has loop phase +/- pi/4.
    B=np.vdot(BASE[0],BASE[1])*np.vdot(BASE[1],BASE[2])*np.vdot(BASE[2],BASE[0])
    assert abs(B-(1+1j)/6)<1e-12
    Bc=np.vdot(BASE[0].conj(),BASE[1].conj())*np.vdot(BASE[1].conj(),BASE[2].conj())*np.vdot(BASE[2].conj(),BASE[0].conj())
    assert abs(Bc-B.conjugate())<1e-12

    profiles={
      'gauge_only':run_profile(2026082301,0.0,0.0),
      'mild':run_profile(2026082302,0.05,0.005),
      'moderate':run_profile(2026082303,0.15,0.02),
      'strong':run_profile(2026082304,0.30,0.05),
      'extreme':run_profile(2026082305,0.50,0.08),
    }
    assert profiles['gauge_only']['bargmann_correct']==2000
    assert profiles['mild']['bargmann_correct']==2000
    assert profiles['moderate']['bargmann_correct']==1993
    assert profiles['strong']['bargmann_correct']==1654
    assert profiles['extreme']['bargmann_correct']==1107
    assert profiles['gauge_only']['naive_absolute_phase_correct']==1009

    out={
      'schema':'w33.pass9917_9924.bargmann_orientation_readout.v1','status':'PASS','passes':'9917-9924',
      'observable':{'B':'<psi0|psi1><psi1|psi2><psi2|psi0>','orientation_bit':'sign(Im B)','ideal_B':'(1+i)/6','ideal_phase':'pi/4'},
      'exact_invariances':[
        'independent port phases psi_j -> exp(i theta_j) psi_j cancel around the loop',
        'a common U(3) mode rotation preserves all three inner products',
        'complex conjugation reverses Im(B) and hence the chirality bit'],
      'seeded_profiles':profiles,
      'control':('The naive sign of Im<psi0|psi1> is gauge-dependent and remains near chance when arbitrary local port phases are present.'),
      'theorem':('A three-qutrit Bargmann loop supplies a gauge-invariant orientation observable that exactly survives arbitrary local U(1) phases and common U(3) mixing. In the seeded model it remains perfect through mild perturbations and 99.65% accurate at the moderate profile, while the absolute-phase control is near chance.'),
      'boundary':('The invariance statements are exact linear algebra. The quoted accuracies are deterministic seeded simulations of independent unitary/tomography perturbations, not hardware data or a statistical performance guarantee.')
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','moderate':profiles['moderate'],'strong':profiles['strong']}))
    return 0
if __name__=='__main__':raise SystemExit(main())
