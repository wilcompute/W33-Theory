#!/usr/bin/env python3
"""Pass5614: a firewall-separated q=3 physics selector stack.

Three logically distinct q-family mechanisms share the factor q-3:
  (A) exact PSL2 fixed-point Bose-Mesner degeneration (Pass5603),
  (B) exact scalar-lift condition: projective lines have q-1 nonzero lifts, so
      a literal two-sheeted sign cover exists iff q=3 among odd q,
  (C) the repo's phenomenological mixing dictionary has the exact defect
      sin^2(theta23)-sin^2(thetaW)-sin^2(theta12)=q(q-3)/Phi3(q).

Only (A),(B) are structural theorems. (C) is a consistency/selection statement
inside the repo's model dictionary, not an independent derivation of measured
mixing.  The older Ollivier/Gauss-Bonnet script is recorded only as q=3 evidence;
its all-q curvature extrapolation is NOT promoted here.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5614_Q3_PHYSICS_SELECTOR.json'

def row(q):
    phi3=q*q+q+1
    k2=q*(q+1)*(q-3)//4
    m1=(q-3)*(q+1)*(q+1)//4
    w=Fraction(q,phi3)
    t12=Fraction(q+1,phi3)
    t23=Fraction(q*q-q+1,phi3)
    defect=t23-w-t12
    assert defect==Fraction(q*(q-3),phi3)
    return {'q':q,'fusion_relation_k2':k2,'fusion_multiplicity_m1':m1,
            'scalar_fiber_q_minus_1':q-1,'is_literal_double_cover':q-1==2,
            'model_mixing_defect':[defect.numerator,defect.denominator]}

def main():
    anchors=[row(q) for q in (3,5,7,9,11,13,25)]
    assert anchors[0]['fusion_relation_k2']==anchors[0]['fusion_multiplicity_m1']==0
    assert anchors[0]['is_literal_double_cover']
    assert all(x['fusion_relation_k2']>0 and x['fusion_multiplicity_m1']>0 for x in anchors[1:])
    assert all(not x['is_literal_double_cover'] for x in anchors[1:])
    assert anchors[0]['model_mixing_defect']==[0,1]
    out={
      'pass':5614,'status':'Q3_TRIPLE_SELECTOR_WITH_SEPARATED_EVIDENCE_LAYERS',
      'structural_selector_1':{
        'name':'fixed-point association-algebra degeneration',
        'formulas':['k_2=q(q+1)(q-3)/4','m_1=(q-3)(q+1)^2/4'],
        'conclusion':'q=3 is the unique odd q>=3 where the generic relation and its companion primitive idempotent both disappear'
      },
      'structural_selector_2':{
        'name':'projective-vector sign lift',
        'formula':'|F_q^*|=q-1 lifts per projective point',
        'conclusion':'a literal two-sheeted nonzero-vector cover exists iff q=3 among odd q'
      },
      'model_selector_3':{
        'name':'repo PMNS/weak-angle sum rule',
        'dictionary':['sin^2 thetaW=q/Phi3','sin^2 theta12=(q+1)/Phi3','sin^2 theta23=(q^2-q+1)/Phi3'],
        'defect':'q(q-3)/(q^2+q+1)',
        'boundary':'this is a selector internal to the repo phenomenological dictionary, not an independent experimental theorem'
      },
      'ollivier_boundary':'GRAVITY_BREAKTHROUGH.py exhaustively verifies kappa=1/6 on all 240 q=3 edges. Its displayed all-q kappa extrapolation is not proved there, so it is not used as an all-q selector in this pass.',
      'anchors':anchors,
      'physics_reading':'The strongest q=3 case now comes from a representation-algebra phase transition plus a spin-like double-cover condition; the mixing identity is supporting model evidence rather than the foundation.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
