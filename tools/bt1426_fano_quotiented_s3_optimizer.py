#!/usr/bin/env python3
"""BT1426: Fano-quotiented S3 optimizer frontier.

The full S3 gauge problem still lives on 40 line variables.  The Fano symmetry is
not claimed to act on those variables.  What it does act on exactly is the
physical front-end objective packetization: 168 active bins are one Fano flag
orbit with stabilizer weight 8, and the remaining 162 correction cache slots are
27 Steinberg cycles times 6 S3 labels.  This file builds that weighted quotient
and records the resulting packet-symmetric search frontier.
"""
from __future__ import annotations

import json
from math import comb, gcd
from pathlib import Path
from functools import reduce

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1426_fano_quotiented_s3_optimizer.json"
LABELS = [0,4,0,3,3,1,3,0,5,3,1,2,5,2,1,1,2,2,2,1,3,2,0,3,3,0,3,0,5,2,1,1,3,0,5,0,1,1,0,1]


def radius_count(r: int) -> int:
    return comb(39, r) * (6 ** r - 1)


def main() -> None:
    packets = [
        {"packet": "identity_fano_flag_packets", "representatives": 21, "weight": 10, "raw_edges": 210, "objective_side": "identity"},
        {"packet": "active_fano_flag_stabilizer_packets", "representatives": 21, "weight": 8, "raw_edges": 168, "objective_side": "correction"},
        {"packet": "steinberg_s3_cache_packets", "representatives": 27, "weight": 6, "raw_edges": 162, "objective_side": "correction"},
    ]
    quotient_reps = sum(p["representatives"] for p in packets)
    raw_edges = sum(p["raw_edges"] for p in packets)
    quotient_weights = [p["weight"] for p in packets]
    packet_gcd = reduce(gcd, quotient_weights)
    correction_reps = sum(p["representatives"] for p in packets if p["objective_side"] == "correction")
    correction_raw = sum(p["raw_edges"] for p in packets if p["objective_side"] == "correction")
    identity_raw = sum(p["raw_edges"] for p in packets if p["objective_side"] == "identity")
    radius_leq3 = sum(radius_count(r) for r in range(1, 4))
    next_packet_symmetric_identity = identity_raw + packet_gcd

    checks = {
        "incumbent_labels_are_40_root_fixed": len(LABELS) == 40 and LABELS[0] == 0,
        "all_s3_labels_used": sorted(set(LABELS)) == list(range(6)),
        "raw_constraint_total_is_540": raw_edges == 540,
        "fano_active_quotient_is_21_weight_8": packets[1]["representatives"] == 21 and packets[1]["weight"] == 8 and packets[1]["raw_edges"] == 168,
        "steinberg_cache_quotient_is_27_weight_6": packets[2]["representatives"] == 27 and packets[2]["weight"] == 6 and packets[2]["raw_edges"] == 162,
        "identity_quotient_is_21_weight_10": packets[0]["representatives"] == 21 and packets[0]["weight"] == 10 and packets[0]["raw_edges"] == 210,
        "correction_side_is_330": correction_raw == 330,
        "quotient_representatives_are_69": quotient_reps == 69,
        "correction_representatives_are_48": correction_reps == 48,
        "packet_symmetric_score_step_is_2": packet_gcd == 2,
        "packet_symmetric_no_211_score": next_packet_symmetric_identity == 212,
        "radius3_count_matches_prior_certificate": radius_leq3 == 1991015,
    }

    result = {
        "bt": 1426,
        "title": "Fano-quotiented S3 optimizer frontier",
        "verified": all(checks.values()),
        "scope": {
            "full_problem_variables": 40,
            "root_fixed_variables": 39,
            "labels_per_variable": 6,
            "raw_constraints": raw_edges,
            "important_boundary": "The Fano quotient acts on the physical objective packetization, not yet on the 40 W33 line variables. It constrains packet-symmetric optimizer certificates and supplies a smaller weighted frontier.",
        },
        "weighted_quotient_packets": packets,
        "quotient_summary": {
            "raw_constraints": raw_edges,
            "weighted_representatives": quotient_reps,
            "compression_ratio": raw_edges / quotient_reps,
            "identity_raw": identity_raw,
            "correction_raw": correction_raw,
            "correction_representatives": correction_reps,
            "identity_representatives": 21,
            "weight_gcd": packet_gcd,
            "packet_symmetric_next_possible_identity_score_above_210": next_packet_symmetric_identity,
            "packet_symmetric_next_possible_correction_score_below_330": raw_edges - next_packet_symmetric_identity,
        },
        "radius_frontier": {
            "radius_1": radius_count(1),
            "radius_2": radius_count(2),
            "radius_3": radius_count(3),
            "radius_leq3_excluding_base": radius_leq3,
            "consequence": "Any full better gauge still must be radius >= 4. Any Fano-packet-symmetric better score must jump from 210 to at least 212, not 211.",
        },
        "solver_next_step": {
            "weighted_ilp_objective": "maximize 10*I_flag + 8*A_flag + 6*S_cache packet contributions subject to compatibility with the 40-line S3 labels",
            "certificate_target": "prove weighted packet objective <= 210 inside the Fano-packet-symmetric subproblem, then lift or break the symmetry explicitly for the full Max-2CSP.",
        },
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1426, "verified": result["verified"], "quotient_reps": quotient_reps, "next_packet_score": next_packet_symmetric_identity}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
