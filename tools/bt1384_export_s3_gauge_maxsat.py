#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

from bt1376_s3_gauge_radius3_local_optimum_certificate import build_score_tables, edge_score
from bt1373_s3_gauge_synchronization_improved_counterconnection import IMPROVED_GAUGE_LABELS, S3_PERMS

LINES = 40
LABELS = 6


def xvar(line: int, label: int) -> int:
    return line * LABELS + label + 1


def svar(edge_index: int) -> int:
    return LINES * LABELS + edge_index + 1


def build_wcnf(out_path: Path) -> dict[str, int | str]:
    tables = build_score_tables()
    edges = tables["edges"]
    edge_scores = tables["edge_scores"]
    label_vars = LINES * LABELS
    sat_vars = len(edges)
    total_vars = label_vars + sat_vars
    top = sat_vars + 1
    hard: list[list[int]] = []
    soft: list[list[int]] = []

    for line in range(LINES):
        hard.append([xvar(line, label) for label in range(LABELS)])
        for a in range(LABELS):
            for b in range(a + 1, LABELS):
                hard.append([-xvar(line, a), -xvar(line, b)])

    hard.append([xvar(0, 0)])
    for label in range(1, LABELS):
        hard.append([-xvar(0, label)])

    for e, (left, right) in enumerate(edges):
        sv = svar(e)
        for ll in range(LABELS):
            for rr in range(LABELS):
                ok = edge_score(edge_scores, left, right, ll, rr)
                hard.append([-xvar(left, ll), -xvar(right, rr), sv if ok else -sv])
        soft.append([sv])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        fh.write(f"p wcnf {total_vars} {len(hard) + len(soft)} {top}\n")
        for clause in hard:
            fh.write(f"{top} " + " ".join(map(str, clause)) + " 0\n")
        for clause in soft:
            fh.write("1 " + " ".join(map(str, clause)) + " 0\n")

    witness_score = sum(edge_score(edge_scores, a, b, IMPROVED_GAUGE_LABELS[a], IMPROVED_GAUGE_LABELS[b]) for a, b in edges)
    return {
        "variables": total_vars,
        "label_variables": label_vars,
        "satisfaction_variables": sat_vars,
        "hard_clauses": len(hard),
        "soft_clauses": len(soft),
        "clauses": len(hard) + len(soft),
        "top_weight": top,
        "constraints": len(edges),
        "bt1373_witness_score": witness_score,
        "wcnf_path": str(out_path.relative_to(ROOT)),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wcnf", type=Path, default=ROOT / "data" / "generated" / "bt1384_s3_gauge_maxsat.wcnf")
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1384_s3_gauge_maxsat_manifest.json")
    ns = ap.parse_args()
    stats = build_wcnf(ns.wcnf)
    checks = {
        "forty_lines": LINES == 40,
        "six_labels": LABELS == 6,
        "variables_780": stats["variables"] == 780,
        "constraints_540": stats["constraints"] == 540,
        "soft_clauses_540": stats["soft_clauses"] == 540,
        "hard_clauses_20086": stats["hard_clauses"] == 20086,
        "witness_score_210": stats["bt1373_witness_score"] == 210,
    }
    result = {
        "bt": 1384,
        "title": "Exact S3 gauge MaxSAT export",
        "verified": all(checks.values()),
        "format": "weighted partial MaxSAT WCNF",
        "checks": checks,
        "stats": stats,
        "objective": "maximize satisfied S3 identity-residual edge variables over the 540 W33 skew-line constraints",
        "boundary": "This exports the exact root-fixed MaxSAT instance. It does not solve global optimality by itself."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1384, "verified": result["verified"], "variables": stats["variables"], "clauses": stats["clauses"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
