#!/usr/bin/env python3
"""Pass 2955: exact finite-horizon Bayesian support-observer optimization.

The initial four-bit support mask is assumed known exactly. Later support observations
pass through an independent coordinate-asymmetric channel. At every posterior the policy
may stop or choose one of the four micro-operations, with distinct operation costs.
The old minimum-depth noise-free tree is evaluated under the same channel as the exact
benchmark; the new policy is not merely a repeated-readout overlay.
"""
from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT2955_BAYES_OPTIMAL_NOISY_OBSERVER_results.json"
STATES = list(product(range(3), repeat=4))
P01 = [0.002, 0.006, 0.002, 0.006]
P10 = [0.02, 0.05, 0.02, 0.05]
ACTION_COST = [1.0, 2.0, 2.0, 1.0]
ACTION_NAMES = ["F_p", "CX_p->f", "CX_f->p", "Z_p"]
OBSERVATIONS = list(range(16))


def support_mask(state):
    return sum((1 << i) for i, value in enumerate(state) if value)


def step(state, operation):
    xp, zp, xf, zf = state
    if operation == 0:
        return ((-zp) % 3, xp, xf, zf)
    if operation == 1:
        return (xp, (zp-zf) % 3, (xf+xp) % 3, zf)
    if operation == 2:
        return ((xp+xf) % 3, zp, xf, (zf-zp) % 3)
    return (xp, (zp+1) % 3, xf, zf)


def rank(state):
    return 27*state[0] + 9*state[1] + 3*state[2] + state[3]


RANK_STATE = {rank(state): state for state in STATES}
STEP_RANK = np.zeros((4,81), dtype=np.int16)
SUPPORT_RANK = np.zeros(81, dtype=np.int8)
for state_rank, state in RANK_STATE.items():
    SUPPORT_RANK[state_rank] = support_mask(state)
    for operation in range(4):
        STEP_RANK[operation, state_rank] = rank(step(state, operation))

LIKELIHOOD = np.zeros((16,16), dtype=float)
for true_mask in range(16):
    for observed_mask in range(16):
        probability = 1.0
        for bit in range(4):
            true_bit = (true_mask >> bit) & 1
            observed_bit = (observed_mask >> bit) & 1
            if true_bit:
                probability *= (1-P10[bit]) if observed_bit else P10[bit]
            else:
                probability *= P01[bit] if observed_bit else (1-P01[bit])
        LIKELIHOOD[true_mask, observed_mask] = probability
assert np.allclose(LIKELIHOOD.sum(axis=1), 1)

GROUPS = defaultdict(list)
for state in STATES:
    GROUPS[support_mask(state)].append(state)


def optimize_group(initial_states, horizon, terminal_error_weight):
    cache = {}
    policy = {}

    def belief_key(ranks, weights, remaining):
        order = np.argsort(ranks)
        return (
            remaining,
            tuple(int(ranks[i]) for i in order),
            tuple(round(float(weights[i]), 13) for i in order),
        )

    def solve(ranks, weights, remaining):
        key = belief_key(ranks, weights, remaining)
        if key in cache:
            return cache[key]
        stop_error = 1 - float(np.max(weights))
        best = (terminal_error_weight * stop_error, stop_error, 0.0, None, True)
        if remaining > 0 and len(ranks) > 1:
            for operation in range(4):
                next_ranks = STEP_RANK[operation, ranks]
                objective = ACTION_COST[operation]
                expected_error = 0.0
                expected_action_cost = ACTION_COST[operation]
                for observed_mask in OBSERVATIONS:
                    likelihood = LIKELIHOOD[SUPPORT_RANK[next_ranks], observed_mask]
                    observation_probability = float(np.dot(weights, likelihood))
                    if observation_probability < 1e-15:
                        continue
                    posterior = weights * likelihood / observation_probability
                    continuation = solve(next_ranks, posterior, remaining - 1)
                    objective += observation_probability * continuation[0]
                    expected_error += observation_probability * continuation[1]
                    expected_action_cost += observation_probability * continuation[2]
                candidate = (objective, expected_error, expected_action_cost, operation, False)
                if candidate[0] < best[0] - 1e-12:
                    best = candidate
            policy[key] = {"operation": best[3], "stop": best[4]}
        cache[key] = best
        return best

    ranks = np.array([rank(state) for state in initial_states], dtype=np.int16)
    prior = np.ones(len(ranks), dtype=float) / len(ranks)
    value = solve(ranks, prior, horizon)
    return value, len(cache), policy


@dataclass
class NoiseFreeNode:
    candidates: tuple
    operation: int | None
    children: dict
    expected_steps: float
    worst_steps: int


def canonical_candidates(candidates):
    return tuple(sorted(candidates, key=lambda item: (item[0], item[1])))


@lru_cache(None)
def solve_noise_free(candidates, remaining):
    if len(candidates) == 1:
        return NoiseFreeNode(candidates, None, {}, 0.0, 0)
    if remaining == 0:
        return None
    best = None
    for operation in range(4):
        buckets = {}
        for original, state in candidates:
            next_state = step(state, operation)
            buckets.setdefault(support_mask(next_state), []).append((original, next_state))
        children = {}
        for mask, items in buckets.items():
            child = solve_noise_free(canonical_candidates(items), remaining - 1)
            if child is None:
                children = None
                break
            children[mask] = child
        if children is None:
            continue
        worst = 1 + max(child.worst_steps for child in children.values())
        expected = 1 + sum(len(child.candidates) / len(candidates) * child.expected_steps for child in children.values())
        node = NoiseFreeNode(candidates, operation, children, expected, worst)
        score = (worst, expected, operation)
        if best is None or score < (best.worst_steps, best.expected_steps, best.operation):
            best = node
    return best


def noise_free_root(states):
    candidates = canonical_candidates(tuple((i, state) for i, state in enumerate(states)))
    for depth in range(5):
        node = solve_noise_free(candidates, depth)
        if node is not None:
            return node
    raise AssertionError("noise-free horizon exceeded")


def evaluate_noise_free_node(node, true_original, true_state):
    if node.operation is None:
        return (1.0 if node.candidates[0][0] == true_original else 0.0, 0.0)
    next_state = step(true_state, node.operation)
    true_mask = support_mask(next_state)
    masks = sorted(node.children)
    priors = {mask: len(node.children[mask].candidates) / len(node.candidates) for mask in masks}
    routes = [max(masks, key=lambda mask: priors[mask] * LIKELIHOOD[mask, observation]) for observation in OBSERVATIONS]
    success = 0.0
    cost = ACTION_COST[node.operation]
    for observation, probability in enumerate(LIKELIHOOD[true_mask]):
        if probability == 0:
            continue
        child_success, child_cost = evaluate_noise_free_node(node.children[routes[observation]], true_original, next_state)
        success += probability * child_success
        cost += probability * child_cost
    return success, cost


def evaluate_noise_free_group(states):
    root = noise_free_root(states)
    success = 0.0
    cost = 0.0
    for original, state in enumerate(states):
        local_success, local_cost = evaluate_noise_free_node(root, original, state)
        success += local_success / len(states)
        cost += local_cost / len(states)
    return {
        "error": 1-success,
        "action_cost": cost,
        "worst_steps": root.worst_steps,
        "noise_free_expected_steps": root.expected_steps,
        "root_action": ACTION_NAMES[root.operation] if root.operation is not None else None,
    }


def aggregate_bayes(weight, horizon=4):
    rows = {}
    for mask, states in sorted(GROUPS.items()):
        value, belief_count, _ = optimize_group(states, horizon, weight)
        rows[str(mask)] = {
            "support": format(mask, "04b"),
            "states": len(states),
            "objective": value[0],
            "error": value[1],
            "action_cost": value[2],
            "root_action": None if value[3] is None else ACTION_NAMES[value[3]],
            "stop_at_root": value[4],
            "belief_states_explored": belief_count,
        }
    aggregate_error = sum(len(GROUPS[mask]) / 81 * rows[str(mask)]["error"] for mask in GROUPS)
    aggregate_cost = sum(len(GROUPS[mask]) / 81 * rows[str(mask)]["action_cost"] for mask in GROUPS)
    return rows, aggregate_error, aggregate_cost


def main():
    benchmark_rows = {str(mask): evaluate_noise_free_group(states) for mask, states in sorted(GROUPS.items())}
    benchmark_error = sum(len(GROUPS[mask]) / 81 * benchmark_rows[str(mask)]["error"] for mask in GROUPS)
    benchmark_cost = sum(len(GROUPS[mask]) / 81 * benchmark_rows[str(mask)]["action_cost"] for mask in GROUPS)
    pareto = {}
    detailed_lambda100 = None
    for weight in (20,50,100,200):
        rows, error, cost = aggregate_bayes(weight)
        pareto[str(weight)] = {"aggregate_error": error, "aggregate_action_cost": cost}
        if weight == 100:
            detailed_lambda100 = rows
    assert detailed_lambda100 is not None
    assert abs(benchmark_error - 0.058694797923555815) < 1e-10
    assert abs(pareto["100"]["aggregate_error"] - 0.016889211063212103) < 1e-10
    assert pareto["100"]["aggregate_action_cost"] < benchmark_cost
    result = {
        "schema": "w33.pass2955.bayes_optimal_noisy_observer.v1",
        "status": "COMPLETE_EXACT_FINITE_HORIZON",
        "model": {
            "initial_support_known_exactly": True,
            "horizon": 4,
            "p01": P01,
            "p10": P10,
            "action_costs": dict(zip(ACTION_NAMES, ACTION_COST)),
            "stopping_allowed": True,
        },
        "noise_free_tree_under_noisy_channel": {
            "aggregate_error": benchmark_error,
            "aggregate_action_cost": benchmark_cost,
            "by_initial_support": benchmark_rows,
        },
        "bayes_pareto": pareto,
        "lambda100_by_initial_support": detailed_lambda100,
        "headline": "Posterior-policy optimization cuts aggregate error from 5.87% to 1.69% and slightly lowers expected action cost at terminal-error weight 100.",
        "boundary": "Exact for this horizon, known initial support, synthetic independent detector channel, and stated action costs; not an infinite-horizon or laboratory-calibrated optimum."
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS benchmark_error=%.9f bayes100_error=%.9f" % (benchmark_error, pareto["100"]["aggregate_error"]))


if __name__ == "__main__":
    main()
