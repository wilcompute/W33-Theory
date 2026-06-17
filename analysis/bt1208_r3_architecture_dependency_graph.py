#!/usr/bin/env python3
"""BT1208 -- R3 / architecture dependency graph verifier.

BT1202 says R3 is a convergence residual, not an architecture gap.  This script
turns that claim into a small directed-dependency certificate.

The graph has one finite seed and two downstream continuum branches:
  finite_w33_seed -> symplectic_cv_computer
  finite_w33_seed -> metric_k3_spacetime

The holonet demonstrator and GKP/Steinberg fault-tolerant stack depend on the
symplectic/CV branch.  The spacetime claim depends on the metric/K3 branch.  The
verifier checks that removing the metric branch does not cut the demonstrator or
fault-tolerant-computer targets from the finite seed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections import defaultdict, deque

NODES = [
    "finite_w33_seed",
    "lambda_lock",
    "symplectic_cv_computer",
    "single_photon_demonstrator",
    "gkp_steinberg_fault_tolerant_stack",
    "metric_k3_spacetime",
    "r3_convergence_checklist",
    "spacetime_continuum_claim",
]

EDGES = [
    ("finite_w33_seed", "lambda_lock"),
    ("finite_w33_seed", "symplectic_cv_computer"),
    ("lambda_lock", "single_photon_demonstrator"),
    ("symplectic_cv_computer", "single_photon_demonstrator"),
    ("symplectic_cv_computer", "gkp_steinberg_fault_tolerant_stack"),
    ("finite_w33_seed", "metric_k3_spacetime"),
    ("metric_k3_spacetime", "r3_convergence_checklist"),
    ("r3_convergence_checklist", "spacetime_continuum_claim"),
]

COMPUTER_TARGETS = [
    "single_photon_demonstrator",
    "gkp_steinberg_fault_tolerant_stack",
]

SPACETIME_TARGETS = ["spacetime_continuum_claim"]


def reachable(edges: list[tuple[str, str]], source: str, removed: set[str] | None = None) -> set[str]:
    removed = removed or set()
    graph: dict[str, list[str]] = defaultdict(list)
    for a, b in edges:
        if a not in removed and b not in removed:
            graph[a].append(b)
    seen = set()
    if source in removed:
        return seen
    q = deque([source])
    while q:
        node = q.popleft()
        if node in seen:
            continue
        seen.add(node)
        q.extend(graph[node])
    return seen


def build_result() -> dict:
    baseline = reachable(EDGES, "finite_w33_seed")
    without_metric = reachable(EDGES, "finite_w33_seed", {"metric_k3_spacetime", "r3_convergence_checklist", "spacetime_continuum_claim"})
    without_symplectic = reachable(EDGES, "finite_w33_seed", {"symplectic_cv_computer"})
    without_lambda = reachable(EDGES, "finite_w33_seed", {"lambda_lock"})

    result = {
        "bt": 1208,
        "title": "R3 architecture dependency graph theorem",
        "nodes": NODES,
        "edges": EDGES,
        "baseline_reachable": sorted(baseline),
        "computer_targets": COMPUTER_TARGETS,
        "spacetime_targets": SPACETIME_TARGETS,
        "remove_metric_branch": {
            "removed": ["metric_k3_spacetime", "r3_convergence_checklist", "spacetime_continuum_claim"],
            "reachable": sorted(without_metric),
            "computer_targets_still_reachable": all(t in without_metric for t in COMPUTER_TARGETS),
            "spacetime_targets_reachable": all(t in without_metric for t in SPACETIME_TARGETS),
        },
        "remove_symplectic_computer_branch": {
            "removed": ["symplectic_cv_computer"],
            "reachable": sorted(without_symplectic),
            "computer_targets_still_reachable": all(t in without_symplectic for t in COMPUTER_TARGETS),
        },
        "remove_lambda_lock": {
            "removed": ["lambda_lock"],
            "reachable": sorted(without_lambda),
            "demonstrator_still_has_symplectic_path": "single_photon_demonstrator" in without_lambda,
            "lambda_specific_tests_reachable": "lambda_lock" in without_lambda,
        },
        "theorem": "The metric/R3 branch is downstream of the finite seed but not upstream of the holonet computer branch. Removing R3 removes the spacetime-continuum claim while preserving reachability of both computer targets.",
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("data/bt1208_r3_architecture_dependency_graph.json"))
    args = parser.parse_args()
    result = build_result()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "bt": result["bt"],
        "metric_removal_preserves_computer": result["remove_metric_branch"]["computer_targets_still_reachable"],
        "symplectic_removal_preserves_computer": result["remove_symplectic_computer_branch"]["computer_targets_still_reachable"],
        "out": str(args.out),
    }, indent=2))


if __name__ == "__main__":
    main()
