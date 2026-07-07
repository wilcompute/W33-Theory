#!/usr/bin/env python3
"""BT1847: shot protocol compression by center/phase symmetry.

Compresses the 1440-row BT1843 protocol into 360 balanced measurement bundles.
Each bundle is one center/phase row containing four striation detector settings.
The compressed protocol preserves full center/phase/striation coverage while
making the run plan easier to schedule.
"""
from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bt1843_aperture_to_shot_protocol as proto  # noqa: E402

CSV_OUT = Path("data/PART_BT1847_SHOT_PROTOCOL_COMPRESSION.csv")
JSON_OUT = Path("data/PART_BT1847_SHOT_PROTOCOL_COMPRESSION_summary.json")


def compressed_rows():
    rows = list(proto.protocol_rows())
    bundles = {}
    for r in rows:
        key = (int(r["center"]), int(r["phase"]))
        bundles.setdefault(key, []).append(r)
    for (center, phase), rs in sorted(bundles.items()):
        assert len(rs) == 4
        striations = sorted(int(r["striation"]) for r in rs)
        assert striations == [0, 1, 2, 3]
        yield {
            "center": center,
            "phase": phase,
            "bundle_id": f"C{center:02d}_P{phase:02d}",
            "detector_channels": " ".join(sorted(r["detector_channel"] for r in rs)),
            "measurement_settings": " ".join(sorted(r["measurement_setting"] for r in rs)),
            "e8_selector_pairs": " | ".join(f"{r['e8_selector_pair_a']}-{r['e8_selector_pair_b']}" for r in sorted(rs, key=lambda x: int(x["striation"]))),
            "shot_budget_total": sum(int(r["shot_budget"]) for r in rs),
            "observed_bundle_counts": "",
            "analysis_status": "pending_data"
        }


def theorem_summary():
    rs = list(compressed_rows())
    assert len(rs) == 360
    assert sum(int(r["shot_budget_total"]) for r in rs) == 144000
    centers = sorted(set(int(r["center"]) for r in rs))
    assert centers == list(range(40))
    per_center = {}
    for r in rs:
        per_center[int(r["center"])] = per_center.get(int(r["center"]), 0) + 1
    assert set(per_center.values()) == {9}
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rs[0].keys()))
        writer.writeheader()
        writer.writerows(rs)
    summary = {
        "theorem": "BT1847 Shot Protocol Compression",
        "uncompressed_rows": 1440,
        "compressed_bundles": len(rs),
        "compression_factor": 4,
        "total_nominal_shots_preserved": 144000,
        "bundles_per_center": 9,
        "csv": str(CSV_OUT),
        "checks": {
            "compressed_to_360_bundles": True,
            "full_center_coverage": True,
            "four_striations_per_bundle": True,
            "shot_budget_preserved": True,
            "observed_columns_blank_until_data": True
        },
        "honest_scope": "Scheduling compression only. It preserves coverage but is not measured data."
    }
    JSON_OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    summary = theorem_summary()
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
