#!/usr/bin/env python3
"""BT1875: integral E8 representative template.

Creates the first row schema for instantiating the BT1870 physical E8 model on
the four canonical selector pairs. Rows are intentionally placeholders until the
BT982 integral basis is wired to each support pair with chain-boundary data.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1875_INTEGRAL_E8_REPRESENTATIVE_TEMPLATE.json")

CANONICAL_SELECTOR = [[3, 68], [4, 42], [38, 65], [90, 144]]
PHASE_BITS = [0, 1]


def template_rows():
    rows = []
    for slot, pair in enumerate(CANONICAL_SELECTOR):
        for phase_bit in PHASE_BITS:
            rows.append({
                "selector_slot": slot,
                "support_pair": pair,
                "phase_coset_bit": phase_bit,
                "phase_class": "identity/W(A2)" if phase_bit == 0 else "central_inversion/O(A2)_mod_W(A2)",
                "integral_E8_vector_a": None,
                "integral_E8_vector_b": None,
                "A2_plane_id": slot,
                "A2_lattice_coordinates_a": None,
                "A2_lattice_coordinates_b": None,
                "Gram_value": None,
                "metric_score_contribution": None,
                "chain_boundary_compatibility": "pending_integral_vector_model",
                "source_basis_candidate": "analysis/bt982_explicit_integral_e8_basis.py",
                "status": "template_pending_instantiation"
            })
    return rows


def theorem_summary():
    rows = template_rows()
    checks = {
        "four_selector_pairs": len(CANONICAL_SELECTOR) == 4,
        "two_phase_rows_per_pair": len(rows) == 8,
        "bt1870_required_integral_fields_present": all("integral_E8_vector_a" in r and "integral_E8_vector_b" in r for r in rows),
        "chain_boundary_pending_recorded": all(r["chain_boundary_compatibility"] == "pending_integral_vector_model" for r in rows),
        "bt982_candidate_basis_linked": all(r["source_basis_candidate"].endswith("bt982_explicit_integral_e8_basis.py") for r in rows),
    }
    return {
        "theorem": "BT1875 Integral E8 Representative Template",
        "row_count": len(rows),
        "canonical_selector": CANONICAL_SELECTOR,
        "phase_bits": PHASE_BITS,
        "rows": rows,
        "next_instantiation_source": "analysis/bt982_explicit_integral_e8_basis.py",
        "checks": checks,
        "all_pass": all(checks.values()),
        "honest_scope": "Template only. Integral E8 vectors and chain-boundary compatibility remain unfilled until BT982 is wired into the selector-pair model."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
