#!/usr/bin/env python3
"""Strict promotion gate for a future explicit U4(2):2 computational embedding."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data" / "PART_3769_3786_FINITE_GROUP_DESCENT_candidate.json"
EXPECTED = {
    "group_order": 51840,
    "index_two_subgroup_order": 25920,
    "distinguished_involutions": 36,
    "generalized_quadrangle_points": 45,
    "generalized_quadrangle_lines": 27,
    "order_1152_stabilizers": 45,
    "order_192_frames": 135,
    "plane_ovoids": 40,
    "plane_ovoid_graph_parameters": [40, 12, 2, 4],
    "all_nonsingular_projective_lines": 120,
}


def canonical_hash(payload):
    clean = {k: v for k, v in payload.items() if k != "content_sha256"}
    return sha256(json.dumps(clean, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate(path: Path, require_ready=False):
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("status") == "PENDING":
        assert payload.get("group_elements") == []
        if require_ready:
            raise SystemExit("PENDING: no explicit finite-group candidate has been supplied")
        return {"status": "PENDING", "validated": False}
    assert payload.get("status") == "READY_FOR_VALIDATION"
    assert payload["expected_finite_structure"] == EXPECTED
    assert payload.get("group_elements")
    evidence = payload["executed_evidence"]
    for key, expected in EXPECTED.items():
        assert evidence[key] == expected
    assert evidence.get("independent_order_certificate")
    assert evidence.get("class_correspondence")
    assert evidence.get("incidence_digest")
    assert evidence.get("content_sha256") == canonical_hash(payload)
    return {"status": "VALIDATED", "validated": True, "content_sha256": evidence["content_sha256"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", nargs="?", type=Path, default=DEFAULT)
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()
    print(json.dumps(validate(args.candidate, args.require_ready), indent=2))


if __name__ == "__main__":
    main()
