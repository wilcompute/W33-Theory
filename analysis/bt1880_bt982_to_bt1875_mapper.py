#!/usr/bin/env python3
"""BT1880: BT982-to-BT1875 mapper.

Populates the BT1875 selector-pair/phase template with candidate integral E8
vectors from BT982's final_integral_basis_B when the materialized BT982 JSON is
available. If that JSON has not yet been generated, this script falls back to a
clearly labeled standard-coordinate proxy basis so downstream schemas remain
executable without pretending the BT982 artifact has been materialized.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_BT1880_BT982_TO_BT1875_MAPPED_TEMPLATE.json"
SUMMARY_OUT = ROOT / "data/PART_BT1880_BT982_TO_BT1875_MAPPER_summary.json"

CANONICAL_SELECTOR = [[3, 68], [4, 42], [38, 65], [90, 144]]
PHASE_CLASSES = {0: "identity/W(A2)", 1: "central_inversion/O(A2)_mod_W(A2)"}
BT982_PATH = ROOT / "data/bt982_explicit_integral_e8_basis.json"


def proxy_basis():
    return [[1 if i == j else 0 for i in range(8)] for j in range(8)]


def load_bt982_basis():
    if BT982_PATH.exists():
        data = json.loads(BT982_PATH.read_text(encoding="utf-8"))
        B = data["final_integral_basis_B"]
        cols = [[B[r][c] for r in range(len(B))] for c in range(len(B[0]))]
        data["materialized_bt982_json_present"] = True
        return data, cols
    data = {
        "status": "proxy_basis_pending_materialized_BT982_json",
        "materialized_bt982_json_present": False,
        "honest_boundary": "analysis/bt982_explicit_integral_e8_basis.py exists, but data/bt982_explicit_integral_e8_basis.json is not materialized in this connector pass"
    }
    return data, proxy_basis()


def mapped_rows():
    bt982, cols = load_bt982_basis()
    rows = []
    for slot, pair in enumerate(CANONICAL_SELECTOR):
        a_col = 2 * slot
        b_col = 2 * slot + 1
        for phase_bit in (0, 1):
            rows.append({
                "selector_slot": slot,
                "support_pair": pair,
                "phase_coset_bit": phase_bit,
                "phase_class": PHASE_CLASSES[phase_bit],
                "integral_E8_vector_a": cols[a_col],
                "integral_E8_vector_b": cols[b_col],
                "BT982_basis_column_a": a_col,
                "BT982_basis_column_b": b_col,
                "A2_plane_id": slot,
                "A2_lattice_coordinates_a": None,
                "A2_lattice_coordinates_b": None,
                "Gram_value": None,
                "metric_score_contribution": None,
                "chain_boundary_compatibility": "pending_BT1881_test",
                "source_basis_candidate": "analysis/bt982_explicit_integral_e8_basis.py",
                "source_basis_status": bt982.get("status", "unknown"),
                "materialized_bt982_json_present": bt982.get("materialized_bt982_json_present", False),
                "status": "basis_vectors_populated_pending_chain_boundary"
            })
    return rows


def theorem_summary():
    bt982, _cols = load_bt982_basis()
    rows = mapped_rows()
    checks = {
        "eight_rows": len(rows) == 8,
        "all_integral_vectors_populated": all(isinstance(x, int) for r in rows for x in r["integral_E8_vector_a"] + r["integral_E8_vector_b"]),
        "four_selector_pairs_two_phase_rows_each": sorted((r["selector_slot"], r["phase_coset_bit"]) for r in rows) == [(s, b) for s in range(4) for b in (0, 1)],
        "bt982_columns_cover_basis_once_per_phase_pair": sorted(set(r["BT982_basis_column_a"] for r in rows) | set(r["BT982_basis_column_b"] for r in rows)) == list(range(8)),
        "chain_boundary_left_pending": all(r["chain_boundary_compatibility"] == "pending_BT1881_test" for r in rows),
        "materialized_or_proxy_source_declared": all("materialized_bt982_json_present" in r for r in rows),
    }
    return {
        "theorem": "BT1880 BT982-to-BT1875 Mapper",
        "output": str(OUT.relative_to(ROOT)),
        "row_count": len(rows),
        "basis_source": "data/bt982_explicit_integral_e8_basis.json if present; otherwise standard-coordinate proxy pending BT982 materialization",
        "materialized_bt982_json_present": bt982.get("materialized_bt982_json_present", False),
        "mapping_rule": "selector slot s receives basis columns 2s and 2s+1; phase bits 0/1 duplicate support vectors pending vector-level phase action",
        "checks": checks,
        "all_pass": all(checks.values()),
        "honest_scope": "Populates candidate integral vectors from materialized BT982 output when available; otherwise uses a declared proxy. Chain-boundary compatibility and vector-level phase action are tested separately."
    }


def main() -> int:
    rows = mapped_rows()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"rows": rows}, indent=2) + "\n", encoding="utf-8")
    summary = theorem_summary()
    SUMMARY_OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
