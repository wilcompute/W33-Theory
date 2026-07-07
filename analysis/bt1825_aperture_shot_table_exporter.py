#!/usr/bin/env python3
"""BT1825: raw aperture shot-table exporter.

Exports the full 1440-row center/phase/striation/aperture table induced by the
BT1815 Hesse aperture dictionary. This is the physical-readout skeleton for
future shot data; it contains expected labels, not observed outcomes.
"""
from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bt1807_defect_phase_plane_transversal_design as td43  # noqa: E402

CSV_OUT = Path("data/PART_BT1825_APERTURE_SHOT_TABLE.csv")
JSON_OUT = Path("data/PART_BT1825_APERTURE_SHOT_TABLE_summary.json")


def rows():
    pts, adj, lines = td43.build_w33()
    for center in range(40):
        table, _neighbors, _safe = td43.vector_table(center, pts, adj)
        groups = td43.star_lines(center, lines)
        group_id = {x: gi for gi, group in enumerate(groups) for x in group}
        for phase, row in enumerate(table):
            for aperture_point in row["quad"]:
                striation = group_id[aperture_point]
                yield {
                    "center": center,
                    "phase": phase,
                    "striation": striation,
                    "aperture_point": aperture_point,
                    "safe_triad": " ".join(map(str, row["triad"])),
                    "contextual_fraction_target": "0.1",
                    "observed_shots": "",
                    "observed_successes": "",
                }


def theorem_summary():
    rs = list(rows())
    assert len(rs) == 1440
    assert sorted(set(r["striation"] for r in rs)) == [0, 1, 2, 3]
    per_phase = {}
    for r in rs:
        per_phase.setdefault((r["center"], r["phase"]), set()).add(r["striation"])
    assert len(per_phase) == 360
    assert all(v == {0, 1, 2, 3} for v in per_phase.values())
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rs[0].keys()))
        writer.writeheader()
        writer.writerows(rs)
    summary = {
        "theorem": "BT1825 Raw Aperture Shot-Table Exporter",
        "rows": len(rs),
        "center_fibers": 40,
        "phase_rows_per_center": 9,
        "apertures_per_phase_row": 4,
        "csv": str(CSV_OUT),
        "checks": {
            "full_1440_rows_exported": True,
            "each_phase_row_has_four_striations": True,
            "target_contextual_fraction_label_present": True
        },
        "honest_scope": "Readout skeleton only. observed_shots and observed_successes are blank until a physical or simulated run fills them."
    }
    JSON_OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    summary = theorem_summary()
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
