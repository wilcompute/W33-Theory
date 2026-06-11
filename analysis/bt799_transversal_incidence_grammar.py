#!/usr/bin/env python3
"""
BT799 - The four-transversal incidence grammar.

BT798 identified the residual tetrahedral 48-packet as the four common
transversal lines of the base skew-pair chart.  BT799 reads the nearby rank-32
packets by how their two target lines meet those four transversals.

This separates the live face sheets, handle octet, live edge packet, shadow
edge packet, and face connectors by a small grammar over symbols:

    00 = misses a transversal
    10 = first target line meets it
    01 = second target line meets it
    11 = both target lines meet it

The key result is R11:

    R11 = one 11 plus three 00.

So the handle octet is exactly the packet that selects one common transversal
and bridges both target lines through it.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

from bt787_rank4_incidence_r11_handle import compute_rank32
from bt798_residual_tetrahedral_carrier import common_transversals


ROOT = Path(__file__).resolve().parents[1]


def signature_for_skew_pair(geom, transversals, pair):
    a, b = pair
    sig = []
    for row in transversals:
        line = set(row["points"])
        sig.append((len(line & geom["line_sets"][a]), len(line & geom["line_sets"][b])))
    return tuple(sig)


def profile_for_orbit(rank32, transversals, orbit_id):
    geom = rank32["geometry"]
    profile = Counter()
    examples = []
    for skew_index in rank32["orbits"][orbit_id]:
        pair = geom["skew"][skew_index]
        sig = signature_for_skew_pair(geom, transversals, pair)
        canonical = tuple(sorted(sig))
        profile[canonical] += 1
        if len(examples) < 3:
            examples.append({
                "target_skew_pair": list(pair),
                "signature_by_transversal": [list(x) for x in sig],
            })
    return {
        "orbit": orbit_id,
        "size": len(rank32["orbits"][orbit_id]),
        "profile": {
            str(tuple(tuple(x) for x in key)): count
            for key, count in sorted(profile.items(), key=lambda kv: str(kv[0]))
        },
        "examples": examples,
    }


def shorthand(profile):
    assert len(profile["profile"]) == 1 or profile["orbit"] in (9, 10)
    if profile["orbit"] in (9, 10):
        return "face_sheet: anchored side meets all four transversals, other side meets one"
    key = next(iter(profile["profile"]))
    if key == "((0, 0), (0, 0), (0, 0), (1, 1))":
        return "handle: one transversal bridges both target lines"
    if key == "((1, 0), (1, 0), (1, 0), (1, 0))":
        return "live_edge: one target line is the base-side anchor"
    if key == "((0, 0), (0, 0), (0, 0), (0, 0))":
        return "shadow_edge: both target lines miss the transversal tetrad"
    if key == "((0, 0), (0, 0), (0, 1), (1, 0))":
        return "face_connector: two separate one-sided transversal hits"
    return "unclassified"


def main():
    rank32 = compute_rank32()
    geom = rank32["geometry"]
    base_a, base_b = geom["skew"][0]
    transversals = common_transversals(geom, base_a, base_b)
    watched_orbits = [9, 10, 11, 12, 13, 24, 26]

    rows = {}
    for orbit_id in watched_orbits:
        row = profile_for_orbit(rank32, transversals, orbit_id)
        row["grammar_role"] = shorthand(row)
        rows[f"R{orbit_id:02d}"] = row

    checks = {
        "four_common_transversals": len(transversals) == 4,
        "R11_is_one_11_three_00": rows["R11"]["profile"] == {"((0, 0), (0, 0), (0, 0), (1, 1))": 8},
        "R12_is_four_10": rows["R12"]["profile"] == {"((1, 0), (1, 0), (1, 0), (1, 0))": 12},
        "R13_is_four_00": rows["R13"]["profile"] == {"((0, 0), (0, 0), (0, 0), (0, 0))": 12},
        "R24_is_split_one_sided_connector": rows["R24"]["profile"] == {"((0, 0), (0, 0), (0, 1), (1, 0))": 12},
        "R26_is_split_one_sided_connector": rows["R26"]["profile"] == {"((0, 0), (0, 0), (0, 1), (1, 0))": 12},
        "R09_face_sheet_has_two_mirrors": sorted(rows["R09"]["profile"].values()) == [4, 4],
        "R10_face_sheet_has_two_mirrors": sorted(rows["R10"]["profile"].values()) == [4, 4],
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT799 check failed: {name}")

    out = {
        "theorem": "BT799 four-transversal incidence grammar",
        "base_skew_pair": [base_a, base_b],
        "transversal_lines": [
            {
                "line_id": row["line_id"],
                "points": list(row["points"]),
                "base_points": list(row["base_points"]),
                "shadow_points": list(row["shadow_points"]),
            }
            for row in transversals
        ],
        "symbol_legend": {
            "00": "target pair misses this transversal",
            "10": "first target line meets this transversal",
            "01": "second target line meets this transversal",
            "11": "both target lines meet this transversal",
        },
        "orbit_grammar": rows,
        "interpretation": {
            "R11": "the handle octet is exactly the one-transversal double-hit packet",
            "faces": "R09/R10 are anchored face sheets: one side sees all transversals and the other side selects one",
            "edges": "R12 is live anchored edge; R13 is shadow edge; R24/R26 are split one-sided connectors",
        },
        "checks": checks,
    }

    path = ROOT / "data" / "bt799_transversal_incidence_grammar.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)

    print("BT799 four-transversal incidence grammar")
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
