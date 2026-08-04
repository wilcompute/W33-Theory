#!/usr/bin/env python3
"""Passes 3252-3253: independent, numbering-free verifier for the 876-state ROM.

This implementation does not import the Pass-3194 or Pass-3216 D4 arithmetic,
state numbering, or recursive serializer.  D4 is reconstructed as permutations
of a square, reachable raw subsets are generated explicitly, and the Moore
quotient is formed bottom-up by subset cardinality.  Candidate ROMs are reduced
back to state-number-independent recursive signatures before comparison.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "PART_BT3252_BT3253_INDEPENDENT_CURVATURE_VERIFIER.json"
ROM_OUT = DATA / "PART_BT3253_INDEPENDENT_CURVATURE_ROM.json"
EXPECTED_SEMANTIC_SHA256 = "40fdb368a43f2e6f6eab6981e02d41b25f93993a6f1a3cab45ec263367a33675"

ROTATION = (1, 2, 3, 0)
REFLECTION = (0, 3, 2, 1)
IDENTITY_PERM = tuple(range(4))


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[i]] for i in range(len(right)))


def power(permutation: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    result = IDENTITY_PERM
    for _ in range(exponent):
        result = compose(result, permutation)
    return result


D4_LABELS = [(a, b) for a in range(4) for b in range(2)]
D4_PERMS = [compose(power(ROTATION, a), power(REFLECTION, b)) for a, b in D4_LABELS]
PERM_TO_INDEX = {permutation: i for i, permutation in enumerate(D4_PERMS)}
assert len(PERM_TO_INDEX) == 8
D4_MUL = np.empty((8, 8), dtype=np.uint8)
D4_INV = np.empty(8, dtype=np.uint8)
for i, left in enumerate(D4_PERMS):
    for j, right in enumerate(D4_PERMS):
        D4_MUL[i, j] = PERM_TO_INDEX[compose(left, right)]
    D4_INV[i] = next(j for j in range(8) if D4_MUL[i, j] == 0 and D4_MUL[j, i] == 0)

FAULTS = tuple(range(1, 8))
EDGES = list(itertools.combinations(range(10), 2))
TRIANGLES = list(itertools.combinations(range(10), 3))
FROZEN23 = [
    (5, 6, 9), (2, 5, 9), (4, 5, 8), (2, 4, 7), (0, 3, 6),
    (0, 1, 8), (1, 2, 4), (1, 3, 5), (3, 4, 8), (0, 4, 9),
    (2, 3, 8), (4, 8, 9), (1, 7, 8), (1, 4, 6), (0, 2, 3),
    (3, 7, 9), (1, 3, 9), (2, 6, 9), (3, 5, 7), (0, 1, 7),
    (3, 6, 8), (0, 4, 5), (4, 6, 7),
]
SELECTED = [TRIANGLES.index(triangle) for triangle in FROZEN23]
REMAINING = [i for i in range(len(TRIANGLES)) if i not in set(SELECTED)]


def directed(edge: tuple[int, int], group_index: int, u: int, v: int) -> int:
    if (u, v) == edge:
        return group_index
    if (v, u) == edge:
        return int(D4_INV[group_index])
    return 0


def syndrome(hypothesis: tuple[tuple[tuple[int, int], int], ...]) -> tuple[int, ...]:
    values = []
    for i, j, k in TRIANGLES:
        product = 0
        for u, v in ((i, j), (j, k), (k, i)):
            factor = 0
            for edge, group_index in hypothesis:
                factor = int(D4_MUL[directed(edge, group_index, u, v), factor])
            product = int(D4_MUL[factor, product])
        values.append(product)
    return tuple(values)


def hypothesis_universe() -> list[tuple]:
    rows: list[tuple] = [tuple()]
    rows.extend(((edge, group_index),) for edge in EDGES for group_index in FAULTS)
    rows.extend(
        ((edge, group_index), (other, second_index))
        for edge, other in itertools.combinations(EDGES, 2)
        for group_index in FAULTS
        for second_index in FAULTS
    )
    assert len(rows) == 48_826
    return rows


def curvature_labels(rows: list[tuple]) -> list[int]:
    measured_pairs = set()
    for triangle in FROZEN23:
        triangle_edges = [tuple(sorted(edge)) for edge in itertools.combinations(triangle, 2)]
        measured_pairs.update(tuple(sorted(pair)) for pair in itertools.combinations(triangle_edges, 2))
    assert len(measured_pairs) == 69

    central_r2 = PERM_TO_INDEX[power(ROTATION, 2)]
    labels = []
    for row in rows:
        if len(row) != 2:
            labels.append(0)
            continue
        (edge, a), (other, b) = row
        if tuple(sorted((edge, other))) not in measured_pairs:
            labels.append(0)
            continue
        commutator = int(
            D4_MUL[
                D4_MUL[D4_MUL[a, b], D4_INV[a]],
                D4_INV[b],
            ]
        )
        labels.append(2 if commutator == central_r2 else 1)
    assert Counter(labels) == Counter({0: 45_445, 1: 1_725, 2: 1_656})
    return labels


def choose_action(indices: tuple[int, ...], full: np.ndarray) -> tuple[int, dict[int, tuple[int, ...]]]:
    best = None
    for triangle in REMAINING:
        parts: dict[int, list[int]] = defaultdict(list)
        for index in indices:
            parts[int(full[index, triangle])].append(index)
        key = (-len(parts), max(map(len, parts.values())), triangle)
        if best is None or key < best[0]:
            best = (key, triangle, {outcome: tuple(child) for outcome, child in parts.items()})
    assert best is not None
    return best[1], best[2]


def histogram(indices: tuple[int, ...], labels: list[int]) -> tuple[int, int, int]:
    count = Counter(labels[index] for index in indices)
    return count[0], count[1], count[2]


def build_raw_dag(
    collisions: list[tuple[int, ...]], full: np.ndarray, labels: list[int]
) -> tuple[dict[tuple[int, ...], dict], dict[tuple[int, ...], tuple]]:
    pending = list(collisions)
    raw: dict[tuple[int, ...], dict] = {}
    while pending:
        state = tuple(sorted(pending.pop()))
        if state in raw:
            continue
        typed = histogram(state, labels)
        if len(state) == 1:
            raw[state] = {"terminal": True, "histogram": typed, "action": None, "children": {}}
            continue
        action, children = choose_action(state, full)
        canonical_children = {outcome: tuple(sorted(child)) for outcome, child in children.items()}
        assert all(len(child) < len(state) for child in canonical_children.values())
        raw[state] = {
            "terminal": False,
            "histogram": typed,
            "action": action,
            "children": canonical_children,
        }
        pending.extend(canonical_children.values())

    signatures: dict[tuple[int, ...], tuple] = {}
    for size in (1, 2, 3):
        for state in sorted((s for s in raw if len(s) == size)):
            node = raw[state]
            if node["terminal"]:
                signatures[state] = ("STOP", node["histogram"])
            else:
                signatures[state] = (
                    "TEST",
                    node["action"],
                    node["histogram"],
                    tuple(
                        sorted(
                            (outcome, signatures[child])
                            for outcome, child in node["children"].items()
                        )
                    ),
                )
    assert len(signatures) == len(raw)
    return raw, signatures


def row_from_signature(state_id: int, signature: tuple, signature_ids: dict[tuple, int]) -> dict:
    if signature[0] == "STOP":
        return {
            "state_id": state_id,
            "terminal": True,
            "action": None,
            "curvature_histogram": list(signature[1]),
            "transitions": {},
        }
    return {
        "state_id": state_id,
        "terminal": False,
        "action": int(signature[1]),
        "curvature_histogram": list(signature[2]),
        "transitions": {str(outcome): signature_ids[child] for outcome, child in signature[3]},
    }


def semantic_digest(states: list[dict], initial_state_ids: list[int]) -> str:
    semantic = {"states": states, "initial_state_ids": initial_state_ids}
    return hashlib.sha256(json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def construct_reference() -> dict:
    rows = hypothesis_universe()
    full = np.array([syndrome(row) for row in rows], dtype=np.uint8)
    grouped: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for index, key in enumerate(map(tuple, full[:, SELECTED])):
        grouped[key].append(index)
    collisions = [tuple(values) for values in grouped.values() if len(values) > 1]
    assert len(grouped) == 46_284
    assert len(collisions) == 1_436
    assert Counter(map(len, collisions)) == Counter({2: 330, 3: 1_106})

    labels = curvature_labels(rows)
    raw, raw_signatures = build_raw_dag(collisions, full, labels)
    unique_signatures = set(raw_signatures.values())
    ordered = sorted(unique_signatures, key=repr)
    signature_ids = {signature: i for i, signature in enumerate(ordered)}
    states = [row_from_signature(i, signature, signature_ids) for i, signature in enumerate(ordered)]
    initial_state_ids = [signature_ids[raw_signatures[tuple(sorted(collision))]] for collision in collisions]

    assert len(raw) == 5_620
    assert Counter(map(len, raw)) == Counter({1: 3_978, 2: 536, 3: 1_106})
    assert len(unique_signatures) == 876
    assert len(set(initial_state_ids)) == 770
    assert Counter(len(signature) == 2 for signature in ordered)[True] == 3
    digest = semantic_digest(states, initial_state_ids)
    assert digest == EXPECTED_SEMANTIC_SHA256

    return {
        "schema": "w33.pass3253.independent_curvature_rom.v1",
        "status": "EXACT_INDEPENDENT_ROM",
        "hypotheses": 48_826,
        "base_signatures": 46_284,
        "collision_classes": 1_436,
        "raw_reachable_subsets": len(raw),
        "raw_subset_size_histogram": {str(k): v for k, v in sorted(Counter(map(len, raw)).items())},
        "unique_initial_states": 770,
        "all_recursive_states": 876,
        "terminal_states": 3,
        "semantic_sha256": digest,
        "states": states,
        "initial_state_ids": initial_state_ids,
    }


def signature_from_candidate(state_id: int, by_id: dict[int, dict], memo: dict[int, tuple], visiting: set[int]) -> tuple:
    if state_id in memo:
        return memo[state_id]
    if state_id in visiting:
        raise ValueError("candidate transition graph contains a cycle")
    visiting.add(state_id)
    row = by_id[state_id]
    typed = tuple(map(int, row["curvature_histogram"]))
    if row["terminal"]:
        if row["action"] is not None or row["transitions"]:
            raise ValueError("terminal row carries action or transitions")
        signature = ("STOP", typed)
    else:
        transitions = tuple(
            sorted(
                (
                    int(outcome),
                    signature_from_candidate(int(child), by_id, memo, visiting),
                )
                for outcome, child in row["transitions"].items()
            )
        )
        signature = ("TEST", int(row["action"]), typed, transitions)
    visiting.remove(state_id)
    memo[state_id] = signature
    return signature


def canonicalize_candidate(candidate: dict) -> dict:
    rows = candidate["states"]
    by_id = {int(row["state_id"]): row for row in rows}
    if len(by_id) != len(rows):
        raise ValueError("duplicate state id")
    memo: dict[int, tuple] = {}
    for state_id in by_id:
        signature_from_candidate(state_id, by_id, memo, set())
    ordered = sorted(set(memo.values()), key=repr)
    if len(ordered) != 876:
        raise ValueError(f"candidate has {len(ordered)} semantic states, expected 876")
    signature_ids = {signature: i for i, signature in enumerate(ordered)}
    states = [row_from_signature(i, signature, signature_ids) for i, signature in enumerate(ordered)]
    initial = [signature_ids[memo[int(state_id)]] for state_id in candidate["initial_state_ids"]]
    if len(set(initial)) != 770:
        raise ValueError("candidate initial quotient does not contain 770 states")
    return {"states": states, "initial_state_ids": initial, "semantic_sha256": semantic_digest(states, initial)}


def reverse_numbering(reference: dict) -> dict:
    n = len(reference["states"])
    remap = {old: n - 1 - old for old in range(n)}
    states = []
    for row in reference["states"]:
        states.append(
            {
                "state_id": remap[int(row["state_id"])],
                "terminal": bool(row["terminal"]),
                "action": row["action"],
                "curvature_histogram": list(row["curvature_histogram"]),
                "transitions": {str(outcome): remap[int(child)] for outcome, child in row["transitions"].items()},
            }
        )
    states.sort(key=lambda row: row["state_id"])
    return {"states": states, "initial_state_ids": [remap[int(x)] for x in reference["initial_state_ids"]]}


def verification_report(candidate: dict, reference_digest: str) -> dict:
    try:
        canonical = canonicalize_candidate(candidate)
    except Exception as exc:
        return {"accepted": False, "reason": str(exc)}
    return {
        "accepted": canonical["semantic_sha256"] == reference_digest,
        "semantic_sha256": canonical["semantic_sha256"],
        "reason": "semantic digest match" if canonical["semantic_sha256"] == reference_digest else "semantic digest mismatch",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path)
    args = parser.parse_args()

    reference = construct_reference()
    ROM_OUT.parent.mkdir(parents=True, exist_ok=True)
    ROM_OUT.write_text(json.dumps(reference, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    reversed_candidate = reverse_numbering(reference)
    reverse_result = verification_report(reversed_candidate, reference["semantic_sha256"])
    assert reverse_result["accepted"]

    action_mutation = json.loads(json.dumps(reversed_candidate))
    target = next(row for row in action_mutation["states"] if not row["terminal"])
    target["action"] = (int(target["action"]) + 1) % 120
    action_result = verification_report(action_mutation, reference["semantic_sha256"])
    assert not action_result["accepted"]

    cycle_mutation = json.loads(json.dumps(reversed_candidate))
    target = next(row for row in cycle_mutation["states"] if not row["terminal"] and row["transitions"])
    first_outcome = next(iter(target["transitions"]))
    target["transitions"][first_outcome] = target["state_id"]
    cycle_result = verification_report(cycle_mutation, reference["semantic_sha256"])
    assert not cycle_result["accepted"]

    external = None
    if args.candidate:
        external = verification_report(json.loads(args.candidate.read_text()), reference["semantic_sha256"])

    payload = {
        "schema": "w33.pass3252_3253.independent_curvature_verifier.v1",
        "status": "PASS_INDEPENDENT_876_STATE_VERIFICATION",
        "construction": {
            "group_model": "D4 as permutations of the four vertices of a square",
            "quotient_algorithm": "explicit reachable raw-subset DAG followed by bottom-up Moore partitioning by subset cardinality",
            "state_numbering": "discarded before comparison; recursive semantics are canonicalized independently",
        },
        "counts": {
            key: reference[key]
            for key in (
                "hypotheses",
                "base_signatures",
                "collision_classes",
                "raw_reachable_subsets",
                "raw_subset_size_histogram",
                "unique_initial_states",
                "all_recursive_states",
                "terminal_states",
            )
        },
        "semantic_sha256": reference["semantic_sha256"],
        "expected_pass3216_semantic_sha256": EXPECTED_SEMANTIC_SHA256,
        "numbering_permutation_control": reverse_result,
        "action_mutation_control": action_result,
        "cycle_mutation_control": cycle_result,
        "external_candidate": external,
        "boundary": "This independently verifies the frozen noiseless policy quotient and canonical ROM semantics. It does not verify noisy-belief optimality, FPGA implementation, or laboratory sensing channels.",
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "states": 876, "initial": 770, "sha256": reference["semantic_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
