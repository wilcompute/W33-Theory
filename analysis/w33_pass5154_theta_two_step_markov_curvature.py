#!/usr/bin/env python3
"""Pass5154: one-step theta walk is blind; two-step return sees curvature."""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5154_THETA_TWO_STEP_MARKOV_CURVATURE.json'

def row(q):
    D=8*(q-1);k=D//2;bound=Fraction(k*(k+2),D*D)
    assert bound==Fraction(1,4)+Fraction(1,D)
    return {'q':q,'theta_degree':D,'one_step_stay':'1/2','two_step_minimum':str(bound)}

def main():
    out={'pass':5154,'status':'THEOREM_THETA_TWO_STEP_MARKOV_CURVATURE',
         'setup':'Simple random walk on the intrinsic D=8(q-1) regular theta graph, started uniformly on a nonzero codeword support S.',
         'one_step':'P[X_1 in S]=1/2 for every codeword support by Pass5119.',
         'two_step':'P[X_2 in S]=(1_S^T A^2 1_S)/(D^2|S|)>=1/4+1/D.',
         'exact_excess':'P2-(1/4+1/D)=Delta_2/(D^2|S|), with Delta_2 from Pass5151.',
         'equality':'Equality iff every exterior boundary vertex has exactly two selected theta-neighbors. Chamber stars attain equality at q=2,3,4,5.',
         'q2_complete':'Pass5151 proves exactly 45 q2 nonzero words attain equality, all weight 16.',
         'anchors':[row(q) for q in (2,3,4,5)],
         'boundary':'Finite theta-graph random-walk theorem, not physical diffusion or a hardware-noise model.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
