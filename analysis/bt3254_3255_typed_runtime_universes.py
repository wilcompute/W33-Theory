#!/usr/bin/env python3
"""Passes 3254-3255: exact typed ISA universes and fail-closed projections.

The repository uses three distinct scopes: universal four-opcode baselines, the
194 universal five/six-opcode census, and explicitly reserved future families.
Records may be compared across scopes only through a named common projection;
comparison never changes census membership.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3254_BT3255_TYPED_RUNTIME_UNIVERSES.json"

LIN = {
    "F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
    "F_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
    "S_p": ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
    "S_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1)),
    "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
    "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1)),
}
IDENTITY = np.eye(4, dtype=np.int8)
NAMES = list(LIN) + [f"Z{i}" for i in range(4)]
MATS = {name: np.array(value, dtype=np.int8) for name, value in LIN.items()}
TRANS = {name: np.zeros(4, dtype=np.int8) for name in LIN}
for index in range(4):
    MATS[f"Z{index}"] = IDENTITY.copy()
    vector = np.zeros(4, dtype=np.int8)
    vector[index] = 1
    TRANS[f"Z{index}"] = vector

TARGET_ORDER = 4_199_040
LINEAR_ORDER = 51_840
PROJECTION_ID = "w33.affine_runtime_common.v1"


def matrix_key(matrix: np.ndarray) -> bytes:
    return bytes((matrix % 3).astype(np.uint8).ravel())


def linear_closure(names: tuple[str, ...]) -> list[np.ndarray]:
    generators = [MATS[name] for name in names]
    seen = {matrix_key(IDENTITY)}
    rows = [IDENTITY.copy()]
    queue = deque([IDENTITY.copy()])
    while queue:
        left = queue.popleft()
        for generator in generators:
            right = (left @ generator) % 3
            key = matrix_key(right)
            if key not in seen:
                seen.add(key)
                rows.append(right)
                queue.append(right)
    return rows


def rank_stream(vectors) -> int:
    basis: list[np.ndarray] = []
    pivots: list[int] = []
    for raw in vectors:
        vector = np.array(raw, dtype=np.int8) % 3
        for row, pivot in zip(basis, pivots):
            if vector[pivot]:
                vector = (vector - vector[pivot] * row) % 3
        nonzero = np.flatnonzero(vector)
        if nonzero.size:
            pivot = int(nonzero[0])
            vector = (vector * (1 if vector[pivot] == 1 else 2)) % 3
            for i, row in enumerate(basis):
                if row[pivot]:
                    basis[i] = (row - row[pivot] * vector) % 3
            position = sum(old < pivot for old in pivots)
            pivots.insert(position, pivot)
            basis.insert(position, vector)
            if len(basis) == 4:
                return 4
    return len(basis)


def universal_sets() -> dict[int, list[tuple[str, ...]]]:
    closure_cache = {}
    for size in range(len(LIN) + 1):
        for subset in itertools.combinations(LIN, size):
            closure_cache[frozenset(subset)] = linear_closure(subset)
    result: dict[int, list[tuple[str, ...]]] = {}
    for size in (4, 5, 6):
        rows = []
        for subset in itertools.combinations(NAMES, size):
            linear_names = frozenset(name for name in subset if name in LIN)
            linear = closure_cache[linear_names]
            if len(linear) != LINEAR_ORDER:
                continue
            translations = [TRANS[name] for name in subset if name.startswith("Z")]
            if not translations:
                continue
            rank = rank_stream(
                (matrix @ translation) % 3
                for matrix in linear
                for translation in translations
            )
            if rank == 4:
                rows.append(tuple(subset))
        result[size] = rows
    assert {size: len(rows) for size, rows in result.items()} == {4: 24, 5: 80, 6: 114}
    return result


def canonical_generators(names) -> list[str]:
    order = {name: i for i, name in enumerate(NAMES)}
    return sorted(names, key=order.__getitem__)


def runtime_records() -> list[dict]:
    return [
        {
            "record_id": "current4",
            "generators": canonical_generators(("F_p", "CX_pf", "CX_fp", "Z1")),
            "declared_universe": "affine_universal_4op_v1",
            "group_order_reached": TARGET_ORDER,
            "mean_distance": 14.175585133744857,
            "diameter": 19,
            "collision_probability": 45 / 324,
        },
        {
            "record_id": "low4",
            "generators": canonical_generators(("CX_fp", "CX_pf", "F_f", "Z0")),
            "declared_universe": "affine_universal_4op_v1",
            "group_order_reached": TARGET_ORDER,
            "mean_distance": 15.216323969288219,
            "diameter": 20,
            "collision_probability": 36 / 324,
        },
        {
            "record_id": "fast6",
            "generators": canonical_generators(("F_f", "CX_pf", "CX_fp", "Z0", "Z1", "Z3")),
            "declared_universe": "affine_universal_5_6op_v1",
            "group_order_reached": TARGET_ORDER,
            "mean_distance": 13.72936957018747,
            "diameter": 19,
            "collision_probability": 63 / 486,
        },
    ]


def universe_manifest(universal: dict[int, list[tuple[str, ...]]]) -> dict:
    return {
        "affine_universal_4op_v1": {
            "allowed_opcode_counts": [4],
            "member_count": len(universal[4]),
            "members": [canonical_generators(row) for row in universal[4]],
            "role": "exact comparison baselines and four-opcode design studies",
            "is_194_census": False,
        },
        "affine_universal_5_6op_v1": {
            "allowed_opcode_counts": [5, 6],
            "member_count": len(universal[5]) + len(universal[6]),
            "member_count_by_opcode_count": {"5": len(universal[5]), "6": len(universal[6])},
            "members": [canonical_generators(row) for row in universal[5] + universal[6]],
            "role": "the exact 194-design information and full-affine-runtime census",
            "is_194_census": True,
        },
        "future_affine_family_v1": {
            "allowed_opcode_counts": [],
            "member_count": 0,
            "members": [],
            "role": "reserved; admission requires a new versioned manifest",
            "is_194_census": False,
        },
    }


def admit(record: dict, universes: dict) -> dict:
    universe_id = record.get("declared_universe")
    if universe_id not in universes:
        return {"accepted": False, "reason": "unknown_universe"}
    universe = universes[universe_id]
    generators = canonical_generators(record.get("generators", []))
    if len(generators) not in universe["allowed_opcode_counts"]:
        return {"accepted": False, "reason": "generator_cardinality_out_of_scope"}
    if generators not in universe["members"]:
        return {"accepted": False, "reason": "generator_set_not_a_universe_member"}
    if int(record.get("group_order_reached", -1)) != TARGET_ORDER:
        return {"accepted": False, "reason": "incomplete_affine_group_order"}
    return {
        "accepted": True,
        "reason": "typed_universe_member_with_complete_affine_runtime",
        "census_member": bool(universe["is_194_census"]),
        "comparison_only": not bool(universe["is_194_census"]),
    }


def project(record: dict, admission: dict, projection_id: str | None) -> dict:
    if not admission.get("accepted"):
        raise ValueError("cannot project a rejected record")
    if projection_id != PROJECTION_ID:
        raise ValueError("missing or wrong common projection contract")
    return {
        "projection_id": PROJECTION_ID,
        "record_id": record["record_id"],
        "source_universe": record["declared_universe"],
        "generator_count": len(record["generators"]),
        "group_order_reached": record["group_order_reached"],
        "mean_distance": record["mean_distance"],
        "diameter": record["diameter"],
        "collision_probability": record["collision_probability"],
        "census_member": admission["census_member"],
    }


def compute() -> dict:
    universal = universal_sets()
    universes = universe_manifest(universal)
    records = runtime_records()
    admissions = {record["record_id"]: admit(record, universes) for record in records}
    assert all(row["accepted"] for row in admissions.values())
    assert admissions["current4"]["comparison_only"]
    assert admissions["low4"]["comparison_only"]
    assert admissions["fast6"]["census_member"]

    projections = {
        record["record_id"]: project(record, admissions[record["record_id"]], PROJECTION_ID)
        for record in records
    }
    comparison_rows = []
    for left, right in itertools.combinations(records, 2):
        l = projections[left["record_id"]]
        r = projections[right["record_id"]]
        comparison_rows.append(
            {
                "left": l["record_id"],
                "right": r["record_id"],
                "projection_id": PROJECTION_ID,
                "cross_universe": l["source_universe"] != r["source_universe"],
                "mean_distance_delta_left_minus_right": l["mean_distance"] - r["mean_distance"],
                "collision_probability_delta_left_minus_right": l["collision_probability"] - r["collision_probability"],
                "membership_effect": "none; projection permits metric comparison but never transfers census membership",
            }
        )

    mistagged = dict(records[0], declared_universe="affine_universal_5_6op_v1")
    wrong_order = dict(records[1], group_order_reached=81)
    future = dict(records[2], declared_universe="future_affine_family_v1")
    controls = {
        "current4_mistagged_as_194_census": admit(mistagged, universes),
        "low4_incomplete_group_order": admit(wrong_order, universes),
        "fast6_future_family_without_manifest": admit(future, universes),
    }
    assert not any(control["accepted"] for control in controls.values())
    try:
        project(records[0], admissions["current4"], None)
        missing_projection_rejected = False
    except ValueError:
        missing_projection_rejected = True
    assert missing_projection_rejected

    migration = {
        "source_status": "PARTIAL_RUNTIME_1_OF_194_PLUS_2_BASELINES",
        "typed_census_joined": ["fast6"],
        "typed_out_of_census_baselines": ["current4", "low4"],
        "pending_194_census_records": 193,
        "global_194_runtime_optimum_allowed": False,
    }

    payload = {
        "schema": "w33.pass3254_3255.typed_runtime_universes.v1",
        "status": "PASS_EXACT_TYPED_RUNTIME_UNIVERSES",
        "target_affine_group_order": TARGET_ORDER,
        "universes": universes,
        "records": records,
        "admissions": admissions,
        "common_projection": {
            "projection_id": PROJECTION_ID,
            "fields": [
                "group_order_reached",
                "mean_distance",
                "diameter",
                "collision_probability",
            ],
            "rule": "Cross-universe metric comparison requires this explicit projection and never changes source-universe membership or census denominators.",
        },
        "projections": projections,
        "pairwise_comparisons": comparison_rows,
        "pass3195_migration": migration,
        "negative_controls": controls,
        "missing_projection_rejected": missing_projection_rejected,
        "boundary": "This is an exact finite classification for the frozen ten-operation affine library. It does not promote decoder area, timing, energy, calibration, or a global 194-design runtime optimum before the complete aggregate exists.",
    }
    semantic = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["semantic_sha256"] = hashlib.sha256(semantic.encode()).hexdigest()
    return payload


def main() -> None:
    payload = compute()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "universe_counts": {key: value["member_count"] for key, value in payload["universes"].items()},
                "migration": payload["pass3195_migration"],
                "sha256": payload["semantic_sha256"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
