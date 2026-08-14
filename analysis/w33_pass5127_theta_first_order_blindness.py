#!/usr/bin/env python3
"""Pass5127: all-q first-order theta spectral blindness theorem.

Pass5119 proves that every binary apartment-code support S induces degree
r=4(q-1) inside the intrinsic theta graph of degree D=8(q-1), and every
selected vertex has the same r external neighbors.  This pass records the
exact spectral/random-walk consequences: one-step stay/escape probabilities
are both 1/2, the indicator Laplacian Rayleigh quotient is D/2, and these
quantities are independent of |S|.  Therefore ordinary first-order
Cheeger/Rayleigh expansion cannot by itself distinguish minimum codewords.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/PART_W33_PASS5119_THETA_HALF_REGULAR_SUPPORT.json'
OUT=ROOT/'data/PART_W33_PASS5127_THETA_FIRST_ORDER_BLINDNESS.json'

def row(q,N):
    D=8*(q-1); r=D//2
    return {'q':q,'apartments':N,'ambient_degree':D,'support_induced_degree':r,
            'support_external_degree':r,'internal_edges_per_support_vertex':'2(q-1)',
            'boundary_edges_per_support_vertex':r,'one_step_stay_probability':'1/2',
            'one_step_escape_probability':'1/2','indicator_laplacian_rayleigh':r}

def main():
    old=json.loads(SRC.read_text()); assert old['pass']==5119
    anchors={k:row(int(k),v['apartment_count']) for k,v in old['anchors'].items()}
    for k,v in anchors.items():
        q=int(k); assert v['ambient_degree']==old['anchors'][k]['theta_graph_degree']
        assert v['support_induced_degree']==old['anchors'][k]['selected_induced_degree']
        assert v['support_external_degree']==old['anchors'][k]['selected_external_degree']
    out={'pass':5127,'status':'THEOREM_ALL_Q_THETA_FIRST_ORDER_SPECTRAL_BLINDNESS',
         'statement':'For every nonzero apartment-code support S, the intrinsic theta graph has D=8(q-1), Gamma[S] is D/2-regular, and every selected vertex has D/2 neighbors outside S.',
         'consequences':{
           'induced_edges':'|E(S)|=2(q-1)|S|',
           'edge_boundary':'|delta(S)|=4(q-1)|S|',
           'one_step_random_walk':'from the uniform distribution on S, P(stay)=P(exit)=1/2',
           'indicator_rayleigh':'1_S^T L 1_S / ||1_S||^2 = 4(q-1) = D/2'},
         'interpretation':'All codeword supports have the same first-order theta escape/Rayleigh value regardless of Hamming weight. A distance proof must use additional triangle/chart parity or other higher-order curvature information; ordinary first-order expansion alone is blind.',
         'anchors':anchors,
         'boundary':'This is an exact finite graph/code theorem. It does not say every D/2-regular induced subgraph is a codeword support, nor does it prove the minimum distance.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
