#!/usr/bin/env python3
"""Pass 3029: minimize the exact escalation controller by future-action equivalence.

Two post-base collision classes are identified when the canonical controller emits the
same next test and, for every possible D4 observation, enters equivalent future states.
Leaves emit only STOP; correction synthesis remains a separate downstream action. This is
an exact Moore-machine quotient for the noiseless two-step escalation policy.
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

from bt3025_3031_common import FROZEN_23, TRIANGLES, frozen_collision_classes, sparse_prior, syndrome_matrix

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3029_PREDICTIVE_CAUSAL_STATES_results.json"


def entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities if p > 0)


def main():
    full = syndrome_matrix()
    collisions = frozen_collision_classes(full)
    prior = sparse_prior()
    frozen = {TRIANGLES.index(t) for t in FROZEN_23}
    remaining = [i for i in range(120) if i not in frozen]

    def signature(indices):
        indices = tuple(indices)
        if len(indices) <= 1:
            return ("STOP",)
        best = None
        for triangle in remaining:
            parts = defaultdict(list)
            for index in indices:
                parts[int(full[index, triangle])].append(index)
            key = (-len(parts), max(map(len,parts.values())), triangle)
            if best is None or key < best[0]:
                best = (key, triangle, parts)
        _, triangle, parts = best
        return (
            "TEST", triangle,
            tuple(sorted((observation, signature(child)) for observation, child in parts.items())),
        )

    initial_signatures = [signature(row) for row in collisions]
    unique_initial = {repr(row) for row in initial_signatures}
    all_states = set()

    def collect(row):
        all_states.add(repr(row))
        if row[0] == "TEST":
            for _, child in row[2]:
                collect(child)

    for row in initial_signatures:
        collect(row)

    collision_mass = float(sum(prior[list(row)].sum() for row in collisions))
    raw_distribution = []
    causal_distribution = defaultdict(float)
    for collision, state in zip(collisions, initial_signatures):
        mass = float(prior[list(collision)].sum() / collision_mass)
        raw_distribution.append(mass)
        causal_distribution[repr(state)] += mass

    depths = Counter()
    def depth(state):
        if state[0] == "STOP":
            return 0
        return 1 + max(depth(child) for _, child in state[2])
    for state in initial_signatures:
        depths[depth(state)] += 1

    raw_entropy = entropy(raw_distribution)
    causal_entropy = entropy(causal_distribution.values())
    payload = {
        "schema": "w33.pass3029.predictive_causal_states.v1",
        "status": "COMPLETE_EXACT_NOISELESS_FUTURE_ACTION_QUOTIENT",
        "raw_collision_classes": len(collisions),
        "initial_future_action_causal_states": len(unique_initial),
        "all_recursive_controller_states_including_stop": len(all_states),
        "test_states": len(all_states)-1,
        "stop_states": 1,
        "depth_histogram": {str(k):v for k,v in sorted(depths.items())},
        "raw_fixed_bits": math.ceil(math.log2(len(collisions))),
        "causal_fixed_bits": math.ceil(math.log2(len(unique_initial))),
        "raw_conditional_entropy_bits": raw_entropy,
        "causal_conditional_entropy_bits": causal_entropy,
        "entropy_reduction_bits": raw_entropy-causal_entropy,
        "drifting_prior_extension": {
            "hidden_regimes": ["calm","burst"],
            "transition_matrix": [[0.999,0.001],[0.05,0.95]],
            "principle": "Retain the posterior burst probability together with the finite causal state. The raw fault transcript is not predictive once these are known.",
            "status": "EXPLICIT_MODEL_SOURCE_NOT_A_LABORATORY_FIT",
        },
        "checks": {
            "raw_1436": len(collisions)==1436,
            "initial_457": len(unique_initial)==457,
            "all_states_470": len(all_states)==470,
            "depths_1230_206": depths==Counter({1:1230,2:206}),
        },
        "design_decision": "Implement the 457-state future-action quotient for proof/model reduction; preserve semantic class labels only where downstream correction synthesis needs them.",
        "claim_boundary": "Exact for the canonical noiseless escalation policy and STOP-only terminal action. Noisy belief states are continuous unless a calibrated finite model or quantization is specified; the two-regime extension is a proposed explicit model, not a measured prior drift law.",
    }
    assert all(payload["checks"].values())
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status":payload["status"],"raw":1436,"causal":457,"entropy_reduction":payload["entropy_reduction_bits"]}, sort_keys=True))


if __name__ == "__main__":
    main()
