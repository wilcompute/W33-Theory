#!/usr/bin/env python3
"""Current Holonet/W33 machine datasheet with exact QEC evidence boundaries."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    datasheet=[
      {"subsystem":"processor","spec":"balanced-ternary/qutrit finite processor; exact Clifford packet layer plus explicit non-Clifford logical T port","substrate":"W33/Sp(4,3) finite architecture","evidence":"exact finite/software"},
      {"subsystem":"interconnect","spec":"W(3,3)=SRG(40,12,2,4), 240 edge carriers; routed two-qutrit primitives use shared-point locality","substrate":"W33 point/edge geometry","evidence":"exact finite/software"},
      {"subsystem":"protected store A","spec":"explicit [[66,8,3]]_3 stabilizer: eight cyclic [[5,1,3]]_3 blocks plus 26 frozen Z ancillas","substrate":"Pass79 noncanonical block-plus-ancilla witness","evidence":"exact finite stabilizer witness"},
      {"subsystem":"K12 incidence/QEC layer","spec":"committed V=12,E=66,F=44 oriented twofold-triple pseudocomplex; raw GF(3) chain code [[66,13,3]]_3; five explicit Z-logical gauge constraints give native K12-labelled [[66,8,3]]_3","substrate":"singular Reye-K12 pseudocomplex; normalization T^2 disjoint-union S^2","evidence":"exact topology + chain-complex + distance-3 search"},
      {"subsystem":"recode","spec":"exact source-decode / seven-logical-handoff / seven-block-encode Clifford tableau; REFUSED as FT because all 56 bare-handoff Pauli faults are target logical faults","substrate":"[[20,7,2]]_3 -> Pass79 store","evidence":"exact symplectic fault no-go"},
      {"subsystem":"physical fault tolerance","spec":"REFUSED until hardware-backed W33 optical calibration, a physical threshold, and an encoded no-bare-window code switch exist","substrate":"optical compiler + circuit-location census","evidence":"open physical gate"},
    ]
    correction={
      "old_identification":"the 44-face K12 table is a connected closed genus-6 surface and its standard code is [[66,8,3]]_3",
      "status":"RETRACTED",
      "exact_replacement":{"face_dual_components":[40,4],"raw_vertex_count":12,"normalized_vertex_count":24,"normalization_components":["torus","sphere"],"rank_d1_GF3":11,"rank_d2_GF3":42,"raw_betti_GF3":[1,13,2],"raw_chain_code":"[[66,13,3]]_3","gauge_fixed_native_code":"[[66,8,3]]_3","extra_independent_Z_logical_constraints":5},
      "reason":"Euler's genus formula was applied before checking the 2-manifold hypothesis. Disconnected vertex links make the raw 44-face object singular; chi=-10 comes from vertex identifications in a pseudocomplex, not genus 6.",
    }
    out={"schema":"w33.holonet-system-datasheet.v3","status":"PASS_WITH_PHYSICAL_FT_OPEN","datasheet":datasheet,"qec_correction":correction,"von_neumann":{"universal computer":"finite/software constructions in corpus","universal constructor":"gate/compiler/network candidate; physical construction not certified","error-corrected description":"two exact 66-qutrit stabilizer witnesses now exist, but physical recode remains open"},"summary":"The finite/software stack now has exact routing, optical candidate compilation, decoding, location-level fault classification, Pass79's explicit [[66,8,3]]_3 store, and a second native K12-labelled [[66,8,3]]_3 obtained by five gauge-fixing checks on the actual singular pseudocomplex. The obvious bare-logical recode is proved non-FT. Hardware calibration, threshold, and an encoded code-switch remain open.","sources":["w33_pass79_full_closure.py","analysis/w33_reye_k12_orientable_horizon_completion.py","analysis/w33_k12_singular_css_closure.py","analysis/w33_qutrit_20_7_2_to_66_recode_circuit.py","analysis/w33_qutrit_20_7_2_adapter_attack.py"]}
    p=ROOT/"data/w33_holonet_system.json";p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8");print(json.dumps(out,indent=2));return 0
if __name__=="__main__":raise SystemExit(main())
