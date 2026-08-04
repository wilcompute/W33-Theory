#!/usr/bin/env python3
"""Pass 3031 (BONKERS): choose the syndrome alphabet as well as the triangle.

The full D4 detector Blackwell-dominates every deterministic coarse-graining, but the
coarser detector may be cheaper, faster, or more robust. This file computes the exact
one-probe Bayes frontier over the repository's 1,436 collision classes for four alphabets:
full D4, conjugacy class, abelianization V4, and reflection parity.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from bt3025_3031_common import (
    D4, D4_INDEX, FROZEN_23, TRIANGLES, conjugacy_class_id,
    frozen_collision_classes, inverse, multiply, sparse_prior, syndrome_matrix,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3031_MEASUREMENT_BASIS_PORTFOLIO_results.json"
R=(1,0)


def conjugate(a,g):
    return multiply(multiply(a,g),inverse(a))


def moderate_channel():
    erasure,partial,drift,dark=0.05,0.02,0.01,0.002
    matrix=np.zeros((8,9),float)
    remaining=1-erasure
    for true_index,g in enumerate(D4):
        matrix[true_index,D4_INDEX[g]] += remaining*(1-partial-drift-dark)
        matrix[true_index,D4_INDEX[multiply(R,g)]] += remaining*partial/2
        matrix[true_index,D4_INDEX[multiply(inverse(R),g)]] += remaining*partial/2
        matrix[true_index,D4_INDEX[conjugate(R,g)]] += remaining*drift
        matrix[true_index,:8] += remaining*dark/8
        matrix[true_index,8] += erasure
    return matrix


def coarse_channel(full,map_values):
    count=max(map_values)+1
    matrix=np.zeros((8,count+1),float)
    for observation,coarse in enumerate(map_values):
        matrix[:,coarse]+=full[:,observation]
    matrix[:,-1]=full[:,8]
    assert np.allclose(matrix.sum(axis=1),1)
    return matrix


def one_probe(collision,full_syndrome,prior,likelihood,remaining):
    local_prior=prior[list(collision)]
    local_prior/=local_prior.sum()
    stop=1-float(local_prior.max())
    best=stop
    patterns={}
    for triangle in remaining:
        key=tuple(int(full_syndrome[index,triangle]) for index in collision)
        patterns.setdefault(key,triangle)
    for true_symbols in patterns:
        local=likelihood[np.asarray(true_symbols)]
        error=1-float(np.max(local_prior[:,None]*local,axis=0).sum())
        best=min(best,error)
    return stop,best


def main():
    full_syndrome=syndrome_matrix()
    collisions=frozen_collision_classes(full_syndrome)
    prior=sparse_prior()
    collision_mass=float(sum(prior[list(row)].sum() for row in collisions))
    frozen={TRIANGLES.index(t) for t in FROZEN_23}
    remaining=[i for i in range(120) if i not in frozen]
    base=moderate_channel()
    maps={
        "full_D4":list(range(8)),
        "conjugacy_class_5":[conjugacy_class_id(g) for g in D4],
        "abelianization_V4":[(g[0]%2)*2+g[1] for g in D4],
        "reflection_parity":[g[1] for g in D4],
    }
    results={}
    for name,mapping in maps.items():
        likelihood=coarse_channel(base,mapping)
        stop_error=best_error=0.0
        improved=0
        for collision in collisions:
            mass=float(prior[list(collision)].sum()/collision_mass)
            stop,best=one_probe(collision,full_syndrome,prior,likelihood,remaining)
            stop_error+=mass*stop
            best_error+=mass*best
            improved += best < stop-1e-15
        results[name]={
            "outcomes_including_erasure":likelihood.shape[1],
            "conditional_stop_error":stop_error,
            "conditional_best_one_probe_error":best_error,
            "conditional_risk_reduction":stop_error-best_error,
            "collision_classes_improved":improved,
        }

    expected={
        "full_D4":0.0012229105256245734,
        "conjugacy_class_5":0.0012393612221768486,
        "abelianization_V4":0.002411084033776952,
        "reflection_parity":0.004097881158066848,
    }
    for name,value in expected.items():
        assert abs(results[name]["conditional_best_one_probe_error"]-value)<2e-12

    premium=(results["conjugacy_class_5"]["conditional_best_one_probe_error"]-
             results["full_D4"]["conditional_best_one_probe_error"])
    retained=(results["conjugacy_class_5"]["conditional_risk_reduction"]/
              results["full_D4"]["conditional_risk_reduction"])
    payload={
        "schema":"w33.pass3031.measurement_basis_portfolio.v1",
        "status":"COMPLETE_EXACT_ONE_PROBE_BLACKWELL_FRONTIER_FOR_STATED_CHANNEL",
        "synthetic_channel":"moderate Pass-3025 profile",
        "collision_prior_mass":collision_mass,
        "alphabets":results,
        "blackwell_order":["full_D4","conjugacy_class_5","abelianization_V4","reflection_parity"],
        "conjugacy_sensor_retains_fraction_of_full_risk_reduction":retained,
        "full_sensor_break_even_cost_premium_per_collision_decision":premium,
        "full_sensor_break_even_cost_premium_unconditional":premium*collision_mass,
        "theorem":"Every coarse alphabet is a deterministic post-processing of full D4, so full D4 Blackwell-dominates it. Cost can nevertheless move the optimum to a coarse detector.",
        "design_decision":"Expose detector alphabet as part of the action: choose (triangle, full/class/V4/parity sensor) by expected posterior risk reduction per physical cost.",
        "claim_boundary":"Exact Bayes risks for the explicit moderate synthetic channel and frozen sparse prior, conditional on the exact base collision class. Sensor costs and laboratory confusion matrices are not measured here.",
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":payload["status"],"retained":retained,"premium":premium},sort_keys=True))


if __name__=="__main__":
    main()
