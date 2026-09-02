#!/usr/bin/env python3
"""Single-process executor for the current [[20,7,2]]_3 physical-FT frontier."""
from __future__ import annotations
import json
import w33_qutrit_20_7_2_multiminor_optimizer as multi
import w33_qutrit_20_7_2_w33_route_compiler as route
import w33_qutrit_20_7_2_packet_decoder as decoder
import w33_qutrit_20_7_2_logical_quotient as logical
import w33_qutrit_20_7_2_optical_primitive as optical
import w33_qutrit_optical_calibration_ingest as calibration
import w33_qutrit_20_7_2_circuit_noise as circuit_noise
import w33_qutrit_20_7_2_fault_location_census as locations
import w33_qutrit_20_7_2_threshold as threshold
import w33_k12_singular_css_closure as k12css
import w33_qutrit_20_7_2_to_66_bridge as bridge66
import w33_qutrit_20_7_2_to_66_recode_circuit as recode
import w33_qutrit_20_7_2_adapter_attack as adapter
import w33_magic_resource_scheduler as magic

def verify():
    c1=multi.verify();c2=route.verify();c3=decoder.verify();c4=logical.verify();c5=optical.verify();cc=calibration.verify(circuit_noise.DEFAULT_RATES);c6=circuit_noise.verify();cl=locations.verify();c7=threshold.verify();ck=k12css.verify();c8=bridge66.verify();cr=recode.verify();c9=adapter.verify();c10=magic.verify();audit=c9.get("w33_adapter_audit",{})
    checks={
      "multiminor_optimizer_passes":c1.get("status")=="PASS",
      "w33_route_compiler_passes":c2.get("status")=="PASS",
      "mapped_decoder_passes":c3.get("status")=="PASS",
      "seven_logical_quotient_passes":c4.get("status")=="PASS",
      "optical_candidate_compiler_passes":c5.get("status")=="PASS" and c5.get("optical_compiler_verified") is True,
      "calibration_ingest_passes_and_matches_optical_gate":cc.get("status")=="PASS" and c5.get("hardware_calibration_verified")==cc.get("effective_rate_source",{}).get("hardware_backed"),
      "circuit_level_noise_census_passes":c6.get("status")=="PASS",
      "fault_location_census_passes":cl.get("status")=="PASS",
      "block_pseudothreshold_experiment_passes":c7.get("status")=="PASS",
      "K12_singular_topology_and_native_gauge_fix_pass":ck.get("status")=="PASS" and ck.get("raw_css",{}).get("parameters")=="[[66,13,3]]_3" and ck.get("native_k8_gauge_fix",{}).get("parameters")=="[[66,8,3]]_3",
      "distance3_store_bridge_passes":c8.get("status")=="PASS",
      "naive_recode_no_go_passes":cr.get("status")=="PASS" and cr.get("decision")=="REFUSE_NAIVE_RECODE_AS_FAULT_TOLERANT",
      "adapter_audit_passes_and_remains_evidence_scoped":c9.get("status")=="PASS",
      "magic_scheduler_passes":c10.get("status")=="PASS",
    }
    checks={k:bool(v) for k,v in checks.items()}
    return {
      "schema":"w33.qutrit-20-7-2-ft-frontier-closure.v4","status":"PASS" if all(checks.values()) else "FAIL","checks":checks,
      "optimizer":{"candidate_count":c1.get("candidate_count"),"line_graph_diameter":c1.get("line_graph_diameter"),"winner":c1.get("winner")},
      "routing":c2.get("routing"),"decoder":c3.get("decoder"),"syndrome_schedule":c3.get("syndrome_schedule"),
      "logical_quotient":{"basis":c4.get("logical_basis",{}),"weight2":c4.get("weight2"),"weight3":c4.get("weight3"),"weight3_exhaustive":c4.get("weight3_exhaustive")},
      "optical":{"device_inventory":c5.get("device_inventory"),"compiled_primitive_count":c5.get("compiled_primitive_count"),"hardware_calibration_verified":c5.get("hardware_calibration_verified"),"rate_source":c6.get("rate_source")},
      "fault_locations":{"syndrome":cl.get("syndrome_locations"),"weighted_SUM_data":cl.get("weighted_SUM_data_locations"),"recode":cl.get("recode_locations")},
      "K12":{"topology":ck.get("raw_complex"),"normalization":ck.get("normalization"),"raw_css":ck.get("raw_css"),"native_k8_gauge_fix":ck.get("native_k8_gauge_fix")},
      "recode":{"circuit":cr.get("circuit"),"fault_census":cr.get("fault_census"),"decision":cr.get("decision")},
      "ft_decision":c9.get("decision"),"remaining_blockers":audit.get("blockers",[]),"magic_candidate":c10.get("candidate_adapter"),
      "boundary":"The committed K12 face object is a singular pseudocomplex, not a genus-6 surface. Its raw chain code is [[66,13,3]]_3 and five explicit Z-logical gauge constraints give a native [[66,8,3]]_3. The natural source-decode/bare-handoff/target-encode recode is exactly compiled and exactly rejected as non-FT because all 56 bare-handoff Pauli faults are target logical faults. Hardware-backed W33 calibration, a physical threshold, and an encoded no-bare-window recode remain physical evidence gates.",
    }
if __name__=="__main__":
    out=verify();print(json.dumps(out,indent=2));raise SystemExit(0 if out["status"]=="PASS" else 1)
