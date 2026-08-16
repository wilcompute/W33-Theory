#!/usr/bin/env python3
"""Pass5625: replace legacy anomaly overclaims by an exact finite eta/spectral-flow diagram.

The repo's old tests/test_anomaly_polynomial.py is quarantined by the Pass1150
shifted-adjacency retraction and is not evidence for physical anomaly
cancellation.  Here we use only the frozen intrinsic magnetic spectra.

For a finite Hermitian mass operator M(r)=rI+H, define away from zero modes
  eta(M)=#positive eigenvalues - #negative eigenvalues.
For the full 32-state lift the seven walls occur at r=-h.  For the canonical
deck-odd 16-sector particle-hole symmetry reduces this to four walls.

This is a finite APS-like spectral-asymmetry diagnostic.  It is not a continuum
index theorem, gauge-anomaly polynomial, or Green-Schwarz mechanism.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5625_FINITE_ETA_SPECTRAL_FLOW.json'

def eta(bands,r):
    pos=neg=zero=0
    for h,m in bands:
        x=r+h
        if x>0: pos+=m
        elif x<0: neg+=m
        else: zero+=m
    return pos-neg,zero

def phase_diagram(bands):
    walls=sorted(set(-h for h,m in bands))
    probes=[walls[0]-1]+[(a+b)/2 for a,b in zip(walls,walls[1:])]+[walls[-1]+1]
    chambers=[]
    bounds=[None]+walls+[None]
    for i,r in enumerate(probes):
        e,z=eta(bands,r); assert z==0
        chambers.append({'left':bounds[i],'right':bounds[i+1],'eta':e})
    wall_rows=[]
    for r in walls:
        e,z=eta(bands,r); wall_rows.append({'r':r,'eta_excluding_zero':e,'zero_modes':z})
    return walls,chambers,wall_rows

def main():
    full=[(-6,6),(-3,7),(-1,3),(2,6),(3,5),(6,4),(9,1)]
    odd=[(-6,4),(-3,4),(3,4),(6,4)]
    wf,cf,zf=phase_diagram(full); wo,co,zo=phase_diagram(odd)
    assert wf==[-9,-6,-3,-2,1,3,6]
    assert [x['eta'] for x in cf]==[-32,-30,-22,-12,0,6,20,32]
    assert [x['zero_modes'] for x in zf]==[1,4,5,6,3,7,6]
    assert wo==[-6,-3,3,6]
    assert [x['eta'] for x in co]==[-16,-8,0,8,16]
    assert [x['zero_modes'] for x in zo]==[4,4,4,4]
    assert eta(full,0)==(0,0) and eta(odd,0)==(0,0)

    out={
      'pass':5625,'status':'EXACT_FINITE_ETA_BALANCED_CHAMBERS_AND_SPECTRAL_FLOW_WALLS',
      'definition':'eta(rI+H)=N_+(r)-N_-(r), away from zero-mode walls',
      'full32':{'walls':wf,'chambers':cf,'wall_zero_modes':zf,'balanced_chamber':'-2 < r < 1'},
      'deck_odd16':{'walls':wo,'chambers':co,'wall_zero_modes':zo,'balanced_particle_hole_chamber':'-3 < r < 3'},
      'spectral_flow':'At each wall eta jumps by twice the zero-mode multiplicity; half the jump is the finite spectral-flow multiplicity.',
      'legacy_firewall':'tests/test_anomaly_polynomial.py is skipped/quarantined under PASS1150_SHIFTED_ADJACENCY_RETRACTION and is not used here.',
      'physics_firewall':'eta=0 is a finite spectral-balance statement. It does not establish perturbative gauge-anomaly cancellation, a continuum APS index, anomaly inflow, or Green-Schwarz factorization.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
