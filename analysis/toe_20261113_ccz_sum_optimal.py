#!/usr/bin/env python3
"""Exact minimal SUM cost of the CCZ normal form's F3-linear Clifford L.

Exhaustive Dijkstra on all GL(3,3) matrices, using free output-row swaps
and nonzero local scalings, and qutrit SUM (row add +/-) with unit cost.
Does not prove a lower bound allowing arbitrary local non-monomial Cliffords.
"""
from __future__ import annotations
from collections import Counter
from heapq import heappush,heappop
from pathlib import Path
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_ccz_clifford_normalform as C
OUT=ROOT/"data/toe_20261113_ccz_sum_optimal.json"
L=tuple(int(x) for x in C.L.reshape(-1))
ID=tuple(int(x) for x in np.eye(3,dtype=int).reshape(-1))

def apply(x,g):
    arr=list(x)
    if g[0]=="sum":
        _,i,j,t=g
        for k in range(3):arr[3*j+k]=(arr[3*j+k]+t*arr[3*i+k])%3
    elif g[0]=="scale":
        _,i=g
        for k in range(3):arr[3*i+k]=(2*arr[3*i+k])%3
    else:
        _,i,j=g
        for k in range(3):arr[3*i+k],arr[3*j+k]=arr[3*j+k],arr[3*i+k]
    return tuple(arr)

OPS=[(1,("sum",i,j,t)) for i in range(3) for j in range(3)
     if i!=j for t in (1,2)]
OPS.extend((0,("scale",i)) for i in range(3))
OPS.extend((0,("swap",i,j)) for i in range(3) for j in range(i+1,3))

def verify():
    assert len(OPS)==18
    dist={ID:0}
    heap=[(0,ID)]
    while heap:
        du,u=heappop(heap)
        if du!=dist[u]:continue
        for cost,g in OPS:
            v=apply(u,g)
            nd=du+cost
            if nd<dist.get(v,999):
                dist[v]=nd
                heappush(heap,(nd,v))
    census=Counter(dist.values())
    assert len(dist)==11232
    assert census==Counter({0:48,1:576,2:3600,3:6336,4:672})
    assert dist[L]==4
    witness=(("sum",2,0,1),("sum",0,2,1),
             ("sum",1,2,1),("sum",2,1,1))
    x=ID
    for g in witness:x=apply(x,g)
    assert x==L
    # Operational orientation on basis labels, not just 3x3 matrix product:
    for k in C.V:
        vec=tuple(k)
        for _,i,j,t in witness:
            q=list(vec);q[j]=(q[j]+t*q[i])%3;vec=tuple(q)
        assert vec==C.transform(k)
    res={
      "status":"PASS_EXHAUSTIVE_MINIMUM_FOUR_SUM_LINEAR_COMPILER",
      "group":"GL(3,3)","all_invertible_matrices_checked":11232,
      "zero_cost_generators":"single-coordinate nonzero scalar multiplication and coordinate SWAP",
      "unit_cost_generators":"SUM(control, target, amount=1 or 2 mod3)",
      "cost_census":{str(i):int(census[i]) for i in range(5)},
      "target_linear_map":np.array(L).reshape(3,3).tolist(),
      "target_minimum_SUM_cost":4,
      "four_SUM_witness":[list(g) for g in witness],
      "full_chiral_clock_compiler":{
         "local_qutrit_fourier":6,
         "SUM":8,
         "CCZ":1,
         "formula":"U=F P_L^dag CCZ P_L F^dag with P_L and inverse each 4 SUM"},
      "optimality_boundary":"4-SUM minimum within linear reversible qutrit circuits with free SWAP/scalings; no claim this is the minimum over all qutrit Clifford circuits with arbitrary intermediate Fourier, ancillary or measurement gates.",
      "physics_boundary":"No demonstrated optical device, fault-tolerance or physical TOE."}
    OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return res
if __name__=="__main__":
    r=verify()
    print(json.dumps({k:r[k] for k in ("status","all_invertible_matrices_checked","cost_census","target_minimum_SUM_cost","four_SUM_witness","full_chiral_clock_compiler")},indent=2))
