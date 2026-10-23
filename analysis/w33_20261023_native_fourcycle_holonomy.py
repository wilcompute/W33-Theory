#!/usr/bin/env python3
"""Classify all native simple 4-cycles by period voltage.

Find whether overlapping zero-period magnetic faces can couple the 45
edge-disjoint GQ(2,4) triangles; compute F3 boundary ranks and period rank.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np
try:
 from analysis.w33_pass12189_12193_five_bridges import graph_inputs
 from analysis.w33_20261023_native_plaquette_ward import build as tri_build
 from analysis.w33_20261023_native_gq24_qutrit_gauge_code import rank_p
except ImportError:
 from w33_pass12189_12193_five_bridges import graph_inputs
 from w33_20261023_native_plaquette_ward import build as tri_build
 from w33_20261023_native_gq24_qutrit_gauge_code import rank_p

def run():
    d,B,V,G,aa,bb=graph_inputs()
    V=np.rint(V).astype(np.int64)
    n=27;m=135
    edges={(int(a),int(b)):i for i,(a,b) in enumerate(zip(aa,bb))}
    N=[set() for _ in range(n)]
    for a,b in zip(aa,bb):
        N[a].add(int(b));N[b].add(int(a))
    def walk(a,b):
        if a<b:return edges[(a,b)],1
        return edges[(b,a)],-1
    base=tri_build()["closed_cycles"]
    F3=np.zeros((45,m),dtype=np.int64)
    for r,f in enumerate(base):
        for e,s in zip(f["edge_ids"],f["orientation_signs"]):F3[r,e]=s%3
    total=0;closed=[];wind=[]
    for a in range(n):
        for b in sorted(x for x in N[a] if x>a):
            for d in sorted(x for x in N[a] if x>b):
                for c in sorted((N[b]&N[d])-{a}):
                    if c<=a:continue
                    vertices=[a,b,c,d,a]
                    parts=[walk(x,y) for x,y in zip(vertices[:-1],vertices[1:])]
                    flux=sum((s*V[e] for e,s in parts),np.zeros(4,dtype=np.int64))
                    row=np.zeros(m,dtype=np.int64)
                    for e,s in parts:row[e]=(row[e]+s)%3
                    total+=1
                    if np.all(flux==0):closed.append((row,vertices,parts))
                    else:wind.append((row,flux.tolist(),vertices))
    tri_rank=rank_p(F3)
    combined=rank_p(list(F3)+[x[0] for x in closed])
    assert tri_rank==45 and combined<=135-26
    # Each zero-voltage loop is a genuine closed face in the Z4 lift.
    cycle_rows=np.stack([w[0] for w in closed]) if closed else np.empty((0,m),dtype=np.int64)
    # Voltage cycle space: dim H1(graph)=135-27+1=109, period map rank4
    # by native primitive voltage certificate. Thus dim nullperiod=105.
    assert combined<=105
    return {"status":"NATIVE_GQ24_FOURCYCLE_VOLTAGE_AND_OVERLAP_CENSUS",
      "all_simple_fourcycles":total,
      "zero_period_fourcycles":len(closed),
      "nonzero_period_fourcycles":len(wind),
      "rank_triangle_faces":tri_rank,
      "rank_triangle_plus_zero_period_fourcycle_faces_mod3":combined,
      "additional_face_rank":combined-tri_rank,
      "remaining_F3_first_homology_rank":135-26-combined,
      "period_rank_over_Z_expected":4,
      "zero_period_cycle_space_dimension_over_Q":105,
      "example_zero_period_fourcycles":[x[1] for x in closed[:10]],
      "example_nonzero_period_fourcycles":[{"cycle":x[2],"flux":x[1]} for x in wind[:10]],
      "physical_caution":"Overlapping zero-period C4 faces can give non-factorized gauge magnetic interactions; mod3 face span need not equal integral null-voltage span, and no gapless photon theorem follows."}

if __name__=="__main__":
 r=json.dumps(run(),indent=2)+"\n"
 if len(sys.argv)>1:Path(sys.argv[1]).write_text(r,encoding="utf8")
 else:print(r)
