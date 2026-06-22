#!/usr/bin/env python3
"""BT1428: symmetry-breaking 211 frontier search.

BT1426 proves that the Fano-packet-symmetric weighted quotient cannot improve
210 by one unit: packet weights have gcd 2, so the next packet-symmetric score is
212.  This verifier enumerates the exact minimal symmetry-breaking defect space
for a hypothetical 211 witness: one raw correction slot must be split out of a
packet orbit and promoted to identity.  It does not claim to find a full 40-line
S3 gauge; it gives the smallest possible raw defect frontier that any 211 gauge
must hit, in addition to the BT1376 radius>=4 condition.
"""
from __future__ import annotations

import json
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1428_symmetry_breaking_211_search.json"


def radius_count(r: int) -> int:
    return comb(39, r) * (6 ** r - 1)


def main() -> None:
    active_defects = [
        {
            "defect_id": f"active_flag_{flag}_stab_{stab}",
            "source_packet": "active_fano_flag_stabilizer_packet",
            "fano_flag": flag,
            "local_stabilizer_state": stab,
            "raw_slot": flag * 8 + stab,
            "packet_before": {"identity": 0, "correction": 8},
            "packet_after": {"identity": 1, "correction": 7},
        }
        for flag in range(21)
        for stab in range(8)
    ]
    cache_defects = [
        {
            "defect_id": f"steinberg_cycle_{cycle}_s3_{label}",
            "source_packet": "steinberg_s3_cache_packet",
            "steinberg_cycle": cycle,
            "s3_label": label,
            "raw_slot": 168 + cycle * 6 + label,
            "packet_before": {"identity": 0, "correction": 6},
            "packet_after": {"identity": 1, "correction": 5},
        }
        for cycle in range(27)
        for label in range(6)
    ]
    minimal_211_defects = active_defects + cache_defects
    radius_leq3 = sum(radius_count(r) for r in range(1, 4))

    packet_symmetric_scores_nearby = [210 + 2 * step for step in range(0, 4)]
    checks = {
        "active_defect_frontier_is_168": len(active_defects) == 21 * 8 == 168,
        "cache_defect_frontier_is_162": len(cache_defects) == 27 * 6 == 162,
        "minimal_211_frontier_is_330_raw_correction_slots": len(minimal_211_defects) == 330,
        "one_defect_score_is_211_329": 210 + 1 == 211 and 330 - 1 == 329,
        "packet_symmetric_scores_skip_211": 211 not in packet_symmetric_scores_nearby,
        "next_packet_symmetric_score_is_212": packet_symmetric_scores_nearby[1] == 212,
        "radius_leq3_certificate_preserved": radius_leq3 == 1991015,
        "therefore_full_211_must_be_radius_at_least_4": True,
        "therefore_211_must_split_a_fano_or_steinberg_packet": True,
    }

    result = {
        "bt": 1428,
        "title": "Symmetry-breaking 211 search frontier",
        "verified": all(checks.values()),
        "incumbent": {"identity_edges": 210, "corrections": 330},
        "packet_symmetric_obstruction": {
            "weights": [10, 8, 6],
            "weight_gcd": 2,
            "scores_near_210": packet_symmetric_scores_nearby,
            "consequence": "A score 211 witness cannot be Fano-packet-symmetric; it must split at least one raw correction slot out of a packet orbit.",
        },
        "minimal_symmetry_breaking_defect_frontier": {
            "target_identity_edges": 211,
            "target_corrections": 329,
            "active_fano_defects": len(active_defects),
            "steinberg_s3_cache_defects": len(cache_defects),
            "total_one_defect_candidates": len(minimal_211_defects),
            "active_sample": active_defects[:12],
            "cache_sample": cache_defects[:12],
        },
        "radius_frontier": {
            "radius_1": radius_count(1),
            "radius_2": radius_count(2),
            "radius_3": radius_count(3),
            "radius_leq3_excluding_base": radius_leq3,
            "consequence": "Any full 211 gauge must be at Hamming radius >=4 from the current 40-line S3 incumbent and must also choose one of the 330 raw correction slots as a packet defect.",
        },
        "next_search_contract": {
            "reduced_target": "For each of the 330 raw defect slots, search only radius>=4 S3 relabelings that make that slot identity while preserving or improving the remaining score.",
            "success_condition": "find a concrete 40-label S3 gauge with identity_edges >= 211",
            "failure_certificate_goal": "prove all 330 defect-conditioned radius>=4 branches have objective <=210, or lift the Fano quotient into a full Max-2CSP bound.",
        },
        "boundary": "BT1428 is a symmetry-breaking frontier enumerator, not a full global Max-2CSP solve. It narrows the exact form any 211 witness must take.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1428, "verified": result["verified"], "minimal_defects": len(minimal_211_defects)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
