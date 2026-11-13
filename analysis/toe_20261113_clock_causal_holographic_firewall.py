#!/usr/bin/env python3
"""Unroll periodic internal chiral shifts into a finite causal microcircuit;
measure exactly why U|000> is not a holographic perfect-tensor seed.

This DOES NOT build a causal-set quantum gravity or a physical light cone.
"""
from __future__ import annotations
from pathlib import Path
from fractions import Fraction
from collections import Counter
import json,sys,math
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_chiral_null_order3_gate as G
OUT=ROOT/"data/toe_20261113_causal_holographic_firewalls.json"
V=G.V; VID=G.VID

def mat_for_step(v):
    A=np.zeros((27,27),dtype=np.int64)
    for x in V:
        y=tuple((x[j]+v[j])%3 for j in range(3))
        A[VID[x],VID[y]]=1
    return A

def unroll():
    # Spatial four directions each admit closed directed q-cycles, hence
    # cannot by themselves constitute a causal partial order.
    assert all(tuple((3*x)%3 for x in v)==(0,0,0) for v in G.FUTURE)
    distributions=[]
    reachable={(0,0,0)}
    rot=np.eye(27)
    t=2*math.pi/(9*math.sqrt(3))
    for step,v in enumerate(G.FUTURE,1):
        T=mat_for_step(v)
        Ui=expm(t*(T-T.T))
        assert np.max(abs(Ui.T@Ui-np.eye(27)))<1e-12
        pattern=(np.abs(Ui)>1e-13)
        assert np.all(pattern.sum(axis=1)==3)
        for x in V:
            neighbors={x,tuple((x[j]+v[j])%3 for j in range(3)),
                          tuple((x[j]-v[j])%3 for j in range(3))}
            assert {V[k] for k in np.flatnonzero(pattern[VID[x]])}==neighbors
        nxt=set()
        for x in reachable:
            for k in (-1,0,1):
                nxt.add(tuple((x[j]+k*v[j])%3 for j in range(3)))
        reachable=nxt
        distributions.append({"microstep":step,"supported_spatial_sites":len(reachable),
                              "per_vertex_spacetime_out_degree":3})
        rot=rot@Ui
    _,_,D=G.build()
    U=(18*np.eye(27)+3*D+D@D)/18
    assert np.max(abs(rot-U))<1e-12
    assert [r["supported_spatial_sites"] for r in distributions]==[3,9,27,27]
    assert np.count_nonzero((np.abs(U)>1e-13)[0,:])==27
    # All temporal edges advance from layer t to t+1, so no cycles.
    # There are 5 slices of 27 vertices (t=0..4), 4*27*3 arrows.
    return {
      "internal_chiral_graph_has_directed_3_cycles":True,
      "strict_temporal_unrolling_acyclic":True,
      "temporal_slices":5,"events":135,"interlayer_links":324,
      "four_layer_support_counts":distributions,
      "all_27_amplitudes_nonzero_after_four_layers":True,
      "max_numerical_factorization_error":float(np.max(abs(rot-U))),
      "interpretation":"internal cyclic memory + acyclic ordered circuit depth is algebraically consistent; only a finite schedule, no derived Lorentzian time or causal-set field equation"}

def holography():
    _,_,D=G.build()
    M=(18*np.eye(27,dtype=np.int64)+3*D+D@D)//2
    psi=M[:,0].reshape(3,3,3)
    numerators=[]
    purities=[]
    ranks=[]
    for j in range(3):
        tensor=np.moveaxis(psi,j,0).reshape(3,9)
        rho=tensor@tensor.T
        assert np.trace(rho)==81
        numerators.append(rho)
        p=Fraction(int(np.trace(rho@rho)),81*81)
        purities.append(str(p))
        ranks.append(int(np.linalg.matrix_rank(rho)))
    left=9*np.array([[4,-1,1],[-1,2,0],[1,0,3]],dtype=np.int64)
    mid=9*np.array([[5,-1,-1],[-1,2,2],[-1,2,2]],dtype=np.int64)
    assert np.array_equal(numerators[0],left)
    assert np.array_equal(numerators[1],mid)
    assert np.array_equal(numerators[2],left)
    assert purities==["11/27","5/9","11/27"]
    assert ranks==[3,2,3]
    assert all(not np.array_equal(3*R,81*np.eye(3,dtype=np.int64))
               for R in numerators)
    # In any pure 3-party state S(AB)=S(C), etc; I3 identically zero.
    return {"input":"pure U|000> on three qutrits",
            "reduced_density_matrices_denominator_9":[
                (R//9).tolist() for R in numerators],
            "reduced_purities":purities,"single_qutrit_schmidt_ranks":ranks,
            "is_one_uniform_AME_3_3":False,
            "three_party_pure_I3_exactly_zero":True,
            "scope":"Cannot treat this specific output as an absolutely maximally entangled three-leg seed. This is NOT a test of six-leg Choi perfection or a global holographic code. Transversal Clifford restrictions only follow when separate code assumptions hold."}

def verify():
    r={"schema":"toe.chiral_causal_holography.v1",
       "status":"PASS_EXPLICIT_MICROCAUSAL_UNROLLING_AND_ENTROPIC_FIREWALL",
       "unrolling":unroll(),"holographic_output":holography(),
       "external_prior":[
         "Surya 2019 Living Reviews Relativity causal sets",
         "D'Ariano Perinotti 2014 Phys Rev A 90 062106 QCA continuum",
         "Pastawski Yoshida Harlow Preskill 2015 JHEP HaPPY codes",
         "Cree Dolev Calvera Williamson 2021 PRX Quantum 2 030337 transversal restrictions"] }
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return r
if __name__=="__main__":
    r=verify()
    print(json.dumps({"status":r["status"],"microsteps":r["unrolling"]["four_layer_support_counts"],
                     "purities":r["holographic_output"]["reduced_purities"],
                     "ranks":r["holographic_output"]["single_qutrit_schmidt_ranks"]},indent=2))
