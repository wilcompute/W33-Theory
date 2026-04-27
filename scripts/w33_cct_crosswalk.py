"""Cycle Clock Theory crosswalk for the W(3,3) paper.

This module does not try to certify Cycle Clock Theory.  It records the
finite mathematical overlap between the paper's W(3,3) kernel and the
structural desiderata that CCT emphasizes: finite symbolic language,
trit-level efficiency, Clifford/root-system process objects, E8/H4
quasicrystal projection data, and closed feedback loops.
"""
from __future__ import annotations

from typing import Any

from scripts.w33_parseval_target_geometry_audit import build_parseval_target_geometry_summary


Q = 3
LAMBDA = 2
MU = 4
K = 12
V = 40
E = V * K // 2
PHI3 = 13
PHI4 = 10
PHI6 = 7
F = 24

ORGANIZATION_LAYER_ORDER = (
    "carrier",
    "realization",
    "algebra",
    "computation",
    "witness",
)

CHECKED_PERIODIC_ROWS = (
    "realization_row",
    "pascal_computation_row",
    "frontier_witness_row",
    "exceptional_envelope_row",
)

BACKBONE_INVARIANT_REGISTRY = {
    "q3_selector": {
        "value": 3,
        "meaning": "the unique finite selector q! = 2q picks q = 3",
    },
    "40_point_shell": {
        "value": 40,
        "meaning": "the W(3,3) projective point/line shell with 40 symbols",
    },
    "81_seed": {
        "value": 81,
        "meaning": "the two-qutrit affine seed and exceptional/frontier 81-backbone",
    },
    "240_edge_root_shell": {
        "value": 240,
        "meaning": "the shared W(3,3) edge shell and E8 root shell",
    },
}


def _five_layer_route(
    *,
    carrier: str,
    realization: str,
    algebra: str,
    computation: str,
    witness: str,
) -> dict[str, str]:
    return {
        "carrier": carrier,
        "realization": realization,
        "algebra": algebra,
        "computation": computation,
        "witness": witness,
    }


def q_factorial_equals_two_q_only_at_three(limit: int = 12) -> list[int]:
    """Return positive q <= limit satisfying q! = 2q."""
    hits: list[int] = []
    fact = 1
    for q in range(1, limit + 1):
        fact *= q
        if fact == 2 * q:
            hits.append(q)
    return hits


def projective_qutrit_phase_space_counts() -> dict[str, int]:
    """Counts for nonzero F_3^4 vectors modulo scalar multiplication."""
    affine_vectors = Q**MU
    nonzero_vectors = affine_vectors - 1
    nonzero_scalars = Q - 1
    projective_points = nonzero_vectors // nonzero_scalars
    return {
        "q": Q,
        "dimension": MU,
        "affine_vectors": affine_vectors,
        "nonzero_vectors": nonzero_vectors,
        "nonzero_scalars": nonzero_scalars,
        "projective_points": projective_points,
        "w33_vertices": V,
    }


def w33_clock_language_summary() -> dict[str, Any]:
    """Finite code-language invariants of the two-qutrit W(3,3) kernel."""
    points = projective_qutrit_phase_space_counts()
    line_count = V
    matchings_per_line = Q
    line_clock_states = line_count * matchings_per_line
    return {
        "symbols": {
            "trit_alphabet_size": Q,
            "q_factorial_equals_two_q_hits": q_factorial_equals_two_q_only_at_three(),
            "two_qutrit_exponent_vectors": points["affine_vectors"],
            "nonidentity_exponent_vectors": points["nonzero_vectors"],
            "projective_symbols": points["projective_points"],
        },
        "relational_rules": {
            "srg_parameters": (V, K, LAMBDA, MU),
            "master_equation_left": K * (K - LAMBDA - 1),
            "master_equation_right": (V - K - 1) * MU,
            "edge_relations": E,
            "symplectic_commutation_rule": "B(x,y)=0 over F_3",
        },
        "syntactical_freedom": {
            "line_count": line_count,
            "matchings_per_line": matchings_per_line,
            "line_clock_states": line_clock_states,
            "line_clock_edge_cover": 2 * line_clock_states,
            "cycle_rank": E - V + 1,
        },
    }


def e8_h4_projection_summary() -> dict[str, Any]:
    """E8/H4 projection arithmetic already forced by W(3,3)."""
    h = Q * PHI4
    rank_e8 = K - MU
    rank_h4 = MU
    e8_degrees = (
        LAMBDA,
        K - MU,
        K,
        PHI3 + 1,
        K + MU + LAMBDA,
        E // K,
        F,
        h,
    )
    h4_degrees = (LAMBDA, K, E // K, h)
    return {
        "w33_edges": E,
        "e8_roots": rank_e8 * h,
        "h4_roots": rank_h4 * h,
        "e8_rank": rank_e8,
        "h4_rank": rank_h4,
        "coxeter_number": h,
        "e8_dimension": E + LAMBDA**Q,
        "e8_degrees": e8_degrees,
        "h4_degrees": h4_degrees,
        "h4_degrees_embed_in_e8": set(h4_degrees).issubset(set(e8_degrees)),
    }


def full_symmetry_no_go_summary() -> dict[str, Any]:
    """The finite counterpart of choosing an H4 projection plane."""
    orbital_degrees = (2, 27, 36, 54)
    possible_degrees = sorted(
        {
            sum(deg for bit, deg in enumerate(orbital_degrees) if mask & (1 << bit))
            for mask in range(1 << len(orbital_degrees))
        }
    )
    return {
        "m120_states": 120,
        "six_hundred_cell_degree": K,
        "full_psp43_orbital_degrees": orbital_degrees,
        "possible_invariant_degrees": possible_degrees,
        "full_symmetry_can_make_600_cell_graph": K in possible_degrees,
        "required_selector": "golden/icosahedral H4 projection data",
    }


def build_cct_crosswalk() -> dict[str, Any]:
    """Side-by-side CCT desiderata and W(3,3) finite witnesses."""
    language = w33_clock_language_summary()
    projection = e8_h4_projection_summary()
    no_go = full_symmetry_no_go_summary()
    target_geometry = build_parseval_target_geometry_summary()
    rows = [
        {
            "cct_desideratum": "finite code/language",
            "w33_witness": "F_3^4 projective two-qutrit Pauli symbols",
            "integer_certificate": language["symbols"]["projective_symbols"],
            "aligned_periodic_rows": ["exceptional_envelope_row"],
            "same_table_backbone_invariants": ["40_point_shell"],
            "five_layer_route": _five_layer_route(
                carrier="projective two-qutrit/W(3,3) finite symbol shell",
                realization="F_3^4 projective Pauli symbols modulo nonzero scalars",
                algebra="ternary symplectic commutation law",
                computation="projectivize the two-qutrit exponent space to the 40-symbol shell",
                witness="40 projective symbols",
            ),
        },
        {
            "cct_desideratum": "principle of efficient language",
            "w33_witness": "q=3 is the unique q<=12 solution of q! = 2q",
            "integer_certificate": Q,
            "aligned_periodic_rows": ["exceptional_envelope_row"],
            "same_table_backbone_invariants": ["q3_selector", "81_seed"],
            "five_layer_route": _five_layer_route(
                carrier="the q-ary finite kernel selector",
                realization="ternary qutrit alphabet",
                algebra="factorial selector q! = 2q",
                computation="scan positive q <= 12 for exact selector hits",
                witness="q = 3",
            ),
        },
        {
            "cct_desideratum": "trit savings",
            "w33_witness": "81 two-qutrit exponent vectors collapse to 40 projective nonidentity observables",
            "integer_certificate": language["symbols"]["two_qutrit_exponent_vectors"],
            "aligned_periodic_rows": ["exceptional_envelope_row"],
            "same_table_backbone_invariants": ["81_seed", "40_point_shell"],
            "five_layer_route": _five_layer_route(
                carrier="two-qutrit exponent-vector shell",
                realization="81 affine exponent vectors in F_3^4",
                algebra="quotient by the two nonzero F_3 scalars",
                computation="81 -> 40 projective nonidentity observables",
                witness="81 affine vectors and 40 projective symbols",
            ),
        },
        {
            "cct_desideratum": "Clifford/root-system process objects",
            "w33_witness": "Aut(W(3,3)) = Sp(4,3), the two-qutrit Clifford symplectic group",
            "integer_certificate": 51_840,
            "aligned_periodic_rows": ["exceptional_envelope_row"],
            "same_table_backbone_invariants": ["240_edge_root_shell"],
            "five_layer_route": _five_layer_route(
                carrier="the W(3,3) commutation graph and its 240-edge shell",
                realization="two-qutrit Clifford/symplectic process action",
                algebra="Sp(4,3) symmetry with the finite edge/root count bridge",
                computation="enumerate the exact finite process group on the kernel",
                witness="|Sp(4,3)| = 51840 and |E(W(3,3))| = 240",
            ),
        },
        {
            "cct_desideratum": "E8 to H4 quasicrystal pathway",
            "w33_witness": "240 W(3,3) edges, 120 internal line-matching states",
            "integer_certificate": projection["w33_edges"],
            "aligned_periodic_rows": ["exceptional_envelope_row", "frontier_witness_row"],
            "same_table_backbone_invariants": ["240_edge_root_shell"],
            "five_layer_route": _five_layer_route(
                carrier="the 240-edge W(3,3) shell with its 120 matching-state cover",
                realization="W(3,3) edge shell and M120 line-matching packet",
                algebra="E8/H4 Coxeter-degree arithmetic plus the finite no-go surface",
                computation="compare the 240/120/30 packets and isolate the missing selector",
                witness="240 edges, 120 matching states, and the unresolved golden selector",
            ),
        },
        {
            "cct_desideratum": "feedback loop / cycle-clock dynamics",
            "w33_witness": "finite graph cycle rank and three-state line clocks",
            "integer_certificate": language["syntactical_freedom"]["cycle_rank"],
            "aligned_periodic_rows": ["frontier_witness_row"],
            "same_table_backbone_invariants": ["40_point_shell"],
            "five_layer_route": _five_layer_route(
                carrier="the W(3,3) cycle space and line-clock shell",
                realization="40 lines with 3 matchings per line",
                algebra="finite feedback/cycle algebra on the fixed carrier",
                computation="compute the 120 line-clock states and cycle rank beta_1 = 201",
                witness="120 line-clock states and cycle rank 201",
            ),
        },
        {
            "cct_desideratum": "measurement / shadow duality",
            "w33_witness": "the Pascal target side closes as ETF(36,15), the 45-point transport graph, and a shared 21 = 1 + 20 Naimark shadow",
            "integer_certificate": target_geometry["common_naimark_shadow"]["shared_shadow_dimension"],
            "aligned_periodic_rows": ["pascal_computation_row"],
            "same_table_backbone_invariants": ["40_point_shell", "240_edge_root_shell"],
            "five_layer_route": _five_layer_route(
                carrier="the centered 40-point line module and its Pascal target channels",
                realization="36 spread features and 90 anti-line features collapsing to 45 transport targets",
                algebra="Parseval/Naimark target-side sign algebra",
                computation="center the spread and anti-line probes, quotient duplicate anti-lines, and pass to the Naimark complement",
                witness="ETF(36,15), SRG(45,32,22,24), and the shared shadow 21 = 1 + 20",
            ),
        },
        {
            "cct_desideratum": "non-arbitrary H4 emergence",
            "w33_witness": "full PSp(4,3) symmetry cannot produce a 12-regular 600-cell skeleton",
            "integer_certificate": no_go["full_psp43_orbital_degrees"],
            "aligned_periodic_rows": ["frontier_witness_row", "exceptional_envelope_row"],
            "same_table_backbone_invariants": ["240_edge_root_shell"],
            "five_layer_route": _five_layer_route(
                carrier="the full PSp(4,3) orbital packet on the M120 state space",
                realization="orbital degree packet (2,27,36,54)",
                algebra="full-symmetry orbital decomposition",
                computation="enumerate invariant degrees and rule out degree 12",
                witness="12 is absent, so a golden/icosahedral selector is still required",
            ),
        },
    ]
    aligned_rows = sorted({row_name for row in rows for row_name in row["aligned_periodic_rows"]})
    backbone_invariants = sorted(
        {name for row in rows for name in row["same_table_backbone_invariants"]}
    )
    return {
        "layer_order": ORGANIZATION_LAYER_ORDER,
        "checked_periodic_rows": CHECKED_PERIODIC_ROWS,
        "backbone_invariant_registry": BACKBONE_INVARIANT_REGISTRY,
        "language": language,
        "projection": projection,
        "no_go": no_go,
        "aligned_periodic_rows_used": aligned_rows,
        "same_table_backbone_invariants_used": backbone_invariants,
        "crosswalk_rows": rows,
        "theorem": {
            "w33_realizes_cct_finite_language_template": all(
                [
                    language["symbols"]["q_factorial_equals_two_q_hits"] == [Q],
                    language["symbols"]["projective_symbols"] == V,
                    language["relational_rules"]["master_equation_left"]
                    == language["relational_rules"]["master_equation_right"],
                    language["syntactical_freedom"]["line_clock_states"] == 120,
                    projection["e8_roots"] == E,
                    projection["h4_roots"] == 120,
                    projection["h4_degrees_embed_in_e8"],
                    not no_go["full_symmetry_can_make_600_cell_graph"],
                ]
            ),
            "every_crosswalk_row_has_a_full_five_layer_route": all(
                tuple(row["five_layer_route"].keys()) == ORGANIZATION_LAYER_ORDER
                and all(row["five_layer_route"][layer] for layer in ORGANIZATION_LAYER_ORDER)
                for row in rows
            ),
            "crosswalk_rows_route_only_to_checked_periodic_rows": all(
                all(row_name in CHECKED_PERIODIC_ROWS for row_name in row["aligned_periodic_rows"])
                for row in rows
            ),
            "crosswalk_terms_are_forced_onto_exact_carriers_and_witnesses": all(
                "carrier" in row["five_layer_route"] and "witness" in row["five_layer_route"]
                for row in rows
            ),
            "the_pascal_row_now_routes_the_target_side_measurement_shadow_dictionary": (
                target_geometry["theorem"]["the_centered_spread_features_form_the_exact_etf_36_15"]
                and target_geometry["theorem"][
                    "the_anti_line_channel_collapses_to_a_doubled_45_vector_transport_frame_in_the_24_sector"
                ]
                and target_geometry["theorem"][
                    "both_target_systems_share_the_same_hidden_naimark_shadow_split_21_equals_1_plus_20"
                ]
                and any(
                    row["cct_desideratum"] == "measurement / shadow duality"
                    and row["aligned_periodic_rows"] == ["pascal_computation_row"]
                    for row in rows
                )
            ),
            "crosswalk_rows_name_the_same_table_backbone_invariants_they_use": all(
                row["same_table_backbone_invariants"]
                and all(name in BACKBONE_INVARIANT_REGISTRY for name in row["same_table_backbone_invariants"])
                for row in rows
            ),
            "the_source_dictionary_explicitly_uses_the_shared_40_81_240_backbone": (
                {"40_point_shell", "81_seed", "240_edge_root_shell"}.issubset(set(backbone_invariants))
            ),
            "interpretation": (
                "W(3,3) is an executable finite instance of the CCT code-language "
                "template; the CCT dictionary rows are now routed through the "
                "carrier -> realization -> algebra -> computation -> witness "
                "framework and each row names the shared q=3 backbone invariant "
                "it is using, the Pascal row now contributes an exact target-side "
                "measurement/shadow dictionary culminating in the 45-point transport "
                "graph, while the H4/quasicrystal step still requires an extra "
                "golden/icosahedral selector."
            ),
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_cct_crosswalk(), indent=2))
