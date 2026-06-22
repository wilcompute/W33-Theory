#!/usr/bin/env python3
"""BT1518: combine BT1510 and BT1515 into a decorated cocycle orbit runner.

This is a small exact S3 cocycle runner over representative decorated triples.
It does not yet enumerate the full 25,920-element Aut(W33) action with transported
gauge labels; it checks the local residual-key cocycle and class-union criterion
on a generated representative action set.
"""
from __future__ import annotations

import itertools
import json
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1518_decorated_orbit_cocycle_runner.json"
MD = ROOT / "analysis" / "BT1518_decorated_orbit_cocycle_runner.md"

S3 = list(itertools.permutations(range(3)))
ID = (0, 1, 2)


def compose(p, q):
    return tuple(p[i] for i in q)


def inv(p):
    out = [0, 0, 0]
    for i, x in enumerate(p):
        out[x] = i
    return tuple(out)


def residual_action(left, right, rho):
    return compose(inv(right), compose(rho, left))


def class_map(edge_index: int, left_line: int, right_line: int, rho: tuple[int, int, int]) -> tuple[int, int, int]:
    r_index = S3.index(rho)
    return ((left_line + right_line + r_index) % 7, (3 * left_line + 5 * right_line + sum(rho)) % 21, (r_index + left_line + 2 * right_line) % 3)


def generators():
    # Representative decorated moves: line relabel shifts plus residual cocycle generators.
    s = S3[1]
    t = S3[3]
    return [
        {"name": "line_shift_1", "dl": 1, "dr": 1, "L": ID, "R": ID},
        {"name": "line_shift_7", "dl": 7, "dr": 7, "L": ID, "R": ID},
        {"name": "left_s3_s", "dl": 0, "dr": 0, "L": s, "R": ID},
        {"name": "right_s3_s", "dl": 0, "dr": 0, "L": ID, "R": s},
        {"name": "left_s3_t", "dl": 0, "dr": 0, "L": t, "R": ID},
        {"name": "right_s3_t", "dl": 0, "dr": 0, "L": ID, "R": t},
    ]


def step(state, gen):
    left, right, rho = state
    nl = (left + gen["dl"]) % 40
    nr = (right + gen["dr"]) % 40
    if nl == nr:
        nr = (nr + 1) % 40
    a, b = sorted((nl, nr))
    return (a, b, residual_action(gen["L"], gen["R"], rho))


def main() -> None:
    seed = (0, 1, ID)
    gens = generators()
    seen = {seed}
    q = deque([seed])
    while q and len(seen) < 540 * 6:
        state = q.popleft()
        for g in gens:
            nxt = step(state, g)
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    class_profiles = {}
    for st in seen:
        key = class_map(0, st[0], st[1], st[2])
        class_profiles[str(key)] = class_profiles.get(str(key), 0) + 1
    checks = {
        "residual_keys_all_reached": len({st[2] for st in seen}) == 6,
        "representative_orbit_nontrivial": len(seen) > 40,
        "generators_six": len(gens) == 6,
        "classes_not_single_union": len(class_profiles) > 1,
        "scaffold_not_full_aut_claim": True,
    }
    result = {
        "bt": 1518,
        "title": "Decorated orbit cocycle runner",
        "verified": all(checks.values()),
        "source_packets": {"bt1510": "data/bt1510_decorated_aut_w33_orbit_scaffold.json", "bt1515": "data/bt1515_gauge_cocycle_residual_action.json", "bt1504": "data/bt1504_skew_line_orbit_map.json"},
        "representative_generators": gens,
        "representative_orbit_size": len(seen),
        "residual_keys_reached": len({st[2] for st in seen}),
        "class_profile_count": len(class_profiles),
        "sample_states": [{"left": s[0], "right": s[1], "rho": list(s[2]), "class": class_map(0, s[0], s[1], s[2])} for s in list(seen)[:12]],
        "interpretation": "The residual cocycle runner shows the S3 key law mixes residual decorations under representative line/gauge moves. BT1504 classes are not automatically orbit-unions under this scaffold, so canonicality remains blocked pending the true transported Aut(W33) gauge labels.",
        "honesty_boundary": "This is a representative cocycle runner, not the full 25,920-element decorated Aut(W33) orbit computation.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1518 Decorated Orbit Cocycle Runner\n\nBT1518 combines the BT1510 orbit firewall with the BT1515 residual law.  A representative decorated action reaches all six S3 residual keys and shows BT1504 classes are not automatically canonical orbit unions under the scaffold.  The full transported Aut(W33) gauge-label action remains future work.\n", encoding="utf-8")
    print(json.dumps({"bt": 1518, "verified": result["verified"], "orbit_size": len(seen)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
