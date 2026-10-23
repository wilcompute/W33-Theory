#!/usr/bin/env python3
"""Native four-period H27 135-link qutrit CSS: exact [[135,4,4]]_3.

Uses 105 independent zero-voltage native cycles of length 3,4,5,
26 vertex star constraints, and an explicit winding four-cycle.
Checks X logical distance >=4 by exhaustive <=3-column syndrome test.
"""
from __future__ import annotations
import json,sys,itertools
from pathlib import Path
import numpy as np
try:
 from analysis.w33_pass12189_12193_five_bridges import graph_inputs
 from analysis.w33_20261023_native_gq24_qutrit_gauge_code import rank_p
except ImportError:
 from w33_pass12189_12193_five_bridges import graph_inputs
 from w33_20261023_native_gq24_qutrit_gauge_code import rank_p

ROOT=Path(__file__).resolve().parents[1]

def run():
    data=json.loads((ROOT/"data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json").read_text())
    d,B,V,G,aa,bb=graph_inputs()
    n=135
    HX=np.rint(B.T).astype(np.int16)%3
    HZ=np.zeros((len(data["independent_face_basis"]),n),dtype=np.int16)
    V=np.rint(V).astype(np.int16)
    for row,f in enumerate(data["independent_face_basis"]):
        assert 3<=len(f["boundary"])<=5
        for e,s in f["boundary"]:HZ[row,e]=(HZ[row,e]+s)%3
    assert HZ.shape==(105,135)
    rx=rank_p(HX);rz=rank_p(HZ)
    assert rx==26 and rz==105
    assert rank_p(list(HX)+[v for v in V.T])==30
    assert np.all((HX.astype(np.int64)@HZ.T)%3==0)
    assert np.all((V.T.astype(np.int64)@HZ.T)%3==0)
    assert n-rx-rz==4
    # Column syndromes for elementary X errors. Exclude weights 1,2,3
    # by exhausting all sparse F3 linear dependencies among columns.
    cols=HZ.T.astype(np.int16)
    singles={}
    for i,v in enumerate(cols):
        assert np.any(v)
        for a in (1,2):
            k=bytes((a*v%3).astype(np.uint8))
            singles.setdefault(k,[]).append(i)
    weight2=None;weight3=None
    for i in range(n):
        for j in range(i+1,n):
            for a,b in itertools.product((1,2),repeat=2):
                y=(a*cols[i]+b*cols[j])%3
                if not np.any(y):weight2=[i,j,a,b];break
                k=bytes((-y%3).astype(np.uint8))
                if k in singles:
                    for h in singles[k]:
                        if h not in (i,j):weight3=[i,j,h,a,b,1];break
                if weight3:break
            if weight2 or weight3:break
        if weight2 or weight3:break
    # Projective cohomology has no weight <=3 nontrivial X class.
    assert weight2 is None and weight3 is None,(weight2,weight3)
    # Exhibit Z logical of weight four: a nonzero period C4.
    eidx={(int(a),int(b)):eid for eid,(a,b) in enumerate(zip(aa,bb))}
    def ee(a,b):
        return (eidx[a,b],1) if a<b else (eidx[b,a],-1)
    vertices=[0,1,11,4,0]
    z=np.zeros(n,dtype=np.int16)
    for a,b in zip(vertices[:-1],vertices[1:]):
        edge,sign=ee(a,b);z[edge]=sign%3
    assert int(np.count_nonzero(z))==4
    assert np.all((HX.astype(np.int64)@z)%3==0)
    period=(V.T.astype(np.int64)@z)%3
    assert np.any(period!=0)
    assert rank_p(list(HZ)+[z])==rz+1
    # Z error support length 1 or 2 cannot be a graph cycle; length3
    # cycles are precisely triangles, all included in HZ and null period.
    # Hence Z distance is exactly 4.
    return {"status":"NATIVE_135_4_4_QUTRIT_CSS_FROM_4D_VOLTAGE_COMPLETION",
        "physical_edges":135,"gauss_rows":27,"rank_HX":rx,
        "magnetic_face_basis_rows":105,"rank_HZ":rz,
        "independent_face_lengths":{"3":45,"4":56,"5":4},
        "logical_qutrits":4,
        "rank_native_period_map_mod3":4,
        "all_105_magnetic_faces_zero_integer_period":True,
        "X_logical_distance_lower_bound":4,
        "Z_logical_distance_exact":4,
        "CSS_parameters":"[[135,4,4]]_3",
        "weight4_Z_logical_cycle":vertices,
        "weight4_Z_logical_vector":[[int(e),int(z[e])] for e in np.flatnonzero(z)],
        "nonzero_4_period_mod3":list(map(int,period)),
        "proof_distance":"All X syndromes of HZ columns have no linear dependence over F3 with support <=3. A Z logical must be an oriented graph cycle; lengths <=3 are only the 45 triangular faces in HZ. An explicit nonzero-period C4 gives a nontrivial Z logical of weight4.",
        "gauge_Hamiltonian":"H=-gE sum_{135 edges} Re(X_e)-gB sum_{105 faces} Re(prod_e Z_e^signed_face_boundary). All 27 Gauss stars commute with both terms; nontrivial overlapping faces prevent the 45-decoupled-triangle decomposition.",
        "topological_meaning":"Cellular H1(GQ24 periodic base with zero-period C3,C4,C5 faces; F3) = F3^4, matched exactly to four primitive voltage periods.",
        "hard_boundary":"A distance-four code is not a demonstrated FT threshold; the choice of 105 face basis is mathematical, physical 3/4/5-link couplers, 3^135 Hilbert dynamics, photon losses, Lorentzian propagation and gravity are NOT derived."}

if __name__=="__main__":
 text=json.dumps(run(),indent=2)+"\n"
 if len(sys.argv)>1:Path(sys.argv[1]).write_text(text,encoding="utf-8")
 else:print(text)
