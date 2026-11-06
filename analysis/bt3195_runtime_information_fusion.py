#!/usr/bin/env python3
"""Pass 3195: fail-closed fusion of all-194 information with observed affine BFS.

The information census is complete. Runtime is joined only for exact 4,199,040-state
BFS records whose generator sets belong to the 80 five-opcode or 114 six-opcode
census. A complete Pass-3163 aggregate is accepted when present; otherwise one
frozen six-opcode record joins the census and two four-opcode records remain typed
as out-of-census baselines.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter, deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "PART_BT3195_RUNTIME_INFORMATION_FUSION_results.json"
AGGREGATE = DATA / "PART_BT3163_ISA_FULL_BFS_AGGREGATE.json"
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
OPS = {name: (2 if name.startswith("CX") else 1) for name in NAMES}
VECTORS = np.array(list(itertools.product(range(3), repeat=4)), dtype=np.int8)
VECTOR_INDEX = {tuple(map(int, vector)): i for i, vector in enumerate(VECTORS)}


def matrix_key(matrix: np.ndarray) -> bytes:
    return bytes((matrix % 3).astype(np.uint8).ravel())


def closure(names) -> list[np.ndarray]:
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


def information_rows() -> list[dict]:
    closure_cache = {}
    for size in range(7):
        for subset in itertools.combinations(LIN, size):
            closure_cache[frozenset(subset)] = closure(subset)
    rows = []
    for size in (5, 6):
        for subset in itertools.combinations(NAMES, size):
            linear = closure_cache[frozenset(name for name in subset if name in LIN)]
            if len(linear) != 51_840:
                continue
            translations = [TRANS[name] for name in subset if name.startswith("Z")]
            if rank_stream(
                (matrix @ translation) % 3
                for matrix in linear
                for translation in translations
            ) != 4:
                continue
            entropies = []
            collisions = 0
            for frame, vector in enumerate(VECTORS):
                destinations = []
                seen = set()
                for name in subset:
                    destination = VECTOR_INDEX[
                        tuple(map(int, (MATS[name] @ vector + TRANS[name]) % 3))
                    ]
                    destinations.append(destination)
                    if destination == frame or destination in seen:
                        collisions += 1
                    seen.add(destination)
                counts = Counter(destinations)
                probabilities = [count / size for count in counts.values()]
                entropies.append(-sum(p * math.log2(p) for p in probabilities))
            average = float(np.mean(entropies))
            rows.append(
                {
                    "generators": list(subset),
                    "size": size,
                    "information_average": average,
                    "information_minimum": min(entropies),
                    "information_maximum": max(entropies),
                    "information_variance": float(np.var(entropies)),
                    "information_normalized": average / math.log2(size),
                    "collision_probability": collisions / (81 * size),
                    "decoder_operation_units": sum(OPS[name] for name in subset),
                }
            )
    rows.sort(key=lambda row: (row["size"], row["generators"]))
    assert len(rows) == 194
    assert sum(row["size"] == 5 for row in rows) == 80
    return rows


FROZEN_RUNTIME = {
    frozenset(("F_p", "CX_pf", "CX_fp", "Z1")): {
        "name": "current4",
        "mean_distance": 14.175585133744857,
        "diameter": 19,
        "group_order_reached": 4_199_040,
    },
    frozenset(("CX_fp", "CX_pf", "F_f", "Z0")): {
        "name": "low4",
        "mean_distance": 15.216323969288219,
        "diameter": 20,
        "group_order_reached": 4_199_040,
    },
    frozenset(("F_f", "CX_pf", "CX_fp", "Z0", "Z1", "Z3")): {
        "name": "fast6",
        "mean_distance": 13.72936957018747,
        "diameter": 19,
        "group_order_reached": 4_199_040,
    },
}


def runtime_records() -> tuple[dict[frozenset[str], dict], str]:
    if not AGGREGATE.exists():
        return dict(FROZEN_RUNTIME), "PARTIAL_RUNTIME_1_OF_194_PLUS_2_BASELINES"
    data = json.loads(AGGREGATE.read_text(encoding="utf-8"))
    records = data.get("records", [])
    assert len(records) == 194
    result = {}
    for record in records:
        full = record["full_group"]
        assert full["group_order_reached"] == 4_199_040
        result[frozenset(record["generators"])] = {
            "name": "complete_aggregate",
            "mean_distance": full["mean_distance"],
            "diameter": full["diameter"],
            "group_order_reached": full["group_order_reached"],
        }
    assert len(result) == 194
    return result, "COMPLETE_RUNTIME_194_OF_194"


def dominates(left: dict, right: dict) -> bool:
    weak = (
        left["information_average"] >= right["information_average"] - 1e-12
        and left["information_minimum"] >= right["information_minimum"] - 1e-12
        and left["collision_probability"] <= right["collision_probability"] + 1e-12
        and left["decoder_operation_units"] <= right["decoder_operation_units"]
        and left["runtime"]["mean_distance"]
        <= right["runtime"]["mean_distance"] + 1e-12
        and left["runtime"]["diameter"] <= right["runtime"]["diameter"]
    )
    strict = (
        left["information_average"] > right["information_average"] + 1e-12
        or left["information_minimum"] > right["information_minimum"] + 1e-12
        or left["collision_probability"] < right["collision_probability"] - 1e-12
        or left["decoder_operation_units"] < right["decoder_operation_units"]
        or left["runtime"]["mean_distance"]
        < right["runtime"]["mean_distance"] - 1e-12
        or left["runtime"]["diameter"] < right["runtime"]["diameter"]
    )
    return weak and strict


def main() -> None:
    information = information_rows()
    information_by_key = {
        frozenset(row["generators"]): row for row in information
    }
    runtime, status = runtime_records()
    joined = []
    out_of_census_baselines = []
    for key, observed in runtime.items():
        row = information_by_key.get(key)
        if row is None:
            out_of_census_baselines.append(
                {
                    "generators": sorted(key),
                    "runtime": observed,
                    "reason": (
                        "four-opcode baseline outside the frozen five/six-opcode "
                        "194-design information census"
                    ),
                }
            )
        else:
            joined.append(dict(row, runtime=observed))

    joined.sort(key=lambda row: (row["size"], row["generators"]))
    out_of_census_baselines.sort(key=lambda row: row["generators"])
    assert len(joined) + len(out_of_census_baselines) == len(runtime)
    if status == "COMPLETE_RUNTIME_194_OF_194":
        assert len(joined) == 194
        assert not out_of_census_baselines
    else:
        assert len(joined) == 1
        assert len(out_of_census_baselines) == 2

    frontier = [
        row for row in joined if not any(dominates(other, row) for other in joined)
    ]
    result = {
        "schema": "w33.pass3195.runtime_information_fusion.v2",
        "status": status,
        "information_records": len(information),
        "runtime_records_total": len(runtime),
        "joined_records": len(joined),
        "out_of_census_baseline_count": len(out_of_census_baselines),
        "out_of_census_baselines": out_of_census_baselines,
        "pending_runtime_records": 194 - len(joined),
        "joined_pareto_count": len(frontier),
        "joined_pareto": frontier,
        "joined_records_detail": joined,
        "promotion_rule": (
            "A global runtime-information optimum exists only when status is "
            "COMPLETE_RUNTIME_194_OF_194 and every joined record reaches order 4,199,040."
        ),
        "boundary": (
            "Information is complete for all 194 five/six-opcode designs. Runtime fusion "
            "is exact only for observed full-BFS records belonging to that census; "
            "current4 and low4 are typed four-opcode baselines, not two of the 194. "
            "Missing rows are never estimated from the 81-frame graph. Placement cost "
            "and physical energy remain separate."
        ),
    }
    DATA.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": status,
                "joined": len(joined),
                "baselines": len(out_of_census_baselines),
                "frontier": len(frontier),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
