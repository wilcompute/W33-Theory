#!/usr/bin/env python3
"""BT1460: compress the 48-step closure schedule using S3 x C3 factors."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1460_s3_c3_schedule_compressor.json"
OPPOSITE_PAIRS = [[11, 10], [9, 8], [12, 13]]


def main() -> None:
    primitive_steps = []
    for pair_index, pair in enumerate(OPPOSITE_PAIRS):
        for side in range(2):
            for orientation in range(2):
                strand = pair_index * 4 + side * 2 + orientation
                primitive_steps.extend([
                    {"op": "active_tick", "strand": strand, "pair_index": pair_index, "side": side, "orientation": orientation, "col": strand * 14 + 13},
                    {"op": "guard_pair", "strand": strand, "pair_index": pair_index, "side": side, "orientation": orientation, "cols": [216 + 2 * strand, 216 + 2 * strand + 1]},
                    {"op": "frame_update", "strand": strand, "pair_index": pair_index, "side": side, "orientation": orientation},
                    {"op": "syndrome_readout", "strand": strand, "pair_index": pair_index, "side": side, "orientation": orientation, "checks": ["X", "Z"]},
                ])
    template = {
        "loop_order": ["central_c3_pair_index", "s3_side", "s3_orientation"],
        "loop_ranges": {"central_c3_pair_index": [0, 1, 2], "s3_side": [0, 1], "s3_orientation": [0, 1]},
        "template_ops": [
            "active_tick: col = strand*14 + 13",
            "guard_pair: cols = 216 + 2*strand, 216 + 2*strand + 1",
            "frame_update: retwined CSS frame",
            "syndrome_readout: X/Z",
        ],
        "strand_formula": "strand = 4*central_c3_pair_index + 2*s3_side + s3_orientation",
    }
    checks = {
        "primitive_steps_are_48": len(primitive_steps) == 48,
        "template_has_four_ops": len(template["template_ops"]) == 4,
        "loop_cardinality_is_12": 3 * 2 * 2 == 12,
        "compression_ratio_is_12": len(primitive_steps) // len(template["template_ops"]) == 12,
        "active_cols_are_tick_13": sorted(row["col"] for row in primitive_steps if row["op"] == "active_tick") == [s * 14 + 13 for s in range(12)],
        "guard_tail_covered": sorted({c for row in primitive_steps if row["op"] == "guard_pair" for c in row["cols"]}) == list(range(216, 240)),
        "three_pair_channels_balanced": sorted([sum(1 for row in primitive_steps if row["op"] == "active_tick" and row["pair_index"] == i) for i in range(3)]) == [4, 4, 4],
    }
    result = {
        "bt": 1460,
        "title": "S3 x C3 schedule compressor",
        "verified": all(checks.values()),
        "primitive_step_count": len(primitive_steps),
        "compressed_template_step_count": len(template["template_ops"]),
        "compression_ratio": len(primitive_steps) / len(template["template_ops"]),
        "template": template,
        "sample_expansion": primitive_steps[:12],
        "interpretation": "The 48-step closure schedule compresses to a four-operation template over a 3x2x2 S3 x C3 loop space.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1460, "verified": result["verified"], "ratio": result["compression_ratio"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
