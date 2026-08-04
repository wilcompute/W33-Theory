#!/usr/bin/env python3
"""Pass 3195: fuse frame-local information with observed full-affine runtime evidence.

The information side is recomputed for all 194 universal five/six-opcode ISAs. The runtime
side is fail-closed: the complete frontier is promoted only when the 194-record Pass-3163
aggregate is present and every record reaches 4,199,040 affine elements. Until then, the
three independently frozen full-BFS records are joined and the remaining 191 are marked
pending rather than silently imputed.
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
RUNTIME_AGGREGATE = DATA / "PART_BT3163_ISA_FULL_BFS_AGGREGATE.json"
LIN = {
    "F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
    "F_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
    "S_p": ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
    "S_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1)),
    "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
    "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1)),
}
I4 = np.eye(4, dtype=np.int8)
NAMES = list(LIN) + [f"Z{i}" for i in range(4)]
MATS = {name: np.array(value, dtype=np.int8) for name, value in LIN.items()}
TRANS = {name: np.zeros(4, dtype=np.int8) for name in LIN}
for i in range(4):
    MATS[f"Z{i}"] = I4.copy()
    vector = np.zeros(4, dtype=np.int8)
    vector[i] = 1
    TRANS[f"Z{i}"] = vector
OPS = {name: (2 if name.startswith("CX") else 1) for name in NAMES}
VECTORS = np.array(list(itertools.product(range(3), repeat=4)), dtype=np.int8)
VID = {tuple(map(int, vector)): i for i, vector in enumerate(VECTORS)}


def key(matrix):
    return bytes((matrix % 3).astype(np.uint8).ravel())


def linear_closure(names):
    generators = [MATS[name] for name in names]
    seen = {key(I4)}
    rows = [I4.copy()]
    queue = deque([I4.copy()])
    while queue:
        left = queue.popleft()
        for generator in generators:
            right = (left @ generator) % 3
            encoded = key(right)
            if encoded not in seen:
                seen.add(encoded)
                rows.append(right)
                queue.append(right)
    return rows


def rank_stream(vectors):
    basis = []
    pivots = []
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
            position = sum(x < pivot for x in pivots)
            pivots.insert(position, pivot)
            basis.insert(position, vector)
            if len(basis) == 4:
                return 4
    return len(basis)


def information_rows():
    cache = {}
    for size in range(7):
        for subset in itertools.combinations(LIN, size):
            cache[frozenset(subset)] = linear_closure(subset)
    rows = []
    for size in (5, 6):
        for subset in itertools.combinations(NAMES, size):
            closure = cache[frozenset(name for name in subset if name in LIN)]
            if len(closure) != 51_840:
                continue
            translations = [TRANS[name] for name in subset if name.startswith("Z")]
            if rank_stream((matrix @ translation) % 3 for matrix in closure for translation in translations) != 4:
                continue
            entropies = []
            collisions = 0
            for i, vector in enumerate(VECTORS):
                destinations = []
                seen = set()
                for name in subset:
                    destination = VID[tuple(map(int, (MATS[name] @ vector + TRANS[name]) % 3))]
                    destinations.append(destination)
                    if destination == i or destination in seen:
                        collisions += 1
                    seen.add(destination)
                counts = Counter(destinations)
                probabilities = [count / size for count in counts.values()]
                entropies.append(-sum(p * math.log2(p) for p in probabilities))
            average = float(np.mean(entropies))
            rows.append({
                "generators": list(subset),
                "size": size,
                "information_average": average,
                "information_minimum": min(entropies),
                "information_maximum": max(entropies),
                "information_variance": float(np.var(entropies)),
                "information_normalized": average / math.log2(size),
                "collision_probability": collisions / (81 * size),
                "decoder_operation_units": sum(OPS[name] for name in subset),
            })
    rows.sort(key=lambda row: (row["size"], row["generators"]))
    assert len(rows) == 194
    assert sum(row["size"] == 5 for row in rows) == 80
    return rows


FROZEN_RUNTIME = {
    ("F_p", "CX_pf", "CX_fp", "Z1"): {"name": "current4", "mean_distance": 14.175585133744857, "diameter": 19, "group_order_reached": 4_199_040},
    ("CX_fp", "CX_pf", "F_f", "Z0"): {"name": "low4", "mean_distance": 15.216323969288219, "diameter": 20, "group_order_reached": 4_199_040},
    ("F_f", "CX_pf", "CX_fp", "Z0", "Z1", "Z3"): {"name": "fast6", "mean_distance": 13.72936957018747, "diameter": 19, "group_order_reached": 4_199_040},
}


def load_runtime():
    if not RUNTIME_AGGREGATE.exists():
        return {tuple(key): value for key, value in FROZEN_RUNTIME.items()}, "PARTIAL_RUNTIME_3_OF_194"
    aggregate = json.loads(RUNTIME_AGGREGATE.read_text(encoding="utf-8"))
    records = aggregate.get("records", [])
    assert len(records) == 194
    runtime = {}
    for record in records:
        full = record["full_group"]
        assert full["group_order_reached"] == 4_199_040
        runtime[tuple(record["generators"])] = {
            "name": "complete_aggregate",
            "mean_distance": full["mean_distance"],
            "diameter": full["diameter"],
            "group_order_reached": full["group_order_reached"],
        }
    return runtime, "COMPLETE_RUNTIME_194_OF_194"


def dominates(a, b):
    better_or_equal = (
        a["information_average"] >= b["information_average"] - 1e-12
        and a["information_minimum"] >= b["information_minimum"] - 1e-12
        and a["collision_probability"] <= b["collision_probability"] + 1e-12
        and a["decoder_operation_units"] <= b["decoder_operation_units"]
        and a["runtime"]["mean_distance"] <= b["runtime"]["mean_distance"] + 1e-12
        and a["runtime"]["diameter"] <= b["runtime"]["diameter"]
    )
    strict = (
        a["information_average"] > b["information_average"] + 1e-12
        or a["information_minimum"] > b["information_minimum"] + 1e-12
        or a["collision_probability"] < b["collision_probability"] - 1e-12
        or a["decoder_operation_units"] < b["decoder_operation_units"]
        or a["runtime"]["mean_distance"] < b["runtime"]["mean_distance"] - 1e-12
        or a["runtime"]["diameter"] < b["runtime"]["diameter"]
    )
    return better_or_equal and strict


def main() -> None:
    information = information_rows()
    runtime, status = load_runtime()
    joined = []
    for row in information:
        record = runtime.get(tuple(row["generators"]))
        if record is not None:
            joined.append(dict(row, runtime=record))
    frontier = [row for row in joined if not any(dominates(other, row) for other in joined)]
    result = {
        "schema": "w33.pass3195.runtime_information_fusion.v1",
        "status": status,
        "information_records": len(information),
        "runtime_records": len(runtime),
        "joined_records": len(joined),
        "pending_runtime_records": 194 - len(runtime),
        "joined_pareto_count": len(frontier),
        "joined_pareto": frontier,
        "joined_records_detail": joined,
        "promotion_rule": "A global runtime-information optimum exists in this artifact only when status is COMPLETE_RUNTIME_194_OF_194 and every full-group order is 4,199,040.",
        "boundary": "Information metrics are complete for all 194 designs. Runtime fusion is exact only for observed full-BFS records; missing records are never estimated from the 81-frame graph. Decoder area, Fmax and energy remain separate placement evidence."
    }
    DATA.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "joined": len(joined), "frontier": len(frontier)}, sort_keys=True))


if __name__ == "__main__":
    main()
