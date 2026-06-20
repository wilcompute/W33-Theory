#!/usr/bin/env python3
"""BT1376: radius-3 local optimality certificate for the BT1373 S3 gauge.

BT1373 found a root-fixed S3 gauge with 210 identity residual edges and 330
corrections.  Its verifier proved strict one-line stability only.

This verifier strengthens the optimization frontier without claiming global
optimality: it exhaustively checks every root-fixed relabeling of one, two, or
three W33 lines around the BT1373 witness.  Every such move strictly decreases
the identity-edge score; the best radius-1/2/3 move has delta -5.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from typing import Iterable

from bt1367_global_qutrit_phase_gauge_holonomy import (
    build_phase_transport,
    compose_perm,
)
from bt1373_s3_gauge_synchronization_improved_counterconnection import (
    IMPROVED_GAUGE_LABELS,
    S3_PERMS,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1376_s3_gauge_radius3_local_optimum_certificate.json"


def edge_score(
    edge_scores: dict[tuple[int, int], list[list[int]]],
    left: int,
    right: int,
    left_label: int,
    right_label: int,
) -> int:
    """Return 1 iff the oriented edge is identity-satisfied by two labels."""
    if left < right:
        return edge_scores[(left, right)][left_label][right_label]
    return edge_scores[(right, left)][right_label][left_label]


def build_score_tables() -> dict[str, object]:
    data = build_phase_transport()
    edges: list[tuple[int, int]] = data["skew_edges"]
    transport = data["transport"]
    perm_index = {perm: index for index, perm in enumerate(S3_PERMS)}

    adjacency: list[set[int]] = [set() for _ in range(len(IMPROVED_GAUGE_LABELS))]
    edge_scores: dict[tuple[int, int], list[list[int]]] = {}
    for left, right in edges:
        matrix = [[0 for _ in S3_PERMS] for _ in S3_PERMS]
        for left_label, left_perm in enumerate(S3_PERMS):
            right_label = perm_index[compose_perm(transport[(left, right)], left_perm)]
            matrix[left_label][right_label] = 1
        edge_scores[(left, right)] = matrix
        adjacency[left].add(right)
        adjacency[right].add(left)

    labels = list(IMPROVED_GAUGE_LABELS)
    base_scores = [[0 for _ in S3_PERMS] for _ in labels]
    for line in range(len(labels)):
        for label in range(len(S3_PERMS)):
            base_scores[line][label] = sum(
                edge_score(edge_scores, line, other, label, labels[other])
                for other in adjacency[line]
            )

    current_edge_scores = {
        edge: edge_score(
            edge_scores, edge[0], edge[1], labels[edge[0]], labels[edge[1]]
        )
        for edge in edges
    }

    return {
        "edges": edges,
        "adjacency": adjacency,
        "edge_scores": edge_scores,
        "base_scores": base_scores,
        "current_edge_scores": current_edge_scores,
        "labels": labels,
    }


def strict_relabel_assignments(
    subset: tuple[int, ...], labels: list[int]
) -> Iterable[tuple[int, ...]]:
    for trial in product(range(len(S3_PERMS)), repeat=len(subset)):
        if all(trial[index] == labels[line] for index, line in enumerate(subset)):
            continue
        yield trial


def scan_radius(radius: int, tables: dict[str, object]) -> dict[str, object]:
    edges: list[tuple[int, int]] = tables["edges"]  # type: ignore[assignment]
    adjacency: list[set[int]] = tables["adjacency"]  # type: ignore[assignment]
    edge_scores = tables["edge_scores"]  # type: ignore[assignment]
    base_scores: list[list[int]] = tables["base_scores"]  # type: ignore[assignment]
    current_edge_scores: dict[tuple[int, int], int] = tables[
        "current_edge_scores"
    ]  # type: ignore[assignment]
    labels: list[int] = tables["labels"]  # type: ignore[assignment]

    profile: Counter[int] = Counter()
    best_delta: int | None = None
    best_examples: list[dict[str, object]] = []
    checked = 0

    # Line 0 remains fixed to identity; this removes the global S3 gauge
    # symmetry and matches the BT1373 witness convention.
    for subset in combinations(range(1, len(labels)), radius):
        subset_set = set(subset)
        current_affected_score = sum(
            current_edge_scores[edge]
            for edge in edges
            if edge[0] in subset_set or edge[1] in subset_set
        )
        internal_edges = [
            (left, right)
            for index, left in enumerate(subset)
            for right in subset[index + 1 :]
            if right in adjacency[left]
        ]

        for trial in strict_relabel_assignments(subset, labels):
            assignment = dict(zip(subset, trial, strict=True))
            affected_score = sum(base_scores[line][assignment[line]] for line in subset)

            for left, right in internal_edges:
                left_trial = assignment[left]
                right_trial = assignment[right]
                affected_score -= edge_score(
                    edge_scores, left, right, left_trial, labels[right]
                )
                affected_score -= edge_score(
                    edge_scores, left, right, labels[left], right_trial
                )
                affected_score += edge_score(
                    edge_scores, left, right, left_trial, right_trial
                )

            delta = affected_score - current_affected_score
            checked += 1
            profile[delta] += 1
            if best_delta is None or delta > best_delta:
                best_delta = delta
                best_examples = [
                    {
                        "lines": list(subset),
                        "trial_labels": list(trial),
                        "delta": delta,
                    }
                ]
            elif delta == best_delta and len(best_examples) < 8:
                best_examples.append(
                    {
                        "lines": list(subset),
                        "trial_labels": list(trial),
                        "delta": delta,
                    }
                )

    if best_delta is None:
        raise AssertionError(f"no radius-{radius} relabels checked")

    return {
        "radius": radius,
        "candidate_relabels_checked": checked,
        "best_delta": best_delta,
        "best_alternative_identity_edges": 210 + best_delta,
        "delta_profile": {str(key): value for key, value in sorted(profile.items())},
        "best_examples": best_examples,
    }


def build_result(max_radius: int = 3) -> dict[str, object]:
    if max_radius < 1 or max_radius > 3:
        raise ValueError("max_radius must be in 1..3 for this exhaustive certificate")

    tables = build_score_tables()
    radius_results = [
        scan_radius(radius, tables) for radius in range(1, max_radius + 1)
    ]
    total_checked = sum(
        int(result["candidate_relabels_checked"]) for result in radius_results
    )

    checks = {
        "bt1373_identity_edge_score_is_210": sum(
            tables["current_edge_scores"].values()  # type: ignore[union-attr]
        )
        == 210,
        "root_line_fixed_to_identity": IMPROVED_GAUGE_LABELS[0] == 0,
        "all_540_skew_edges_used": len(tables["edges"]) == 540,  # type: ignore[arg-type]
        "radius_1_checked_195_candidates": radius_results[0][
            "candidate_relabels_checked"
        ]
        == 195,
        "all_requested_radii_strictly_decrease_score": all(
            int(result["best_delta"]) < 0 for result in radius_results
        ),
        "best_radius_delta_is_minus_5": all(
            result["best_delta"] == -5 for result in radius_results
        ),
    }
    if max_radius >= 2:
        checks["radius_2_checked_25935_candidates"] = (
            radius_results[1]["candidate_relabels_checked"] == 25935
        )
    if max_radius >= 3:
        checks["radius_3_checked_1964885_candidates"] = (
            radius_results[2]["candidate_relabels_checked"] == 1964885
        )

    return {
        "bt": 1376,
        "title": "Radius-3 local optimum certificate for the S3 synchronization gauge",
        "verified": all(checks.values()),
        "base_witness": {
            "source": "BT1373 improved S3 synchronization gauge",
            "identity_edges": 210,
            "nonidentity_corrections": 330,
            "root_fixed_line": 0,
            "labels_in_s3_perm_order": list(IMPROVED_GAUGE_LABELS),
        },
        "local_certificate": {
            "max_radius": max_radius,
            "total_candidate_relabels_checked": total_checked,
            "radii": radius_results,
        },
        "interpretation": (
            "The BT1373 330-correction witness is a strict root-fixed local "
            "minimum through radius 3: changing any one, two, or three line "
            "labels lowers the identity-edge score by at least five."
        ),
        "boundary": (
            "This is an exhaustive local certificate, not a global optimum "
            "proof over all 6^39 root-fixed S3 gauges."
        ),
        "checks": checks,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--max-radius", type=int, default=3)
    ns = ap.parse_args()
    result = build_result(max_radius=ns.max_radius)
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "identity_edges": result["base_witness"]["identity_edges"],
                "corrections": result["base_witness"]["nonidentity_corrections"],
                "total_candidate_relabels_checked": result["local_certificate"][
                    "total_candidate_relabels_checked"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
