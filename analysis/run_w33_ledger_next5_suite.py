#!/usr/bin/env python3
"""Run the five Ledger/W33 follow-up experiments and freeze one aggregate certificate."""
from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;DATA=HERE.parent/"data"
PARTS=[
 ("audit","w33_ledger_audit_depth3_allq.py","PART_LEDGER_AUDIT_DEPTH3_ALLQ.json","DEPTH_Q_CONJECTURE_KILLED_DEPTH3_OPEN_FAMILY"),
 ("tomita","w33_ledger_tomita_mirror_fold.py","PART_LEDGER_TOMITA_MIRROR_FOLD.json","PASS_TOMITA_TO_W33_MIRROR_AFTER_COMMUTANT_FOLD"),
 ("h2","w33_ledger_allq_h2.py","PART_LEDGER_ALLQ_H2.json","THEOREM_ALL_W3Q_H2_ZERO"),
 ("darkbond","w33_ledger_dark_bond_route_census.py","PART_LEDGER_DARK_BOND_ROUTE_CENSUS.json","NO_INTERACTION_FREE_DYNAMIC_BOND_FOUND_AUXILIARY_ROUTE_TREE_LEVEL_ONLY"),
 ("deficiency80","w33_ledger_deficiency80_invariance.py","PART_LEDGER_DEFICIENCY80_INVARIANCE.json","DEFICIENCY80_IS_NOT_W33_BUILDING_MODULE")]
def main():
    parts={}
    for key,script,name,status in PARTS:
        subprocess.run([sys.executable,str(HERE/script)],check=True,stdout=subprocess.DEVNULL)
        x=json.loads((DATA/name).read_text());assert x["status"]==status and all(x["checks"].values())
        parts[key]={"path":f"data/{name}","status":status}
    out={"schema":"w33.ledger.next-five-2026-09-21.v1",
         "status":"PASS_FIVE_EXECUTED_WITH_TWO_THEOREMS_TWO_CORRECTIONS_ONE_OPEN_CANDIDATE",
         "parts":parts,
         "headline":["three-party depth=q conjecture is false; q=4,5 close at depth 3 on an open faithful family",
                     "standard-form Tomita commutant exchange becomes the base W33 anti-symplectic mirror after transpose fold; 540 is its Clifford-frame orbit",
                     "H1(W(3,q);Z)=Z^(q^4) and Hk=0 for all k>=2 over the whole prime-power family",
                     "no interaction-free dynamic dark-bond escape found; a nondynamical auxiliary Weinberg contact survives tree level only",
                     "the 80-dimensional qutrit audit deficiency is not PSp(4,3)-invariant and is not the W33 building module"]}
    p=DATA/"PART_LEDGER_NEXT5_2026_09_21.json";p.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=="__main__":main()
