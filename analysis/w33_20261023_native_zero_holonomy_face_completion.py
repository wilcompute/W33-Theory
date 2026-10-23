#!/usr/bin/env python3
"""Minimal local magnetic face lengths needed to span native Z4-voltage kernel.

Enumerate canonically oriented simple cycles of lengths 3,4,5 (and 6 only
if necessary). Keep only cycles with zero *integer* four-period flux;
measure accumulated face rank over F3. Rank cannot exceed 109-4=105
since the primitive four period directions survive as homology classes.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np
try:
 from analysis.w33_pass12189_12193_five_bridges import graph_inputs
except ImportError:
 from w33_pass12189_12193_five_bridges import graph_inputs

def run():
    d,B,V,G,aa,bb=graph_inputs()
    V=np.rint(V).astype(np.int16)
    n=27;m=135
    edge={(int(a),int(b)):i for i,(a,b) in enumerate(zip(aa,bb))}
    nbr=[set() for _ in range(n)]
    for a,b in zip(aa,bb):nbr[a].add(int(b));nbr[b].add(int(a))
    def step(a,b):
        if a<b:return edge[a,b],1
        return edge[b,a],-1
    piv={}
    def insert(row):
        z=np.array(row,dtype=np.int16)%3
        while True:
            nz=np.flatnonzero(z)
            if not len(nz):return False
            j=int(nz[0])
            if j in piv:z=(z-int(z[j])*piv[j])%3
            else:
                piv[j]=z*int(z[j])%3
                return True
    summary=[];new_basis=[]
    for length in (3,4,5,6):
        total=0;closed=0;new=0
        def visit(start,path,used):
            nonlocal total,closed,new
            if len(path)==length:
                if start not in nbr[path[-1]]:return
                # first vertex is global minimum and orientation non-duplicated.
                if path[1]>=path[-1]:return
                cyc=path+[start]
                edges=[step(a,b) for a,b in zip(cyc[:-1],cyc[1:])]
                flux=sum((sgn*V[e] for e,sgn in edges),np.zeros(4,dtype=np.int64))
                total+=1
                if np.any(flux):return
                closed+=1
                vec=np.zeros(m,dtype=np.int16)
                for e,sgn in edges:vec[e]=(vec[e]+sgn)%3
                if insert(vec):
                    new+=1
                    new_basis.append({"length":length,"vertices":cyc,
                                      "flux":[0,0,0,0],
                                      "boundary":[[int(e),int(s)] for e,s in edges]})
                return
            for v in sorted(nbr[path[-1]]):
                if v<=start or v in used:continue
                visit(start,path+[v],used|{v})
        for start in range(n):
            visit(start,[start],{start})
        summary.append({"length":length,"all_cycles":total,"zero_voltage_cycles":closed,
                        "independent_new_zero_faces":new,"cumulative_F3_face_rank":len(piv),
                        "remaining_h1_F3":m-(n-1)-len(piv)})
        if len(piv)==105:break
    assert summary[0]["all_cycles"]==45 and summary[0]["cumulative_F3_face_rank"]==45
    assert summary[1]["all_cycles"]==1080 and summary[1]["zero_voltage_cycles"]==189
    assert summary[1]["cumulative_F3_face_rank"]==101
    assert len(piv)<=105
    return {"status":"NATIVE_MINIMAL_ZERO_HOLONOMY_FACE_COMPLETION",
      "primitivity_of_native_voltage":"Z^4 period rank 4 from Pass11991/12192",
      "underlying_graph_cycle_rank":109,
      "maximum_F3_zero_period_face_rank":105,
      "length_census":summary,
      "rank_final":len(piv),
      "independent_face_basis":new_basis,
      "resulting_h1":m-(n-1)-len(piv),
      "caution":"F3-homology rank and integer period-map primitivity are distinct questions; a four-dimensional leftover must be independently validated as actual lattice holonomy, not assumed to be physical spacetime photons."}

if __name__=="__main__":
 data=json.dumps(run(),indent=2)+"\n"
 if len(sys.argv)>1:Path(sys.argv[1]).write_text(data,encoding="utf8")
 else:print(data)
