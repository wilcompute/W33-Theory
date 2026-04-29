#!/usr/bin/env python3
"""Direct cubic-carrier audit for the current W33 -> E6 bridge.

This audit packages the strongest conservative statement that the live repo can
support about the current E6 trilinear witness surface:

1. The exact carrier is the 27-line dual GQ(4,2) line graph SRG(27,10,1,5).
2. The canonical signed cubic support is exactly the 45 triangles on that
   27-line carrier.
3. The current E6/F3 symmetry-breaking artifact should be read as a downstream
   witness riding on that exact cubic carrier, not as a stronger standalone
   exact product law.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
import time
from typing import Dict, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_center_quad_gq42_e6_bridge import (  # noqa: E402
    build_center_quad_gq42_e6_bridge_summary,
)
from scripts.w33_local_albert_shadow_audit import (  # noqa: E402
    canonical_signed_cubic_summary,
)


E6_TRILINEAR_ARTIFACT = ROOT / "artifacts" / "e6_f3_trilinear_symmetry_breaking.json"


@lru_cache(maxsize=1)
def dual_27line_carrier_summary() -> Dict[str, object]:
    summary = build_center_quad_gq42_e6_bridge_summary()
    return {
        "dual_gq42_incidence": summary["dual_gq42_incidence"],
        "line_graph_srg": summary["exceptional_graphs"]["line_graph_srg"],
        "line_graph_triangle_count": summary["exceptional_graphs"]["line_graph_triangles"],
        "points_equal_line_graph_triangles": summary["exceptional_graphs"][
            "points_equal_line_graph_triangles"
        ],
        "bridge_verdict": summary["bridge_verdict"],
    }


@lru_cache(maxsize=1)
def signed_cubic_on_27line_carrier_summary() -> Dict[str, object]:
    cubic = canonical_signed_cubic_summary()
    return {
        "triad_count": cubic["triad_count"],
        "fiber_triad_count": cubic["fiber_triad_count"],
        "affine_triad_count": cubic["affine_triad_count"],
        "point_tritangent_incidence_values": cubic["point_tritangent_incidence_values"],
        "uniform_point_tritangent_incidence": cubic["uniform_point_tritangent_incidence"],
        "point_tritangent_incidence": cubic["point_tritangent_incidence"],
        "canonical_solution_solvable": cubic["canonical_solution_solvable"],
        "triad_set_matches_hessian_partition": cubic["triad_set_matches_hessian_partition"],
        "total_positive_signs": cubic["total_positive_signs"],
        "total_negative_signs": cubic["total_negative_signs"],
    }


@lru_cache(maxsize=1)
def downstream_e6_trilinear_witness_summary() -> Dict[str, object]:
    if not E6_TRILINEAR_ARTIFACT.exists():
        return {
            "artifact_present": False,
            "line_product_closed_form_holds": False,
            "line_product_mismatch_count": None,
            "full_sign_closed_form_holds": False,
            "full_sign_mismatch_count": None,
        }

    payload = json.loads(E6_TRILINEAR_ARTIFACT.read_text(encoding="utf-8"))
    checks = payload["cross_checks"]
    line = checks["line_product_closed_form"]
    full = checks["full_sign_closed_form"]
    return {
        "artifact_present": True,
        "line_product_closed_form_holds": bool(line["holds"]),
        "line_product_mismatch_count": int(line["mismatch_count"]),
        "full_sign_closed_form_holds": bool(full["holds"]),
        "full_sign_mismatch_count": int(full["mismatch_count"]),
    }


@lru_cache(maxsize=1)
def classify_e6_27line_cubic_carrier() -> Tuple[Dict[str, object], ...]:
    carrier = dual_27line_carrier_summary()
    cubic = signed_cubic_on_27line_carrier_summary()
    witness = downstream_e6_trilinear_witness_summary()

    return (
        {
            "name": "dual_27line_gq42_carrier",
            "support_level": "repo-exact carrier",
            "statement": (
                "The exact exceptional carrier already present in the repo is the dual "
                "GQ(4,2) 27-line graph SRG(27,10,1,5), reconstructed directly from W33 "
                "center-quads."
            ),
            "evidence": carrier,
        },
        {
            "name": "canonical_signed_cubic_support_on_27line_carrier",
            "support_level": "repo-exact cubic support",
            "statement": (
                "The canonical signed E6-local cubic support is exactly the 45 triangles "
                "of that 27-line carrier, with each carrier line lying on 5 cubic terms."
            ),
            "evidence": cubic,
        },
        {
            "name": "current_e6_trilinear_symmetry_breaking_as_downstream_witness",
            "support_level": "downstream witness on exact carrier",
            "statement": (
                "The current E6/F3 symmetry-breaking artifact is best read as a downstream "
                "witness on the exact 27-line cubic carrier: its stabilized closed forms hold "
                "up to the canonical gauge-equivalent mismatch patterns already audited."
            ),
            "evidence": witness,
        },
    )


@lru_cache(maxsize=1)
def analyze() -> Dict[str, object]:
    carrier = dual_27line_carrier_summary()
    cubic = signed_cubic_on_27line_carrier_summary()
    witness = downstream_e6_trilinear_witness_summary()
    records = classify_e6_27line_cubic_carrier()

    theorem = {
        "the_exact_exceptional_carrier_is_the_dual_27line_gq42_graph": (
            carrier["dual_gq42_incidence"]
            == {
                "points": 45,
                "lines": 27,
                "points_per_line": 5,
                "lines_per_point": 3,
                "incidences": 135,
            }
            and carrier["line_graph_srg"]
            == {
                "vertices": 27,
                "degree": 10,
                "lambda": 1,
                "mu": 5,
                "edge_count": 135,
                "degree_spectrum_singleton": True,
                "adjacent_common_singleton": True,
                "nonadjacent_common_singleton": True,
            }
            and carrier["line_graph_triangle_count"] == 45
            and carrier["points_equal_line_graph_triangles"] is True
        ),
        "the_signed_cubic_support_is_exactly_the_45_triangles_on_that_carrier": (
            cubic["triad_count"] == 45
            and cubic["fiber_triad_count"] == 9
            and cubic["affine_triad_count"] == 36
            and cubic["uniform_point_tritangent_incidence"] is True
            and cubic["point_tritangent_incidence_values"] == (5,)
            and cubic["point_tritangent_incidence"] == 5
            and cubic["canonical_solution_solvable"] is True
            and cubic["triad_set_matches_hessian_partition"] is True
            and carrier["line_graph_triangle_count"] == cubic["triad_count"]
        ),
        "the_current_e6_trilinear_symmetry_breaking_surface_is_a_downstream_witness_on_that_exact_cubic": (
            witness["artifact_present"] is True
            and witness["line_product_closed_form_holds"] is True
            and witness["line_product_mismatch_count"] in (0, 4)
            and witness["full_sign_closed_form_holds"] is True
            and witness["full_sign_mismatch_count"] in (0, 20)
        ),
    }

    return {
        "status": "ok",
        "dual_27line_carrier": carrier,
        "signed_cubic_support": cubic,
        "downstream_trilinear_witness": witness,
        "record_details": records,
        "e6_27line_cubic_carrier_theorem": theorem,
        "boundary_note": (
            "The repo's strongest honest E6 statement is now sharper than a downstream cross-check: "
            "the exact carrier is the dual 27-line GQ(4,2) graph, the canonical signed cubic support is "
            "exactly its 45 triangles, and the present E6/F3 symmetry-breaking artifact should be read as "
            "a downstream witness on that carrier rather than as a full standalone Albert-product theorem."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXX_e6_27line_cubic_carrier_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("E6 27-line cubic carrier audit")
    print(f"  27-line carrier triangles: {payload['dual_27line_carrier']['line_graph_triangle_count']}")
    print(
        "  Signed cubic support: "
        f"{payload['signed_cubic_support']['fiber_triad_count']} + "
        f"{payload['signed_cubic_support']['affine_triad_count']} = "
        f"{payload['signed_cubic_support']['triad_count']}"
    )
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()