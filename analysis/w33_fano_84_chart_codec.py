#!/usr/bin/env python3
"""Fano 84 chart-codec verifier.

Previous theorem:
    The Fano plane is an atlas of seven AG(2,2) / tetrahedral charts.  Each
    chart is obtained by choosing one Fano line as the line at infinity; its
    complement has four affine points and three infinity directions.

This verifier isolates the exact 84-state chart codec:

    84 = 7 * 12 = 7 * 4 * 3.

Meaning:
    choose one of 7 Fano lines as infinity;
    choose one of 4 affine anchors in its complement;
    choose one of 3 infinity directions.

Equivalently, for each chart, the 12 local states are the 4 affine anchors times
3 direction choices.  At a chosen anchor, the three direction choices are exactly
the three non-anchor affine points translated to the line at infinity.

This gives a precise Fano-atlas realization of the recurring 84 local flag count.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

Vec3 = tuple[int, int, int]


def add(a: Vec3, b: Vec3) -> Vec3:
    return tuple((x + y) % 2 for x, y in zip(a, b))  # type: ignore[return-value]


def points() -> list[Vec3]:
    return [v for v in itertools.product(range(2), repeat=3) if any(v)]


def lines(points_: list[Vec3]) -> list[tuple[Vec3, Vec3, Vec3]]:
    out = set()
    for a, b in itertools.combinations(points_, 2):
        out.add(tuple(sorted((a, b, add(a, b)))))
    return sorted(out)


def line_through_pair(lines_: list[tuple[Vec3, Vec3, Vec3]], a: Vec3, b: Vec3) -> tuple[Vec3, Vec3, Vec3]:
    for L in lines_:
        if a in L and b in L:
            return L
    raise RuntimeError("no Fano line through pair")


def chart_states(points_: list[Vec3], lines_: list[tuple[Vec3, Vec3, Vec3]], infinity: tuple[Vec3, Vec3, Vec3]):
    inf = set(infinity)
    affine = sorted(set(points_) - inf)
    states = []
    for anchor in affine:
        nonanchors = sorted(p for p in affine if p != anchor)
        for q in nonanchors:
            L = line_through_pair(lines_, anchor, q)
            direction = next(p for p in L if p in inf)
            states.append(
                {
                    "infinity_line": infinity,
                    "anchor": anchor,
                    "nonanchor": q,
                    "direction": direction,
                    "affine_pair_line": L,
                }
            )
    return states


def build_payload() -> dict:
    P = points()
    Ls = lines(P)
    all_states = []
    chart_records = []
    for infinity in Ls:
        states = chart_states(P, Ls, infinity)
        all_states.extend(states)
        direction_counts = Counter(s["direction"] for s in states)
        anchor_counts = Counter(s["anchor"] for s in states)
        chart_records.append(
            {
                "infinity_line": infinity,
                "affine_points": sorted(set(P) - set(infinity)),
                "state_count": len(states),
                "anchor_count_distribution": dict(Counter(anchor_counts.values())),
                "direction_count_distribution": dict(Counter(direction_counts.values())),
                "directions_used": sorted(direction_counts),
                "all_directions_are_infinity_points": set(direction_counts) == set(infinity),
            }
        )

    # Global incidence distributions.
    point_as_infinity = Counter()
    point_as_anchor = Counter()
    point_as_direction = Counter()
    for s in all_states:
        for p in s["infinity_line"]:
            point_as_infinity[p] += 1
        point_as_anchor[s["anchor"]] += 1
        point_as_direction[s["direction"]] += 1

    # Each Fano line should contribute 12 states; each state can be read as an ordered
    # affine edge from anchor to nonanchor, colored by its point at infinity.
    ordered_affine_edge_count_by_chart = Counter(rec["state_count"] for rec in chart_records)
    unique_state_keys = {
        (s["infinity_line"], s["anchor"], s["direction"])
        for s in all_states
    }
    unique_edge_keys = {
        (s["infinity_line"], s["anchor"], s["nonanchor"])
        for s in all_states
    }

    identities = {
        "fano_points_7": len(P) == 7,
        "fano_lines_7": len(Ls) == 7,
        "chart_count_7": len(chart_records) == 7,
        "each_chart_has_12_states": ordered_affine_edge_count_by_chart == {12: 7},
        "total_states_84": len(all_states) == 84,
        "unique_infinity_anchor_direction_states_84": len(unique_state_keys) == 84,
        "unique_infinity_anchor_nonanchor_edges_84": len(unique_edge_keys) == 84,
        "each_chart_anchor_distribution_four_anchors_each_three": all(rec["anchor_count_distribution"] == {3: 4} for rec in chart_records),
        "each_chart_direction_distribution_three_directions_each_four": all(rec["direction_count_distribution"] == {4: 3} for rec in chart_records),
        "directions_are_infinity_line_points": all(rec["all_directions_are_infinity_points"] for rec in chart_records),
        "each_point_in_infinity_lines_36_times": set(point_as_infinity.values()) == {36},
        "each_point_as_affine_anchor_48_times": set(point_as_anchor.values()) == {48},
        "each_point_as_direction_12_times": set(point_as_direction.values()) == {12},
    }
    return {
        "theorem": "fano_84_chart_codec",
        "identity": "84 = 7 * 12 = 7 infinity lines * 4 affine anchors * 3 directions",
        "fano_counts": {"points": len(P), "lines": len(Ls)},
        "chart_records": chart_records,
        "global_state_count": len(all_states),
        "global_distributions": {
            "point_as_infinity_membership": {str(k): v for k, v in point_as_infinity.items()},
            "point_as_affine_anchor": {str(k): v for k, v in point_as_anchor.items()},
            "point_as_direction": {str(k): v for k, v in point_as_direction.items()},
        },
        "interpretation": {
            "7": "choice of Fano line as line at infinity / chart axis",
            "12": "local chart codec = 4 affine anchors * 3 infinity directions",
            "84": "oriented chart-edge/direction states over the full Fano atlas",
            "relation_to_toroidal_flags": "This is a finite Fano-atlas realization of the recurring 84=7*12 flag-codec count; mapping it to Csaszar/Szilassi flags requires an explicit labeling of the seven axes.",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_fano_84_chart_codec.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
