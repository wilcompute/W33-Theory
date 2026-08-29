#!/usr/bin/env python3
"""Koopman/Floquet-style audit of the deterministic Holotrade recovery 2-cycles.

Input provenance is the exhaustive Holotrade long-horizon certificate at
commit d21a08bacf9802da0ba4bb8176b074fbc9ac7722.  This script does not
recompute the Holotrade corpus; it checks the exact two-state Koopman algebra
and the overlap of the measured free-line observable with the -1 mode.
"""
from __future__ import annotations
import json
from pathlib import Path
from sympy import Matrix
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260829_RECOVERY_KOOPMAN_TIMECRYSTAL_BOUNDARY.json'

HIST={(19,19):2255,(17,17):572,(16,17):36,(16,16):17}

def main():
    assert sum(HIST.values())==2880
    U=Matrix([[0,1],[1,0]])
    assert U.eigenvals()=={1:1,-1:1}
    # For a 2-cycle observable h=(h0,h1), the -1 Koopman amplitude is
    # proportional to h0-h1.  Headroom therefore sees the pi mode only when
    # the two cycle headrooms differ.
    pi_overlap=sum(n for (a,b),n in HIST.items() if a!=b)
    zero_overlap=2880-pi_overlap
    assert pi_overlap==36 and zero_overlap==2844
    out={
      'schema':'w33.20260829.recovery-koopman-timecrystal-boundary.v1','status':'PASS',
      'provenance':{'repo':'wilcompute/Holotrade','commit':'d21a08bacf9802da0ba4bb8176b074fbc9ac7722'},
      'cycleOperator':{'matrix':'[[0,1],[1,0]]','eigenvalues':{'+1':1,'-1':1},'quasienergyReading':'0 and pi for unit update period'},
      'headroomObservable':{
        'cycleHistogram':{'19/19':2255,'17/17':572,'16/17':36,'16/16':17},
        'nonzeroPiModeStarts':36,'zeroPiModeStarts':2844,
        'fractionWithPeriodDoubledHeadroom':36/2880},
      'falsifier':'State period two is universal for the declared deterministic policy, but free-line headroom is period doubled on only 36/2880 starts. The dominant 19/19 attractor has no headroom oscillation at all.',
      'timeCrystalBoundary':[
        'the update map is a deterministic scheduler rule, not a demonstrated periodically driven Hamiltonian',
        'no thermodynamic/infinite-volume limit is present',
        'no perturbation-robust spontaneous time-translation-symmetry breaking is established',
        'the policy uses lexicographic tie-breaking and its selected 933 high cycles are not PSp-invariant'
      ],
      'reading':'The -1 Koopman eigenmode is an exact finite-state period-two mode. It is useful for controller spectral analysis but is insufficient evidence for a discrete time-crystal phase.',
      'boundary':'Finite deterministic dynamical-systems statement; explicitly a no-promotion result for physical time-crystal language.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','piModeStarts':pi_overlap,'zeroOverlap':zero_overlap,'fraction':pi_overlap/2880}))
if __name__=='__main__':main()
