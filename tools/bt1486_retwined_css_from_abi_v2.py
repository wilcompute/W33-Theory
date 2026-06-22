#!/usr/bin/env python3
"""BT1486: rerun the retwined CSS join from ABI v2 rows.

BT1471 proved that the older closure packets feed the retwined W33 CSS frame.
BT1483 then upgraded the ABI to a C3 x V4 row layer.  This verifier repeats the
CSS join from the ABI v2 packet coordinates, preserving both axes:

    C3 channels P0,P1,P2 -> 24 rows each
    V4 triangles T0,T1,T2,T3 -> 18 rows each

Every active/guard value row is checked against the original and retwined CSS
syndromes.  The retwining rule is still the BT1425 guard-tail permutation.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from bt1425_retwined_css_frame_correction import (  # noqa: E402
    build_w33,
    dense_hx,
    dense_hz,
    gf_rank,
    guard_shear_perm,
    permute_columns,
    permute_vector,
    syndrome,
)

OUT = ROOT / "data" / "bt1486_retwined_css_from_abi_v2.json"


def load_json(relpath: str) -> dict:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def one_hot(col: int, value: int, n: int = 240) -> list[int]:
    vec = [0] * n
    vec[col] = value % 3
    return vec


def rows_from_abi_v2_packet(packet: dict) -> list[dict]:
    inputs = packet["inputs"]
    base = {
        "strand": packet["strand"],
        "c3_channel": inputs["c3_channel"],
        "v4_branch": inputs["v4_branch"],
        "channel": packet["channel_membership"],
        "triangle": packet["triangle_membership"],
    }
    rows: list[dict] = []
    for value in (1, 2):
        rows.append(
            {
                **base,
                "kind": "active",
                "col": packet["active_col"],
                "value": value,
            }
        )
    for col in packet["guard_cols"]:
        for value in (1, 2):
            rows.append({**base, "kind": "guard", "col": col, "value": value})
    return rows


def abi_v2_packets() -> list[dict]:
    packets = []
    for c3_channel in range(3):
        for v4_branch in range(4):
            side_bit, orientation_bit = ((0, 0), (1, 0), (0, 1), (1, 1))[v4_branch]
            strand = 4 * c3_channel + v4_branch
            packets.append(
                {
                    "inputs": {
                        "c3_channel": c3_channel,
                        "v4_branch": v4_branch,
                        "side_bit": side_bit,
                        "orientation_bit": orientation_bit,
                    },
                    "strand": strand,
                    "active_col": 14 * strand + 13,
                    "guard_cols": [216 + 2 * strand, 216 + 2 * strand + 1],
                    "channel_membership": f"P{c3_channel}",
                    "triangle_membership": f"T{v4_branch}",
                }
            )
    return packets


def main() -> None:
    abi_v2 = load_json("data/bt1482_closure_abi_v2.json")
    consumer = load_json("data/bt1483_closure_abi_v2_consumer.json")
    bt1425 = load_json("data/bt1425_retwined_css_frame_correction.json")

    points, edges, triangles = build_w33()
    hx = dense_hx(edges)
    hz = dense_hz(edges, triangles)
    perm = guard_shear_perm()
    hx_r = permute_columns(hx, perm)
    hz_r = permute_columns(hz, perm)

    packets = abi_v2_packets()
    rows = [row for packet in packets for row in rows_from_abi_v2_packet(packet)]
    row_checks = []
    for row in rows:
        vec = one_hot(row["col"], row["value"])
        retwined = permute_vector(vec, perm)
        moved_col = retwined.index(row["value"])
        row_checks.append(
            {
                **row,
                "retwined_col": moved_col,
                "moved": moved_col != row["col"],
                "x_ok": syndrome(hx, vec) == syndrome(hx_r, retwined),
                "z_ok": syndrome(hz, vec) == syndrome(hz_r, retwined),
            }
        )

    channel_counts = Counter(row["channel"] for row in row_checks)
    triangle_counts = Counter(row["triangle"] for row in row_checks)
    active_channel_counts = Counter(
        row["channel"] for row in row_checks if row["kind"] == "active"
    )
    guard_channel_counts = Counter(
        row["channel"] for row in row_checks if row["kind"] == "guard"
    )
    active_triangle_counts = Counter(
        row["triangle"] for row in row_checks if row["kind"] == "active"
    )
    guard_triangle_counts = Counter(
        row["triangle"] for row in row_checks if row["kind"] == "guard"
    )

    moved_guard_value_rows = [
        row for row in row_checks if row["kind"] == "guard" and row["moved"]
    ]
    checks = {
        "abi_v2_verified": abi_v2["verified"] is True
        and abi_v2["preferred_structure"] == "C3 x V4"
        and abi_v2["row_expansion"]["packet_count"] == len(packets),
        "bt1483_consumer_verified": consumer["verified"] is True,
        "bt1425_retwined_rule_verified": bt1425["verified"] is True,
        "css_ranks_match_w33": gf_rank(hx) == 39
        and gf_rank(hz) == 120
        and 240 - gf_rank(hx) - gf_rank(hz) == 81,
        "row_count_matches_bt1483": len(row_checks) == consumer["counts"]["rows"] == 72,
        "active_guard_split_matches_bt1483": sum(
            1 for row in row_checks if row["kind"] == "active"
        )
        == 24
        and sum(1 for row in row_checks if row["kind"] == "guard") == 48,
        "channel_rows_balanced_24_each": dict(sorted(channel_counts.items()))
        == consumer["channel_row_counts"]
        == {"P0": 24, "P1": 24, "P2": 24},
        "triangle_rows_balanced_18_each": dict(sorted(triangle_counts.items()))
        == consumer["triangle_row_counts"]
        == {"T0": 18, "T1": 18, "T2": 18, "T3": 18},
        "active_channel_rows_are_8_each": dict(sorted(active_channel_counts.items()))
        == {"P0": 8, "P1": 8, "P2": 8},
        "guard_channel_rows_are_16_each": dict(sorted(guard_channel_counts.items()))
        == {"P0": 16, "P1": 16, "P2": 16},
        "active_triangle_rows_are_6_each": dict(sorted(active_triangle_counts.items()))
        == {"T0": 6, "T1": 6, "T2": 6, "T3": 6},
        "guard_triangle_rows_are_12_each": dict(sorted(guard_triangle_counts.items()))
        == {"T0": 12, "T1": 12, "T2": 12, "T3": 12},
        "active_cols_fixed_by_retwine": all(
            not row["moved"] for row in row_checks if row["kind"] == "active"
        ),
        "moved_guard_value_rows_are_24": len(moved_guard_value_rows) == 24,
        "x_syndromes_equivariant": all(row["x_ok"] for row in row_checks),
        "z_syndromes_equivariant": all(row["z_ok"] for row in row_checks),
    }

    result = {
        "bt": 1486,
        "title": "Retwined CSS join from ABI v2",
        "verified": all(checks.values()),
        "source_packets": {
            "abi": "data/bt1482_closure_abi_v2.json",
            "consumer": "data/bt1483_closure_abi_v2_consumer.json",
            "retwined_rule": "data/bt1425_retwined_css_frame_correction.json",
        },
        "counts": {
            "rows": len(row_checks),
            "active_rows": sum(1 for row in row_checks if row["kind"] == "active"),
            "guard_rows": sum(1 for row in row_checks if row["kind"] == "guard"),
            "moved_guard_value_rows": len(moved_guard_value_rows),
        },
        "css": {
            "rank_hx": gf_rank(hx),
            "rank_hz": gf_rank(hz),
            "k": 240 - gf_rank(hx) - gf_rank(hz),
            "retwined_rule": "BT1425 guard-tail permutation on both HX and HZ",
        },
        "axis_profiles": {
            "channel_rows": dict(sorted(channel_counts.items())),
            "triangle_rows": dict(sorted(triangle_counts.items())),
            "active_channel_rows": dict(sorted(active_channel_counts.items())),
            "guard_channel_rows": dict(sorted(guard_channel_counts.items())),
            "active_triangle_rows": dict(sorted(active_triangle_counts.items())),
            "guard_triangle_rows": dict(sorted(guard_triangle_counts.items())),
        },
        "row_checks_sample": row_checks[:12],
        "moved_guard_rows_sample": moved_guard_value_rows[:12],
        "interpretation": (
            "ABI v2 is now joined to the retwined CSS frame, not merely counted. "
            "Every C3 x V4 row preserves X and Z syndromes under the BT1425 "
            "frame update; the channel and triangle axes survive to the CSS layer."
        ),
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {"bt": 1486, "verified": result["verified"], "rows": len(row_checks)},
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
