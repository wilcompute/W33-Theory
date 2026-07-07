#!/usr/bin/env python3
"""BT1881: chain-boundary compatibility tester.

Defines the first executable tester for BT1880 mapped rows. At this stage the
available BT982 basis is in vertex E8 root coordinates, while the chain A/2 form
and explicit Z^40 representative split remain a separate model layer. Therefore
BT1881 can verify vector-shape/integrality and keep the actual chain-boundary
compatibility as a fenced pending field rather than falsely passing it.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPED = ROOT / "data/PART_BT1880_BT982_TO_BT1875_MAPPED_TEMPLATE.json"
OUT = ROOT / "data/PART_BT1881_CHAIN_BOUNDARY_COMPATIBILITY_TEST_results.json"


def load_rows():
    return json.loads(MAPPED.read_text(encoding="utf-8"))["rows"]


def vector_shape_ok(v):
    return isinstance(v, list) and len(v) == 8 and all(isinstance(x, int) for x in v)


def theorem_summary():
    rows = load_rows()
    row_results = []
    for r in rows:
        ok_shape = vector_shape_ok(r["integral_E8_vector_a"]) and vector_shape_ok(r["integral_E8_vector_b"])
        row_results.append({
            "selector_slot": r["selector_slot"],
            "support_pair": r["support_pair"],
            "phase_coset_bit": r["phase_coset_bit"],
            "integral_vector_shape_ok": ok_shape,
            "chain_boundary_compatibility": "pending_explicit_Z40_chain_model",
            "reason": "BT982 vectors are integral in vertex E8 root coordinates; explicit Z^40 chain A/2 representatives are still needed for boundary testing"
        })
    checks = {
        "eight_rows_loaded": len(rows) == 8,
        "all_integral_vector_shapes_ok": all(x["integral_vector_shape_ok"] for x in row_results),
        "boundary_not_falsely_passed": all(x["chain_boundary_compatibility"] == "pending_explicit_Z40_chain_model" for x in row_results),
        "explicit_Z40_layer_named": True,
    }
    return {
        "theorem": "BT1881 Chain-Boundary Compatibility Tester",
        "input": str(MAPPED.relative_to(ROOT)),
        "row_results": row_results,
        "closed_now": "BT982 vector integrality and 8-coordinate shape in vertex E8 root coordinates",
        "remaining_needed": "explicit Z^40 chain A/2 representative model and boundary operator/action on mapped vectors",
        "checks": checks,
        "all_pass": all(checks.values()),
        "honest_scope": "Tester scaffold with integrality/shape checks. Chain-boundary compatibility remains pending until the explicit Z^40 chain model is supplied."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
