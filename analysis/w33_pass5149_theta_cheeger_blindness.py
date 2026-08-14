#!/usr/bin/env python3
"""Pass5149 (outside box): ordinary theta conductance is identically 1/2 on codewords."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5149_THETA_CHEEGER_BLINDNESS.json'

def row(q):
    D=8*(q-1);k=4*(q-1)
    assert k*2==D
    return {'q':q,'theta_degree':D,'inside_degree_on_codeword':k,'outside_degree_on_codeword':k,
            'conductance':'1/2','one_step_stay_probability':'1/2','one_step_exit_probability':'1/2',
            'adjacency_Rayleigh':'%d'%k,'normalized_Laplacian_Rayleigh':'1/2'}

def main():
    out={'pass':5149,'status':'THEOREM_FIRST_ORDER_THETA_EXPANSION_BLINDNESS',
         'statement':'For every nonzero apartment-code support S, ordinary edge conductance in the intrinsic theta graph is exactly 1/2, independent of |S|.',
         'proof':'Pass5142 gives ambient degree D=8(q-1) and exactly D/2 edges from each selected vertex to S and D/2 to its complement.',
         'random_walk':'A one-step simple random walk started uniformly on a selected apartment remains in S with probability exactly 1/2 and exits with probability exactly 1/2.',
         'spectral':'For x=1_S, x^T A_theta x / x^T x = D/2 and x^T L_norm x / x^T x = 1/2 for every codeword support.',
         'no_go':'Therefore a distance proof based only on first-order theta conductance or the indicator Rayleigh quotient cannot distinguish a chamber-star word of weight q^4 from a heavier codeword.',
         'first_discriminator':'Pass5143 supplies the next local statistic: the second adjacency moment has a quantized nonnegative curvature defect and is sharp on chamber stars.',
         'anchors':[row(q) for q in (2,3,4,5)],
         'boundary':'This no-go concerns first-order conductance of the theta point graph only; stronger spectral, higher-moment or representation-theoretic inequalities may still prove the distance theorem.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
