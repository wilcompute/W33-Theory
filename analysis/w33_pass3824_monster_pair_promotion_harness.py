#!/usr/bin/env python3
"""Fail-closed promotion gate for a concrete Monster realization of Passes 3821-3828.

This harness does not search the Monster. It validates a separately produced,
content-addressed runtime artifact against the complete abstract U4(2)
standard-pair census and the functorial 36-seed fingerprints.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATE = ROOT / "data" / "PART_3824_MONSTER_STANDARD_PAIR_candidate.json"
EXPECTED = {
    "group_order": 25920,
    "a_order": 2,
    "a_class_size": 45,
    "b_order": 5,
    "b_class_size": 5184,
    "ab_order": 9,
    "ab_class_size": 2880,
    "commutator_order": 3,
    "generated_group_order": 25920,
    "axis_count": 36,
    "frame_count": 135,
    "norton_triple_count": 120,
    "code_weight_distribution": {"0": 1, "16": 27, "20": 36},
    "line_split": {"0": 45, "1": 216, "2": 270, "3": 120},
    "frame_sha256": "9c59605c3da8d39651555da942133650977b9c9b22135a3993c78b993bbaaf39",
    "norton_sha256": "cf12c3080fb3673b64aad5e339df2eaee3f2d16a8932fbc4662bef67e81da398",
    "abstract_lines_sha256": "a8dc7bd4fa3079c95ddf029131a94840daf6222f3701d92254ff7ef192b354d9",
}


def canonical_sha256(payload: object) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(text.encode()).hexdigest()


def validate(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {
            "status": "PENDING_NO_CONCRETE_MONSTER_ARTIFACT",
            "candidate": str(path.relative_to(ROOT)),
            "promoted": False,
        }
    payload = json.loads(path.read_text())
    if payload.get("schema") != "w33.monster_standard_pair_candidate.v1":
        raise SystemExit("candidate schema mismatch")
    if payload.get("runtime") not in {"mmgroup", "GAP+mmgroup"}:
        raise SystemExit("candidate lacks an accepted executed runtime")
    for key in ("serialized_a", "serialized_b", "runtime_version", "provenance"):
        if not payload.get(key):
            raise SystemExit(f"candidate missing {key}")
    observed = payload.get("observed")
    if not isinstance(observed, dict):
        raise SystemExit("candidate observed block missing")
    for key, expected in EXPECTED.items():
        if observed.get(key) != expected:
            raise SystemExit(f"candidate mismatch for {key}: {observed.get(key)!r} != {expected!r}")
    claimed = payload.get("candidate_sha256")
    material = {k: v for k, v in payload.items() if k != "candidate_sha256"}
    actual = canonical_sha256(material)
    if claimed != actual:
        raise SystemExit("candidate content hash mismatch")
    return {
        "status": "PROMOTABLE_CONCRETE_MONSTER_STANDARD_PAIR",
        "candidate": str(path.relative_to(ROOT)),
        "candidate_sha256": actual,
        "promoted": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, default=DEFAULT_CANDIDATE)
    args = parser.parse_args()
    print(json.dumps(validate(args.candidate), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
