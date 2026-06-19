#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1327_q4_diamond_audit.json")
    ns = ap.parse_args()
    checks = {
        "q4_vertices_16": 2**4 == 16,
        "q4_edges_32": 4 * 2**3 == 32,
        "atlas_540": 120 * 9 // 2 == 540,
        "slots_2160": 540 * 4 == 2160,
        "marker_14641": 11**4 == 14641,
        "intersections_3240": 540 * 12 // 2 == 3240,
        "syndrome_bits_6480": 3240 * 2 == 6480,
        "independent_syndromes_1620": 6480 // 4 == 1620,
        "logical_per_revolution_268": 67 * 4 == 268,
        "spinor_modes_8": 2**3 == 8,
        "waveguide_channels_4320": 540 * 8 == 4320,
        "concat_modes_near_70p8m": 70_000_000 < 540 * 4 * 32**3 < 71_000_000,
        "epoch_lcm_10980": math.lcm(3660, 1620) == 10980,
    }
    values = {
        "q4_vertices": 16,
        "q4_edges": 32,
        "atlas_charts": 540,
        "slots": 2160,
        "marker_11_to_4": 14641,
        "intersections": 3240,
        "syndrome_bits": 6480,
        "independent_syndromes": 1620,
        "logical_per_revolution": 268,
        "spinor_modes": 8,
        "waveguide_channels": 4320,
        "concat_modes": 540 * 4 * 32**3,
        "literal_lcm_3660_1620": math.lcm(3660, 1620),
        "claimed_epoch": 10980,
    }
    failed = [k for k, ok in checks.items() if not ok]
    result = {"bt": 1327, "all_exact_checks_pass": not failed, "failed": failed, "checks": checks, "values": values}
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1327, "all_exact_checks_pass": not failed, "failed": failed}, indent=2))


if __name__ == "__main__":
    main()
