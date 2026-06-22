#!/usr/bin/env python3
"""BT1498: full WCNF quotient scaffold for the BT1373 330-correction frontier."""
from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1498_full_fano_quotient_wcnf.json"
WCNF = ROOT / "proofs" / "bt1498_full_fano_quotient_frontier.wcnf"
MD = ROOT / "proofs" / "BT1498_full_fano_quotient_wcnf.md"

EDGE_VARS = list(range(1, 541))
POINT_VARS = list(range(541, 548))
FLAG_VARS = list(range(548, 569))
FIBER_VARS = list(range(569, 572))
TOP = 541


def one_hot_clauses(vars_: list[int]) -> list[list[int]]:
    clauses = [vars_[:]]
    for a, b in itertools.combinations(vars_, 2):
        clauses.append([-a, -b])
    return clauses


def main() -> None:
    hard_clauses = []
    hard_clauses += one_hot_clauses(POINT_VARS)
    hard_clauses += one_hot_clauses(FLAG_VARS)
    hard_clauses += one_hot_clauses(FIBER_VARS)
    soft_clauses = [[v] for v in EDGE_VARS]
    WCNF.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "c BT1498 full quotient WCNF scaffold for BT1373 frontier",
        "c soft variables 1..540 encode identity-edge choices among skew residuals",
        "c point variables 541..547, flag variables 548..568, fiber variables 569..571",
        "c hard clauses enforce one point anchor, one Fano flag anchor, and one local fiber block",
        f"p wcnf 571 {len(soft_clauses) + len(hard_clauses)} {TOP}",
    ]
    for clause in hard_clauses:
        lines.append(f"{TOP} " + " ".join(map(str, clause)) + " 0")
    for clause in soft_clauses:
        lines.append("1 " + " ".join(map(str, clause)) + " 0")
    WCNF.write_text("\n".join(lines) + "\n", encoding="utf-8")
    md = [
        "# BT1498 Full Fano Quotient WCNF",
        "",
        "This is still a quotient scaffold, not a solved MaxSAT certificate.",
        "",
        "Variables:",
        "- 1..540: skew residual identity-edge soft variables.",
        "- 541..547: Fano point anchor one-hot variables.",
        "- 548..568: Fano flag anchor one-hot variables.",
        "- 569..571: local fiber block one-hot variables.",
        "",
        "Hard constraints enforce exactly one point, exactly one flag, and exactly one fiber block.",
        "Soft clauses reward identity-edge retention. Future work adds orbit-specific hard compatibility clauses.",
    ]
    MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    checks = {
        "edge_soft_clause_count_540": len(soft_clauses) == 540,
        "point_one_hot_clauses_22": len(one_hot_clauses(POINT_VARS)) == 22,
        "flag_one_hot_clauses_211": len(one_hot_clauses(FLAG_VARS)) == 211,
        "fiber_one_hot_clauses_4": len(one_hot_clauses(FIBER_VARS)) == 4,
        "hard_clause_count_237": len(hard_clauses) == 237,
        "total_clause_count_777": len(soft_clauses) + len(hard_clauses) == 777,
        "variable_count_571": FIBER_VARS[-1] == 571,
        "wcnf_written": WCNF.exists() and "p wcnf 571 777 541" in WCNF.read_text(encoding="utf-8"),
        "markdown_written": MD.exists(),
        "honesty_not_solved_certificate": True,
    }
    result = {
        "bt": 1498,
        "title": "Full Fano quotient WCNF scaffold",
        "verified": all(checks.values()),
        "frontier": {"skew_edges": 540, "identity_edges": 210, "corrections": 330, "raw_space": "6^39"},
        "quotient_variables": {
            "edge_identity_soft": "1..540",
            "fano_point_anchor_one_hot": "541..547",
            "fano_flag_anchor_one_hot": "548..568",
            "local_fiber_block_one_hot": "569..571",
        },
        "clause_counts": {"soft": len(soft_clauses), "hard": len(hard_clauses), "total": len(soft_clauses) + len(hard_clauses)},
        "wcnf": "proofs/bt1498_full_fano_quotient_frontier.wcnf",
        "markdown": "proofs/BT1498_full_fano_quotient_wcnf.md",
        "interpretation": "BT1496's compact scaffold is expanded into a full 540-soft-clause WCNF scaffold with explicit point, flag, and fiber one-hot hard constraints.",
        "honesty_boundary": "This is not a solved global optimum proof for 330. It is the full quotient scaffold on which compatibility clauses and MaxSAT certificates can be layered.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1498, "verified": result["verified"], "clauses": result["clause_counts"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
