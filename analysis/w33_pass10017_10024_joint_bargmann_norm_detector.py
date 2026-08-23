#!/usr/bin/env python3
"""Pass10017-10024: combine Bargmann chirality with the F9 norm-parity C2 channel.

The Bargmann loop gives a continuous/gauge-invariant chirality bit; the F9 norm
map gives an exact discrete C2 parity invariant under the full norm-one C4 phase
gauge.  Encode the same orientation bit in both channels and use an
AGREE-OR-ERASE decoder: accept only when they agree.

If the Bargmann bit flips with probability p_B and an F9 symbol is independently
corrupted with probability epsilon, uniformly to one of the other seven nonzero
symbols, then exactly four of those seven alternatives lie in the opposite norm
coset.  Hence p_N=4 epsilon/7.  The decoder acceptance and conditional error are

 a=(1-p_B)(1-p_N)+p_B p_N,
 e_cond=p_B p_N/a.

The p_B values below are the deterministic seeded accuracies already frozen at
Pass9949-9956.  The F9 epsilon values are explicit stress assumptions, not data.
"""
from __future__ import annotations
from fractions import Fraction
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10017_10024_JOINT_BARGMANN_NORM_DETECTOR.json'

PROFILES={
 'gauge_only':(Fraction(0),Fraction(0)),
 'mild':(Fraction(0),Fraction(1,100)),
 'moderate':(Fraction(7,2000),Fraction(1,20)),
 'strong':(Fraction(346,2000),Fraction(3,20)),
 'extreme':(Fraction(893,2000),Fraction(3,10)),
}

def rec(pB,eps):
    pN=Fraction(4,7)*eps
    accept=(1-pB)*(1-pN)+pB*pN
    err=pB*pN/accept if accept else Fraction(0)
    return {'p_B':float(pB),'epsilon_F9_symbol':float(eps),'p_N':float(pN),
            'acceptance':float(accept),'conditional_error':float(err),
            'exact':{'p_N':str(pN),'acceptance':str(accept),'conditional_error':str(err)}}

def main():
    rows={k:rec(*v) for k,v in PROFILES.items()}
    assert rows['moderate']['exact']['p_N']=='1/35'
    assert rows['moderate']['exact']['acceptance']=='67769/70000'
    assert rows['moderate']['exact']['conditional_error']=='7/67769'
    assert abs(rows['moderate']['conditional_error']-0.00010329206569375378)<1e-15
    assert rows['strong']['exact']['conditional_error']=='519/26983'
    assert rows['extreme']['exact']['conditional_error']=='1786/12487'
    out={
      'schema':'w33.pass10017_10024.joint_bargmann_norm_detector.v1','status':'PASS','passes':'10017-10024',
      'decoder':'encode one C2 orientation bit in Bargmann chirality and F9 norm parity; accept only when the two decoded bits agree',
      'exact_model':{
        'F9_norm_flip_given_uniform_nonzero_symbol_corruption':'p_N=4 epsilon/7',
        'independence_assumption':True,
        'acceptance':'(1-p_B)(1-p_N)+p_B p_N',
        'conditional_error':'p_B p_N / acceptance'},
      'profiles':rows,
      'moderate_result':{
        'Bargmann_error_alone':0.0035,
        'F9_symbol_corruption':0.05,
        'acceptance':rows['moderate']['acceptance'],
        'accepted_error':rows['moderate']['conditional_error'],
        'suppression_factor_vs_Bargmann':0.0035/rows['moderate']['conditional_error']},
      'theorem':('Under the stated independent-error model, the exact agree-or-erase fusion converts the 0.35% moderate Bargmann error and 5% F9 symbol-corruption stress into 96.812857% acceptance with only 7/67769 = 0.0103292% error among accepted shots. The protection is multiplicative because both channels must flip together to create an undetected error.'),
      'boundary':'The decoder algebra is exact. Bargmann p_B comes from deterministic seeded simulation; epsilon and independence are modeling assumptions, not hardware measurements or statistical guarantees.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','moderate':out['moderate_result']}))
    return 0
if __name__=='__main__':raise SystemExit(main())
