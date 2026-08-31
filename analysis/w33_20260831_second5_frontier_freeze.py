#!/usr/bin/env python3
"""Cheap regression lock for the second five exact circuit frontier closures."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/PART_W33_20260831_SECOND_FIVE_FRONTIER_KEY_RESULTS.json'

def main():
    x=json.loads(DATA.read_text())
    assert x['status']=='PASS'
    c=x['commonColour60']
    assert c['dimension']==60 and c['equalsTransported60Sector'] is False
    assert c['transported60DirectIntersections']==[0,0]
    assert c['sectorwiseDiagonalIntersections']==[0,0,0,20,0,24,1]
    assert c['nonzeroOffDiagonalPairwiseIntersections']==[]
    assert c['moduleDecomposition']==[1,15,20,24]

    L=x['leftC5Wedderburn']
    assert L['orbitalAlgebraDimension']==10 and L['centerDimension']==7
    assert L['complexBlockSizes']==[2,1,1,1,1,1,1]
    assert L['leftModuleDecompositionByDegree']=={'1':1,'15':2,'20':1,'24':1,'30':1,'30bar':1,'81':1}
    assert L['symmetric60Sector']['complexSplit']==[30,30]
    assert L['symmetric60Sector']['discriminant']==-21168
    assert L['symmetric60Sector']['field']=='Q(sqrt(-3))'

    R=x['rightC6AndKernel324']
    assert R['orbitalAlgebraDimension']==32 and R['centerDimension']==9
    assert R['complexBlockSizes']==[3,2,2,2,2,2,1,1,1]
    assert R['kernelDimension']==324 and R['kernelCharacterNorm']==8
    assert R['kernelMultiplicityFreeComplexDecomposition']==[15,20,24,30,30,60,64,81]
    assert R['kernelQuadratic30Pair']['discriminant']==-3888
    assert R['kernelQuadratic30Pair']['field']=='Q(sqrt(-3))'

    S=x['incidenceSmith']
    assert S['M']['nonzeroSmithForm']=='1^156 2^44 4^15 8^1'
    assert S['Mplus']['nonzeroSmithForm']=='1^201 2^14 4^1'
    assert S['Mminus']['nonzeroSmithForm']=='1^201 2^14 4^1'
    assert S['M']['twoAdicIndexExponent']==77
    assert S['Mplus']['twoAdicIndexExponent']==S['Mminus']['twoAdicIndexExponent']==16

    E=x['eisensteinSixNoGo']
    assert E['dark20OmegaNorm']==E['sector24OmegaNorm']==1
    assert E['omegaCrossInnerProduct']==0 and E['bestProjectedRationalRank']==0
    assert E['KOrbitalCount']==111 and E['conclusion']=='NO_GO'

    print(json.dumps({
      'status':'PASS','common60':c['moduleDecomposition'],
      'leftWedderburn':L['complexBlockSizes'],'kernelNorm':R['kernelCharacterNorm'],
      'smith':[S['M']['nonzeroSmithForm'],S['Mplus']['nonzeroSmithForm']],
      'sixNoGo':E['omegaCrossInnerProduct']
    },sort_keys=True))

if __name__=='__main__': main()
