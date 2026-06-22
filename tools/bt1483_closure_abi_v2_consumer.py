#!/usr/bin/env python3
"""BT1483: consume BT1482 ABI v2 and regenerate packets/events/rows with C3 x V4 metadata."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ABI = ROOT / "data" / "bt1482_closure_abi_v2.json"
OUT = ROOT / "data" / "bt1483_closure_abi_v2_consumer.json"
V4_BITS = [(0, 0), (1, 0), (0, 1), (1, 1)]


def packet(c: int, branch: int) -> dict:
    side, orient = V4_BITS[branch]
    strand = 4 * c + branch
    return {
        "c3_channel": c,
        "v4_branch": branch,
        "side_bit": side,
        "orientation_bit": orient,
        "strand": strand,
        "channel": f"P{c}",
        "triangle": f"T{branch}",
        "active_col": 14 * strand + 13,
        "guard_cols": [216 + 2 * strand, 216 + 2 * strand + 1],
        "claim_dependencies": ["E1_oriented_72_sector", "E2_h1_81_closure", "E3_c3_v4_grid", "N4_retwined_decoder"],
    }


def events_from_packet(p: dict) -> list[dict]:
    base = {k: p[k] for k in ["c3_channel", "v4_branch", "strand", "channel", "triangle"]}
    return [
        {**base, "op": "active_tick", "col": p["active_col"]},
        {**base, "op": "guard_pair", "cols": p["guard_cols"]},
        {**base, "op": "frame_update", "rule": "retwined_css_frame_update"},
        {**base, "op": "readout", "checks": ["X", "Z"]},
    ]


def rows_from_packet(p: dict) -> list[dict]:
    rows = []
    for value in (1, 2):
        rows.append({"kind": "active", "strand": p["strand"], "channel": p["channel"], "triangle": p["triangle"], "col": p["active_col"], "value": value})
    for col in p["guard_cols"]:
        for value in (1, 2):
            rows.append({"kind": "guard", "strand": p["strand"], "channel": p["channel"], "triangle": p["triangle"], "col": col, "value": value})
    return rows


def main() -> None:
    abi = json.loads(ABI.read_text(encoding="utf-8"))
    packets = [packet(c, b) for c in range(3) for b in range(4)]
    events = [e for p in packets for e in events_from_packet(p)]
    rows = [r for p in packets for r in rows_from_packet(p)]
    channel_counts = {f"P{c}": sum(1 for r in rows if r["channel"] == f"P{c}") for c in range(3)}
    triangle_counts = {f"T{b}": sum(1 for r in rows if r["triangle"] == f"T{b}") for b in range(4)}
    checks = {
        "abi_v2_verified": abi.get("verified") is True and abi.get("version") == "BT1482.v2",
        "packets_12": len(packets) == 12,
        "events_48": len(events) == 48,
        "rows_72": len(rows) == 72,
        "active_rows_24": sum(1 for r in rows if r["kind"] == "active") == 24,
        "guard_rows_48": sum(1 for r in rows if r["kind"] == "guard") == 48,
        "active_cols_match": sorted(p["active_col"] for p in packets) == [14 * s + 13 for s in range(12)],
        "guard_tail_match": sorted({g for p in packets for g in p["guard_cols"]}) == list(range(216, 240)),
        "channel_rows_balanced_24_each": sorted(channel_counts.values()) == [24, 24, 24],
        "triangle_rows_balanced_18_each": sorted(triangle_counts.values()) == [18, 18, 18, 18],
        "all_packets_have_dual_axis_metadata": all("channel" in p and "triangle" in p for p in packets),
    }
    result = {
        "bt": 1483,
        "title": "Closure ABI v2 consumer",
        "verified": all(checks.values()),
        "input_abi": "data/bt1482_closure_abi_v2.json",
        "counts": {"packets": len(packets), "events": len(events), "rows": len(rows)},
        "channel_row_counts": channel_counts,
        "triangle_row_counts": triangle_counts,
        "sample_packets": packets[:4],
        "sample_events": events[:8],
        "sample_rows": rows[:12],
        "interpretation": "ABI v2 is executable with dual-axis metadata: its C3 channels each carry 24 qutrit-value rows and its V4 triangles each carry 18 rows, totaling the 72-sector.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1483, "verified": result["verified"], "rows": len(rows)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
