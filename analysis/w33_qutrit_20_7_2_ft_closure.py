#!/usr/bin/env python3
"""Single-process executor for the current [[20,7,2]]_3 physical-FT frontier.

The deterministic multi-minor optimizer is memoized and consumed unchanged by
routing, decoding, optical lowering, noise analysis, storage recoding, adapter
audit, and magic admission.  The closure deliberately separates executable
software/compiler evidence from measured photonic evidence.
"""
from __future__ import annotations
import json

import w33_qutrit_20_7_2_multiminor_optimizer as multi
import w33_qutrit_20_7_2_w33_route_compiler as route
import w33_qutrit_20_7_2_packet_decoder as decoder
import w33_qutrit_20_7_2_logical_quotient as logical
import w33_qutrit_20_7_2_optical_primitive as optical
import w33_qutrit_20_7_2_circuit_noise as circuit_noise
import w33_qutrit_20_7_2_threshold as threshold
import w33_qutrit_20_7_2_to_66_bridge as bridge66
import w33_qutrit_20_7_2_adapter_attack as adapter
import w33_magic_resource_scheduler as magic


def verify():
    c1=multi.verify(); c2=route.verify(); c3=decoder.verify(); c4=logical.verify()
    c5=optical.verify(); c6=circuit_noise.verify(); c7=threshold.verify(); c8=bridge66.verify()
    c9=adapter.verify(); c10=magic.verify()
    audit=c9.get("w33_adapter_audit",{})
    checks={
        "multiminor_optimizer_passes":c1.get("status")=="PASS",
        "w33_route_compiler_passes":c2.get("status")=="PASS",
        "mapped_decoder_passes":c3.get("status")=="PASS",
        "seven_logical_quotient_passes":c4.get("status")=="PASS",
        "optical_candidate_compiler_passes":c5.get("status")=="PASS" and c5.get("optical_compiler_verified") is True,
        "hardware_calibration_not_fabricated":c5.get("hardware_calibration_verified") is False,
        "circuit_level_noise_census_passes":c6.get("status")=="PASS",
        "block_pseudothreshold_experiment_passes":c7.get("status")=="PASS",
        "distance3_store_bridge_passes":c8.get("status")=="PASS" and c8.get("checks",{}).get("pass79_target_is_verified_66_8_3") is True,
        "standard_K12_k8_surface_claim_closed_by_no_go":c8.get("checks",{}).get("standard_genus6_K12_surface_code_encodes_12_not_8") is True,
        "pseudothreshold_not_promoted_to_physical_ft":audit.get("mapped_pseudothreshold_experiment_verified") is True and audit.get("mapped_threshold_certificate_present") is False,
        "adapter_audit_passes_and_refuses_ft":c9.get("status")=="PASS" and not audit.get("adapter_enabled",True),
        "magic_scheduler_passes_and_refuses_ft":c10.get("status")=="PASS" and not c10.get("candidate_adapter",{}).get("enabled",True),
    }
    checks={k:bool(v) for k,v in checks.items()}
    return {
        "schema":"w33.qutrit-20-7-2-ft-frontier-closure.v3",
        "status":"PASS" if all(checks.values()) else "FAIL",
        "checks":checks,
        "optimizer":{"candidate_count":c1.get("candidate_count"),"line_graph_diameter":c1.get("line_graph_diameter"),"winner":c1.get("winner")},
        "routing":c2.get("routing"),
        "decoder":c3.get("decoder"),"syndrome_schedule":c3.get("syndrome_schedule"),
        "logical_quotient":{"basis":c4.get("logical_basis",{}),"weight2":c4.get("weight2"),"weight3":c4.get("weight3"),"weight3_exhaustive":c4.get("weight3_exhaustive")},
        "optical":{"device_inventory":c5.get("device_inventory"),"compiled_primitive_count":c5.get("compiled_primitive_count"),"hardware_calibration_verified":c5.get("hardware_calibration_verified"),"engineering_parameters_required":c5.get("engineering_parameters_required")},
        "circuit_noise":{"schedule":c6.get("schedule"),"single_syndrome_fault_census":c6.get("single_syndrome_fault_census"),"sweep":c6.get("sweep")},
        "routed_exposure_pseudothreshold":{"weight2_exact":c7.get("weight2_exact"),"asymptotic":c7.get("asymptotic"),"certified_block_grid_crossing_bracket":c7.get("certified_block_grid_crossing_bracket")},
        "protected_store":{"bridge":c8.get("bridge"),"K12_surface_code_audit":c8.get("K12_surface_code_audit")},
        "ft_decision":c9.get("decision"),"remaining_blockers":audit.get("blockers",[]),"magic_candidate":c10.get("candidate_adapter"),
        "boundary":"Executable algebra, W33 routing, optical candidate compilation, seven-logical quotient resolution, circuit-level syndrome fault census, and logical recoding into an explicit distance-3 66-qutrit store are closed. Measured optical calibration, a hardware-calibrated physical threshold, and a fault-tolerant physical code-switch remain separate physical evidence gates. The standard closed genus-6 K12 edge surface code has k=12 over GF(3), not k=8 without four extra constraints.",
    }

if __name__=="__main__":
    out=verify(); print(json.dumps(out,indent=2)); raise SystemExit(0 if out["status"]=="PASS" else 1)
