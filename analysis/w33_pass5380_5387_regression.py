#!/usr/bin/env python3
"""Regression lock for Pass5380--5387."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'data/PART_W33_PASS5380_5387_RESULTS.json'

def main():
    x=json.loads(R.read_text())
    assert x['status']=='EXECUTED_WITH_HOFFMAN_SOLVER_PENDING'
    assert x['5380']['codes']==['C_A=[73125,625,625]_2','K0=[73125,560,1000]_2','C_F=[325,65,25]_2']
    assert x['5381']['eventual_radius']==9 and x['5381']['monotone_true_only_radius']==7
    assert x['5382']['minimal_polynomial']=='x^3(x+1)^4'
    assert x['5382']['projectors']==['P1=A_L^4','P0=I+A_L^4']
    assert x['5383']['status']=='EXACT_HOFFMAN_XORSAT_REPLAY_COMMITTED_SOLVER_PENDING'
    assert x['5384']['exact_sequence']=='0 -> D_q=K0 -> C_A -> C_F -> 0'
    assert x['5385']['reconstructed_graph']=='SRG(156,30,4,6)=W(3,5)'
    assert x['5386']['tower']==['q^4','q^3','q^2','q','1']
    assert x['5387']['difference_set']=='(16,6,2)'
    manifest=(ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex').read_text()
    assert '\\input{analysis/PASS5380_5387_distance_radius9_projector_gallery_insert}' in manifest
    print(json.dumps({'status':'PASS','checks':10,'hoffman':'PENDING'},indent=2))
if __name__=='__main__':main()
