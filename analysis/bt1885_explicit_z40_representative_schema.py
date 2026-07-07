#!/usr/bin/env python3
"""BT1885: explicit Z^40 representative schema.

Defines the schema for lifting each BT1880 vertex-E8 8-vector into the W(3,3)
40-coordinate chain model. The first candidate lift uses BT982's vertex_subset
when the materialized BT982 JSON is present; otherwise it uses the vertex subset
recorded in the BT982 source. This is a schema/candidate lift, not yet a proof
that it is the correct chain A/2 representative model.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BT982 = ROOT / "data/bt982_explicit_integral_e8_basis.json"
MAPPED = ROOT / "data/PART_BT1880_BT982_TO_BT1875_MAPPED_TEMPLATE.json"
OUT = ROOT / "data/PART_BT1885_EXPLICIT_Z40_REPRESENTATIVE_SCHEMA.json"
SUMMARY_OUT = ROOT / "data/PART_BT1885_EXPLICIT_Z40_REPRESENTATIVE_SCHEMA_summary.json"
FALLBACK_VERTEX_SUBSET = [0, 1, 4, 22, 27, 35, 23, 34]


def load_vertex_subset():
    if BT982.exists():
        return json.loads(BT982.read_text(encoding="utf-8"))["vertex_subset"], True
    return FALLBACK_VERTEX_SUBSET, False


def embed_z40(v, vertex_subset):
    out = [0] * 40
    for i, x in enumerate(v):
        out[vertex_subset[i]] = x
    return out


def schema_rows():
    vertex_subset, materialized = load_vertex_subset()
    rows = json.loads(MAPPED.read_text(encoding="utf-8"))["rows"]
    out = []
    for r in rows:
        z40a = embed_z40(r["integral_E8_vector_a"], vertex_subset)
        z40b = embed_z40(r["integral_E8_vector_b"], vertex_subset)
        out.append({
            "selector_slot": r["selector_slot"],
            "support_pair": r["support_pair"],
            "phase_coset_bit": r["phase_coset_bit"],
            "vertex_subset": vertex_subset,
            "materialized_bt982_json_present": materialized,
            "z40_vector_a": z40a,
            "z40_vector_b": z40b,
            "z40_support_a": [i for i, x in enumerate(z40a) if x != 0],
            "z40_support_b": [i for i, x in enumerate(z40b) if x != 0],
            "lift_rule": "BT982 vertex_subset sparse embedding",
            "chain_A_over_2_status": "candidate_sparse_embedding_pending_operator_validation",
        })
    return out


def theorem_summary():
    rows = schema_rows()
    checks = {
        "eight_rows": len(rows) == 8,
        "all_z40_vectors_length_40": all(len(r["z40_vector_a"]) == 40 and len(r["z40_vector_b"]) == 40 for r in rows),
        "all_supports_inside_vertex_subset": all(set(r["z40_support_a"]).issubset(r["vertex_subset"]) and set(r["z40_support_b"]).issubset(r["vertex_subset"]) for r in rows),
        "vertex_subset_size_8": all(len(r["vertex_subset"]) == 8 for r in rows),
        "operator_validation_not_claimed": all(r["chain_A_over_2_status"] == "candidate_sparse_embedding_pending_operator_validation" for r in rows),
    }
    return {
        "theorem": "BT1885 Explicit Z40 Representative Schema",
        "output": str(OUT.relative_to(ROOT)),
        "row_count": len(rows),
        "lift_rule": "embed each 8-vector sparsely into Z^40 on BT982 vertex_subset or its recorded fallback",
        "materialized_bt982_json_present": all(r["materialized_bt982_json_present"] for r in rows),
        "checks": checks,
        "all_pass": all(checks.values()),
        "honest_scope": "Defines candidate sparse Z^40 representatives. It does not prove this is the final chain A/2 representative model."
    }


def main() -> int:
    rows = schema_rows()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"rows": rows}, indent=2) + "\n", encoding="utf-8")
    summary = theorem_summary()
    SUMMARY_OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
