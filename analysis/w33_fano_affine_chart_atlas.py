#!/usr/bin/env python3
"""Fano affine-chart atlas.

Previous theorem:
    PG(1,3)/tetrahedral four-point geometry is modeled as one affine chart
    AG(2,2) inside the Fano plane PG(2,2); the missing three points are one line
    at infinity.

This verifier globalizes that construction.

In the Fano plane, every line can serve as the line at infinity.  Removing that
line leaves four points and six remaining lines, which form AG(2,2): three
parallel classes of two lines each.  Therefore the global seven-point Fano
wedge/dot codec is an atlas of seven tetrahedral/AG(2,2) charts, one for each
choice of infinity line.

Inside a fixed chart, changing the affine anchor is a translation of AG(2,2).
The three non-anchor points seen from any anchor map to the three directions on
the chosen infinity line.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

Vec3 = tuple[int, int, int]


def add(a: Vec3, b: Vec3) -> Vec3:
    return tuple((x + y) % 2 for x, y in zip(a, b))  # type: ignore[return-value]


def nonzero_f2_3() -> list[Vec3]:
    return [v for v in itertools.product(range(2), repeat=3) if any(v)]


def fano_lines(points: list[Vec3]) -> list[tuple[Vec3, Vec3, Vec3]]:
    lines = set()
    for a, b in itertools.combinations(points, 2):
        c = add(a, b)
        lines.add(tuple(sorted((a, b, c))))
    return sorted(lines)


def line_through_pair(lines: list[tuple[Vec3, Vec3, Vec3]], a: Vec3, b: Vec3) -> tuple[Vec3, Vec3, Vec3]:
    for L in lines:
        if a in L and b in L:
            return L
    raise RuntimeError("no line")


def chart_for_infinity(infinity_line: tuple[Vec3, Vec3, Vec3], points: list[Vec3], lines: list[tuple[Vec3, Vec3, Vec3]]) -> dict:
    infinity = set(infinity_line)
    affine = sorted(set(points) - infinity)
    affine_lines = [L for L in lines if not set(L).issubset(infinity)]
    finite_line_segments = []
    direction_to_segments: dict[Vec3, list[tuple[Vec3, Vec3]]] = {d: [] for d in infinity_line}
    for L in affine_lines:
        direction = next(p for p in L if p in infinity)
        finite_pair = tuple(sorted(p for p in L if p not in infinity))
        assert len(finite_pair) == 2
        finite_line_segments.append(finite_pair)
        direction_to_segments[direction].append(finite_pair)  # type: ignore[arg-type]

    # Coordinate model: choose an affine origin O and two finite points as basis; third direction is their sum.
    origin = affine[0]
    non_origin = [p for p in affine if p != origin]
    # Pick a basis pair whose sum from origin gives the remaining non-origin point.
    basis = None
    for e1, e2 in itertools.combinations(non_origin, 2):
        e1v = add(e1, origin)
        e2v = add(e2, origin)
        if e1v != e2v and any(e1v) and any(e2v):
            basis = (e1, e2)
            break
    assert basis is not None
    e1, e2 = basis
    coord = {
        origin: (0, 0),
        e1: (1, 0),
        e2: (0, 1),
    }
    remaining = [p for p in affine if p not in coord][0]
    coord[remaining] = (1, 1)

    anchor_records = []
    for anchor in affine:
        nonanchors = [p for p in affine if p != anchor]
        directions_seen = set()
        mapping = []
        for q in nonanchors:
            L = line_through_pair(lines, anchor, q)
            direction = next(p for p in L if p in infinity)
            directions_seen.add(direction)
            mapping.append({"nonanchor": q, "infinity_direction": direction})
        anchor_records.append({"anchor": anchor, "direction_mapping": mapping, "sees_all_three_directions": directions_seen == infinity})

    # Translations inside the chart: for each ordered pair of anchors, translation by vector target-origin maps chart to itself.
    translations_ok = True
    translation_records = []
    affine_set = set(affine)
    for source, target in itertools.product(affine, repeat=2):
        t = add(source, target)  # over F2, source+t=target
        image = {add(p, t) for p in affine}
        ok = image == affine_set
        translations_ok = translations_ok and ok
        if len(translation_records) < 8:
            translation_records.append({"source": source, "target": target, "translation": t, "ok": ok})

    return {
        "infinity_line": infinity_line,
        "affine_points": affine,
        "affine_point_count": len(affine),
        "affine_line_segment_count": len(finite_line_segments),
        "parallel_classes": {str(k): sorted(v) for k, v in direction_to_segments.items()},
        "parallel_class_sizes": sorted(len(v) for v in direction_to_segments.values()),
        "coordinate_model": {str(k): v for k, v in coord.items()},
        "anchor_records": anchor_records,
        "all_anchors_see_all_directions": all(r["sees_all_three_directions"] for r in anchor_records),
        "translations_preserve_chart": translations_ok,
        "translation_records_sample": translation_records,
    }


def build_payload() -> dict:
    points = nonzero_f2_3()
    lines = fano_lines(points)
    charts = [chart_for_infinity(L, points, lines) for L in lines]

    point_line_counts = Counter()
    pair_counts = Counter()
    for L in lines:
        for p in L:
            point_line_counts[p] += 1
        for a, b in itertools.combinations(L, 2):
            pair_counts[tuple(sorted((a, b)))] += 1

    identities = {
        "fano_points_7": len(points) == 7,
        "fano_lines_7": len(lines) == 7,
        "each_line_size_3": all(len(L) == 3 for L in lines),
        "each_point_on_3_lines": set(point_line_counts.values()) == {3},
        "each_pair_on_one_line": len(pair_counts) == 21 and set(pair_counts.values()) == {1},
        "seven_affine_charts": len(charts) == 7,
        "each_chart_has_AG22_counts": all(c["affine_point_count"] == 4 and c["affine_line_segment_count"] == 6 and c["parallel_class_sizes"] == [2, 2, 2] for c in charts),
        "each_anchor_sees_infinity_directions": all(c["all_anchors_see_all_directions"] for c in charts),
        "translations_preserve_each_chart": all(c["translations_preserve_chart"] for c in charts),
    }
    return {
        "theorem": "fano_affine_chart_atlas",
        "construction": "Every Fano line can be chosen as line at infinity; its complement is an AG(2,2) tetrahedral chart.",
        "fano_plane": {
            "points": points,
            "lines": lines,
            "point_line_counts": {str(k): v for k, v in point_line_counts.items()},
        },
        "chart_count": len(charts),
        "charts": charts,
        "interpretation": {
            "global_fano_codec": "seven-point Fano wedge/dot codec",
            "local_tetrahedral_chart": "choose one Fano line as infinity; the remaining four points form AG(2,2), the tetrahedral/PG(1,3) chart",
            "changing_anchor": "inside a fixed chart, changing anchor is an affine translation of AG(2,2)",
            "changing_infinity_line": "moving between the seven charts changes which Fano line carries the C3 direction/orientation triple",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_fano_affine_chart_atlas.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
