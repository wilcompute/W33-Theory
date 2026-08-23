#!/usr/bin/env python3
"""Pass9949-9956: gauge-invariant qutrit orientation readout for the Holonet.

Renumbered from the earlier Pass9917-9924 draft to avoid the later parallel
Pass9921-9944 packet already landed on master.

Replace the fragile absolute phase tag by the three-state Bargmann/Pancharatnam
loop B=<psi0|psi1><psi1|psi2><psi2|psi0>.  B is exactly invariant under
independent U(1) phase gauges and any common U(3) mode rotation.  Complex
conjugation reverses Im(B), giving an orientation bit.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9949_9956_BARGMANN_ORIENTATION_READOUT.json'
BASE=[np.array([1,0,0],complex),np.array([1,1,0],complex)/np.sqrt(2),np.array([1,1j,1],complex)/np.sqrt(3)]

def run_profile(seed,eps,noise,n=2000):
    rng=np.random.default_rng(seed)
    def haar():
        Z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));Q,R=np.linalg.qr(Z);d=np.diag(R)
        return Q*(d/np.abs(d)).conj()
    def small_u(e):
        H=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));H=(H+H.conj().T)/2
        w,V=np.linalg.eigh(H);return V@np.diag(np.exp(1j*e*w))@V.conj().T
    good=naive=0
    for t in range(n):
        chir=1 if t%2==0 else -1;states=[x.copy() if chir==1 else x.conj() for x in BASE];U=haar();obs=[]
        for x in states:
            y=small_u(eps)@(U@x);y*=np.exp(1j*rng.uniform(0,2*np.pi));y+=noise*(rng.normal(size=3)+1j*rng.normal(size=3));y/=np.linalg.norm(y);obs.append(y)
        B=np.vdot(obs[0],obs[1])*np.vdot(obs[1],obs[2])*np.vdot(obs[2],obs[0]);good+=int((1 if B.imag>=0 else -1)==chir)
        A=np.vdot(obs[0],obs[1]);naive+=int((1 if A.imag>=0 else -1)==chir)
    return {'trials':n,'bargmann_correct':good,'bargmann_accuracy':good/n,'naive_absolute_phase_correct':naive,'naive_accuracy':naive/n}

def main():
    B=np.vdot(BASE[0],BASE[1])*np.vdot(BASE[1],BASE[2])*np.vdot(BASE[2],BASE[0]);assert abs(B-(1+1j)/6)<1e-12
    profiles={'gauge_only':run_profile(2026082301,0,0),'mild':run_profile(2026082302,.05,.005),'moderate':run_profile(2026082303,.15,.02),'strong':run_profile(2026082304,.30,.05),'extreme':run_profile(2026082305,.50,.08)}
    assert [profiles[k]['bargmann_correct'] for k in profiles]==[2000,2000,1993,1654,1107]
    out={'schema':'w33.pass9949_9956.bargmann_orientation_readout.v1','status':'PASS','passes':'9949-9956','renumbered_from':'9917-9924 due later parallel collision',
         'observable':{'B':'<psi0|psi1><psi1|psi2><psi2|psi0>','orientation_bit':'sign(Im B)','ideal_B':'(1+i)/6','ideal_phase':'pi/4'},
         'exact_invariances':['independent port phases cancel around the loop','common U(3) preserves all inner products','complex conjugation reverses Im(B)'],
         'seeded_profiles':profiles,'control':'naive absolute overlap phase is near chance under arbitrary local phases',
         'theorem':'The Bargmann loop is an exact gauge-invariant qutrit chirality observable and stays 99.65% accurate in the deterministic moderate stress profile while the absolute-phase control is near chance.',
         'boundary':'Exact invariance; seeded simulation accuracies are not hardware data or statistical guarantees.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','moderate':profiles['moderate']}));return 0
if __name__=='__main__':raise SystemExit(main())
