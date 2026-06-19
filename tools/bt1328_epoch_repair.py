#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1328_epoch_repair.json")
    ns = ap.parse_args()
    ihara_frame = 3660
    charts = 540
    rolling_offset = ihara_frame % charts
    phase_closure_steps = charts // rolling_offset
    epoch = ihara_frame * phase_closure_steps
    checks = {
        "ihara_decomposition": ihara_frame == 6 * charts + rolling_offset,
        "offset_is_one_third_chart_cycle": rolling_offset * 3 == charts,
        "phase_closure_steps_3": phase_closure_steps == 3,
        "epoch_10980": epoch == 10980,
        "epoch_is_three_ihara_frames": epoch == 3 * ihara_frame,
        "literal_lcm_not_epoch": math.lcm(3660, 1620) != epoch,
    }
    result = {
        "bt": 1328,
        "title": "Rolling epoch repair",
        "verified": all(checks.values()),
        "checks": checks,
        "values": {
            "ihara_frame": ihara_frame,
            "charts": charts,
            "rolling_offset": rolling_offset,
            "phase_closure_steps": phase_closure_steps,
            "epoch": epoch,
            "literal_lcm_3660_1620": math.lcm(3660, 1620),
        },
        "correction": "10980 is verified as 3*3660 by rolling chart phase closure, not as lcm(3660,1620)."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1328, "verified": result["verified"], "epoch": epoch}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
