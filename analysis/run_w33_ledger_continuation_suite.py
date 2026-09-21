#!/usr/bin/env python3
"""Run the five post-next5 Ledger/W33 continuation certificates."""
from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;DATA=HERE.parent/"data"
PARTS=[
 ("nparty_depth3","w33_ledger_depth3_nparty_theorem.py","PART_LEDGER_DEPTH3_NPARTY.json","THEOREM_DEPTH3_EXISTS_FOR_ALL_N_GE_3_Q_GE_3"),
 ("modular_flow","w33_ledger_modular_flow_firewall.py","PART_LEDGER_MODULAR_FLOW_FIREWALL.json","NO_GO_NONTRIVIAL_CONTINUOUS_MODULAR_FLOW_INSIDE_W33_AUTOMORPHISMS"),
 ("simple_homotopy","w33_w3q_simple_homotopy_collapse.py","PART_W3Q_SIMPLE_HOMOTOPY_COLLAPSE.json","THEOREM_W3Q_CLIQUE_SIMPLE_HOMOTOPY_WEDGE_Q4_CIRCLES"),
 ("winding","w33_ledger_winding_sector_firewall.py","PART_LEDGER_WINDING_SECTOR_FIREWALL.json","TOPOLOGY_SUPPLIES_Q4_WINDING_GENERATORS_NOT_A_UNIQUE_MATTER_SPECTRUM"),
 ("auxiliary","w33_ledger_auxiliary_radiative_firewall.py","PART_LEDGER_AUXILIARY_RADIATIVE_FIREWALL.json","AUXILIARY_CONTACT_REMOVES_HEAVY_POLE_THRESHOLD_UV_COMPLETION_STILL_OPEN"),
]
def main():
    parts={}
    for key,script,name,status in PARTS:
        subprocess.run([sys.executable,str(HERE/script)],check=True,stdout=subprocess.DEVNULL)
        x=json.loads((DATA/name).read_text())
        assert x["status"]==status and all(x["checks"].values())
        parts[key]={"path":f"data/{name}","status":status}
    out={
      "schema":"w33.ledger.continuation-2026-09-21.v1",
      "status":"PASS_FIVE_CONTINUATION_WITH_THREE_THEOREMS_ONE_FIREWALL_ONE_CANDIDATE_UPGRADE",
      "parts":parts}
    p=DATA/"PART_LEDGER_CONTINUATION_2026_09_21.json"
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
    return out
if __name__=="__main__":main()
