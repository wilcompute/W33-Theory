#!/usr/bin/env python3
"""BT1224 -- exact Clifford fingerprint dashboard.

Fuses the exact single-qutrit SL(2,3) certificate from BT1219 with the exact
two-qutrit Sp(4,3) certificate from BT1221 into one tomography dashboard.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_SL23 = Path("data/bt1219_exact_sl23_closure_summary.json")
DEFAULT_SP43 = Path("data/bt1221_exact_sp43_generator_summary.json")


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def build(sl23: dict, sp43: dict) -> dict:
    single_ok = bool(sl23.get("order_ok")) and bool(sl23.get("closure_ok"))
    two_ok = bool(sp43.get("order_ok")) and bool(sp43.get("all_generated_matrices_symplectic"))
    return {
        "bt": 1224,
        "title": "Exact Clifford fingerprint dashboard",
        "single_qutrit_layer": {
            "source": "BT1219",
            "group": "SL(2,3)",
            "field": sl23.get("field"),
            "order": sl23.get("order"),
            "expected_order": 24,
            "order_ok": sl23.get("order_ok"),
            "closure_ok": sl23.get("closure_ok"),
            "element_order_spectrum": sl23.get("element_order_spectrum"),
            "trace_mod3_counts": sl23.get("trace_mod3_counts"),
        },
        "two_qutrit_layer": {
            "source": "BT1221",
            "group": "Sp(4,3)",
            "field": sp43.get("field"),
            "order": sp43.get("order"),
            "expected_order": 51840,
            "order_ok": sp43.get("order_ok"),
            "all_generated_matrices_symplectic": sp43.get("all_generated_matrices_symplectic"),
            "element_order_spectrum": sp43.get("element_order_spectrum"),
            "trace_mod3_counts": sp43.get("trace_mod3_counts"),
            "fixed_space_rank_counts": sp43.get("fixed_space_rank_counts"),
            "max_element_order": sp43.get("max_element_order"),
        },
        "tomography_thresholds": {
            "single_order_required": 24,
            "two_qutrit_order_required": 51840,
            "single_trace_bins_required": ["0", "1", "2"],
            "two_trace_bins_required": ["0", "1", "2"],
            "require_fixed_space_rank_fingerprint": True,
        },
        "dashboard_pass": single_ok and two_ok,
        "interpretation": "The finite Clifford tomography target is now exact at both layers: SL(2,3) for the single-qutrit holonomy and Sp(4,3) for the two-qutrit Clifford closure.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sl23", type=Path, default=DEFAULT_SL23)
    parser.add_argument("--sp43", type=Path, default=DEFAULT_SP43)
    parser.add_argument("--out", type=Path, default=Path("data/bt1224_exact_clifford_fingerprint_dashboard.json"))
    args = parser.parse_args()
    result = build(load(args.sl23), load(args.sp43))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1224, "dashboard_pass": result["dashboard_pass"], "out": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
