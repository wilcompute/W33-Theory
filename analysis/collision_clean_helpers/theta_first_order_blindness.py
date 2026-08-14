#!/usr/bin/env python3
"""Pass5134: all-q first-order theta spectral blindness theorem."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/PART_W33_PASS5119_THETA_HALF_REGULAR_SUPPORT.json'
OUT=ROOT/'data/PART_W33_PASS5134_THETA_FIRST_ORDER_BLINDNESS.json'

def row(q,N):
    D=8*(q-1);r=D//2
    return {'q':q,'apartments':N,'ambient_degree':D,'support_induced_degree':r,
            'support_external_degree':r,'one_step_stay_probability':'1/2',
            'one_step_escape_probability':'1/2','indicator_laplacian_rayleigh':r}

def main():
    old=json.loads(SRC.read_text());assert old['pass']==5119
    anchors={k:row(int(k),v['apartment_count']) for k,v in old['anchors'].items()}
    for k,v in anchors.items():
        assert v['ambient_degree']==old['anchors'][k]['theta_graph_degree']
        assert v['support_induced_degree']==old['anchors'][k]['selected_induced_degree']
        assert v['support_external_degree']==old['anchors'][k]['selected_external_degree']
    out={'pass':5134,'status':'THEOREM_ALL_Q_THETA_FIRST_ORDER_SPECTRAL_BLINDNESS',
         'statement':'For every nonzero apartment-code support S, the intrinsic theta graph has D=8(q-1), Gamma[S] is D/2-regular, and every selected vertex has D/2 neighbors outside S.',
         'consequences':{'induced_edges':'|E(S)|=2(q-1)|S|','edge_boundary':'|delta(S)|=4(q-1)|S|',
           'one_step_random_walk':'from the uniform distribution on S, P(stay)=P(exit)=1/2',
           'indicator_rayleigh':'1_S^T L 1_S / ||1_S||^2 = 4(q-1)=D/2'},
         'interpretation':'All codeword supports have identical first-order theta escape/Rayleigh data regardless of Hamming weight. A distance proof must retain triangle/chart parity or other higher-order curvature information.',
         'anchors':anchors,
         'boundary':'Exact necessary code-support theorem; no converse and no minimum-distance proof.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
