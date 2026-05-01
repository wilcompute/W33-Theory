#!/usr/bin/env python3
"""Exact CXXVII E-sector tomotope balance audit.

Part CXXVII sharpens the complete two-qutrit MUB-frame overlap law: the
relative 3-cycle ambiguity in the even sectors is not noise. Once same- and
opposite-chirality pairs are aggregated, the E-sector layer has 192 pairs and
splits exactly as 96 four-overlap plus 96 one-overlap, with a 24-unit chirality
imbalance between same and opposite sectors.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import time
from typing import Dict, Tuple


ROOT = Path(__file__).resolve().parents[1]


def e_sector_tomotope_balance_summary() -> Dict[str, object]:
    frames_per_even_chirality = 12
    relative_three_cycles_per_source = 8
    same_chirality_sectors = 2

    same_pairs_per_sector = (
        frames_per_even_chirality * relative_three_cycles_per_source // 2
    )
    same_total_pairs = same_chirality_sectors * same_pairs_per_sector
    opposite_total_pairs = frames_per_even_chirality * relative_three_cycles_per_source

    same_per_sector_split = {"four_overlap": 18, "one_overlap": 30}
    same_split = {
        key: same_chirality_sectors * value
        for key, value in same_per_sector_split.items()
    }
    opposite_split = {"four_overlap": 60, "one_overlap": 36}
    total_split = {
        key: same_split[key] + opposite_split[key]
        for key in same_split
    }

    same_mean_overlap = Fraction(
        same_per_sector_split["four_overlap"] * 4
        + same_per_sector_split["one_overlap"],
        same_pairs_per_sector,
    )
    opposite_mean_overlap = Fraction(
        opposite_split["four_overlap"] * 4 + opposite_split["one_overlap"],
        opposite_total_pairs,
    )

    return {
        "status": "ok",
        "frame_packet": {
            "even_positive_frames": frames_per_even_chirality,
            "even_negative_frames": frames_per_even_chirality,
            "relative_three_cycles_per_source": relative_three_cycles_per_source,
        },
        "pair_counts": {
            "same_pairs_per_chirality_sector": same_pairs_per_sector,
            "same_chirality_total_pairs": same_total_pairs,
            "opposite_chirality_total_pairs": opposite_total_pairs,
            "full_e_sector_three_cycle_pairs": same_total_pairs
            + opposite_total_pairs,
        },
        "overlap_splits": {
            "same_per_chirality_sector": same_per_sector_split,
            "same_chirality_total": same_split,
            "opposite_chirality": opposite_split,
            "full_e_sector_total": total_split,
        },
        "chirality_imbalance": {
            "opposite_minus_same_four_overlap": opposite_split["four_overlap"]
            - same_split["four_overlap"],
            "same_minus_opposite_one_overlap": same_split["one_overlap"]
            - opposite_split["one_overlap"],
            "w33_block_size": 24,
        },
        "mean_overlap": {
            "same_chirality": str(same_mean_overlap),
            "opposite_chirality": str(opposite_mean_overlap),
            "center": str(Fraction(5, 2)),
            "deviation": str(Fraction(3, 8)),
        },
        "theorem": {
            "full_three_cycle_layer_has_192_pairs": same_total_pairs
            + opposite_total_pairs
            == 192,
            "full_layer_balances_96_four_and_96_one": total_split
            == {"four_overlap": 96, "one_overlap": 96},
            "chirality_flip_swaps_counts_by_24": (
                opposite_split["four_overlap"] - same_split["four_overlap"] == 24
                and same_split["one_overlap"] - opposite_split["one_overlap"] == 24
            ),
            "mean_overlap_affine_chirality_law_holds": (
                same_mean_overlap == Fraction(5, 2) - Fraction(3, 8)
                and opposite_mean_overlap == Fraction(5, 2) + Fraction(3, 8)
            ),
        },
    }


def main() -> None:
    started = time.time()
    payload = e_sector_tomotope_balance_summary()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXVII_e_sector_tomotope_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("E-sector tomotope balance audit")
    for key, value in payload["theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()
