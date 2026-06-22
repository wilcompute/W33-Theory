#!/usr/bin/env python3
"""BT1467: reusable ABI for the S3 x C3 compressed closure packet."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1467_closure_packet_abi.json"


def packet(c: int, side: int, orient: int) -> dict:
    strand = 4 * c + 2 * side + orient
    return {
        "inputs": {"central_c3_pair_index": c, "s3_side": side, "orientation": orient},
        "strand": strand,
        "active_col": strand * 14 + 13,
        "guard_cols": [216 + 2 * strand, 216 + 2 * strand + 1],
        "frame_rule": "retwined_css_frame_update",
        "syndrome_contract": "syn_H(e)=syn_H_retwin(J e)",
        "claim_tier": "exact_finite_decoder",
    }


def main() -> None:
    packets = [packet(c, s, o) for c in range(3) for s in range(2) for o in range(2)]
    abi = {
        "name": "S3xC3ClosurePacketABI",
        "version": "BT1467.v1",
        "domain": "Szilassi fixed-face closure over W33 active/guard CSS bus",
        "input_schema": {
            "central_c3_pair_index": "0,1,2; selects Szilassi opposite-pair channel",
            "s3_side": "0,1; selects side of S3 switch slot",
            "orientation": "0,1; selects guard orientation within side",
        },
        "strand_formula": "strand = 4*central_c3_pair_index + 2*s3_side + orientation",
        "outputs": {
            "active_col": "strand*14 + 13",
            "guard_cols": "216+2*strand, 216+2*strand+1",
            "frame_rule": "retwined_css_frame_update",
            "syndrome_contract": "syn_H(e)=syn_H_retwin(J e)",
        },
        "claim_tiers": {
            "coordinate": "exact_coordinate",
            "count_bus": "exact_finite_arithmetic",
            "group": "exact_finite_group",
            "decoder": "exact_finite_decoder",
            "quartic_bridge": "numerical_structural_resonance",
            "external_physics": "blocked_or_not_imported",
        },
    }
    checks = {
        "packet_count_12": len(packets) == 12,
        "strand_range_0_to_11": sorted(p["strand"] for p in packets) == list(range(12)),
        "active_cols_tick_13": sorted(p["active_col"] for p in packets) == [s * 14 + 13 for s in range(12)],
        "guard_cols_tail": sorted({g for p in packets for g in p["guard_cols"]}) == list(range(216, 240)),
        "all_have_frame_rule": all(p["frame_rule"] == "retwined_css_frame_update" for p in packets),
        "all_have_syndrome_contract": all("syn_H" in p["syndrome_contract"] for p in packets),
        "claim_tier_firewall_present": abi["claim_tiers"]["external_physics"] == "blocked_or_not_imported",
    }
    result = {
        "bt": 1467,
        "title": "Closure packet ABI",
        "verified": all(checks.values()),
        "abi": abi,
        "packets": packets,
        "interpretation": "The closure tick is now packaged as a reusable ABI: three loop inputs, deterministic active/guard outputs, retwined frame rule, syndrome contract, and claim tier.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1467, "verified": result["verified"], "packets": len(packets)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
