#!/usr/bin/env python3
"""Aggregate certificate for the five v5 architecture closures."""
from __future__ import annotations
from pathlib import Path
import importlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
NAMES = ["fourier", "extension", "lanes", "hybrid", "hardware"]
OUT = ROOT / "data" / "PART_2026_07_11_LEVI_NEXT5_V5_results.json"


def json_normalized(value):
    """Compare witness objects exactly as committed JSON (tuples become arrays)."""
    return json.loads(json.dumps(value, sort_keys=True))


def analyze() -> dict:
    cached = {}
    results = {}
    fresh_matches_cached = {}
    for name in NAMES:
        path = ROOT / f"data/PART_2026_07_11_LEVI_NEXT5_V5_{name}.json"
        cached[name] = json.loads(path.read_text(encoding="utf-8"))
        module = importlib.import_module(f"w33_levi_next5_v5_{name}")
        results[name] = module.analyze()
        fresh_matches_cached[name] = json_normalized(results[name]) == cached[name]
    checks = {
        name: result.get("status") == "PASS" and fresh_matches_cached[name]
        for name, result in results.items()
    }
    return {
        "schema": "w33.levi_next5_v5.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "results": {
            "fourier": {
                "q3_matrix_dimensions": {
                    "symmetric": results["fourier"]["symmetric_matrix_q3"]["symmetric_dimension"],
                    "alternating": results["fourier"]["symmetric_matrix_q3"]["alternating_dimension"],
                    "diagonal_map_rank": results["fourier"]["symmetric_matrix_q3"]["diagonal_map_rank"],
                },
                "w33_ranks": {"incidence": results["fourier"]["full_w33"]["incidence_rank"], "point_gram": results["fourier"]["full_w33"]["point_gram_rank"], "line_gram": results["fourier"]["full_w33"]["line_gram_rank"]},
                "jordan": results["fourier"]["full_w33"]["jordan_blocks"],
            },
            "extension": {
                "H1_dimension": results["extension"]["periodic_cohomology"]["H1_dimension"],
                "H2_dimension": results["extension"]["periodic_cohomology"]["H2_dimension"],
                "H2_classes": len(results["extension"]["H2_extension_classes_prescribed_action"]),
                "transgression": results["extension"]["transgression"]["delta_class"],
                "fixed_order8_gauge": results["extension"]["transgression"]["minimal_gauge_mask"],
            },
            "lanes": {
                "decomposition": results["lanes"]["decomposition"]["orbit_sizes"],
                "payload_addresses": results["lanes"]["routing"]["payload_addresses"],
                "seeded_replay_smoke_steps": results["lanes"]["seeded_replay_smoke"]["steps"],
            },
            "hybrid": {
                "power_mw": results["hybrid"]["power_budget"]["total_mw"],
                "synthetic_phase_p05": results["hybrid"]["synthetic_phase_corners"]["p05"],
                "tracked_min": results["hybrid"]["drift"]["tracked_min"],
                "phase_word_range": [results["hybrid"]["compiler"]["command_word_min"],results["hybrid"]["compiler"]["command_word_max"]],
                "layout_kind": results["hybrid"]["layout"]["kind"],
                "gds_sha256": results["hybrid"]["layout"]["gds_sha256"],
            },
            "hardware": {
                "reference_events": results["hardware"]["reference_reducer"]["input_events"],
                "reference_frames": results["hardware"]["reference_reducer"]["frames"],
                "w33_points_covered": results["hardware"]["runtime_replay"]["w33_points_covered"],
                "payload_addresses_covered": results["hardware"]["runtime_replay"]["payload_addresses_covered"],
                "rtl_scope": results["hardware"]["rtl"]["execution"],
                "route_digest": results["hardware"]["runtime_replay"]["route_digest"],
            },
        },
        "fresh_matches_cached": fresh_matches_cached,
        "execution": "all five witness analyze() functions regenerated in this process before cache comparison",
        "synthesis": "The exact q=3 matrix-space and separate W33 rank censuses, prescribed-action H2 classes, and typed E8 witnesses are joined to a sub-100 mW architectural phase model, a record-valid placement-sketch GDS, documentation-shaped vendor adapters, a million-event Python reference replay, and an independently smoke-simulated two-frame RTL reducer. No Fourier-incidence bridge, fabricated device, PDK closure, or million-event FPGA run is claimed.",
    }


def main() -> int:
    out = analyze()
    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if out["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
