#!/usr/bin/env python3
"""Pass5081: dual minimum shell = theta; q=2 MacWilliams checksum."""
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5081_DUAL_MINIMUM_THETA_SHELL.json'
A={0:1,16:45,24:90,28:360,30:360,34:1440,36:1740,38:1440,40:5634,42:8520,44:10440,46:11520,48:11580,50:8280,52:2520,54:1080,56:450,60:36}

def K(j,w,n=90):
    return sum(((-1)**i)*math.comb(w,i)*math.comb(n-w,j-i)
               for i in range(max(0,j-(n-w)),min(j,w)+1))

def main():
    B={j:sum(c*K(j,w) for w,c in A.items())//(2**16) for j in range(9)}
    assert (B[0],B[1],B[2],B[3])==(1,0,0,120)
    out={'pass':5081,'status':'THEOREM_WITH_Q2_MACWILLIAMS_CHECK',
         'theorem':'For any finite generalized quadrangle apartment code, the weight-3 dual words are exactly local theta triples.',
         'proof':['If dA+dB+dC=0 then C=A symmetric-difference B; since A,B,C are 8-cycles, A and B share exactly four edges.',
                  'In a girth-8 GQ incidence graph this four-edge overlap is one contiguous length-four root; otherwise the symmetric difference splits or creates a shorter circuit.',
                  'The complementary roots form C, so A,B,C are a theta triple. The converse is immediate.'],
         'dual_minimum_distance':3,'dual_minimum_shell':'theta hypergraph',
         'theta_count_formula':'q^3(q+1)(q^2+1) C(q+1,3)',
         'q2_macwilliams_dual_coefficients_0_to_8':B,'q2_theta_checks':120,
         'boundary':'Finite code/building theorem only.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__':main()
