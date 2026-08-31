#!/usr/bin/env python3
"""Freeze the key all-five frontier invariants after the reconstruction steps.

This script is intentionally cheap.  In CI it runs after the expensive all-five
and directed-A20 audits, reads their regenerated certificates, and compares the
key theorem invariants against the committed release packet.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
KEY=json.loads((ROOT/'data/PART_W33_20260831_ALL5_FRONTIER_KEY_RESULTS.json').read_text())
A=json.loads((ROOT/'data/PART_W33_20260831_ALL5_FRONTIER_AUDIT.json').read_text())
D=json.loads((ROOT/'data/PART_W33_20260831_A20_DIRECTED_ORBITAL_REFINEMENT.json').read_text())

assert KEY['status']=='PASS' and A['status']=='PASS' and D['status']=='PASS'

rows=A['track1_allSevenKRestrictions']['sectorRows']
actual=[
    {
        'dimension':r['dimension'],
        'central':[r['centralDimensions']['trivial'],r['centralDimensions']['omega'],r['centralDimensions']['omega2']],
        'characterNorm':r['characterNorm'],
    }
    for r in rows
]
assert actual==KEY['track1_KRestrictions']

E=A['track2_eisensteinSixes']; K=KEY['track2_EisensteinCarrier']
assert E['sectorDimension']==K['sectorDimension']==24
assert E['centralNontrivialRationalDimension']==K['centralNontrivialRationalDimension']==12
assert E['complexDimensions']==K['complexDimensions']==[6,6]
assert E['identity']=='J^2=-3 on the 12-dimensional rational carrier'
assert len(E['deterministicSixFibreBasisWitness'])==K['basisWitnessDeckFibres']==6

R=A['track3_rightKernel']; KR=KEY['track3_RightKernel']
assert R['kernelDimension']==324 and R['imageDimension']==216
assert R['stackedColourRowRank']==KR['stackedColourRowRank']==372
kd=R['kernelDimensions']
assert kd['M']==kd['Mplus']==kd['Mminus']==324
assert kd['pairwiseIntersection']==kd['tripleIntersection']==168
assert 216+216-R['stackedColourRowRank']==KR['colourRowSpaceIntersectionDimension']==60

mod=A['track4_modularSmithFiltration']['ranks']
rankM={str(x['p']):x['rankM'] for x in mod}
rankP={str(x['p']):x['rankMplus'] for x in mod}
rankG={str(x['p']):x['rankGramM'] for x in mod}
assert rankM==KEY['track4_ModularSmith']['rankM']
assert rankP==KEY['track4_ModularSmith']['rankMplus']
assert rankG==KEY['track4_ModularSmith']['rankGramM']
assert A['track4_modularSmithFiltration']['gramDeterminantPrimeValuations']==KEY['track4_ModularSmith']['gramDeterminantPrimeValuations']

C=A['track5_fullCoherentConfiguration']; KC=KEY['track5_CoherentConfiguration']
for k in ('r55','r66','r56','r65','totalRank'):
    assert C[k]==KC[k]
assert C['A30FusionOf55Orbitals']==KC['A30Fusion']==[6]
assert C['A20FusionOf55Orbitals']==KC['A20Fusion']==[1,2]

DD=KEY['directedA20']
assert D['A20OrbitalIds']==DD['transposePairedOrbitalIds']==[1,2]
assert D['A20Valencies']==DD['valencies']==[10,10]
assert D['crossConstants']==DD['MplusMminusTConstants']==[1,3]
assert not D['commutators']['MplusMminusT_with_A20_zero']
assert not D['commutators']['MplusMminusT_with_A30_zero']

print(json.dumps({
    'status':'PASS','sevenSectors':len(rows),'coherentRank':C['totalRank'],
    'commonColourRowSpace':60,'commonKernel':168,'A20Directed':[10,10,1,3]
},sort_keys=True))
