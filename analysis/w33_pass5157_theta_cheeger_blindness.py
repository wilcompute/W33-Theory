#!/usr/bin/env python3
"""Pass5157: ordinary theta conductance is identically 1/2 on codewords."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5157_THETA_CHEEGER_BLINDNESS.json'

def row(q):
    D=8*(q-1);k=4*(q-1)
    return {'q':q,'theta_degree':D,'inside_degree':k,'outside_degree':k,
            'conductance':'1/2','one_step_stay_probability':'1/2','one_step_exit_probability':'1/2',
            'normalized_Laplacian_Rayleigh':'1/2'}

def main():
    out={'pass':5157,'status':'THEOREM_FIRST_ORDER_THETA_EXPANSION_BLINDNESS',
         'statement':'For every nonzero apartment-code support S, ordinary edge conductance in the intrinsic theta graph is exactly 1/2, independent of its Hamming weight.',
         'proof':'Pass5119 gives ambient degree D=8(q-1) and exactly D/2 edges from each selected vertex to S and D/2 to its complement.',
         'random_walk':'A one-step simple random walk started uniformly on a selected apartment remains in S with probability exactly 1/2 and exits with probability exactly 1/2.',
         'spectral':'For x=1_S, x^T A_theta x/x^T x=D/2 and x^T L_norm x/x^T x=1/2 for every codeword support.',
         'no_go':'A distance proof based only on first-order theta conductance or the uncentered indicator Rayleigh quotient cannot distinguish a chamber-star word of weight q^4 from a heavier codeword.',
         'repair':'Pass5151 supplies the second-moment curvature discriminator; Pass5152 shows the centered Rayleigh quotient retains exact weight information.',
         'anchors':[row(q) for q in (2,3,4,5)],
         'boundary':'No-go concerns first-order conductance/uncentered indicator spectrum only; higher-order and centered spectral inequalities remain available.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
