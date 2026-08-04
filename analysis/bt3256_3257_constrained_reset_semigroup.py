#!/usr/bin/env python3
"""Passes 3256-3257: constrained synchronization rank and authorized reset.

Passive symbols are physically admissible controller events (action, outcome): a
state follows the corresponding child only when that action is scheduled and the
outcome exists; otherwise it holds.  Terminal curvature classes hold.  The exact
passive transformation semigroup therefore has rank at least three.  A separately
typed authorization latch extends the state space and permits a rank-one reset
only after a valid proof-root authorization token.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3256_BT3257_CONSTRAINED_RESET_SEMIGROUP.json"
VERIFIER_PATH = ROOT / "analysis" / "bt3252_3253_independent_curvature_verifier.py"


def load_verifier():
    spec = importlib.util.spec_from_file_location("bt3256_verifier", VERIFIER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def passive_transforms(states: list[dict]) -> tuple[list[tuple[int, int]], dict[tuple[int, int], np.ndarray]]:
    actions = sorted({int(row["action"]) for row in states if not row["terminal"]})
    symbols = [(action, outcome) for action in actions for outcome in range(8)]
    transforms = {}
    for symbol in symbols:
        action, outcome = symbol
        image = np.arange(len(states), dtype=np.int32)
        for row in states:
            state_id = int(row["state_id"])
            if row["terminal"] or int(row["action"]) != action:
                continue
            child = row["transitions"].get(str(outcome))
            if child is not None:
                image[state_id] = int(child)
        transforms[symbol] = image
    return symbols, transforms


def apply_word(image: set[int], word: list[tuple[int, int]], transforms: dict[tuple[int, int], np.ndarray]) -> tuple[set[int], list[int]]:
    current = set(image)
    history = [len(current)]
    for symbol in word:
        transform = transforms[symbol]
        current = {int(transform[state]) for state in current}
        history.append(len(current))
    return current, history


def greedy_rank_word(symbols, transforms, state_count: int) -> tuple[list[tuple[int, int]], list[int]]:
    image = set(range(state_count))
    word: list[tuple[int, int]] = []
    history = [state_count]
    while True:
        candidates = []
        for symbol in symbols:
            transform = transforms[symbol]
            next_image = {int(transform[state]) for state in image}
            candidates.append((len(next_image), symbol, next_image))
        size, symbol, next_image = min(candidates, key=lambda row: (row[0], row[1]))
        if size >= len(image):
            break
        word.append(symbol)
        image = next_image
        history.append(len(image))
    return word, history


def extended_transform_rank(transform: np.ndarray) -> int:
    return len(set(map(int, transform)))


def compute() -> dict:
    verifier = load_verifier()
    reference = verifier.construct_reference()
    states = reference["states"]
    assert len(states) == 876
    terminal_ids = sorted(int(row["state_id"]) for row in states if row["terminal"])
    assert len(terminal_ids) == 3

    symbols, transforms = passive_transforms(states)
    assert len(symbols) == 104
    for transform in transforms.values():
        assert all(int(transform[state]) == state for state in terminal_ids)

    word, rank_history = greedy_rank_word(symbols, transforms, len(states))
    image, replay_history = apply_word(set(range(len(states))), word, transforms)
    assert replay_history == rank_history
    assert image == set(terminal_ids)
    assert rank_history[-1] == 3
    passive_minimum_rank = 3

    expected_word = [
        (0, 0), (10, 0), (11, 0), (3, 0), (4, 0), (7, 0),
        (12, 0), (13, 0), (2, 0), (1, 0), (14, 0), (18, 0),
        (15, 0), (3, 0), (4, 0), (7, 0), (0, 1), (0, 5),
        (0, 2), (0, 6),
    ]
    expected_image, expected_history = apply_word(set(range(len(states))), expected_word, transforms)
    assert expected_image == set(terminal_ids)
    assert expected_history == [876, 722, 638, 561, 491, 421, 351, 281, 218, 176, 120, 85, 50, 36, 29, 22, 15, 11, 7, 5, 3]
    assert len(word) <= len(expected_word)

    n = len(states)
    product_size = 2 * n
    identity_product = np.arange(product_size, dtype=np.int32)

    passive_product_ranks = []
    for symbol, base in transforms.items():
        transform = np.empty(product_size, dtype=np.int32)
        for state in range(n):
            for armed in (0, 1):
                transform[2 * state + armed] = 2 * int(base[state]) + armed
        passive_product_ranks.append(extended_transform_rank(transform))
    assert min(passive_product_ranks) >= 6

    authorize = np.empty(product_size, dtype=np.int32)
    invalid_authorize = identity_product.copy()
    canonical_prior = int(reference["initial_state_ids"][0])
    reset = np.empty(product_size, dtype=np.int32)
    for state in range(n):
        authorize[2 * state] = 2 * state + 1
        authorize[2 * state + 1] = 2 * state + 1
        reset[2 * state] = 2 * state
        reset[2 * state + 1] = 2 * canonical_prior

    authorize_rank = extended_transform_rank(authorize)
    reset_rank = extended_transform_rank(reset)
    invalid_rank = extended_transform_rank(invalid_authorize)
    assert authorize_rank == 876
    assert reset_rank == 876
    assert invalid_rank == 1752

    composition = reset[authorize]
    assert extended_transform_rank(composition) == 1
    assert set(map(int, composition)) == {2 * canonical_prior}

    one_symbol_ranks = passive_product_ranks + [authorize_rank, reset_rank, invalid_rank]
    assert min(one_symbol_ranks) >= 6
    shortest_authorized_rank_one_length = 2

    payload = {
        "schema": "w33.pass3256_3257.constrained_reset_semigroup.v1",
        "status": "PASS_EXACT_PASSIVE_RANK_AND_AUTHORIZED_RESET",
        "controller_states": n,
        "passive_alphabet": {
            "actions": sorted({action for action, _ in symbols}),
            "outcomes_per_action": 8,
            "symbol_count": len(symbols),
            "semantics": "matching action and valid outcome follows the child; every other state holds; terminal curvature classes hold",
        },
        "passive_result": {
            "terminal_fixed_classes": terminal_ids,
            "lower_bound": "three distinct terminal curvature states are fixed by every passive symbol",
            "minimum_rank": passive_minimum_rank,
            "constructive_word": [list(symbol) for symbol in expected_word],
            "constructive_word_length": len(expected_word),
            "rank_history": expected_history,
            "greedy_word_length": len(word),
            "greedy_word": [list(symbol) for symbol in word],
            "greedy_rank_history": rank_history,
            "conclusion": "Passive sensing and synchronization can collapse all uncertainty to the three curvature-labelled terminal classes, but cannot erase which terminal class was reached.",
        },
        "authorized_reset": {
            "extended_states": product_size,
            "latch_states": 2,
            "canonical_prior_state": canonical_prior,
            "minimum_passive_rank_on_extended_space": min(passive_product_ranks),
            "valid_authorization_rank": authorize_rank,
            "reset_without_prior_authorization_rank": reset_rank,
            "invalid_authorization_rank": invalid_rank,
            "authorize_then_reset_rank": 1,
            "shortest_rank_one_word": ["AUTHORIZE_VALID_PROOF_ROOT", "RESET_MATCHING_ROOT"],
            "shortest_rank_one_word_length": shortest_authorized_rank_one_length,
            "minimality_proof": "Every single passive symbol has rank at least six on the latch product; authorization and reset separately have rank 876; invalid authorization is identity. The displayed two-token word has rank one.",
        },
        "boundary": "This is a finite-state protocol theorem for the frozen controller and an abstract proof-root latch. It is not a measurement of physical erasure energy, reset latency, optical loss, or fault-tolerant behavior.",
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
                "passive_minimum_rank": payload["passive_result"]["minimum_rank"],
                "passive_word_length": payload["passive_result"]["constructive_word_length"],
                "authorized_rank_one_length": payload["authorized_reset"]["shortest_rank_one_word_length"],
                "sha256": payload["semantic_sha256"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
