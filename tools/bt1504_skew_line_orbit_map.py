#!/usr/bin/env python3
"""BT1504: replace the BT1501 edge-index placeholder by a data-derived skew-line map.

The map is built from the actual 540 skew-line residuals produced by BT1367 and
the BT1373 improved S3 gauge labels.  It is a deterministic quotient projection
for the SAT scaffold, not yet a proof of a canonical Aut(W33)-orbit quotient.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

from bt1367_global_qutrit_phase_gauge_holonomy import build_phase_transport, compose_perm, invert_perm, perm_key, perm_order
from bt1373_s3_gauge_synchronization_improved_counterconnection import IMPROVED_GAUGE_LABELS, S3_PERMS

OUT = ROOT / "data" / "bt1504_skew_line_orbit_map.json"
WCNF = ROOT / "proofs" / "bt1504_skew_line_orbit_frontier.wcnf"
MD = ROOT / "proofs" / "BT1504_skew_line_orbit_map.md"

EDGE_VARS = list(range(1, 541))
POINT_VARS = list(range(541, 548))
FLAG_VARS = list(range(548, 569))
FIBER_VARS = list(range(569, 572))
TOP = 541


def one_hot(vars_: list[int]) -> list[list[int]]:
    clauses = [vars_[:]]
    for i, a in enumerate(vars_):
        for b in vars_[i + 1 :]:
            clauses.append([-a, -b])
    return clauses


def build_map() -> tuple[list[dict], Counter[str], Counter[str], Counter[str]]:
    data = build_phase_transport()
    skew_edges = data["skew_edges"]
    transport = data["transport"]
    gauge = {line: S3_PERMS[label] for line, label in enumerate(IMPROVED_GAUGE_LABELS)}
    rows: list[dict] = []
    point_profile: Counter[str] = Counter()
    flag_profile: Counter[str] = Counter()
    fiber_profile: Counter[str] = Counter()
    for edge_index, (left, right) in enumerate(skew_edges):
        residual = compose_perm(invert_perm(gauge[right]), compose_perm(transport[(left, right)], gauge[left]))
        rkey = perm_key(residual)
        rorder = perm_order(residual)
        # Actual-data projection: depends on the true skew endpoints and true residual,
        # not on the edge variable index.  This replaces BT1501's e mod classes.
        point = (left + right + rorder) % 7
        flag = (3 * left + 5 * right + sum(residual)) % 21
        fiber = (S3_PERMS.index(residual) + left + 2 * right) % 3
        row = {
            "edge_index": edge_index,
            "edge_var": edge_index + 1,
            "left_line": left,
            "right_line": right,
            "residual_key": rkey,
            "residual_order": rorder,
            "point_class": point,
            "flag_class": flag,
            "fiber_class": fiber,
            "identity": residual == (0, 1, 2),
        }
        rows.append(row)
        point_profile[str(point)] += 1
        flag_profile[str(flag)] += 1
        fiber_profile[str(fiber)] += 1
    return rows, point_profile, flag_profile, fiber_profile


def main() -> None:
    rows, point_profile, flag_profile, fiber_profile = build_map()
    one_hot_hard = one_hot(POINT_VARS) + one_hot(FLAG_VARS) + one_hot(FIBER_VARS)
    compat = []
    for row in rows:
        e = row["edge_var"]
        compat.append([-e, POINT_VARS[row["point_class"]]])
        compat.append([-e, FLAG_VARS[row["flag_class"]]])
        compat.append([-e, FIBER_VARS[row["fiber_class"]]])
    soft = [[row["edge_var"]] for row in rows]
    hard = one_hot_hard + compat
    WCNF.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "c BT1504 data-derived skew-line quotient WCNF scaffold",
        "c quotient map uses actual BT1367 skew endpoints and BT1373 improved residuals",
        "c still not a solved MaxSAT certificate or canonical Aut(W33)-orbit theorem",
        f"p wcnf 571 {len(soft)+len(hard)} {TOP}",
    ]
    for clause in hard:
        lines.append(f"{TOP} " + " ".join(map(str, clause)) + " 0")
    for clause in soft:
        lines.append("1 " + " ".join(map(str, clause)) + " 0")
    WCNF.write_text("\n".join(lines) + "\n", encoding="utf-8")
    MD.write_text("# BT1504 Skew-line Residual Orbit Map\n\nThis replaces BT1501's edge-index modular placeholder with a map derived from the actual 540 skew-line residuals: endpoints plus improved-gauge S3 residual.  It is still a SAT scaffold, not a solved 330-frontier certificate and not yet a proof of canonical Aut(W33)-orbit classes.\n", encoding="utf-8")
    checks = {
        "actual_skew_edges_540": len(rows) == 540,
        "identity_edges_210": sum(1 for r in rows if r["identity"]) == 210,
        "corrections_330": sum(1 for r in rows if not r["identity"]) == 330,
        "point_classes_all_7": len(point_profile) == 7,
        "flag_classes_all_21": len(flag_profile) == 21,
        "fiber_classes_all_3": len(fiber_profile) == 3,
        "one_hot_hard_237": len(one_hot_hard) == 237,
        "compat_hard_1620": len(compat) == 1620,
        "total_clauses_2397": len(soft) + len(hard) == 2397,
        "wcnf_written": WCNF.exists() and "p wcnf 571 2397 541" in WCNF.read_text(encoding="utf-8"),
    }
    result = {
        "bt": 1504,
        "title": "Skew-line residual quotient map",
        "verified": all(checks.values()),
        "source": "BT1367 actual skew-line transport plus BT1373 improved gauge residuals",
        "frontier": {"skew_edges": len(rows), "identity_edges": sum(1 for r in rows if r["identity"]), "corrections": sum(1 for r in rows if not r["identity"])},
        "profiles": {"point": dict(sorted(point_profile.items(), key=lambda kv: int(kv[0]))), "flag": dict(sorted(flag_profile.items(), key=lambda kv: int(kv[0]))), "fiber": dict(sorted(fiber_profile.items(), key=lambda kv: int(kv[0])))},
        "sample_rows": rows[:12],
        "wcnf": "proofs/bt1504_skew_line_orbit_frontier.wcnf",
        "markdown": "proofs/BT1504_skew_line_orbit_map.md",
        "interpretation": "The SAT quotient map now depends on actual skew-line endpoints and actual S3 residuals instead of edge-index modular placeholders.",
        "honesty_boundary": "This is data-derived and reproducible, but not yet a canonical Aut(W33)-orbit theorem or a solved 330 optimum certificate.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1504, "verified": result["verified"], "edges": len(rows)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
