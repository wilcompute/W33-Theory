#!/usr/bin/env python3
"""Exact line-level census for the Marcelis GF(4)->GF(2) trace gauge.

The companion trace-gauge certificate constructs a total, explicitly gauge-
fixed map

    tau_omega : PG(3,4) -> PG(3,2)

by scaling the first nonzero GF(4) coordinate to omega and then applying the
coordinatewise field trace.  It maps 85 projective points onto all 15 binary
projective points with fibre sizes 1,2,4,8.

This pass asks what happens one incidence rank higher, to all 357 projective
lines of PG(3,4).  The answer is highly structured and also supplies an
important firewall: tau_omega is a point map but is not a projective-geometry
morphism carrying every GF(4) line to a binary line.

Exact census:

  * 125 GF(4) lines map onto actual 3-point lines of PG(3,2).
  * 232 GF(4) lines map onto five-point subsets spanning a 7-point binary
    projective plane (a punctured Fano plane), never to any other image type.

All 35 binary lines occur.  Their lift multiplicities are 1,2,4 in a gauge
staircase: 1 binary line has one lift, 6 have two lifts, and 28 have four.
If j is the smallest first-nonzero-coordinate index among the three binary
points of the line, the lift count is exactly 2^(2-j).

The 232 non-line images collapse to 30 distinct five-point subsets: every one
of the 15 binary planes contains exactly two such subsets.  For the special
plane x0=0 the two subsets each have four GF(4)-line preimages; for each of the
other 14 planes they each have eight.  The two punctures in a common binary
plane have missing pairs that share exactly one point.

This is a coordinate/gauge theorem, not a claim about a PGL-canonical
projection and not a cryptographic-security result.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = Path(__file__).resolve().parent
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_marcelis_gf4_trace_gauge import (  # noqa: E402
    gf4_add,
    gf4_mul,
    projective_points_pg34,
    projective_trace_gauge,
    canon_first_one,
)

OUT = ROOT / "data" / "w33_marcelis_pg34_line_trace_census.json"


def gf4_linear_combination(a, p, b, q):
    return tuple(gf4_add(gf4_mul(a, x), gf4_mul(b, y)) for x, y in zip(p, q))


def pg34_lines(points):
    """Enumerate the 357 five-point projective lines of PG(3,4)."""
    index = {p: i for i, p in enumerate(points)}
    lines = set()
    for i, j in combinations(range(len(points)), 2):
        p, q = points[i], points[j]
        span = set()
        for a, b in product(range(4), repeat=2):
            if a == b == 0:
                continue
            v = gf4_linear_combination(a, p, b, q)
            if any(v):
                span.add(canon_first_one(v))
        assert len(span) == 5
        lines.add(tuple(sorted(index[v] for v in span)))
    return tuple(sorted(lines))


def rank_f2(rows):
    A = [list(map(int, row)) for row in rows]
    r = 0
    if not A:
        return 0
    for c in range(len(A[0])):
        pivot = next((i for i in range(r, len(A)) if A[i][c]), None)
        if pivot is None:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        for i in range(len(A)):
            if i != r and A[i][c]:
                A[i] = [x ^ y for x, y in zip(A[i], A[r])]
        r += 1
    return r


def binary_span_nonzero(rows):
    basis = []
    for v in rows:
        if rank_f2(basis + [v]) > len(basis):
            basis.append(v)
    out = set()
    for coeffs in product(range(2), repeat=len(basis)):
        if not any(coeffs):
            continue
        w = (0, 0, 0, 0)
        for c, b in zip(coeffs, basis):
            if c:
                w = tuple(x ^ y for x, y in zip(w, b))
        out.add(w)
    return tuple(sorted(out))


def first_one(v):
    return next(i for i, x in enumerate(v) if x)


def plane_normal(plane):
    binary_points = [v for v in product(range(2), repeat=4) if any(v)]
    for n in binary_points:
        if all(sum(a * b for a, b in zip(n, v)) % 2 == 0 for v in plane):
            return tuple(n)
    raise AssertionError("binary rank-3 plane has no normal")


def bits(v):
    return "".join(map(str, v))


def build_result():
    points = projective_points_pg34()
    assert len(points) == 85
    lines = pg34_lines(points)
    assert len(lines) == 357

    shape_hist = Counter()
    binary_line_lifts = Counter()
    punctured_subset_lifts = Counter()
    punctured_container_plane = {}

    for L in lines:
        image = tuple(sorted({projective_trace_gauge(points[i]) for i in L}))
        rank = rank_f2(image)
        shape_hist[(len(image), rank)] += 1
        if (len(image), rank) == (3, 2):
            binary_line_lifts[image] += 1
        elif (len(image), rank) == (5, 3):
            punctured_subset_lifts[image] += 1
            punctured_container_plane[image] = binary_span_nonzero(image)
        else:
            raise AssertionError((L, image, rank))

    # Actual binary-line lift staircase.
    line_lift_hist = Counter(binary_line_lifts.values())
    line_first_index_hist = Counter()
    line_law_ok = True
    line_rows = []
    for line, count in sorted(binary_line_lifts.items()):
        j = min(first_one(v) for v in line)
        line_first_index_hist[j] += 1
        expected = 2 ** (2 - j)
        line_law_ok &= count == expected
        if len(line_rows) < 12:
            line_rows.append({
                "binary_line": [bits(v) for v in line],
                "earliest_first_one_index": j,
                "gf4_line_lifts": count,
                "expected_lifts": expected,
            })

    # Punctured-plane structure.
    subset_lift_hist = Counter(punctured_subset_lifts.values())
    subsets_by_plane = defaultdict(list)
    gf4_lines_by_plane = Counter()
    for subset, count in punctured_subset_lifts.items():
        plane = punctured_container_plane[subset]
        subsets_by_plane[plane].append(subset)
        gf4_lines_by_plane[plane] += count

    plane_total_lift_hist = Counter(gf4_lines_by_plane.values())
    plane_normal_rows = []
    shared_missing_ok = True
    special_plane_ok = True
    for plane, subsets in sorted(subsets_by_plane.items()):
        assert len(plane) == 7
        assert len(subsets) == 2
        missing = [set(plane) - set(subset) for subset in subsets]
        shared = missing[0] & missing[1]
        shared_missing_ok &= len(missing[0]) == len(missing[1]) == 2
        shared_missing_ok &= len(shared) == 1 and len(missing[0] | missing[1]) == 3
        normal = plane_normal(plane)
        total = gf4_lines_by_plane[plane]
        if normal == (1, 0, 0, 0):
            special_plane_ok &= total == 8
            special_plane_ok &= all(punctured_subset_lifts[s] == 4 for s in subsets)
        else:
            special_plane_ok &= total == 16
            special_plane_ok &= all(punctured_subset_lifts[s] == 8 for s in subsets)
        plane_normal_rows.append({
            "normal": bits(normal),
            "gf4_lines_mapping_into_plane": total,
            "punctured_subsets": [
                {
                    "image": [bits(v) for v in subset],
                    "missing_pair": [bits(v) for v in sorted(set(plane) - set(subset))],
                    "gf4_line_lifts": punctured_subset_lifts[subset],
                }
                for subset in sorted(subsets)
            ],
            "shared_missing_point": bits(next(iter(shared))),
        })

    checks = {
        "PG34_has_85_points": len(points) == 85,
        "PG34_has_357_lines": len(lines) == 357,
        "only_two_trace_image_shapes_occur": (
            dict(shape_hist) == {(3, 2): 125, (5, 3): 232}
        ),
        "125_GF4_lines_descend_to_binary_lines": shape_hist[(3, 2)] == 125,
        "232_GF4_lines_become_punctured_binary_planes": shape_hist[(5, 3)] == 232,
        "all_35_binary_lines_are_hit": len(binary_line_lifts) == 35,
        "binary_line_lift_histogram_is_1_2_4_staircase": (
            dict(sorted(line_lift_hist.items())) == {1: 1, 2: 6, 4: 28}
        ),
        "binary_line_first_index_histogram_is_28_6_1": (
            dict(sorted(line_first_index_hist.items())) == {0: 28, 1: 6, 2: 1}
        ),
        "binary_line_lift_law_is_2_power_2_minus_j": line_law_ok,
        "thirty_distinct_punctured_plane_images": len(punctured_subset_lifts) == 30,
        "punctured_subset_lift_histogram_is_4_or_8": (
            dict(sorted(subset_lift_hist.items())) == {4: 2, 8: 28}
        ),
        "all_15_binary_planes_are_hit": len(subsets_by_plane) == 15,
        "each_binary_plane_has_exactly_two_punctured_images": (
            {len(v) for v in subsets_by_plane.values()} == {2}
        ),
        "plane_total_lift_histogram_is_one_8_and_fourteen_16": (
            dict(sorted(plane_total_lift_hist.items())) == {8: 1, 16: 14}
        ),
        "special_x0_zero_plane_is_the_unique_8_line_container": special_plane_ok,
        "two_punctures_per_plane_have_missing_pairs_sharing_one_point": shared_missing_ok,
        "line_and_punctured_counts_sum_to_357": 125 + 232 == 357,
    }

    return {
        "schema": "w33.marcelis-pg34-line-trace-census.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "Under the explicit omega-normalized Marcelis trace gauge, the 357 "
            "lines of PG(3,4) have exactly two image types in PG(3,2): 125 "
            "descend to genuine three-point binary lines, while 232 become "
            "five-point subsets spanning binary projective planes. The point "
            "map is therefore structured but not an incidence morphism."
        ),
        "counts": {
            "PG34_points": len(points),
            "PG34_lines": len(lines),
            "PG32_points_hit": 15,
            "PG32_lines_hit": len(binary_line_lifts),
            "GF4_lines_to_binary_lines": shape_hist[(3, 2)],
            "GF4_lines_to_five_point_plane_subsets": shape_hist[(5, 3)],
            "distinct_five_point_plane_subsets": len(punctured_subset_lifts),
            "binary_planes_hit": len(subsets_by_plane),
        },
        "binary_line_lift_staircase": {
            "lift_multiplicity_histogram": {
                str(k): v for k, v in sorted(line_lift_hist.items())
            },
            "earliest_first_one_index_histogram": {
                str(k): v for k, v in sorted(line_first_index_hist.items())
            },
            "law": (
                "For a binary line ell, let j be the minimum index of the first "
                "1 among its three points. Then the number of PG(3,4) lines "
                "whose tau_omega image is ell is 2^(2-j)."
            ),
            "sample_rows": line_rows,
        },
        "punctured_plane_census": {
            "distinct_subsets": len(punctured_subset_lifts),
            "subset_lift_multiplicity_histogram": {
                str(k): v for k, v in sorted(subset_lift_hist.items())
            },
            "container_plane_total_lift_histogram": {
                str(k): v for k, v in sorted(plane_total_lift_hist.items())
            },
            "law": (
                "Each of the 15 binary projective planes contains exactly two "
                "five-point trace images. The x0=0 plane receives 8 GF4 lines "
                "in total (4 per punctured subset); every other binary plane "
                "receives 16 (8 per subset). Within a plane the two missing "
                "pairs share exactly one point."
            ),
            "planes": plane_normal_rows,
        },
        "marcelis_reading": (
            "Marcelis' GF(4)->GF(2) trace tables should be read as structured, "
            "gauge-fixed coordinate projections. Some selected GF4 lines really "
            "do descend to PG(3,2) lines, but most do not; 232/357 become "
            "punctured Fano planes. This exact census prevents promoting a "
            "useful trace dictionary into a false projective-incidence map."
        ),
        "claim_boundary": [
            "tau_omega depends on the declared first-nonzero-coordinate gauge and is not PGL(4,4)-canonical.",
            "The 125/232 census is exact for this gauge; another gauge may permute or change which individual GF4 lines lie in each class.",
            "No quantum-cryptographic security or physical optical equivalence follows from this finite coordinate census alone.",
        ],
        "checks": checks,
    }


def main() -> int:
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "PG34_lines": result["counts"]["PG34_lines"],
        "to_binary_lines": result["counts"]["GF4_lines_to_binary_lines"],
        "to_punctured_planes": result["counts"]["GF4_lines_to_five_point_plane_subsets"],
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
