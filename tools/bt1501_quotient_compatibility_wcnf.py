#!/usr/bin/env python3
"""BT1501: add orbit-compatibility hard clauses to the Fano quotient WCNF scaffold.

This is still a certificate scaffold.  It makes point/flag/fiber choices constrain
the 540 soft identity-edge variables, but it does not import a solved MaxSAT
certificate.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1501_quotient_compatibility_wcnf.json"
WCNF = ROOT / "proofs" / "bt1501_quotient_compatibility_frontier.wcnf"
MD = ROOT / "proofs" / "BT1501_quotient_compatibility_wcnf.md"

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


def quotient_index(edge_var: int) -> dict[str, int]:
    edge = edge_var - 1
    return {
        "point": edge % 7,
        "flag": edge % 21,
        "fiber": edge % 3,
    }


def compatibility_clauses() -> list[list[int]]:
    clauses: list[list[int]] = []
    for e in EDGE_VARS:
        q = quotient_index(e)
        # If an edge is selected as an identity edge, it must be compatible with
        # the chosen point, flag, and local fiber quotient class.
        clauses.append([-e, POINT_VARS[q["point"]]])
        clauses.append([-e, FLAG_VARS[q["flag"]]])
        clauses.append([-e, FIBER_VARS[q["fiber"]]])
    return clauses


def main() -> None:
    one_hot = one_hot_clauses(POINT_VARS) + one_hot_clauses(FLAG_VARS) + one_hot_clauses(FIBER_VARS)
    compat = compatibility_clauses()
    soft = [[v] for v in EDGE_VARS]
    hard = one_hot + compat
    lines = [
        "c BT1501 quotient compatibility WCNF scaffold",
        "c soft vars 1..540 reward identity-edge choices",
        "c point vars 541..547, flag vars 548..568, fiber vars 569..571",
        "c hard clauses: one-hot anchors plus edge->point/flag/fiber compatibility",
        f"p wcnf 571 {len(soft) + len(hard)} {TOP}",
    ]
    for clause in hard:
        lines.append(f"{TOP} " + " ".join(map(str, clause)) + " 0")
    for clause in soft:
        lines.append("1 " + " ".join(map(str, clause)) + " 0")
    WCNF.parent.mkdir(parents=True, exist_ok=True)
    WCNF.write_text("\n".join(lines) + "\n", encoding="utf-8")
    md = [
        "# BT1501 Quotient Compatibility WCNF",
        "",
        "This file adds hard quotient-compatibility implications to the BT1498 scaffold.",
        "It is not a solved MaxSAT certificate.",
        "",
        "Clause families:",
        "- 540 soft unit clauses reward identity-edge choices.",
        "- 237 one-hot hard clauses select one Fano point, one Fano flag, and one local fiber block.",
        "- 1620 compatibility hard clauses make each selected edge imply its point, flag, and fiber class.",
        "",
        "The next layer is to replace the modular placeholder quotient map by the true skew-line orbit map and import a solver certificate.",
    ]
    MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    checks = {
        "edge_soft_clause_count_540": len(soft) == 540,
        "one_hot_hard_count_237": len(one_hot) == 237,
        "compatibility_clause_count_1620": len(compat) == 3 * 540,
        "total_hard_count_1857": len(hard) == 1857,
        "total_clause_count_2397": len(soft) + len(hard) == 2397,
        "variable_count_571": FIBER_VARS[-1] == 571,
        "top_weight_blocks_all_soft_gain": TOP == len(soft) + 1,
        "wcnf_written": WCNF.exists() and "p wcnf 571 2397 541" in WCNF.read_text(encoding="utf-8"),
        "markdown_written": MD.exists(),
        "not_solver_certificate": True,
    }
    result = {
        "bt": 1501,
        "title": "Quotient compatibility WCNF scaffold",
        "verified": all(checks.values()),
        "status": "compatibility_scaffold_not_solved_certificate",
        "frontier": {"skew_edges": 540, "identity_edges": 210, "corrections": 330, "raw_space": "6^39"},
        "variables": {
            "edge_identity_soft": "1..540",
            "fano_point_anchor": "541..547",
            "fano_flag_anchor": "548..568",
            "local_fiber_block": "569..571",
        },
        "clause_counts": {"soft": len(soft), "one_hot_hard": len(one_hot), "compatibility_hard": len(compat), "hard_total": len(hard), "total": len(soft) + len(hard)},
        "compatibility_rule": "edge_identity(e) implies point(e mod 7), flag(e mod 21), and fiber(e mod 3) for the scaffold quotient map",
        "wcnf": "proofs/bt1501_quotient_compatibility_frontier.wcnf",
        "markdown": "proofs/BT1501_quotient_compatibility_wcnf.md",
        "interpretation": "The quotient choices now constrain the 540 edge identity variables.  This is the first SAT frontier where point/flag/fiber selections are not merely metadata.",
        "honesty_boundary": "The modular quotient map is a deterministic scaffold map, not the final true skew-line orbit map.  No global optimum certificate for 330 is claimed.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1501, "verified": result["verified"], "clauses": result["clause_counts"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
