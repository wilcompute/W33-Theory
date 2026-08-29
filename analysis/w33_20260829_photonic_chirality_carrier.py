#!/usr/bin/env python3
"""Finite carrier audit for the geometric C2 chirality and torsorial C3 qutrit.

Repository inputs:
  * the local six-state action has geometric chirality chi in F2 and a C3 torsor;
  * the Holonet optical dictionary uses OAM shifts for the qutrit X operation;
  * translated qutrit frames are recentered by inverse phase-space shifts.

External optical prior art motivates circular polarization (SAM) as a genuine
binary photonic degree of freedom and q-plates as SAM<->OAM spin-orbit couplers.
This script checks the modular selection rule for a q-plate to flip SAM while
leaving an OAM-residue qutrit coordinate unchanged.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260829_PHOTONIC_CHIRALITY_CARRIER.json'

def induced(q,chi,t):
    # Ideal q-plate rule at full conversion: circular polarization flips and
    # OAM changes by +/-2q.  Only the OAM residue modulo 3 is retained here.
    n=int(2*q)
    sign=1 if chi==0 else -1
    return 1-chi,(t+sign*n)%3

def main():
    candidates=[Fraction(n,2) for n in range(1,13)]
    pure=[]
    for q in candidates:
        ok=all(induced(q,chi,t)==(1-chi,t) for chi in (0,1) for t in range(3))
        if ok:pure.append(q)
    assert pure[:2]==[Fraction(3,2),Fraction(3,1)]
    q=Fraction(3,2)
    table={(chi,t):induced(q,chi,t) for chi in (0,1) for t in range(3)}
    assert all(v==(1-k[0],k[1]) for k,v in table.items())
    # By contrast the common q=1/2 spin-orbit step changes the C3 coordinate.
    assert any(induced(Fraction(1,2),chi,t)!=(1-chi,t) for chi in (0,1) for t in range(3))

    out={
      'schema':'w33.20260829.photonic-chirality-carrier.v1','status':'PASS',
      'abstractTarget':{'stateSpace':'C2 chirality x C3 torsor','chirality':'geometric residual-hinge block','qutritOrigin':'gauge / no canonical F3 zero'},
      'carrierCandidate':{'chiralityDoF':'left/right circular polarization (photon SAM/helicity)',
        'qutritDoF':'OAM label modulo the centered/recentered three-mode convention',
        'independenceReading':'polarization carries the binary block while OAM carries the ternary torsor'},
      'qPlateSelectionRule':{'idealShift':'Delta ell = +/- 2q with circular-polarization flip',
        'pureChiralityModulo3':'2q == 0 mod 3','minimalPositiveHalfIntegerCharge':'q=3/2',
        'inducedActionAtQ3Over2':'(chi,t) -> (1-chi,t)','qHalfCounterexample':'q=1/2 flips chirality but also shifts t by +/-1'},
      'repoCompatibility':{
        'oamDictionary':'BT1568 maps X to an OAM shift/prism step',
        'recenterABI':'BT1573/BT1587 treats translated qutrit frames by inverse recentering',
        'radialFirewall':'BT1589-BT1591 requires radial/mode-overlap leakage checks'},
      'hardwareReading':'Circular polarization is the cleanest existing optical C2 carrier. A q=3/2 q-plate is a gauge-compatible spin-orbit interface at the OAM-residue level because its +/-3 shift is invisible modulo 3.',
      'boundary':'The modular action is exact, but the repository has not calibrated a q=3/2 device, shown that ell->ell+/-3 stays inside the centered radial/OAM code space, or measured loss/coherence. An optical recenter/filter stage remains an engineering requirement.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
