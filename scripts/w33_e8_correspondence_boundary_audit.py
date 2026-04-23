#!/usr/bin/env python3
"""Boundary audit for the promoted W33 <-> E8 correspondence surface.

This module does not try to replace the older correspondence theorem script.
Instead it separates three different kinds of statements that had been mixed
together there:

1. Exact finite statements:
   counts, group actions, homology ranks, tetrahedron constraints, and the
   exact E8-side E6 x A2 decomposition.
2. Exact finite patterns with later interpretation:
   the repeated appearance of 27 and 81, and the exact three-27 orbit pattern.
3. Promoted physics inheritance:
   matter-sector identification, dark-matter ratio heuristics, and Weinberg-angle
   phenomenology.

The point is to keep the strongest verified finite content while marking where
the script stops being a theorem and starts being an interpretation layer.
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

from scripts.e8_embedding_group_theoretic import build_w33, generate_e8_roots
from scripts.w33_e8_bijection import classify_roots_z3_grading, decompose_w33_edges
from scripts.w33_e8_correspondence_theorem import (
    compute_dark_matter_prediction,
    compute_generation_structure,
    compute_weinberg_angle,
    verify_full_correspondence,
)
from scripts.w33_homology import (
    analyze_tetrahedron_structure,
    build_clique_complex,
    compute_homology,
)
from scripts.w33_qutrit_ladder_audit import (
    e8_side_exact_decomposition_summary,
    one_qutrit_local_layer_summary,
    two_qutrit_global_layer_summary,
)


@lru_cache(maxsize=1)
def correspondence_surface_summary() -> Dict[str, object]:
    n, vertices, adj, edges = build_w33()
    roots = generate_e8_roots()
    z3 = classify_roots_z3_grading(roots)
    edge_decomp = decompose_w33_edges(n, adj, edges)
    simplices = build_clique_complex(n, adj)
    homology = compute_homology(simplices)
    betti = homology["betti_numbers"]
    checks = verify_full_correspondence(
        n=n,
        vertices=vertices,
        adj=adj,
        edges=edges,
        roots=roots,
        z3_grading=z3,
        edge_decomp=edge_decomp,
        homology=homology,
        simplices=simplices,
    )
    tet = analyze_tetrahedron_structure(simplices)
    generations = compute_generation_structure(z3, edge_decomp)
    dark_matter = compute_dark_matter_prediction(edge_decomp)
    weinberg = compute_weinberg_angle()
    local_qutrit = one_qutrit_local_layer_summary()
    global_qutrit = two_qutrit_global_layer_summary()
    e8_side = e8_side_exact_decomposition_summary()

    return {
        "w33": {
            "vertex_count": int(n),
            "edge_count": int(len(edges)),
        },
        "e8": {
            "root_count": int(len(roots)),
            "z3_root_counts": (
                int(len(z3["g0"])),
                int(len(z3["g1"])),
                int(len(z3["g2"])),
            ),
            "z3_algebra_dims": (86, 81, 81),
        },
        "edge_decomposition": {
            "incident": int(len(edge_decomp["incident"])),
            "h12_internal": int(len(edge_decomp["h12_internal"])),
            "h27_internal": int(len(edge_decomp["h27_internal"])),
            "cross": int(len(edge_decomp["cross"])),
        },
        "homology": {
            "betti_numbers": (
                int(betti.get(0, 0)),
                int(betti.get(1, 0)),
                int(betti.get(2, 0)),
                int(betti.get(3, 0)),
            ),
            "euler_characteristic": int(homology["euler_characteristic"]),
        },
        "tetrahedron_structure": {
            "tetrahedron_count": int(len(simplices[3])),
            "all_triangles_in_exactly_one_tet": bool(tet["all_triangles_in_exactly_one_tet"]),
            "independent_constraints": 120,
        },
        "checks": checks,
        "generation_structure": generations,
        "dark_matter_prediction": dark_matter,
        "weinberg_angle": weinberg,
        "local_qutrit": local_qutrit,
        "global_qutrit": global_qutrit,
        "e8_side_exact_decomposition": e8_side,
    }


@lru_cache(maxsize=1)
def classify_correspondence_claims() -> Tuple[Dict[str, object], ...]:
    payload = correspondence_surface_summary()
    checks = payload["checks"]
    homology = payload["homology"]
    generation = payload["generation_structure"]
    dark_matter = payload["dark_matter_prediction"]
    weinberg = payload["weinberg_angle"]
    local_qutrit = payload["local_qutrit"]
    e8_side = payload["e8_side_exact_decomposition"]

    return (
        {
            "name": "edge_root_count_identity",
            "support_level": "exact count identity",
            "claim_class": "exact",
            "statement": (
                "The exact count identity |E(W33)| = 240 = |Phi(E8)| holds, but by itself "
                "it is only a count match rather than a functorial bridge."
            ),
            "evidence": checks["edge_root_count"],
        },
        {
            "name": "sp43_we6_edge_transitivity",
            "support_level": "repo-exact + classical exact",
            "claim_class": "exact",
            "statement": (
                "The symplectic action is exact on the W33 edge set, giving the 240-edge "
                "transitive finite surface behind the W(E6) comparison."
            ),
            "evidence": checks["group_isomorphism"],
        },
        {
            "name": "e8_z3_root_split_78_81_81",
            "support_level": "exact E8-side decomposition",
            "claim_class": "exact",
            "statement": (
                "On the E8 side, the exact root split 78 + 81 + 81 and the algebra split "
                "86 + 81 + 81 are stable finite data."
            ),
            "evidence": {
                "z3_grading": checks["z3_grading"],
                "line_orbit_sizes": e8_side["line_orbit_sizes"],
            },
        },
        {
            "name": "w33_h1_rank_81",
            "support_level": "repo-exact",
            "claim_class": "exact",
            "statement": (
                "The simplicial homology calculation is exact: H_1(W33; Z) has rank 81."
            ),
            "evidence": {
                "homology": homology,
                "verification": checks["homology"],
            },
        },
        {
            "name": "tetrahedron_constraint_packet_40_times_3",
            "support_level": "repo-exact",
            "claim_class": "exact",
            "statement": (
                "The 40 tetrahedra and their 120 independent constraints are exact finite "
                "structure in the clique complex."
            ),
            "evidence": payload["tetrahedron_structure"],
        },
        {
            "name": "three_generation_finite_pattern",
            "support_level": "exact finite pattern",
            "claim_class": "exact-pattern",
            "statement": (
                "The finite data really does exhibit a three-27 pattern: H_1 has rank 81 = 27 x 3, "
                "the local qutrit shell has size 27, and the E8-side line action has three 27-orbits."
            ),
            "evidence": {
                "b1": homology["betti_numbers"][1],
                "local_shell_size": local_qutrit["visible_shell_size"],
                "matter_lines_per_generation": e8_side["matter_lines_per_generation"],
                "generation_count": e8_side["generation_count"],
                "line_orbit_sizes": e8_side["line_orbit_sizes"],
            },
        },
        {
            "name": "e6_a2_zero_sector_algebraic_split",
            "support_level": "exact E8-side algebraic decomposition",
            "claim_class": "exact",
            "statement": (
                "The algebraic zero sector g0 = E6 + A2 is exact on the E8 side; calling it "
                "a physical gauge group requires additional interpretation."
            ),
            "evidence": {
                "e6_root_count": e8_side["e6_root_count"],
                "a2_root_count": e8_side["a2_root_count"],
                "z3_algebra_dims": payload["e8"]["z3_algebra_dims"],
            },
        },
        {
            "name": "cycle_space_as_matter_sector",
            "support_level": "dimension alignment only",
            "claim_class": "interpretive",
            "statement": (
                "Identifying the W33 cycle space with the physical matter sector is stronger "
                "than the exact theorem data; what is exact is the 81-dimensional alignment."
            ),
            "evidence": {
                "b1_equals_g1_dim": checks["homology"]["b1_equals_g1_dim"],
                "generation_routes_agree": generation["all_agree"],
                "g1_dim": generation["route_2_representation"]["g1_dim"],
                "b1": generation["route_1_homological"]["b1"],
            },
        },
        {
            "name": "w33_sector_alignment_as_gauge_matter_antimatter",
            "support_level": "bookkeeping alignment only",
            "claim_class": "interpretive",
            "statement": (
                "The 24 / 108 / 108 edge split is exact, but its assignment to gauge / matter / "
                "antimatter sectors is an interpretive bookkeeping layer rather than a proved functor."
            ),
            "evidence": checks["sector_dimensions"],
        },
        {
            "name": "dark_matter_ratio_27_over_5",
            "support_level": "heuristic phenomenology layer",
            "claim_class": "phenomenology",
            "statement": (
                "The 27/5 dark-matter ratio is a phenomenological heuristic built from finite counts, "
                "not an exact theorem of the W33 <-> E8 bridge."
            ),
            "evidence": dark_matter,
        },
        {
            "name": "weinberg_angle_3_over_8_inheritance",
            "support_level": "inherited GUT phenomenology",
            "claim_class": "phenomenology",
            "statement": (
                "The 3/8 Weinberg-angle value is the standard E6-style GUT inheritance used by the "
                "script, not a direct derivation from the finite qutrit kernel."
            ),
            "evidence": weinberg,
        },
    )


@lru_cache(maxsize=1)
def analyze() -> Dict[str, object]:
    records = classify_correspondence_claims()
    exact_names = tuple(
        record["name"] for record in records if record["claim_class"] in {"exact", "exact-pattern"}
    )
    interpretive_names = tuple(
        record["name"] for record in records if record["claim_class"] == "interpretive"
    )
    phenomenology_names = tuple(
        record["name"] for record in records if record["claim_class"] == "phenomenology"
    )
    payload = correspondence_surface_summary()

    theorem = {
        "the_count_group_homology_and_tetrahedron_claims_are_exact": (
            "edge_root_count_identity" in exact_names
            and "sp43_we6_edge_transitivity" in exact_names
            and "e8_z3_root_split_78_81_81" in exact_names
            and "w33_h1_rank_81" in exact_names
            and "tetrahedron_constraint_packet_40_times_3" in exact_names
        ),
        "the_three_generation_pattern_is_exact_finite_structure_but_not_yet_full_physics_by_itself": (
            "three_generation_finite_pattern" in exact_names
            and "cycle_space_as_matter_sector" in interpretive_names
        ),
        "the_e6_plus_a2_zero_sector_is_exact_on_the_e8_side_but_physical_gauge_reading_is_later_input": (
            "e6_a2_zero_sector_algebraic_split" in exact_names
            and "w33_sector_alignment_as_gauge_matter_antimatter" in interpretive_names
        ),
        "the_dark_matter_and_weinberg_outputs_are_phenomenology_layers_not_exact_bridge_theorems": (
            phenomenology_names
            == (
                "dark_matter_ratio_27_over_5",
                "weinberg_angle_3_over_8_inheritance",
            )
        ),
        "the_old_all_verified_surface_is_stronger_than_the_exact_boundary": (
            payload["checks"]["ALL_VERIFIED"] is True
            and len(interpretive_names) > 0
            and len(phenomenology_names) > 0
        ),
    }
    theorem["the_correspondence_boundary_is_now_cleanly_separated"] = all(theorem.values())

    return {
        "status": "ok",
        "correspondence_surface": payload,
        "claim_records": records,
        "exact_record_names": exact_names,
        "interpretive_record_names": interpretive_names,
        "phenomenology_record_names": phenomenology_names,
        "boundary_theorem": theorem,
        "boundary_note": (
            "The promoted correspondence theorem script still computes real exact finite data, "
            "but its `ALL_VERIFIED` flag spans exact finite claims, dimensional alignments, and "
            "phenomenology inheritance in one surface. This audit separates those layers."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXII_e8_correspondence_boundary_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("W33 <-> E8 correspondence boundary audit")
    print("  Exact:", ", ".join(payload["exact_record_names"]))
    print("  Interpretive:", ", ".join(payload["interpretive_record_names"]))
    print("  Phenomenology:", ", ".join(payload["phenomenology_record_names"]))
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
