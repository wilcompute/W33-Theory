#!/usr/bin/env python3
"""Pass5688 bonkers: discrepancy/Ramanujan search on concrete W33 Levi signings.

Three explicit signings are compared on the same 160-edge Levi graph:
  * one negative chord (connected but bottlenecked),
  * a locally balanced 2-factor signing (two negative incidences at every vertex),
  * an edge-balanced spectral-search witness (80 negatives globally).
A fixed random baseline of 256 exactly-half-negative signings is included.

The purpose is not to claim optimality; it is to show quantitatively that the
single-chord construction is a pathological corner of H1 rather than typical,
and that locally balanced explicit signings can already satisfy the d=4 Ramanujan
new-eigenvalue bound.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
import w33_pass5683_balanced_ramanujan_levi_lifts as base
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5688_BALANCED_SIGNING_SEARCH_VS_RANDOM.json'
LOCAL=base.NEG
GLOBAL=[0,1,2,7,8,11,13,14,15,16,19,20,23,25,27,31,33,35,36,37,38,40,41,42,45,46,47,48,53,54,55,56,57,58,60,61,63,66,68,69,70,71,72,78,82,86,87,90,93,95,97,100,103,105,106,107,108,112,115,117,118,119,120,122,123,124,132,135,136,137,138,140,141,142,144,146,148,152,153,156]

def rho(E,neg):
    s=np.ones(160);s[list(neg)]=-1
    return float(np.max(abs(np.linalg.eigvalsh(base.adj(E,s)))))
def degs(E,neg):
    d=np.zeros(80,dtype=int)
    for i in neg:
        u,v=E[i];d[u]+=1;d[v]+=1
    return d

def main():
    E=base.levi();ram=2*math.sqrt(3)
    rs=rho(E,[0]);rl=rho(E,LOCAL);rg=rho(E,GLOBAL)
    assert rs>ram and rl<ram and rg<rl
    assert set(degs(E,LOCAL))=={2}
    assert len(LOCAL)==len(GLOBAL)==80
    rng=np.random.default_rng(5688);random_r=[]
    for _ in range(256):
        neg=rng.choice(160,80,replace=False)
        random_r.append(rho(E,neg))
    below=sum(x<ram for x in random_r)
    out={
      'pass':5688,'status':'SINGLE_CHORD_IS_SPECTRAL_OUTLIER_AND_EXPLICIT_BALANCED_SIGNINGS_ARE_RAMANUJAN',
      'ramanujan_threshold':ram,
      'single_chord':{'negative_edges':1,'signed_radius':rs,'new_gap':4-rs},
      'locally_balanced_2factor':{'negative_edges':80,'negative_degree_every_vertex':2,'signed_radius':rl,'new_gap':4-rl,'negative_edge_indices':LOCAL},
      'edge_balanced_spectral_witness':{'negative_edges':80,'signed_radius':rg,'new_gap':4-rg,'negative_degree_histogram':{str(k):int(np.sum(degs(E,GLOBAL)==k)) for k in sorted(set(degs(E,GLOBAL)))} ,'negative_edge_indices':GLOBAL},
      'fixed_random_half_negative_baseline':{'samples':256,'seed':5688,'min_radius':min(random_r),'median_radius':float(np.median(random_r)),'max_radius':max(random_r),'below_ramanujan_bound':below},
      'conclusion':'The vanishing-gap single-chord tower is not representative of nontrivial H1. Balanced signings are easy to find and explicit locally balanced and spectrally optimized witnesses satisfy the first-level Ramanujan new-spectrum bound.',
      'boundary':'No witness here is proved globally optimal and the hardcoded witnesses select coordinates. Infinite good-tower existence comes from the MSS theorem in Pass5683, not from iterating these particular signings.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
