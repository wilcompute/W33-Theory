#!/usr/bin/env python3
"""BT1373: improved S3 gauge synchronization for the phase counterconnection.

BT1370 flattened the BT1367 S3 connection in the spanning-tree gauge.  That
gauge has 160 identity residual edges and 380 nonidentity corrections.

This verifier asks the sharper synchronization question: can a different
global line gauge make more skew-line transports identity?  Yes.  A concrete
40-line S3 gauge gives 210 identity residual edges, so the spanning-tree
counterconnection is not correction-minimal.

The script intentionally does not claim global optimality.  It records the
verified improvement and a deterministic one-line-local stability certificate:
no single W33 line relabeling improves the 210-edge score.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from bt1367_global_qutrit_phase_gauge_holonomy import (
    ID3,
    build_phase_transport,
    compose_perm,
    invert_perm,
    perm_key,
    perm_order,
    spanning_tree_gauge,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1373_s3_gauge_synchronization_improved_counterconnection.json"

S3_PERMS: tuple[tuple[int, int, int], ...] = (
    (0, 1, 2),
    (0, 2, 1),
    (1, 0, 2),
    (1, 2, 0),
    (2, 0, 1),
    (2, 1, 0),
)

# Found by two independent deterministic local/annealing searches with the
# root line fixed to identity.  The verifier below re-checks every edge.
IMPROVED_GAUGE_LABELS = (
    0,
    4,
    0,
    3,
    3,
    1,
    3,
    0,
    5,
    3,
    1,
    2,
    5,
    2,
    1,
    1,
    2,
    2,
    2,
    1,
    3,
    2,
    0,
    3,
    3,
    0,
    3,
    0,
    5,
    2,
    1,
    1,
    3,
    0,
    5,
    0,
    1,
    1,
    0,
    1,
)


def residual_profile_for_gauge(
    gauge: dict[int, tuple[int, int, int]],
    skew_edges: list[tuple[int, int]],
    transport: dict[tuple[int, int], tuple[int, int, int]],
) -> tuple[Counter[str], Counter[int]]:
    profile: Counter[str] = Counter()
    order_profile: Counter[int] = Counter()
    for left, right in skew_edges:
        residual = compose_perm(
            invert_perm(gauge[right]),
            compose_perm(transport[(left, right)], gauge[left]),
        )
        profile[perm_key(residual)] += 1
        order_profile[perm_order(residual)] += 1
    return profile, order_profile


def local_relabel_deltas(
    labels: tuple[int, ...],
    skew_edges: list[tuple[int, int]],
    transport: dict[tuple[int, int], tuple[int, int, int]],
) -> list[dict[str, int]]:
    perm_index = {perm: i for i, perm in enumerate(S3_PERMS)}
    required: dict[tuple[int, int], list[int]] = {}
    for left, right in skew_edges:
        required[(left, right)] = [
            perm_index[compose_perm(transport[(left, right)], left_label)]
            for left_label in S3_PERMS
        ]
        required[(right, left)] = [
            perm_index[compose_perm(transport[(right, left)], right_label)]
            for right_label in S3_PERMS
        ]

    adjacency = [[] for _ in labels]
    for left, right in skew_edges:
        adjacency[left].append(right)
        adjacency[right].append(left)

    def local_score(line: int, trial_label: int) -> int:
        trial = list(labels)
        trial[line] = trial_label
        score = 0
        for other in adjacency[line]:
            left, right = (line, other) if line < other else (other, line)
            if trial[right] == required[(left, right)][trial[left]]:
                score += 1
        return score

    deltas = []
    for line, current_label in enumerate(labels):
        if line == 0:
            continue
        current_score = local_score(line, current_label)
        for candidate in range(len(S3_PERMS)):
            if candidate == current_label:
                continue
            deltas.append(
                {
                    "line": line,
                    "from_label": current_label,
                    "to_label": candidate,
                    "delta": local_score(line, candidate) - current_score,
                }
            )
    return deltas


def build_result() -> dict[str, object]:
    data = build_phase_transport()
    skew_edges = data["skew_edges"]
    transport = data["transport"]
    skew_adjacency = data["skew_adjacency"]

    tree_gauge, parent = spanning_tree_gauge(skew_adjacency, transport)
    tree_profile, tree_order_profile = residual_profile_for_gauge(
        tree_gauge, skew_edges, transport
    )

    improved_gauge = {
        line: S3_PERMS[label] for line, label in enumerate(IMPROVED_GAUGE_LABELS)
    }
    improved_profile, improved_order_profile = residual_profile_for_gauge(
        improved_gauge, skew_edges, transport
    )
    local_deltas = local_relabel_deltas(IMPROVED_GAUGE_LABELS, skew_edges, transport)
    improving_single_relabels = [row for row in local_deltas if row["delta"] > 0]
    best_single_delta = max(row["delta"] for row in local_deltas)

    tree_identity = tree_profile[perm_key(ID3)]
    improved_identity = improved_profile[perm_key(ID3)]
    tree_corrections = len(skew_edges) - tree_identity
    improved_corrections = len(skew_edges) - improved_identity

    checks = {
        "all_540_skew_edges_used": len(skew_edges) == 540,
        "root_gauge_fixed_to_identity": IMPROVED_GAUGE_LABELS[0] == 0,
        "spanning_tree_gauge_has_160_identity_edges": tree_identity == 160,
        "improved_gauge_has_210_identity_edges": improved_identity == 210,
        "old_380_correction_count_is_not_minimal": improved_corrections
        < tree_corrections,
        "improvement_is_50_fewer_corrections": tree_corrections - improved_corrections
        == 50,
        "single_line_local_search_strictly_stable": not improving_single_relabels
        and best_single_delta < 0,
        "profiles_sum_to_skew_edges": sum(improved_profile.values()) == len(skew_edges),
        "tree_cycle_rank_still_501": len(skew_edges) - (len(parent) - 1) == 501,
    }

    return {
        "bt": 1373,
        "title": "S3 gauge synchronization improves the phase counterconnection",
        "verified": all(checks.values()),
        "spanning_tree_baseline": {
            "identity_edges": tree_identity,
            "nonidentity_corrections": tree_corrections,
            "residual_profile": dict(sorted(tree_profile.items())),
            "residual_order_profile": {
                str(k): v for k, v in sorted(tree_order_profile.items())
            },
        },
        "improved_synchronization_gauge": {
            "labels_in_s3_perm_order": list(IMPROVED_GAUGE_LABELS),
            "identity_edges": improved_identity,
            "nonidentity_corrections": improved_corrections,
            "residual_profile": dict(sorted(improved_profile.items())),
            "residual_order_profile": {
                str(k): v for k, v in sorted(improved_order_profile.items())
            },
            "single_line_relabel_delta_profile": {
                str(k): v
                for k, v in sorted(
                    Counter(row["delta"] for row in local_deltas).items()
                )
            },
            "best_single_line_delta": best_single_delta,
        },
        "interpretation": (
            "The BT1370 spanning-tree counterconnection is a valid flattening "
            "cochain, but it is not a correction-minimal synchronization gauge. "
            "A better global S3 line labeling increases identity residual edges "
            "from 160 to 210 and lowers required corrections from 380 to 330."
        ),
        "boundary": (
            "This proves non-minimality of the old count and local stability of "
            "the 210-edge witness.  It does not prove that 330 is the global "
            "minimum over all 6^39 root-fixed S3 gauges."
        ),
        "checks": checks,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ns = ap.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "baseline_corrections": result["spanning_tree_baseline"][
                    "nonidentity_corrections"
                ],
                "improved_corrections": result["improved_synchronization_gauge"][
                    "nonidentity_corrections"
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
