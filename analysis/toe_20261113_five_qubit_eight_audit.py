#!/usr/bin/env python3
"""Fail-closed status audit for five-qubit 8/9 Pauli MUB candidates.
The 8-set search has timeouts; this file deliberately does NOT claim a no-go.
"""
from __future__ import annotations
from pathlib import Path
import json, hashlib

ROOT=Path(__file__).resolve().parents[1]
EIGHT=ROOT/"data/w33_five_qubit_size8_dlx.json"
NINE=ROOT/"data/w33_five_qubit_size9_verify.json"
OUT=ROOT/"data/toe_20261113_five_qubit_search_boundary.json"

def verify():
    a=json.loads(EIGHT.read_text(encoding="utf-8"))
    b=json.loads(NINE.read_text(encoding="utf-8"))
    assert a["control_n3_size5"]["status"]=="exists"
    assert a["control_n3_size7"]["status"]=="none"
    n=a["n5_size8"]
    assert n["n"]==5 and n["size"]==8
    assert n["status"]=="undecided" and n["example"] is None
    assert len(n["per_rep"])==8
    assert all(row["timeout"] for row in n["per_rep"])
    assert sum(row["nodes"] for row in n["per_rep"])==n["nodes"]==4310000
    assert b["size"]==9 and b["maximal"] is True
    assert b["nonsingular_T_checked"]==13888
    assert b["extendible_T"]==0 and b["graphs_isotropic"] and b["pairwise_disjoint"]
    out={
      "schema":"toe.five_qubit_eight_front.v1",
      "status":"EIGHT_UNDECIDED_NINE_EXACT_WITNESS",
      "eight":{"orbit_representatives":8,"nodes_explored":n["nodes"],
               "all_orbits_timed_out":True,"wall_seconds":n["wall"],
               "search_return":"undecided","exhaustive_nonexistence_proved":False,
               "candidate_found":False,
               "source_file_sha256":hashlib.sha256(EIGHT.read_bytes()).hexdigest()},
      "nine":{"maximal_partial_spread":True,"all_nonsingular_symmetric_matrices_checked":13888,
              "extendible_candidates":0,"seven_symmetric_matrix_codes":b["example"],
              "source_file_sha256":hashlib.sha256(NINE.read_bytes()).hexdigest()},
      "prior_lower_bound":"Pass12649 independently states minimum >= 8, not rerun here",
      "current_interval":"minimum is 8 or 9",
      "literature":"2021 Mathematics 9(12) 1388 also reports five-qubit WUS sizes 9,11,13,15,17, without excluding size8",
      "boundary":"A timeout is not a no-solution certificate. Need full no-8 proof or verified eight-set witness."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return out
if __name__=="__main__":
    print(json.dumps(verify(),indent=2))
