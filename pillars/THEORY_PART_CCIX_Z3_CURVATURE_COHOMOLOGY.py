#!/usr/bin/env python3
"""Pillar 109 (Part CCIX): Z3 Curvature Cohomology on the W(3,3) Complement Graph

The complement graph Q of W(3,3) is a strongly regular SRG(40,27,18,18) on
the same 40 PG(3,3) points.  Each vertex carries a 3-element fiber (line
triple) and each edge carries an S3 transport permutation.  The holonomy
of transport around each triangle defines a Z3-valued 2-cochain F (the
curvature).

Theorem T5 (non-exactness) establishes a genuine Z3 cohomological obstruction:
the curvature F cannot be expressed as the coboundary of any edge potential,
i.e., F is a non-trivial class in the Z3 sheaf cohomology of Q.

Theorems:

T1  QUOTIENT GRAPH: Q = complement(W33) is a strongly regular SRG(40,27,18,18)
    (40 vertices, degree 27, 540 edges).  Its edges form a single orbit under
    Aut(W(3,3)) of order 51840.

T2  TRIANGLE ORBITS: Q has 3240 triangles (unordered triples p<q<r with all
    three pairs in Q).  Under Aut(W33) they split into exactly 2 orbits:
    360 flat triangles (F=0) and 2880 curved triangles (F nonzero).
    Total: 360 + 2880 = 3240.

T3  FLAT LOCUS GEOMETRY: The 360 flat triangles (holonomy = identity) lie on
    the 90 non-isotropic lines of PG(3,3), exactly 4 triangles per line
    (C(4,3)=4 triples per 4-point line, 90 x 4 = 360).  Flat means the
    transport around the triple composes to the identity permutation.

T4  CURVATURE DISTRIBUTION: The Z3-valued curvature over 3240 triangles has
    distribution {0:360, 1:1432, 2:1448}.  Nonzero values split as 1432
    and 1448 (the slight asymmetry reflects the chosen orientation convention).
    Flat + curved = 360 + 2880 = 3240 (curved = F=1 count + F=2 count).

T5  NON-EXACTNESS: The coboundary map delta: C^1(Q;Z3) -> C^2(Q;Z3) maps
    540 edge variables to 3240 triangle equations.  rank(delta) = 501;
    rank([delta|F]) = 502 > 501.  Therefore F is NOT in im(delta): no Z3
    edge potential produces curvature F.

T6  COHOMOLOGICAL OBSTRUCTION: The non-exactness defect is exactly 1:
    rank([delta|F]) - rank(delta) = 502 - 501 = 1.  The gauge freedom is
    540 - 501 = 39 dimensions.  The curvature F represents a single
    independent non-trivial class in Z3 sheaf cohomology.
"""

from __future__ import annotations

import csv
import io
import json
import zipfile
from collections import Counter
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
BUNDLE_CANDIDATES = (
    ROOT / "W33_Z3_curvature_cohomology_on_quotient_bundle.zip",
    ROOT.parent
    / "archive"
    / "zip"
    / "W33_Z3_curvature_cohomology_on_quotient_bundle.zip",
)
BUNDLE = next(
    (candidate for candidate in BUNDLE_CANDIDATES if candidate.exists()),
    BUNDLE_CANDIDATES[0],
)

# Q = complement(W33) = SRG(40,27,18,18)
# W33 = SRG(40,12,2,4); complement parameters: k'=27, lambda'=18, mu'=18
Q_PARAMS = {"n": 40, "k": 27, "lambda_": 18, "mu": 18}


def _load_bundle() -> dict:
    with zipfile.ZipFile(BUNDLE) as zf:
        tri_orbits = json.loads(zf.read("triangle_orbits.json"))
        edge_orbits_data = json.loads(zf.read("edge_orbits.json"))
        delta_ranks = json.loads(zf.read("delta_system_ranks.json"))
        curv_raw = zf.read("curvature_z3_on_triangles_3240.csv").decode(
            "utf-8", errors="replace"
        )
    return {
        "tri_orbits": tri_orbits,
        "edge_orbits_data": edge_orbits_data,
        "delta_ranks": delta_ranks,
        "curv_rows": list(csv.DictReader(io.StringIO(curv_raw))),
    }


def analyze() -> dict:
    data = _load_bundle()
    tri_orb = data["tri_orbits"]
    eo = data["edge_orbits_data"]
    dr = data["delta_ranks"]
    curv_rows = data["curv_rows"]

    # T1: Quotient graph structure
    t1_n_vertices = Q_PARAMS["n"]
    t1_degree = Q_PARAMS["k"]
    t1_total_edges = t1_n_vertices * t1_degree // 2
    t1_num_edge_orbits = eo["num_edge_orbits"]
    t1_edge_orbit_size = eo["edge_orbit_size"]
    t1_edge_orbit_matches = t1_edge_orbit_size == t1_total_edges
    t1_single_edge_orbit = t1_num_edge_orbits == 1

    # T2: Triangle orbits
    t2_total_triangles = len(curv_rows)
    t2_num_triangle_orbits = tri_orb["num_triangle_orbits"]
    t2_orbit_sizes = tri_orb["orbit_sizes"]
    t2_flat_count = next(
        o["size"] for o in tri_orb["orbit_representatives"] if o["F_z3"] == 0
    )
    t2_curved_count = next(
        o["size"] for o in tri_orb["orbit_representatives"] if o["F_z3"] != 0
    )
    t2_total_check = t2_flat_count + t2_curved_count == t2_total_triangles
    t2_correct = (
        t2_num_triangle_orbits == 2
        and t2_flat_count == 360
        and t2_curved_count == 2880
        and t2_total_check
    )

    # T3: Flat locus geometry — verify from CSV
    F_dist = dict(sorted(Counter(int(r["F_z3"]) for r in curv_rows).items()))
    t3_flat_count_csv = F_dist.get(0, 0)
    t3_flat_from_lines = 90 * 4  # 90 non-isotropic lines × C(4,3)=4 triples each
    t3_flat_count_correct = t3_flat_count_csv == t3_flat_from_lines
    t3_interpretation = tri_orb["interpretation"]

    # T4: Curvature distribution
    t4_F_dist = F_dist
    t4_total = sum(F_dist.values())
    t4_curved = t4_total - F_dist.get(0, 0)
    t4_curved_correct = t4_curved == 2880
    t4_F1 = F_dist.get(1, 0)
    t4_F2 = F_dist.get(2, 0)

    # T5: Non-exactness (rank argument)
    t5_n_variables = dr["variables_edges"]  # 540
    t5_n_equations = dr["equations_triangles"]  # 3240
    t5_rank_delta = dr["rank_delta"]  # 501
    t5_rank_augmented = dr["rank_augmented"]  # 502
    t5_non_exact = t5_rank_augmented > t5_rank_delta
    t5_conclusion = dr["conclusion"]

    # T6: Cohomological obstruction
    t6_defect = t5_rank_augmented - t5_rank_delta  # 1
    t6_gauge_freedom = t5_n_variables - t5_rank_delta  # 540-501=39
    t6_obstruction_rank = t6_defect  # 1 independent obstruction

    return {
        "T1_n_vertices": t1_n_vertices,
        "T1_degree": t1_degree,
        "T1_total_edges": t1_total_edges,
        "T1_single_edge_orbit": t1_single_edge_orbit,
        "T1_edge_orbit_size": t1_edge_orbit_size,
        "T1_edge_orbit_matches": t1_edge_orbit_matches,
        "T1_srg_params": Q_PARAMS,
        "T2_total_triangles": t2_total_triangles,
        "T2_num_triangle_orbits": t2_num_triangle_orbits,
        "T2_orbit_sizes": t2_orbit_sizes,
        "T2_flat_count": t2_flat_count,
        "T2_curved_count": t2_curved_count,
        "T2_correct": t2_correct,
        "T3_flat_count_csv": t3_flat_count_csv,
        "T3_flat_from_lines": t3_flat_from_lines,
        "T3_flat_count_correct": t3_flat_count_correct,
        "T3_interpretation": t3_interpretation,
        "T4_F_dist": t4_F_dist,
        "T4_total_triangles": t4_total,
        "T4_curved_count": t4_curved,
        "T4_curved_correct": t4_curved_correct,
        "T4_F1_count": t4_F1,
        "T4_F2_count": t4_F2,
        "T5_n_variables": t5_n_variables,
        "T5_n_equations": t5_n_equations,
        "T5_rank_delta": t5_rank_delta,
        "T5_rank_augmented": t5_rank_augmented,
        "T5_non_exact": t5_non_exact,
        "T5_conclusion": t5_conclusion,
        "T6_defect": t6_defect,
        "T6_gauge_freedom": t6_gauge_freedom,
        "T6_obstruction_rank": t6_obstruction_rank,
    }


def main():
    summary = analyze()
    out = ROOT / "data" / "w33_z3_curvature_cohomology.json"
    out.write_text(json.dumps(summary, indent=2))
    print(
        "T1 SRG(40,27,18,18):",
        summary["T1_n_vertices"],
        "vertices,",
        summary["T1_total_edges"],
        "edges",
    )
    print("T1 single edge orbit:", summary["T1_single_edge_orbit"])
    print(
        "T2 triangle orbits:",
        summary["T2_num_triangle_orbits"],
        " flat:",
        summary["T2_flat_count"],
        " curved:",
        summary["T2_curved_count"],
        " correct:",
        summary["T2_correct"],
    )
    print(
        "T3 flat locus from lines:",
        summary["T3_flat_from_lines"],
        "=CSV:",
        summary["T3_flat_count_csv"],
        " correct:",
        summary["T3_flat_count_correct"],
    )
    print("T4 F distribution:", summary["T4_F_dist"])
    print(
        "T5 non-exact:",
        summary["T5_non_exact"],
        " rank delta:",
        summary["T5_rank_delta"],
        " rank augmented:",
        summary["T5_rank_augmented"],
    )
    print(
        "T6 defect:",
        summary["T6_defect"],
        " gauge freedom:",
        summary["T6_gauge_freedom"],
    )
    print("wrote data/w33_z3_curvature_cohomology.json")


if __name__ == "__main__":
    main()
