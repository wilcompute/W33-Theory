#!/usr/bin/env python3
"""Exact E6 cubic compatibility falsifier for one EXPLICIT, NONCANONICAL address map.
This is not a no-go across all identifications of the two 27D carriers.
"""
from pathlib import Path
import json, sys, itertools
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_chiral_null_order3_gate as G
CANON=ROOT/"extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json"
BRIDGE=ROOT/"data/w33_e6id_current_h27_gauge_bridge.json"
OUT=ROOT/"data/toe_20261113_chiral_e6_cubic_compatibility.json"

def run():
    canon=json.loads(CANON.read_text(encoding="utf-8"))
    bridge=json.loads(BRIDGE.read_text(encoding="utf-8"))
    signs={}
    for row in canon["solution"]["d_triples"]:
        key=tuple(sorted(map(int,row["triple"])))
        signs[key]=1 if int(row["sign"])%3==1 else -1
    assert len(signs)==45 and all(abs(s)==1 for s in signs.values())
    e_to_h={int(k):tuple(map(int,v)) for k,v in bridge["maps"]["e6id_to_current_H27_address"].items()}
    assert len(e_to_h)==27 and set(e_to_h.values())==set(G.V)
    _,_,D=G.build();I=np.eye(27,dtype=np.int64)
    twice=18*I+3*D+D@D
    assert not np.any(twice%2)
    M=twice//2
    # Represent in E6 coordinates via fixed current H27 ADDRESS TABLE,
    # not by asserting a group-equivariant equivalence H27 ~= F3^3.
    # Coordinate re-identification must conjugate BOTH output and input histories.
    C=np.asarray([[M[G.VID[e_to_h[i]],G.VID[e_to_h[j]]] for j in range(27)] for i in range(27)],dtype=np.int64)
    def norm(y):
        return sum(int(s)*int(y[i])*int(y[j])*int(y[k]) for (i,j,k),s in signs.items())
    signed_N_values=[norm(C[:,j]) for j in range(27)]
    nonzero=[{"input_e6_index":j,"input_history":list(e_to_h[j]),"signed_norm_of_9Ue_cubed":int(v)}
             for j,v in enumerate(signed_N_values) if v]
    # Since e_j is a coordinate basis vector, N(e_j)=0.
    # N(Ue_j)=N(M e_j)/9^3 exactly, and one nonzero proves direct incompatibility.
    result={
     "status":"DIRECT_ADDRESS_IDENTIFICATION_TEST",
     "canonical_signed_triads":45,
     "address_table":"data/w33_e6id_current_h27_gauge_bridge.json",
     "e6_normalization":"sum s_{ijk} x_i x_j x_k over 45 monomials",
     "address_identification":"history Sym2(a,b,c) -> physical H27 normal-form address (a,b,c)",
     "validity":"Address bijection, but NOT an H27-equivariant representation identification",
     "nonzero_output_count":len(nonzero),
     "nonzero_examples":nonzero[:7],
     "all_basis_inputs_have_cubic_zero":True,
     "counterexample_to_naive_identification":bool(nonzero),
     "interpretation":"Naive coordinate transport of U is not an E6 cubic automorphism if any N(Ue_j)!=0; no general embedding no-go follows."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    return result
if __name__=="__main__":run()
