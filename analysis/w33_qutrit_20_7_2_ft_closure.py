#!/usr/bin/env python3
"""Single-process executor for the current [[20,7,2]]_3 FT frontier.

Running the stages in one interpreter is intentional: the deterministic
multi-minor CP-SAT result is memoized and consumed unchanged by the route
compiler, packet decoder, routed-exposure experiment, adapter audit and magic
scheduler. The output is a compact certificate summary; detailed modules remain
independently executable.
"""
from __future__ import annotations
import json

import w33_qutrit_20_7_2_multiminor_optimizer as multi
import w33_qutrit_20_7_2_w33_route_compiler as route
import w33_qutrit_20_7_2_packet_decoder as decoder
import w33_qutrit_20_7_2_threshold as threshold
import w33_qutrit_20_7_2_adapter_attack as adapter
import w33_magic_resource_scheduler as magic


def verify():
    c1 = multi.verify()
    c2 = route.verify()
    c3 = decoder.verify()
    c4 = threshold.verify()
    c5 = adapter.verify()
    c6 = magic.verify()
    checks = {
        "multiminor_optimizer_passes": c1.get("status") == "PASS",
        "w33_route_compiler_passes": c2.get("status") == "PASS",
        "mapped_decoder_passes": c3.get("status") == "PASS",
        "block_pseudothreshold_experiment_passes": c4.get("status") == "PASS",
        "pseudothreshold_not_promoted_to_physical_ft": c5.get("w33_adapter_audit", {}).get("mapped_pseudothreshold_experiment_verified") is True and c5.get("w33_adapter_audit", {}).get("mapped_threshold_certificate_present") is False,
        "adapter_audit_passes_and_refuses_ft": c5.get("status") == "PASS" and not c5.get("w33_adapter_audit", {}).get("adapter_enabled", True),
        "magic_scheduler_passes_and_refuses_ft": c6.get("status") == "PASS" and not c6.get("candidate_adapter", {}).get("enabled", True),
    }
    return {
        "schema": "w33.qutrit-20-7-2-ft-frontier-closure.v2",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "optimizer": {
            "candidate_count": c1.get("candidate_count"),
            "line_graph_diameter": c1.get("line_graph_diameter"),
            "winner": c1.get("winner"),
        },
        "routing": c2.get("routing"),
        "decoder": c3.get("decoder"),
        "syndrome_schedule": c3.get("syndrome_schedule"),
        "noise_experiment": {
            "weight2_exact": c4.get("weight2_exact"),
            "asymptotic": c4.get("asymptotic"),
            "certified_block_grid_crossing_bracket": c4.get("certified_block_grid_crossing_bracket"),
        },
        "ft_decision": c5.get("decision"),
        "remaining_blockers": c5.get("w33_adapter_audit", {}).get("blockers", []),
        "magic_candidate": c6.get("candidate_adapter"),
        "boundary": "This closure proves exact finite algebraic/topological/decoder properties and a conservative BLOCK pseudothreshold envelope under the stated phenomenological exposure model. It intentionally does not turn those results into calibrated photonic fault tolerance.",
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2))
    raise SystemExit(0 if out["status"] == "PASS" else 1)
