#!/usr/bin/env python3
"""Cross-audit parallel Pass12654 complete 5-qubit size-eight
Pauli-MUB exact-cover search, without pretending to rerun 433M nodes.

Validates eight O(5) orbit representatives independently from prep,
every per-rep no-timeout/no-witness completion, all node counts and
published n=3 controls with fresh replays of size5-exists/size7-none.
Separately confirms size9 existence with a bounded independent search.
Documents the algorithm's pivot, killers and top-r union-bound logic.

One algorithm with multiple traversal orders is NOT a formal external
proof checker. Its result is a strong computational certificate,
pending independent implementation/reversed-run cross-validation.
"""
from pathlib import Path
import json,sys,inspect
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_five_qubit_size8_dlx as D
OUT=ROOT/"data/toe_20261113_pass12654_MUB_no_size8_completed_run_crossaudit.json"

def main():
    full=json.loads((ROOT/"data/w33_five_qubit_size8_dlx_full.json").read_text())
    root=full["n5_size8"]
    assert root["n"]==5 and root["size"]==8 and root["status"]=="none"
    assert root["example"] is None
    assert len(root["per_rep"])==8
    reps=[int(x["s2"]) for x in root["per_rep"]]
    assert reps==D.prep(5)[-1]==[692,693,694,695,700,701,702,703]
    assert all(x["found"] is None and x["timeout"] is False for x in root["per_rep"])
    assert all(x["nodes"]>0 and x["seconds"]>0 for x in root["per_rep"])
    total=sum(int(x["nodes"]) for x in root["per_rep"])
    assert total==root["nodes"]==433517130
    assert root["wall"]>0
    assert full["control_n3_size5"]["status"]=="exists"
    assert full["control_n3_size7"]["status"]=="none"
    # Replaying controls uses the same solver as the parallel commit:
    # valuable for sanity, not algorithmic independence.
    n3=D.prep(3)[-1]
    assert len(n3)==2
    controls=[]
    for sz in (5,7):
        for rep in n3:
            res=D.search_rep((3,sz,rep,30))
            assert res["timeout"] is False
            controls.append({"n":3,"size":sz,"rep":int(rep),
                             "found":res["found"] is not None,"nodes":res["nodes"]})
    assert all(x["found"] for x in controls if x["size"]==5)
    assert not any(x["found"] for x in controls if x["size"]==7)
    # The n5 size9 witness is a useful positive control on the
    # SAME rank-code geometry, not independent proof of no size8.
    nine=D.search_rep((5,9,692,30))
    assert nine["found"] and not nine["timeout"],nine
    assert len(nine["found"])==7  # I,S2 + 5 more
    # Exhaustiveness rationale for DFS "most constrained uncovered":
    # At any partial set, an uncovered extender r MUST be killed by
    # one new candidate c with c=r or det(c+r)=0; branch over all.
    # The candidate coverage top-r bound is a union bound, safe.
    result={
      "status":"PASS_CROSSAUDIT_OF_PARALLEL_COMPLETE_SIZE8_NO_GO_SINGLE_IMPLEMENTATION",
      "parallel_commit":"cc65eb5d2dd3f806fc0168c9dff0314ba29c4e65",
      "source":"data/w33_five_qubit_size8_dlx_full.json",
      "full_run_eight_O5_representatives":reps,
      "all_eight_orbits_timed_out":False,
      "all_eight_orbits_completed_no_witness":True,
      "total_exact_cover_DFS_nodes":total,
      "per_rep_nodes":{str(x["s2"]):int(x["nodes"]) for x in root["per_rep"]},
      "wall_seconds":root["wall"],
      "fresh_control_n3":controls,
      "fresh_control_n5_size9_found":True,
      "fresh_control_n5_size9_nodes":nine["nodes"],
      "strong_computational_conclusion":"Given the normalization to 0,infinity,I and exhaustive O5 orbits, no maximal partial 5-qubit symplectic spread of cardinality eight. Combined with certified size7-no and size9-yes gives minimum 9. The current exact-cover algorithm is a single solver family, not an externally checked UNSAT certificate.",
      "algorithm_completeness_conditions":{
        "branch_pivot":"Every still-compatible uncovered rank-code T must be killed by at least one remaining candidate, and all such candidates are branched.",
        "sibling_exclusion":"Earlier killer choices are excluded in later sibling subtrees to avoid duplicate unordered sets.",
        "safe_topr_pruning":"Sum of r largest individual coverage counts less than total uncovered implies no r candidates cover the uncovered set.",
        "S2_orbit_coverage":"The eight listed O(5) congruence representatives exhaust the normalized second-matrix choices."
      },
      "limits":"This pass does NOT independently re-execute the 433,517,130-node negative search. The parallel author's reversed traversal on the two S3 classes is not yet independently certified in this file. Our separate lazy CP-SAT test remains undecided and does not contradict the completed full search."
    }
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in ("status","full_run_eight_O5_representatives","total_exact_cover_DFS_nodes","fresh_control_n5_size9_found","fresh_control_n5_size9_nodes")},indent=2),flush=True)
    return result
if __name__=="__main__":main()
