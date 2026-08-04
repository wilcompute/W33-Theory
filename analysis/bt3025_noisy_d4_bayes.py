#!/usr/bin/env python3
"""Pass 3025: noisy collision-conditioned Bayesian D4 escalation.

The common 23-row panel is assumed to have identified one of the exact collision classes.
Escalation symbols are then observed through an explicit synthetic D4-valued channel with
an erasure output. This is an exact finite-horizon Bayes calculation for that stated
channel, not measured optical performance and not yet a noisy decoder for the base panel.
"""
from __future__ import annotations

import json
from collections import Counter
from functools import lru_cache
from pathlib import Path

import numpy as np

from bt3025_3031_common import (
    D4, D4_INDEX, FROZEN_23, TRIANGLES, frozen_collision_classes,
    hypotheses, inverse, multiply, sparse_prior, syndrome_matrix,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3025_NOISY_D4_BAYES_results.json"
R = (1, 0)


def conjugate(a, g):
    return multiply(multiply(a, g), inverse(a))


def channel(erasure, partial, drift, dark):
    """Return P(observation|true D4 symbol), with column eight the erasure."""
    matrix = np.zeros((8, 9), dtype=float)
    remaining = 1.0 - erasure
    if partial + drift + dark > 1.0:
        raise ValueError("non-erasure mixture exceeds one")
    for true_index, g in enumerate(D4):
        matrix[true_index, D4_INDEX[g]] += remaining * (1-partial-drift-dark)
        matrix[true_index, D4_INDEX[multiply(R, g)]] += remaining * partial / 2
        matrix[true_index, D4_INDEX[multiply(inverse(R), g)]] += remaining * partial / 2
        matrix[true_index, D4_INDEX[conjugate(R, g)]] += remaining * drift
        matrix[true_index, :8] += remaining * dark / 8
        matrix[true_index, 8] += erasure
    assert np.allclose(matrix.sum(axis=1), 1.0)
    return matrix


def patterns(collision, full_syndrome, remaining_tests):
    table = {}
    view = full_syndrome[list(collision)][:, remaining_tests]
    for offset, triangle_index in enumerate(remaining_tests):
        key = tuple(int(x) for x in view[:, offset])
        table.setdefault(key, triangle_index)
    return table


def optimize_class(collision, full_syndrome, prior, likelihood, cost=0.001, horizon=2):
    collision = tuple(collision)
    local_prior = prior[list(collision)]
    local_prior /= local_prior.sum()
    frozen = {TRIANGLES.index(t) for t in FROZEN_23}
    remaining = [i for i in range(120) if i not in frozen]
    available = patterns(collision, full_syndrome, remaining)

    @lru_cache(maxsize=None)
    def value(probability_key, steps_left):
        probability = np.asarray(probability_key, dtype=float)
        probability /= probability.sum()
        stop_error = 1.0 - float(probability.max())
        best = (stop_error, stop_error, 0.0, "STOP")
        if steps_left == 0:
            return best
        for true_symbols, triangle_index in available.items():
            local_likelihood = likelihood[np.asarray(true_symbols)]
            observation_probability = probability @ local_likelihood
            future_objective = future_error = future_probes = 0.0
            for observation, mass in enumerate(observation_probability):
                if mass < 1e-15:
                    continue
                posterior = probability * local_likelihood[:, observation] / mass
                key = tuple(float(x) for x in np.round(posterior, 12))
                objective, error, probes, _ = value(key, steps_left-1)
                future_objective += mass * objective
                future_error += mass * error
                future_probes += mass * probes
            candidate = (
                cost + future_objective,
                future_error,
                1.0 + future_probes,
                f"TEST_{triangle_index}",
            )
            if candidate[0] < best[0] - 1e-12:
                best = candidate
        return best

    key = tuple(float(x) for x in np.round(local_prior, 12))
    return value(key, horizon)


def main():
    full = syndrome_matrix()
    collisions = frozen_collision_classes(full)
    prior = sparse_prior()
    collision_mass = float(sum(prior[list(row)].sum() for row in collisions))
    profiles = {
        "mild": channel(0.02, 0.01, 0.005, 0.001),
        "moderate": channel(0.05, 0.02, 0.01, 0.002),
        "severe": channel(0.10, 0.05, 0.02, 0.005),
    }
    results = {}
    for name, likelihood in profiles.items():
        objective = error = probes = 0.0
        actions = Counter()
        for collision in collisions:
            mass = float(prior[list(collision)].sum() / collision_mass)
            local_objective, local_error, local_probes, action = optimize_class(
                collision, full, prior, likelihood
            )
            objective += mass * local_objective
            error += mass * local_error
            probes += mass * local_probes
            actions[action.split("_", 1)[0]] += 1
        results[name] = {
            "synthetic_channel": {
                "erasure": {"mild":0.02,"moderate":0.05,"severe":0.10}[name],
                "partial_left_rotation": {"mild":0.01,"moderate":0.02,"severe":0.05}[name],
                "conjugation_drift": {"mild":0.005,"moderate":0.01,"severe":0.02}[name],
                "uniform_dark_component": {"mild":0.001,"moderate":0.002,"severe":0.005}[name],
            },
            "conditional_objective": objective,
            "conditional_residual_error": error,
            "conditional_expected_extra_probes": probes,
            "unconditional_residual_error": collision_mass * error,
            "unconditional_expected_extra_probes": collision_mass * probes,
            "initial_stop_classes": actions["STOP"],
            "initial_test_classes": actions["TEST"],
        }

    expected = {
        "mild": (0.0006404017282571333, 0.41414732387972136),
        "moderate": (0.0007574986249606812, 0.41454071468346565),
        "severe": (0.0013167797326137658, 0.009295020830901501),
    }
    for name, (error, probes) in expected.items():
        assert abs(results[name]["conditional_residual_error"] - error) < 2e-11
        assert abs(results[name]["conditional_expected_extra_probes"] - probes) < 2e-11

    payload = {
        "schema": "w33.pass3025.noisy_collision_conditioned_d4_bayes.v1",
        "status": "COMPLETE_EXACT_DP_FOR_STATED_SYNTHETIC_ESCALATION_CHANNELS",
        "hypotheses": len(hypotheses()),
        "collision_classes_after_exact_base": len(collisions),
        "collision_prior_mass": collision_mass,
        "probe_cost_to_unit_error_loss": 0.001,
        "horizon": 2,
        "profiles": results,
        "checks": {
            "hypotheses_48826": len(hypotheses()) == 48_826,
            "collision_classes_1436": len(collisions) == 1_436,
            "all_channels_normalized": all(np.allclose(x.sum(axis=1),1) for x in profiles.values()),
            "frozen_reference_reproduced": True,
        },
        "design_decision": "Retain likelihoods and stop by posterior risk; do not map erasure or partial group errors to a hard D4 symbol before inference.",
        "claim_boundary": "Exact finite-horizon Bayes solution conditional on the exact 23-row collision class and the explicitly synthetic channels above. A fully noisy base-panel decoder and laboratory calibration remain open.",
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status":payload["status"],"profiles":results}, sort_keys=True))


if __name__ == "__main__":
    main()
