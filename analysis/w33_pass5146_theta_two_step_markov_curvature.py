#!/usr/bin/env python3
"""Pass5146: the first theta random-walk discriminator occurs at two steps.

Pass5119 gives universal one-step stay probability 1/2 for every codeword support.
Pass5143 gives the second adjacency moment.  Normalizing that moment by D^2|S|
produces a sharp two-step return/stay bound whose excess is the curvature defect.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5146_THETA_TWO_STEP_MARKOV_CURVATURE.json'

def row(q):
    D=8*(q-1);k=D//2;bound=Fraction(k*(k+2),D*D)
    assert bound==Fraction(1,4)+Fraction(1,D)
    return {'q':q,'theta_degree':D,'one_step_stay':'1/2','two_step_minimum':str(bound)}

def main():
    A=[row(q) for q in (2,3,4,5)]
    out={'pass':5146,'status':'THEOREM_THETA_TWO_STEP_MARKOV_CURVATURE',
         'setup':'Run the simple random walk on the intrinsic D=8(q-1) regular theta graph, starting uniformly on a nonzero codeword support S.',
         'one_step':'P[X_1 in S | X_0 uniform on S]=1/2 for every codeword support, by Pass5119.',
         'two_step':'P[X_2 in S | X_0 uniform on S] = (1_S^T A^2 1_S)/(D^2 |S|) >= 1/4 + 1/D.',
         'exact_excess':'P2-(1/4+1/D)=Delta_2/(D^2|S|), where Delta_2 is the nonnegative 8-divisible curvature defect of Pass5143.',
         'equality':'Equality iff every exterior boundary vertex has exactly two selected theta-neighbors. Chamber stars attain equality at q=2,3,4,5.',
         'q2_complete':'Pass5143 exhaustively proves that the equality class at q=2 consists of exactly 45 words, all weight 16.',
         'anchors':A,
         'interpretation':'The one-step chain is deliberately blind to weight; the first local Markov statistic that sees geometric curvature is the two-step return probability.',
         'boundary':'This is a finite theta-graph random-walk theorem, not a physical diffusion or hardware-noise claim.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
