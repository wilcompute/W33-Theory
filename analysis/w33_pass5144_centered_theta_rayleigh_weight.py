#!/usr/bin/env python3
"""Pass5144: centered theta Rayleigh quotient determines codeword weight exactly."""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5144_CENTERED_THETA_RAYLEIGH_WEIGHT.json'

def row(q,N,s):
    D=8*(q-1);a=Fraction(s,N);rho=Fraction(D)*(Fraction(1,2)-a)/(1-a)
    # invert alpha=(D/2-rho)/(D-rho)
    back=(Fraction(D,2)-rho)/(D-rho);assert back==a
    return {'q':q,'apartments':N,'support_weight':s,'alpha':str(a),'theta_degree':D,
            'centered_adjacency_Rayleigh':str(rho),'centered_adjacency_Rayleigh_float':float(rho)}

def main():
    anchors=[row(2,90,16),row(3,1620,81),row(4,13600,256),row(5,73125,625)]
    out={'pass':5144,'status':'THEOREM_CENTERED_THETA_RAYLEIGH_WEIGHT_INVERSION',
         'setup':'Let Theta be D=8(q-1) regular on N apartments, x=1_S for a nonzero proper codeword, alpha=|S|/N, and y=x-alpha*1.',
         'rayleigh_formula':'rho(S)=D(1/2-alpha)/(1-alpha).',
         'weight_inversion':'alpha=(D/2-rho)/(D-rho), hence |S|=N(D/2-rho)/(D-rho).',
         'proof':'Pass5119 gives x^T A x=(D/2)|S|. Subtracting the constant eigendirection from x and using A1=D1 yields the formula by direct quadratic expansion.',
         'anchors_chamber_stars':anchors,
         'consequence':'Although the uncentered indicator Rayleigh quotient is identically D/2, centering restores exact weight information. The distance problem becomes a bound on the largest attainable centered Rayleigh quotient among nonzero codewords.',
         'boundary':'This identity encodes the weight exactly but supplies no new upper bound on rho by itself; the attainable-codeword spectral constraint remains the hard part.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
