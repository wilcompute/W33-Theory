#!/usr/bin/env python3
"""BT1510: exact undecorated Aut(W33) orbit test plus decorated-action firewall.

This file supplies the next safe step after BT1507.  It computes, in a checkout,
the projective symplectic action on W33 lines and verifies the expected single
orbit on the 540 undecorated skew-line pairs.  It also records why the decorated
triple action (left line, right line, residual key) needs a gauge-cocycle law
before being promoted to an Aut(W33)-canonical theorem.
"""
from __future__ import annotations

import json
import sys
from collections import deque
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

from w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers import build_w33, generate_projective_symplectic_group

OUT = ROOT / "data" / "bt1510_decorated_aut_w33_orbit_scaffold.json"


def induced_line_perm(point_perm: tuple[int, ...], lines: list[tuple[int, int, int, int]], index: dict[tuple[int, ...], int]) -> tuple[int, ...]:
    out = []
    for line in lines:
        image = tuple(sorted(point_perm[p] for p in line))
        out.append(index[image])
    return tuple(out)


def orbit(seed: tuple[int, int], line_perms: list[tuple[int, ...]]) -> set[tuple[int, int]]:
    seen = {seed}
    q = deque([seed])
    while q:
        a, b = q.popleft()
        for g in line_perms:
            x, y = sorted((g[a], g[b]))
            nxt = (x, y)
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    return seen


def main() -> None:
    points, _edges, _edge_index, lines, _adjacency = build_w33()
    line_index = {tuple(line): i for i, line in enumerate(lines)}
    line_sets = [set(line) for line in lines]
    skew_pairs = [(a, b) for a, b in combinations(range(len(lines)), 2) if not (line_sets[a] & line_sets[b])]
    group = generate_projective_symplectic_group(points)
    line_perms = [induced_line_perm(g, lines, line_index) for g in group]
    seed_orbit = orbit(skew_pairs[0], line_perms)
    # Decorated triples have residual keys from a chosen gauge.  Without the gauge
    # cocycle action, residual keys cannot be transported canonically by Aut(W33).
    decorated_status = {
        "triple_shape": "(left_line, right_line, residual_key)",
        "required_missing_law": "Aut(W33) action on residual_key via transported gauge cocycle",
        "promotion_status": "blocked_pending_gauge_cocycle_law",
    }
    checks = {
        "line_count_40": len(lines) == 40,
        "group_order_25920": len(group) == 25920,
        "skew_pair_count_540": len(skew_pairs) == 540,
        "single_undecorated_skew_pair_orbit": len(seed_orbit) == 540,
        "decorated_action_not_promoted": decorated_status["promotion_status"] == "blocked_pending_gauge_cocycle_law",
    }
    result = {
        "bt": 1510,
        "title": "Decorated Aut(W33) orbit scaffold",
        "verified": all(checks.values()),
        "exact_undecorated_result": {"line_count": len(lines), "group_order": len(group), "skew_pair_count": len(skew_pairs), "skew_pair_orbit_count": 1, "seed_orbit_size": len(seed_orbit)},
        "decorated_status": decorated_status,
        "interpretation": "The undecorated 540 skew-line pairs form one Aut(W33) orbit under PSp(4,3).  Therefore BT1504's 7/21/3 split remains a gauge-decorated SAT scaffold until the residual-key gauge cocycle law is supplied.",
        "next_exact_test": "Define the gauge-cocycle action on residual_key, then recompute orbits on decorated triples and test BT1504 classes as unions of those orbits.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1510, "verified": result["verified"], "skew_orbit_size": len(seed_orbit)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
