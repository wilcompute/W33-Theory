#!/usr/bin/env python3
"""Pass 4597 bonkers -- the 45 minimum sentinel words reconstruct both graphs.

The complete A8 shell of C=ker(N^T) is the 45x40 transport/support matrix T.
From the shell alone: two minimum words meet in 2 coordinates iff adjacent in
the center-quad transport SRG(45,32,22,24); two coordinates occur together in
3 minimum words iff adjacent in the point-side W33 SRG(40,12,2,4).
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
import w33_pass4592_4593_e6_sentinel_transport_closure as p
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS4597_SENTINEL_MINIMUM_SHELL_SELF_RECONSTRUCTION.json'
def main():
    _,_,lines,_,Apoint,Astar,_,aps,_=build_geometry();Apoint=np.asarray(Apoint,dtype=np.uint8);Astar=np.asarray(Astar,dtype=np.uint8)
    _,T=p.build_new(Astar,lines,aps);assert T.shape==(45,40)
    R=T.astype(int)@T.astype(int).T;C=T.astype(int).T@T.astype(int)
    A45=np.zeros((45,45),dtype=np.uint8);A40=np.zeros((40,40),dtype=np.uint8)
    ri=Counter();ci=Counter()
    for i,j in itertools.combinations(range(45),2):
        z=int(R[i,j]);ri[z]+=1
        if z==2:A45[i,j]=A45[j,i]=1
        else:assert z==0
    for i,j in itertools.combinations(range(40),2):
        z=int(C[i,j]);ci[z]+=1
        if z==3:A40[i,j]=A40[j,i]=1
        else:assert z==1
    assert ri==Counter({2:720,0:270}) and ci==Counter({1:540,3:240})
    assert np.array_equal(A40,Apoint) and not np.array_equal(A40,Astar)
    out={'pass':4597,'minimum_shell':{'code':'sentinel ker(N^T)=[40,15,8]','minimum_words':45,'weight':8},
      'row_reconstruction':{'rule':'two A8 words adjacent iff support intersection=2','intersection_profile':{'0':270,'2':720},'graph':'center-quad/E6 transport SRG(45,32,22,24)'},
      'coordinate_reconstruction':{'rule':'two coordinates adjacent iff they co-occur in 3 A8 words','cooccurrence_profile':{'1':540,'3':240},'graph':'point-side W33 SRG(40,12,2,4)','different_from_line_side_Astar':True},
      'theorem':'The complete minimum shell of the W33 sentinel code intrinsically reconstructs both the 45-point center-quad transport graph and the non-self-dual 40-point W33 graph.',
      'boundary':'Self-reconstruction is a finite code/incidence theorem; coordinate labels remain the point-side W33 carrier, not the inequivalent line-side carrier.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
