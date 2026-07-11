#!/usr/bin/env python3
"""Aggregate certificate for the five v5 architecture closures."""
from __future__ import annotations
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
NAMES = ["fourier", "extension", "lanes", "hybrid", "hardware"]


def analyze() -> dict:
    results = {}
    for name in NAMES:
        path = ROOT / f"data/PART_2026_07_11_LEVI_NEXT5_V5_{name}.json"
        results[name] = json.loads(path.read_text(encoding="utf-8"))
    checks = {name: result.get("status") == "PASS" for name, result in results.items()}
    return {
        "schema": "w33.levi_next5_v5.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "results": {
            "fourier": {
                "q3_local_ranks": {"point": results["fourier"]["heisenberg_q3"]["point_block_rank"], "incidence": results["fourier"]["heisenberg_q3"]["incidence_column_span_dimension"], "line_gram": results["fourier"]["heisenberg_q3"]["line_gram_diagonal_rank"]},
                "w33_ranks": {"incidence": results["fourier"]["full_w33"]["incidence_rank"], "point_gram": results["fourier"]["full_w33"]["point_gram_rank"], "line_gram": results["fourier"]["full_w33"]["line_gram_rank"]},
                "jordan": results["fourier"]["full_w33"]["jordan_blocks"],
            },
            "extension": {
                "H1_dimension": results["extension"]["periodic_cohomology"]["H1_dimension"],
                "H2_dimension": results["extension"]["periodic_cohomology"]["H2_dimension"],
                "H2_classes": len(results["extension"]["H2_extensions"]),
                "transgression": results["extension"]["transgression"]["delta_class"],
                "fixed_order8_gauge": results["extension"]["transgression"]["minimal_gauge_mask"],
            },
            "lanes": {
                "decomposition": results["lanes"]["decomposition"]["orbit_sizes"],
                "payload_addresses": results["lanes"]["routing"]["payload_addresses"],
                "falsifier_steps": results["lanes"]["falsifier"]["steps"],
            },
            "hybrid": {
                "power_mw": results["hybrid"]["power_budget"]["total_mw"],
                "die_p05": results["hybrid"]["foundry_corners"]["p05"],
                "tracked_min": results["hybrid"]["drift"]["tracked_min"],
                "gds_sha256": results["hybrid"]["layout"]["gds_sha256"],
            },
            "hardware": {
                "events": results["hardware"]["fpga"]["input_events"],
                "frames": results["hardware"]["fpga"]["frames"],
                "route_digest": results["hardware"]["runtime_replay"]["route_digest"],
            },
        },
        "synthesis": "Native q=3 Fourier geometry, the periodic H2 extension/transgression, typed E8 carrier lanes, a sub-100 mW hybrid photonic controller, and vendor-normalized FPGA time-tag replay now form one executable v5 stack.",
    }


def main() -> int:
    out = analyze(); print(json.dumps(out, indent=2, sort_keys=True)); return 0 if out["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
