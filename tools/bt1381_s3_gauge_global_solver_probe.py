#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

from bt1376_s3_gauge_radius3_local_optimum_certificate import build_score_tables, edge_score
from bt1373_s3_gauge_synchronization_improved_counterconnection import IMPROVED_GAUGE_LABELS, S3_PERMS


def total_score(labels: list[int], tables: dict[str, object]) -> int:
    edge_scores = tables["edge_scores"]
    return sum(edge_score(edge_scores, a, b, labels[a], labels[b]) for a, b in tables["edges"])


def coordinate_ascent(labels: list[int], tables: dict[str, object]) -> tuple[list[int], int, int]:
    labels = labels[:]
    labels[0] = 0
    sweeps = 0
    improved = True
    while improved and sweeps < 80:
        improved = False
        sweeps += 1
        for line in range(1, len(labels)):
            current = total_score(labels, tables)
            best_label = labels[line]
            best_score = current
            for trial in range(len(S3_PERMS)):
                if trial == labels[line]:
                    continue
                old = labels[line]
                labels[line] = trial
                score = total_score(labels, tables)
                labels[line] = old
                if score > best_score:
                    best_label = trial
                    best_score = score
            if best_label != labels[line]:
                labels[line] = best_label
                improved = True
    return labels, total_score(labels, tables), sweeps


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--restarts", type=int, default=240)
    ap.add_argument("--seed", type=int, default=1381)
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1381_s3_gauge_global_solver_probe.json")
    ns = ap.parse_args()
    rng = random.Random(ns.seed)
    tables = build_score_tables()
    base = list(IMPROVED_GAUGE_LABELS)
    base_score = total_score(base, tables)
    best_labels = base[:]
    best_score = base_score
    best_source = "BT1373 witness"
    local_optima = {str(base_score): 1}
    for r in range(ns.restarts):
        trial = [0] + [rng.randrange(len(S3_PERMS)) for _ in range(39)]
        labels, score, _sweeps = coordinate_ascent(trial, tables)
        local_optima[str(score)] = local_optima.get(str(score), 0) + 1
        if score > best_score:
            best_score = score
            best_labels = labels
            best_source = f"restart_{r}"
    checks = {
        "constraints_540": len(tables["edges"]) == 540,
        "base_score_210": base_score == 210,
        "root_fixed": best_labels[0] == 0,
        "labels_are_s3": all(0 <= x < len(S3_PERMS) for x in best_labels),
        "no_probe_above_210": best_score <= 210,
        "bt1373_witness_retained": best_score == 210,
    }
    result = {
        "bt": 1381,
        "title": "S3 gauge global solver probe",
        "verified": all(checks.values()),
        "checks": checks,
        "problem": {
            "variables": 40,
            "root_fixed_variables": 39,
            "labels_per_variable": 6,
            "constraints": 540,
            "search_space_root_fixed": "6^39",
            "objective": "maximize identity residual edges"
        },
        "solver": {
            "method": "deterministic random-restart coordinate ascent",
            "seed": ns.seed,
            "restarts": ns.restarts,
            "best_score": best_score,
            "best_source": best_source,
            "best_labels": best_labels,
            "local_optima_histogram": local_optima
        },
        "boundary": "This is a global solver probe, not a proof of global optimality. It found no witness beating 210; BT1379 remains the exact Max-2CSP specification for ILP/SAT/branch-and-bound proof work."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1381, "verified": result["verified"], "best_score": best_score}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
