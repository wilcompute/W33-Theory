#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_common_winding_relative_h2.json"

from analysis.w33_20260924_history_invariant_cycle_orientation import (
    HS, EDGES, TRIS, boundary_triangle,
)

def rank_q(A):
    A=np.array(A,dtype=float)
    return int(np.linalg.matrix_rank(A,tol=1e-10))

def main():
    V=len(HS); E=len(EDGES); F=len(TRIS)
    assert (V,E,F)==(27,108,36)

    # Oriented vertex-edge boundary.
    d1=np.zeros((V,E),dtype=int)
    for j,(a,b) in enumerate(EDGES):
        d1[a,j]=-1; d1[b,j]=1

    # Triangle-edge boundary.
    d2=np.column_stack([boundary_triangle(t) for t in TRIS])
    assert d2.shape==(E,F)
    assert np.array_equal(d1@d2,np.zeros((V,F),dtype=int))
    r1=rank_q(d1); r2=rank_q(d2)
    assert (r1,r2)==(26,36)

    h1_graph=E-r1
    h1_filled=(E-r1)-r2
    h2_filled=F-r2
    assert (h1_graph,h1_filled,h2_filled)==(82,46,0)

    # Pair (K,G): K = filled temporal 2-complex, G = its 1-skeleton.
    # C2(K,G)=C2(K)=Q^36 and C1(K,G)=0, hence H2(K,G)=Q^36.
    h2_relative=F
    assert h2_relative==36

    total_face=np.ones(F,dtype=int)
    boundary=d2@total_face

    old=json.loads(
        (ROOT/"data/w33_20260924_history_invariant_cycle_orientation.json").read_text()
    )
    invariant=np.array(old["invariant_cycle"]["edge_coefficients"],dtype=int)
    assert np.array_equal(boundary,invariant)
    assert np.count_nonzero(boundary)==108
    assert set(map(int,boundary))=={-1,1}

    # Since d2 is injective, the connecting map
    # delta:H2(K,G)->H1(G) has rank 36 and trivial kernel.
    assert r2==h2_relative
    winding=json.loads(
        (ROOT/"data/w33_20260924_common_winding_orientation_chain_map.json").read_text()
    )
    assert winding["chain_map"]["equals_preexisting_invariant_orientation_cycle"] is True
    assert winding["homology_resolution"]["filled_history_H1_class"]=="zero"

    out={
      "schema":"w33.20260924.common_winding_relative_h2.v1",
      "status":"PASS_COMMON_WINDING_IS_DISTINGUISHED_RELATIVE_H2_BOUNDARY_CLASS",
      "complex":{
        "vertices":V,"edges":E,"triangles":F,
        "rank_d1":r1,"rank_d2":r2,
        "H1_one_skeleton_dimension":h1_graph,
        "H1_filled_dimension":h1_filled,
        "H2_filled_dimension":h2_filled,
      },
      "relative_pair":{
        "pair":"(K,G), K=filled 27-history complex, G=its null 1-skeleton",
        "H2_KG_dimension":h2_relative,
        "connecting_map_rank":r2,
        "connecting_map_kernel_dimension":h2_relative-r2,
        "exact_sequence_dimensions":"0 -> 36 -> 82 -> 46 -> 0",
        "dimension_identity":"82 = 36 + 46",
      },
      "distinguished_class":{
        "relative_2_cycle":"sum of all 36 oriented temporal triangles",
        "boundary_support_edges":int(np.count_nonzero(boundary)),
        "boundary_coefficients":"all +/-1",
        "boundary_equals_unique_invariant_orientation_cycle":True,
        "source_equals_common_four-null_winding_orbit_sum":True,
      },
      "theorem":(
        "The positive common four-null winding is not lost when the temporal "
        "triangles are filled.  It is the connecting-boundary image of the "
        "distinguished relative class [sum of all 36 temporal triangles] in "
        "H2(K,G).  Because d2 has full column rank 36, H2(K,G) is 36-dimensional "
        "and the connecting map injects it into the 82-dimensional cycle space "
        "of the null graph; quotienting by that 36-dimensional image leaves the "
        "46-dimensional filled-history H1.  The common winding spans the invariant "
        "line inside this relative boundary sector."
      ),
      "boundary":(
        "This is a finite relative-homology statement.  It does not by itself "
        "supply a thermodynamic arrow or a continuum time coordinate; it says "
        "precisely where the monotone integer winding lives topologically after "
        "the finite history graph is filled."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "sequence":out["relative_pair"]["exact_sequence_dimensions"],
      "boundary_edges":out["distinguished_class"]["boundary_support_edges"],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
