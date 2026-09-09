#!/usr/bin/env python3
"""Complete-flag law behind the Marcelis omega-normalized trace census.

The companion certificates established an explicit gauge-fixed point map

    tau_omega : PG(3,4) -> PG(3,2)

and the exact line census

    357 = 125 genuine binary-line images + 232 punctured-Fano images.

This file identifies the coordinate geometry controlling both numbers.  The
first-nonzero/omega gauge selects the complete binary flag

    p_inf = 0001  in  L_inf : x0=x1=0
                      in  H0 : x0=0
                      in  PG(3,2).

Line-preserving lifts stratify exactly by this flag:

  * the unique line L_inf has 1 PG(3,4) line lift;
  * the other 6 lines contained in H0 have 2 lifts each;
  * the 28 binary lines not contained in H0 have 4 lifts each.

Hence 1*1 + 6*2 + 28*4 = 125.

The 232 non-line images also obey the same flag.  Every binary plane P contains
exactly two five-point trace images.  Their two missing pairs have a three-point
union, called the puncture line ell_P.  For P != H0,

    ell_P = P intersect H0,

while the gauge assigns ell_H0 = L_inf.  The two missing pairs meet at a
puncture point r_P.  If ell_P != L_inf then

    r_P = ell_P intersect L_inf,

and if ell_P = L_inf the gauge chooses r_P = p_inf.  Thus if
ell_P={r_P,a,b}, the two five-point images are exactly

    P \ {r_P,a}  and  P \ {r_P,b}.

Across all 15 planes the puncture lines are precisely the seven Fano lines of
H0.  L_inf is used by three planes and every other H0 line by two.  All puncture
points lie on L_inf, with plane multiplicities 7,4,4 on its three points.

This is an exact theorem for the declared coordinate gauge.  The complete flag
is not PGL(4,2)-canonical, and the result does not turn tau_omega into an
incidence morphism.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = Path(__file__).resolve().parent
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_marcelis_gf4_trace_gauge import (  # noqa: E402
    projective_points_pg34,
    projective_trace_gauge,
)
from w33_marcelis_pg34_line_trace_census import (  # noqa: E402
    binary_span_nonzero,
    bits,
    pg34_lines,
    rank_f2,
)

OUT = ROOT / "data" / "w33_marcelis_trace_flag_law.json"


def binary_points_pg32():
    return tuple(sorted(v for v in product(range(2), repeat=4) if any(v)))


def binary_planes():
    points = binary_points_pg32()
    planes = set()
    for normal in points:
        plane = frozenset(
            v for v in points
            if sum(a * b for a, b in zip(normal, v)) % 2 == 0
        )
        assert len(plane) == 7
        planes.add(plane)
    assert len(planes) == 15
    return tuple(sorted(planes, key=lambda P: tuple(sorted(P))))


def is_binary_line(values):
    values = frozenset(values)
    return len(values) == 3 and rank_f2(tuple(sorted(values))) == 2


def build_trace_incidence_data():
    points34 = projective_points_pg34()
    lines34 = pg34_lines(points34)

    binary_line_lifts = Counter()
    punctured_subset_lifts = Counter()
    punctured_container = {}

    for L in lines34:
        image = frozenset(projective_trace_gauge(points34[i]) for i in L)
        rank = rank_f2(tuple(sorted(image)))
        if (len(image), rank) == (3, 2):
            binary_line_lifts[image] += 1
        elif (len(image), rank) == (5, 3):
            punctured_subset_lifts[image] += 1
            punctured_container[image] = frozenset(binary_span_nonzero(tuple(sorted(image))))
        else:
            raise AssertionError((L, image, rank))

    assert sum(binary_line_lifts.values()) == 125
    assert sum(punctured_subset_lifts.values()) == 232
    assert len(binary_line_lifts) == 35
    assert len(punctured_subset_lifts) == 30
    return points34, lines34, binary_line_lifts, punctured_subset_lifts, punctured_container


def build_result():
    (
        points34,
        lines34,
        binary_line_lifts,
        punctured_subset_lifts,
        punctured_container,
    ) = build_trace_incidence_data()

    points32 = binary_points_pg32()
    all_planes = binary_planes()

    H0 = frozenset(v for v in points32 if v[0] == 0)
    L_inf = frozenset(v for v in H0 if v[1] == 0)
    p_inf = (0, 0, 0, 1)
    assert len(H0) == 7
    assert len(L_inf) == 3 and is_binary_line(L_inf)
    assert p_inf in L_inf

    # ------------------------------------------------------------------
    # 125 line-preserving lifts: exact flag/Schubert staircase.
    line_stratum_count = Counter()
    line_stratum_lift_mass = Counter()
    line_stratum_multiplicities = defaultdict(set)
    H0_lines = set()

    for line, lifts in binary_line_lifts.items():
        if line == L_inf:
            stratum = "L_inf"
        elif line <= H0:
            stratum = "H0_minus_L_inf"
        else:
            stratum = "outside_H0"
        line_stratum_count[stratum] += 1
        line_stratum_lift_mass[stratum] += lifts
        line_stratum_multiplicities[stratum].add(lifts)
        if line <= H0:
            H0_lines.add(line)

    line_stratum_expected = {
        "L_inf": (1, {1}),
        "H0_minus_L_inf": (6, {2}),
        "outside_H0": (28, {4}),
    }
    line_flag_ok = all(
        line_stratum_count[name] == count
        and line_stratum_multiplicities[name] == mults
        for name, (count, mults) in line_stratum_expected.items()
    )

    # ------------------------------------------------------------------
    # 232 punctured-plane images: exact plane -> line -> point flag law.
    subsets_by_plane = defaultdict(list)
    for subset, plane in punctured_container.items():
        subsets_by_plane[plane].append(subset)

    assert set(subsets_by_plane) == set(all_planes)
    assert {len(v) for v in subsets_by_plane.values()} == {2}

    puncture_lines = set()
    puncture_line_plane_count = Counter()
    shared_point_plane_count = Counter()
    plane_rows = []

    missing_union_is_line = True
    plane_intersection_law = True
    puncture_point_law = True
    exact_two_subset_law = True
    old_lift_mass_law = True

    for plane in all_planes:
        subsets = sorted(subsets_by_plane[plane], key=lambda S: tuple(sorted(S)))
        missing = [plane - subset for subset in subsets]
        assert all(len(M) == 2 for M in missing)

        ell = frozenset(missing[0] | missing[1])
        shared = frozenset(missing[0] & missing[1])
        missing_union_is_line &= is_binary_line(ell)
        missing_union_is_line &= len(shared) == 1
        r = next(iter(shared))

        if plane == H0:
            expected_ell = L_inf
        else:
            expected_ell = frozenset(plane & H0)
        plane_intersection_law &= ell == expected_ell
        plane_intersection_law &= is_binary_line(expected_ell)

        if ell == L_inf:
            expected_r = p_inf
        else:
            intersection = ell & L_inf
            puncture_point_law &= len(intersection) == 1
            expected_r = next(iter(intersection))
        puncture_point_law &= r == expected_r

        others = sorted(ell - {r})
        expected_subsets = {
            frozenset(plane - {r, others[0]}),
            frozenset(plane - {r, others[1]}),
        }
        exact_two_subset_law &= set(subsets) == expected_subsets

        # Preserve the old 4/8 lift census as a cross-check of the new law.
        if plane == H0:
            old_lift_mass_law &= all(punctured_subset_lifts[S] == 4 for S in subsets)
        else:
            old_lift_mass_law &= all(punctured_subset_lifts[S] == 8 for S in subsets)

        puncture_lines.add(ell)
        puncture_line_plane_count[ell] += 1
        shared_point_plane_count[r] += 1

        plane_rows.append(
            {
                "plane": [bits(v) for v in sorted(plane)],
                "is_H0": plane == H0,
                "puncture_line": [bits(v) for v in sorted(ell)],
                "puncture_point": bits(r),
                "punctured_images": [
                    {
                        "image": [bits(v) for v in sorted(S)],
                        "missing_pair": [bits(v) for v in sorted(plane - S)],
                        "GF4_line_lifts": punctured_subset_lifts[S],
                    }
                    for S in subsets
                ],
            }
        )

    puncture_line_multiplicity_hist = Counter(puncture_line_plane_count.values())
    shared_counts_text = {bits(p): c for p, c in sorted(shared_point_plane_count.items())}

    checks = {
        "PG34_is_85_points_357_lines": len(points34) == 85 and len(lines34) == 357,
        "declared_flag_is_point_in_line_in_plane": (
            len(H0) == 7 and len(L_inf) == 3 and p_inf in L_inf <= H0
        ),
        "all_35_binary_lines_are_hit": len(binary_line_lifts) == 35,
        "line_lift_strata_are_1_6_28_with_multiplicities_1_2_4": line_flag_ok,
        "line_lift_mass_identity_is_125": (
            line_stratum_lift_mass == {
                "L_inf": 1,
                "H0_minus_L_inf": 12,
                "outside_H0": 112,
            }
            and sum(line_stratum_lift_mass.values()) == 125
        ),
        "H0_contains_exactly_7_binary_lines": len(H0_lines) == 7,
        "all_15_binary_planes_have_two_punctured_images": (
            len(subsets_by_plane) == 15
            and {len(v) for v in subsets_by_plane.values()} == {2}
        ),
        "each_pair_of_missing_pairs_unions_to_a_binary_line": missing_union_is_line,
        "puncture_lines_are_exactly_the_7_Fano_lines_of_H0": puncture_lines == H0_lines,
        "puncture_line_plane_multiplicity_is_one_3_and_six_2": (
            dict(sorted(puncture_line_multiplicity_hist.items())) == {2: 6, 3: 1}
            and puncture_line_plane_count[L_inf] == 3
        ),
        "plane_puncture_line_is_P_intersect_H0_except_H0_to_Linf": plane_intersection_law,
        "puncture_point_is_line_intersect_Linf_except_Linf_to_pinf": puncture_point_law,
        "two_images_are_exactly_delete_r_a_and_r_b": exact_two_subset_law,
        "all_puncture_points_lie_on_Linf": set(shared_point_plane_count) <= L_inf,
        "puncture_point_plane_multiplicity_is_7_4_4": (
            sorted(shared_point_plane_count.values()) == [4, 4, 7]
            and shared_point_plane_count[p_inf] == 7
        ),
        "old_4_vs_8_subset_lift_mass_is_recovered": old_lift_mass_law,
        "punctured_GF4_line_mass_is_232": sum(punctured_subset_lifts.values()) == 232,
    }

    return {
        "schema": "w33.marcelis-trace-complete-flag-law.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "The omega-normalized PG(3,4)->PG(3,2) trace gauge is governed by "
            "the complete binary flag p_inf=0001 in L_inf:{x0=x1=0} in "
            "H0:{x0=0}. The 125 incidence-preserving line lifts split as "
            "1 line x1 lift + 6 lines x2 lifts + 28 lines x4 lifts. The 30 "
            "punctured-Fano images are likewise determined plane-by-plane by "
            "a puncture line in H0 and a puncture point on L_inf."
        ),
        "flag": {
            "p_inf": bits(p_inf),
            "L_inf_equations": "x0=x1=0",
            "L_inf_points": [bits(v) for v in sorted(L_inf)],
            "H0_equation": "x0=0",
            "H0_points": [bits(v) for v in sorted(H0)],
        },
        "line_lift_flag_strata": {
            "L_inf": {
                "binary_lines": line_stratum_count["L_inf"],
                "lifts_per_line": sorted(line_stratum_multiplicities["L_inf"]),
                "GF4_line_mass": line_stratum_lift_mass["L_inf"],
            },
            "H0_minus_L_inf": {
                "binary_lines": line_stratum_count["H0_minus_L_inf"],
                "lifts_per_line": sorted(line_stratum_multiplicities["H0_minus_L_inf"]),
                "GF4_line_mass": line_stratum_lift_mass["H0_minus_L_inf"],
            },
            "outside_H0": {
                "binary_lines": line_stratum_count["outside_H0"],
                "lifts_per_line": sorted(line_stratum_multiplicities["outside_H0"]),
                "GF4_line_mass": line_stratum_lift_mass["outside_H0"],
            },
            "mass_identity": "1*1 + 6*2 + 28*4 = 125",
        },
        "punctured_plane_flag_law": {
            "puncture_lines": [
                {
                    "line": [bits(v) for v in sorted(L)],
                    "planes_using_line": puncture_line_plane_count[L],
                    "is_L_inf": L == L_inf,
                }
                for L in sorted(puncture_lines, key=lambda X: tuple(sorted(X)))
            ],
            "puncture_line_plane_multiplicity_histogram": {
                str(k): v for k, v in sorted(puncture_line_multiplicity_hist.items())
            },
            "puncture_point_plane_counts": shared_counts_text,
            "law": (
                "For P != H0, ell_P=P intersect H0; for P=H0, ell_P=L_inf. "
                "For ell_P != L_inf, r_P=ell_P intersect L_inf; for "
                "ell_P=L_inf, r_P=p_inf. If ell_P={r_P,a,b}, the two five-"
                "point images are P\\{r_P,a} and P\\{r_P,b}."
            ),
            "planes": plane_rows,
        },
        "interpretation": (
            "The earlier first-one-index lift staircase is a flag/Schubert "
            "staircase: the coordinate gauge privileges a point, then a line, "
            "then a plane in PG(3,2). This completely explains the 1/2/4 line "
            "lift multiplicities and the combinatorics of all 30 punctured "
            "Fano images without promoting the gauge map to an incidence morphism."
        ),
        "claim_boundary": [
            "The flag is selected by the declared ordered-coordinate omega gauge and is not PGL(4,2)-canonical.",
            "The theorem classifies the exact trace images for this gauge; it does not imply PG(3,4) and PG(3,2) are incidence-isomorphic.",
            "The words 'puncture line' and 'puncture point' describe the finite binary image structure, not physical punctures in an optical device.",
            "No cryptographic-security statement follows from the flag law alone.",
        ],
        "checks": checks,
    }


def main() -> int:
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": result["status"],
                "flag": result["flag"],
                "line_mass": result["line_lift_flag_strata"]["mass_identity"],
                "puncture_lines": len(result["punctured_plane_flag_law"]["puncture_lines"]),
                "puncture_point_counts": result["punctured_plane_flag_law"]["puncture_point_plane_counts"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
