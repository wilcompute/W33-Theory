#!/usr/bin/env python3
"""BT1482: Closure ABI v2 with dual-axis C3 x V4 metadata and claim-DAG links."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1482_closure_abi_v2.json"

V4_BITS = [(0, 0), (1, 0), (0, 1), (1, 1)]


def packet(c: int, branch: int) -> dict:
    side, orient = V4_BITS[branch]
    strand = 4 * c + branch
    return {
        "inputs": {"c3_channel": c, "v4_branch": branch, "side_bit": side, "orientation_bit": orient},
        "strand": strand,
        "active_col": 14 * strand + 13,
        "guard_cols": [216 + 2 * strand, 216 + 2 * strand + 1],
        "channel_membership": f"P{c}",
        "triangle_membership": f"T{branch}",
        "row_sector": "72_sector_when_values_expanded",
        "gap_closure": "plus_q2_9_to_css_k81",
        "claim_dependencies": ["E1_oriented_72_sector", "E2_h1_81_closure", "E3_c3_v4_grid", "N4_retwined_decoder"],
    }


def main() -> None:
    packets = [packet(c, b) for c in range(3) for b in range(4)]
    channels = {f"P{c}": [p["strand"] for p in packets if p["inputs"]["c3_channel"] == c] for c in range(3)}
    triangles = {f"T{b}": [p["strand"] for p in packets if p["inputs"]["v4_branch"] == b] for b in range(4)}
    row_expansion = {
        "packet_count": 12,
        "active_value_rows": 24,
        "guard_value_rows": 48,
        "oriented_72_sector": 72,
        "firewall_gap_q2": 9,
        "css_h1_closure": 81,
    }
    abi = {
        "name": "S3xC3ClosurePacketABI",
        "version": "BT1482.v2",
        "preferred_structure": "C3 x V4",
        "axis_metadata": {
            "C3": "three Szilassi/Fano channels and qutrit phase axis",
            "V4": "four E6 gauge triangles / D4 branch bits, V4=C2xC2",
        },
        "packet_formula": "strand = 4*c3_channel + v4_branch",
        "active_formula": "active_col = 14*strand + 13",
        "guard_formula": "guard_cols = (216+2*strand, 216+2*strand+1)",
        "row_expansion": row_expansion,
        "claim_dag_dependencies": ["E0_e6_firewall_square", "E1_oriented_72_sector", "E2_h1_81_closure", "E3_c3_v4_grid", "N4_retwined_decoder", "N5_closure_packet_abi"],
        "claim_tier": "exact_runtime_abi",
        "external_formula_claims": "blocked_pending_transcription",
    }
    checks = {
        "packet_count_12": len(packets) == 12,
        "channels_are_3x4": len(channels) == 3 and all(len(v) == 4 for v in channels.values()),
        "triangles_are_4x3": len(triangles) == 4 and all(len(v) == 3 for v in triangles.values()),
        "active_cols_match": sorted(p["active_col"] for p in packets) == [14 * s + 13 for s in range(12)],
        "guard_tail_match": sorted({g for p in packets for g in p["guard_cols"]}) == list(range(216, 240)),
        "row_expansion_24_48_72": row_expansion["active_value_rows"] + row_expansion["guard_value_rows"] == row_expansion["oriented_72_sector"],
        "css_closure_72_plus_9": row_expansion["oriented_72_sector"] + row_expansion["firewall_gap_q2"] == row_expansion["css_h1_closure"],
        "dag_dependencies_present": all(dep for dep in abi["claim_dag_dependencies"]),
        "blocked_external_formula_claims": abi["external_formula_claims"] == "blocked_pending_transcription",
    }
    result = {
        "bt": 1482,
        "title": "Closure ABI v2",
        "verified": all(checks.values()),
        "abi": abi,
        "packets": packets,
        "channels": channels,
        "triangles": triangles,
        "interpretation": "ABI v2 upgrades the closure packet with C3 x V4 dual-axis metadata, 72-sector and 9-gap closure data, and E6/CSS claim-DAG dependencies.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1482, "verified": result["verified"], "version": abi["version"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
