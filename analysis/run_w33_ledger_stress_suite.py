#!/usr/bin/env python3
"""Run all five Ledger/W33 stress tests and freeze an aggregate certificate."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
DATA=ROOT/"data"
PARTS=[
 ("modular_character","w33_ledger_modular_character_stress_test.py","PART_LEDGER_MODULAR_CHARACTER_STRESS_TEST.json","PASS_LITERAL_CHARACTER_WITH_THREE_QUTRITS"),
 ("mirror_group","w33_ledger_mirror_group_stress_test.py","PART_LEDGER_MIRROR_GROUP_STRESS_TEST.json","PASS_GEOMETRIC_MIRROR_DOUBLE_COVER"),
 ("audit_completeness","w33_ledger_qutrit_audit_completeness.py","PART_LEDGER_QUTRIT_AUDIT_COMPLETENESS.json","CORRECTION_DEPTH2_FAILS_Q3_DEPTH3_CLOSES"),
 ("monopole_cohomology","w33_ledger_monopole_cohomology.py","PART_LEDGER_MONOPOLE_COHOMOLOGY.json","PASS_W33_H2_ZERO_GLOBAL_EXACTNESS"),
 ("dark_bond","w33_ledger_dark_bond_no_go.py","PART_LEDGER_DARK_BOND_NO_GO.json","NO_GO_H4_PRODUCT_HAMILTONIAN_AS_WRITTEN"),
]
def main():
    parts={}
    for key,script,name,status in PARTS:
        subprocess.run([sys.executable,str(HERE/script)],check=True,stdout=subprocess.DEVNULL)
        x=json.loads((DATA/name).read_text())
        assert x["status"]==status
        assert x.get("checks") and all(x["checks"].values())
        parts[key]={"path":f"data/{name}","status":status}
    out={"schema":"w33.ledger.stress-suite.v1","status":"PASS_WITH_TWO_LEDGER_CORRECTIONS","parts":parts,
      "headline":{"positive":[
        "literal modular character exhibits overlap-only complex phase in a minimal three-qutrit extension",
        "geometric anti-symplectic mirrors generate the 51840 extension and even products recover PSp(4,3)",
        "W33 clique complex has H^2=0 so closed 2-cochains are exact on this carrier"],
        "corrections":[
        "depth-two audit completeness does not naively generalize from qubits to qutrits: 649/729; depth three closes 729/729",
        "H.4 product Hamiltonian preserves Schmidt spectrum and cannot induce a new visible operator by partial trace"]},
      "claim_firewall":{"tomita_equals_geometric_mirror":False,"universal_no_monopoles_from_dF_zero_alone":False,
        "qutrit_A2_completeness":False,"H4_product_hamiltonian_dynamic_dark_bond":False}}
    p=DATA/"PART_LEDGER_STRESS_SUITE.json";p.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=="__main__":main()
