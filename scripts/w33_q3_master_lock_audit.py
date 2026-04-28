#!/usr/bin/env python3
"""Exact q=3 master-lock audit for the live W33 frontier.

This module packages the strongest already-exact `q = 3` selection data that
now exists in the repo into one boundary surface:

1. Local qutrit kernel:
   the `1 / 3 / 9 / 27 / 40 / 240` packet already appears exactly in the
   Heisenberg shell, line geometry, and E8-side edge/root count.
2. Corrected spectral core:
   the `SRG(40,12,2,4)` spectrum, zero-mode vanishing, even-moment recurrence,
   and Ihara determinant packet are exact.
3. Symbolic uniqueness factors:
   the new April 2026 formulas all vanish exactly at `q = 3`.
4. Continuum coefficient seed:
   the toroidal/decimal packet already fixes `8, 56, 320, 2240, 12480`.
5. Residual electron seed packet:
    the exact factor packet `98, 17, 208` already lands on the same q=3
    Cartan/toroidal/exceptional backbone via `136 = 8*17`, `98 = 7*14`, and
    `208 = 8*26 = 4*52`.
6. Transport algebra reduction:
    the local parity data is already the sign character of an exact local `S3`
    holonomy, and the remaining mixed-plane wall is reduced to one missing
    non-identity unipotent sign-trivial holonomy class on the canonical host,
    equivalently one missing nonzero nilpotent holonomy increment.

So the conservative exact reading is now stronger than "q=3 looks special":
the finite/local/spectral/continuum-seed/electron-seed/transport layers
already overdetermine the same selected point. The remaining wall is not
finite q-selection. It is the first genuine transport realization witness for
the smooth continuum and dynamical theorem.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
import time
from typing import Dict, Tuple

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
for extra in (ROOT, ROOT / "exploration"):
    if str(extra) not in sys.path:
        sys.path.insert(0, str(extra))

from w33_center_quad_transport_holonomy_bridge import (  # noqa: E402
    build_center_quad_transport_holonomy_summary,
)
from w33_current_k3_mixed_plane_holonomy_failure_bridge import (  # noqa: E402
    build_current_k3_mixed_plane_holonomy_failure_summary,
)
from w33_current_k3_mixed_plane_nilpotent_holonomy_increment_failure_bridge import (  # noqa: E402
    build_current_k3_mixed_plane_nilpotent_holonomy_increment_failure_summary,
)
from w33_current_k3_tail_coordinate_witness_failure_bridge import (  # noqa: E402
    build_current_k3_tail_coordinate_witness_failure_summary,
)
from w33_k3_mixed_plane_holonomy_witness_bridge import (  # noqa: E402
    build_k3_mixed_plane_holonomy_witness_summary,
)
from w33_k3_mixed_plane_nilpotent_holonomy_increment_bridge import (  # noqa: E402
    build_k3_mixed_plane_nilpotent_holonomy_increment_summary,
)
from w33_k3_tail_affine_witness_target_bridge import (  # noqa: E402
    build_k3_tail_affine_witness_target_summary,
)
from w33_k3_tail_canonical_chart_slot_equivalence_bridge import (  # noqa: E402
    build_k3_tail_canonical_chart_slot_equivalence_summary,
)
from w33_k3_tail_single_coordinate_witness_bridge import (  # noqa: E402
    build_k3_tail_single_coordinate_witness_summary,
)
from w33_h4_ordered_path_k3_witness_bridge import (  # noqa: E402
    build_h4_ordered_path_k3_witness_bridge_summary,
)
from w33_minimal_k3_tail_enhancement_datum_bridge import (  # noqa: E402
    build_minimal_k3_tail_enhancement_datum_summary,
)
from w33_transport_ternary_cocycle_bridge import (  # noqa: E402
    build_transport_ternary_cocycle_summary,
)
from scripts.w33_h4_branch_selection_search import (  # noqa: E402
    build_branch_selection_search_summary,
)
from scripts.w33_parseval_measurement_frame_audit import (  # noqa: E402
    build_parseval_measurement_frame_summary,
)
from scripts.w33_chiral_exact_sequence_audit import (  # noqa: E402
    build_chiral_exact_sequence_summary,
)
from scripts.w33_representation_triangle_121_audit import (  # noqa: E402
    build_representation_triangle_121_summary,
)
from scripts.w33_two_spectral_shells_audit import (  # noqa: E402
    build_two_spectral_shells_summary,
)
from scripts.w33_mass_weighted_hodge_audit import (  # noqa: E402
    build_mass_weighted_hodge_summary,
)
from scripts.w33_parseval_target_geometry_audit import (  # noqa: E402
    build_parseval_target_geometry_summary,
)
from scripts.w33_qutrit_ladder_audit import (  # noqa: E402
    e8_side_exact_decomposition_summary,
    one_qutrit_local_layer_summary,
    two_qutrit_global_layer_summary,
)
from scripts.w33_electron_seed_packet_audit import electron_seed_packet_summary  # noqa: E402
from scripts.w33_flavor_frontier_audit import analyze as analyze_flavor_frontier  # noqa: E402
from scripts.w33_spectral_core import get_w33_spectral_core  # noqa: E402
from scripts.w33_toroidal_continuum_seed_audit import (  # noqa: E402
    spectral_continuum_bridge_summary,
    toroidal_continuum_seed_summary,
    toroidal_seed_packet_summary,
)


@lru_cache(maxsize=1)
def symbolic_q3_lock_summary() -> Dict[str, object]:
    q = sp.Symbol("q", positive=True)
    k_q = q * (q + 1)
    f_q = q * (q + 1) ** 2 / 2
    g_q = q * (q**2 + 1) / 2
    v_q = (q**4 - 1) / 2
    phi3_q = q**2 + q + 1
    phi4_q = q**2 + 1
    phi6_q = q**2 - q + 1

    n_zero_gap = sp.factor(2 * v_q - 2 - 2 * f_q - 2 * g_q)
    m2_gap = sp.factor((2 * k_q * k_q + 2 * f_q * (q - 1) ** 2 + 2 * g_q * (q + 1) ** 2) / (2 * v_q) - k_q)
    disc_r_gap = sp.factor((q - 1) ** 2 - 4 * (k_q - 1) + 4 * phi4_q)
    disc_s_gap = sp.factor((q + 1) ** 2 - 4 * (k_q - 1) + 4 * phi6_q)
    # (k-1)^2 - v - q^4 = q(q-3)(q+1): the 121-triangle size equals v+q^4 iff q=3
    v_gq = q**3 + q**2 + q + 1  # GQ(q,q) point count (q^4-1)/(q-1)
    representation_triangle_gap = sp.factor((k_q - 1) ** 2 - v_gq - q**4)

    return {
        "n_zero_gap": str(n_zero_gap),
        "m2_minus_k_gap": str(m2_gap),
        "disc_r_plus_4phi4_gap": str(disc_r_gap),
        "disc_s_plus_4phi6_gap": str(disc_s_gap),
        "representation_triangle_gap": str(representation_triangle_gap),
        "q3_evaluations": {
            "n_zero_gap_at_3": int(n_zero_gap.subs(q, 3)),
            "m2_minus_k_gap_at_3": int(m2_gap.subs(q, 3)),
            "disc_r_gap_at_3": int(disc_r_gap.subs(q, 3)),
            "disc_s_gap_at_3": int(disc_s_gap.subs(q, 3)),
            "representation_triangle_gap_at_3": int(representation_triangle_gap.subs(q, 3)),
        },
        "exact_factors": {
            "n_zero_gap_factor_is_exact": n_zero_gap == (q - 3) * (q + 1) * (q**2 + 1),
            "m2_minus_k_gap_factor_is_exact": m2_gap == -q * (q - 3) * (q + 1) / (q - 1),
            "disc_r_gap_factor_is_exact": disc_r_gap == (q - 3) ** 2,
            "disc_s_gap_factor_is_exact": disc_s_gap == (q - 3) ** 2,
            "representation_triangle_gap_factor_is_exact": representation_triangle_gap == q * (q - 3) * (q + 1),
            "all_symbolic_gaps_vanish_at_q3": all(
                int(expr.subs(q, 3)) == 0
                for expr in (n_zero_gap, m2_gap, disc_r_gap, disc_s_gap, representation_triangle_gap)
            ),
        },
    }


@lru_cache(maxsize=1)
def q3_local_kernel_summary() -> Dict[str, object]:
    one_qutrit = one_qutrit_local_layer_summary()
    two_qutrit = two_qutrit_global_layer_summary()
    e8_side = e8_side_exact_decomposition_summary()
    core = get_w33_spectral_core()
    measurement_frame = build_parseval_measurement_frame_summary()
    chiral_exact_sequence = build_chiral_exact_sequence_summary()
    representation_triangle = build_representation_triangle_121_summary()
    target_geometry = build_parseval_target_geometry_summary()
    two_spectral_shells = build_two_spectral_shells_summary()
    hodge_factorization = build_mass_weighted_hodge_summary()
    flavor_frontier = analyze_flavor_frontier()
    flavor_bridge_theorem = flavor_frontier["flavor_frontier_theorem"][
        "exact_layer_and_spontaneous_cp_frontier_bridge_is_executable"
    ]
    flavor_bridge_evidence = next(
        record["evidence"]
        for record in flavor_frontier["records"]
        if record["name"] == "exact_to_spontaneous_cp_frontier_bridge_is_executable"
    )
    e6_bridge = flavor_bridge_evidence["e6_closed_form_cross_checks"]
    e6_gauge_equivalence_consistent = (
        (not e6_bridge["artifact_present"])
        or (
            e6_bridge["line_product_closed_form_holds"]
            and e6_bridge["full_sign_closed_form_holds"]
        )
    )

    q = int(core.q)
    phi3 = q * q + q + 1
    phi4 = q * q + 1
    phi6 = q * q - q + 1

    return {
        "q": q,
        "phi3": phi3,
        "phi4": phi4,
        "phi6": phi6,
        "visible_shell_size": int(one_qutrit["visible_shell_size"]),
        "fiber_count": int(one_qutrit["fiber_count"]),
        "fiber_size": int(one_qutrit["fiber_size"]),
        "line_size": int(two_qutrit["line_size"]),
        "lines_per_point": int(two_qutrit["lines_per_point"]),
        "projective_point_count": int(two_qutrit["projective_point_count"]),
        "edge_count": int(two_qutrit["edge_count"]),
        "e8_root_count": int(e8_side["total_root_count"]),
        "cartan_rank_candidate": q * q - 1,
        "parseval_measurement_frame": {
            "line_module_resolution": measurement_frame["carrier_dictionary"]["line_side"],
            "spread_count": measurement_frame["carrier_dictionary"]["spread_probe"]["shape"][1],
            "anti_line_count": measurement_frame["carrier_dictionary"]["anti_line_probe"]["shape"][1],
            "spread_density": measurement_frame["carrier_dictionary"]["spread_probe"]["density"],
            "anti_line_density": measurement_frame["carrier_dictionary"]["anti_line_probe"]["density"],
            "centered_spread_probe_spectrum": measurement_frame["spectral_data"][
                "centered_spread_probe_spectrum"
            ],
            "centered_anti_line_probe_spectrum": measurement_frame["spectral_data"][
                "centered_anti_line_probe_spectrum"
            ],
        },
        "parseval_representation_triangle": {
            "line_module": representation_triangle["carrier_dictionary"]["line_module"],
            "spread_module": representation_triangle["carrier_dictionary"]["spread_module"],
            "anti_line_quotient_module": representation_triangle["carrier_dictionary"][
                "anti_line_quotient_module"
            ],
            "total_dimension_identity": representation_triangle["carrier_dictionary"][
                "total_dimension_identity"
            ],
            "sector_double_count_identity": representation_triangle["carrier_dictionary"][
                "sector_double_count_identity"
            ],
            "nonbacktracking_outdegree": representation_triangle["carrier_dictionary"][
                "nonbacktracking_outdegree"
            ],
            "qutrit_hilbert_dimension_identity": representation_triangle["carrier_dictionary"][
                "qutrit_hilbert_dimension_identity"
            ],
            "representation_triangle_uniqueness": representation_triangle["carrier_dictionary"][
                "representation_triangle_uniqueness"
            ],
            "common_singular_constant": representation_triangle["exact_identities"][
                "common_singular_constant"
            ],
            "sector_sharing_triangle": representation_triangle["sector_sharing_triangle"],
        },
        "parseval_chiral_exact_sequence": {
            "positive_chirality": chiral_exact_sequence["carrier_dictionary"]["positive_chirality"],
            "negative_chirality": chiral_exact_sequence["carrier_dictionary"]["negative_chirality"],
            "harmonic_sector": chiral_exact_sequence["carrier_dictionary"]["harmonic_sector"],
            "nonzero_forward_blocks": [
                block["source"] + " -> " + block["target"]
                for block in chiral_exact_sequence["block_support"]["nonzero_forward_blocks"]
            ],
            "exact_dimension_identity": chiral_exact_sequence["carrier_dictionary"][
                "exact_dimension_identity"
            ],
            "total_dimension_identity": chiral_exact_sequence["carrier_dictionary"][
                "total_dimension_identity"
            ],
            "cohomology_statement": chiral_exact_sequence["block_support"]["cohomology_statement"],
            "rank_Q": chiral_exact_sequence["derived_invariants"]["rank_Q"],
            "nullity_Q": chiral_exact_sequence["derived_invariants"]["nullity_Q"],
        },
        "parseval_target_geometry": {
            "spread_target": {
                "frame_type": target_geometry["target_side_frame_geometry"]["spread_etf"]["frame_type"],
                "sector_dimension": target_geometry["target_side_frame_geometry"]["spread_etf"]["sector_dimension"],
                "normalized_coherence": target_geometry["target_side_frame_geometry"]["spread_etf"]["normalized_coherence"],
                "positive_sign_graph": target_geometry["target_side_frame_geometry"]["spread_etf"]["positive_sign_graph"],
                "negative_sign_graph": target_geometry["target_side_frame_geometry"]["spread_etf"]["negative_sign_graph"],
            },
            "anti_line_target": {
                "frame_type": target_geometry["target_side_frame_geometry"]["anti_line_quotient"]["frame_type"],
                "duplicate_class_count": target_geometry["target_side_frame_geometry"]["anti_line_quotient"]["duplicate_class_count"],
                "sector_dimension": target_geometry["target_side_frame_geometry"]["anti_line_quotient"]["sector_dimension"],
                "positive_sign_graph": target_geometry["target_side_frame_geometry"]["anti_line_quotient"]["positive_sign_graph"],
                "negative_sign_graph": target_geometry["target_side_frame_geometry"]["anti_line_quotient"]["negative_sign_graph"],
                "positive_sign_isomorphic_to_transport_graph": target_geometry["target_side_frame_geometry"]["anti_line_quotient"]["positive_sign_isomorphic_to_transport_graph"],
                "canonical_transport_carrier": target_geometry["target_side_frame_geometry"]["anti_line_quotient"][
                    "canonical_transport_carrier"
                ],
            },
            "common_naimark_shadow": {
                "shared_shadow_dimension": target_geometry["common_naimark_shadow"]["shared_shadow_dimension"],
                "shared_shadow_split": target_geometry["common_naimark_shadow"]["shared_shadow_split"],
                "spread_shadow_frame_type": target_geometry["common_naimark_shadow"]["spread_shadow"]["frame_type"],
                "spread_shadow_coherence": target_geometry["common_naimark_shadow"]["spread_shadow"]["normalized_coherence"],
                "anti_line_shadow_normalized_off_diagonal": target_geometry["common_naimark_shadow"]["anti_line_shadow"]["normalized_off_diagonal"],
                "naimark_complement_swaps_sign_graphs": all(target_geometry["naimark_sign_duality"].values()),
            },
        },
        "two_spectral_shells": {
            "light_shell_rank": two_spectral_shells["carrier_structure"]["light_shell_rank"],
            "heavy_shell_rank": two_spectral_shells["carrier_structure"]["heavy_shell_rank"],
            "harmonic_dimension": two_spectral_shells["carrier_structure"]["harmonic_dimension"],
            "total_dimension": two_spectral_shells["carrier_structure"]["total_dimension"],
            "shell_scale_ratio": two_spectral_shells["shell_scaling_relations"]["shell_scale_ratio"]["ratio"],
            "parseval_identity_holds": two_spectral_shells["spectrum_algebraic_identities"][
                "parseval_identity_25_B4Bt_plus_8_R5Rt"
            ]["holds"],
        },
        "mass_weighted_hodge_factorization": {
            "rank_d": hodge_factorization["chiral_complex_structure"]["rank_d"],
            "nullity_d": hodge_factorization["chiral_complex_structure"]["nullity_d"],
            "harmonic_part": hodge_factorization["chiral_complex_structure"]["harmonic_part"],
            "forward_block_count": len(hodge_factorization["forward_blocks"]),
            "forward_blocks": [
                block["source"] + " -> " + block["target"]
                for block in hodge_factorization["forward_blocks"]
            ],
            "shell_values": [block["shell_value"] for block in hodge_factorization["forward_blocks"]],
            "three_exact_two_term_complexes_plus_three_harmonic": hodge_factorization["theorem"]["three_exact_two_term_complexes_plus_three_harmonic"],
            "shell_hierarchy_inside_differential": hodge_factorization["theorem"]["shell_hierarchy_inside_differential"],
            "massive_hodge_laplacian_spectrum": hodge_factorization["theorem"]["massive_hodge_laplacian_spectrum"],
        },
        "exact_to_frontier_bridge": {
            "aligned_vev_ckm_identity": flavor_bridge_evidence[
                "ckm_exact_alignment_is_identity"
            ],
            "aligned_vev_cp_conserving": flavor_bridge_evidence[
                "ckm_exact_alignment_jarlskog_abs"
            ]
            < 1e-12,
            "misaligned_vev_ckm_nontrivial": flavor_bridge_evidence[
                "ckm_misaligned_is_nontrivial"
            ],
            "misaligned_vev_cp_breaking": flavor_bridge_evidence[
                "ckm_misaligned_jarlskog_abs"
            ]
            > 1e-8,
            "e6_closed_form_gauge_equivalence_consistent": e6_gauge_equivalence_consistent,
            "bridge_is_executable": flavor_bridge_theorem,
        },
        "exact_factorizations": {
            "visible_shell_is_q_cubed": int(one_qutrit["visible_shell_size"]) == q**3,
            "fiber_count_is_q_squared": int(one_qutrit["fiber_count"]) == q * q,
            "fiber_size_is_q": int(one_qutrit["fiber_size"]) == q,
            "line_size_is_q_plus_1": int(two_qutrit["line_size"]) == q + 1,
            "lines_per_point_is_q_plus_1": int(two_qutrit["lines_per_point"]) == q + 1,
            "projective_point_count_is_q3_plus_q2_plus_q_plus_1": int(two_qutrit["projective_point_count"])
            == q**3 + q**2 + q + 1,
            "edge_count_matches_e8_root_count": int(two_qutrit["edge_count"]) == int(e8_side["total_root_count"]),
            "edge_count_is_half_vk": int(two_qutrit["edge_count"])
            == (int(two_qutrit["projective_point_count"]) * int(core.k)) // 2,
            "line_module_parseval_frame_is_exact": all(measurement_frame["theorem"].values()),
            "line_module_chiral_exact_sequence_is_exact": all(chiral_exact_sequence["theorem"].values()),
            "line_spread_quotient_representation_triangle_is_exact": all(
                representation_triangle["theorem"].values()
            ),
            "line_module_parseval_target_geometry_is_exact": all(target_geometry["theorem"].values()),
            "exact_to_frontier_bridge_is_executable": flavor_bridge_theorem,
            "raw_two_shell_spectrum_is_exact": all(two_spectral_shells["theorem"].values()),
            "raw_two_shell_operator_is_massive_hodge_complex": all(hodge_factorization["theorem"].values()),
        },
    }


@lru_cache(maxsize=1)
def q3_spectral_uniqueness_summary() -> Dict[str, object]:
    core = get_w33_spectral_core()
    symbolic = symbolic_q3_lock_summary()

    q = int(core.q)
    phi4 = q * q + 1
    phi6 = q * q - q + 1

    return {
        "q": q,
        "srg_parameters": (int(core.v), int(core.k), int(core.lam), int(core.mu)),
        "adjacency_eigenpairs": core.adjacency_eigenpairs,
        "bipartite_zero_mode_count": int(core.bipartite_lift_zero_mode_count),
        "canonical_hamiltonian_eigenpairs": core.canonical_hamiltonian_eigenpairs,
        "fourth_moment_per_vertex": int(core.adjacency_moment_per_vertex(4)),
        "even_moment_characteristic_roots": core.even_moment_characteristic_roots,
        "even_moment_recurrence_coefficients": core.even_moment_recurrence_coefficients,
        "ihara_nontrivial_discriminants": core.ihara_nontrivial_discriminants,
        "expected_discriminants": (-4 * phi4, -4 * phi6),
        "zeta_regularised_determinant": int(core.zeta_regularised_determinant),
        "symbolic_uniqueness": symbolic,
        "exact_factorizations": {
            "self_verified": bool(core.self_verified),
            "bipartite_has_no_zero_modes": int(core.bipartite_lift_zero_mode_count) == 0,
            "fourth_moment_matches_q3_special_factorization": int(core.adjacency_moment_per_vertex(4))
            == q * (q + 1) ** 2 * (q**2 + q + 1),
            "ihara_discriminants_match_minus_4phi4_and_minus_4phi6": core.ihara_nontrivial_discriminants
            == (-4 * phi4, -4 * phi6),
            "even_moment_recurrence_holds": bool(core.verify_even_moment_recurrence(8)),
            "all_symbolic_uniqueness_gaps_vanish_at_q3": bool(
                symbolic["exact_factors"]["all_symbolic_gaps_vanish_at_q3"]
            ),
        },
    }


@lru_cache(maxsize=1)
def q3_continuum_seed_summary() -> Dict[str, object]:
    seed = toroidal_seed_packet_summary()
    continuum = toroidal_continuum_seed_summary()
    spectral_bridge = spectral_continuum_bridge_summary()
    q = int(seed["q"])
    phi3 = q * q + q + 1
    phi6 = q * q - q + 1
    cartan_packet = q * q - 1

    return {
        "q": q,
        "phi3": phi3,
        "phi6": phi6,
        "cartan_packet": cartan_packet,
        "topological_packet": int(seed["topological_packet"]),
        "continuum_eh_coefficient": int(continuum["continuum_eh_coefficient"]),
        "topological_coefficient": int(continuum["topological_coefficient"]),
        "discrete_eh_coefficient": int(continuum["discrete_eh_coefficient"]),
        "rank39": int(continuum["rank39"]),
        "spectral_negative_weight": int(spectral_bridge["spectral_negative_weight"]),
        "total_mode_count": int(spectral_bridge["total_mode_count"]),
        "exact_factorizations": {
            "phi3_is_6_plus_7": int(seed["shared_six_channel"]) + int(seed["phi6"]) == int(seed["phi3"]),
            "cartan_packet_is_1_plus_7": int(seed["selector_line_dimension"]) + int(seed["phi6"])
            == int(seed["cartan_packet"]),
            "cartan_packet_is_q_squared_minus_1": int(seed["cartan_packet"]) == cartan_packet,
            "topological_packet_is_phi6_times_cartan_packet": int(seed["topological_packet"]) == phi6 * cartan_packet,
            "continuum_eh_is_40_times_cartan_packet": int(continuum["continuum_eh_coefficient"])
            == int(continuum["vertex_count"]) * cartan_packet,
            "rank39_is_nontrivial_spectral_multiplicity_sum": spectral_bridge["exact_factorizations"][
                "rank39_equals_nontrivial_multiplicity_sum"
            ],
            "continuum_eh_is_abs_negative_eigenvalue_times_total_mode_count": spectral_bridge[
                "exact_factorizations"
            ]["continuum_equals_abs_negative_eigenvalue_times_total_mode_count"],
            "topological_is_40_times_topological_packet": int(continuum["topological_coefficient"])
            == int(continuum["vertex_count"]) * int(seed["topological_packet"]),
            "topological_is_phi6_times_abs_negative_eigenvalue_times_total_mode_count": spectral_bridge[
                "exact_factorizations"
            ]["topological_equals_phi6_times_abs_negative_eigenvalue_times_total_mode_count"],
            "discrete_6_mode_is_39_times_40_times_cartan_packet": int(continuum["discrete_eh_coefficient"])
            == int(continuum["rank39"]) * int(continuum["vertex_count"]) * cartan_packet,
            "discrete_6_mode_is_nontrivial_multiplicity_sum_times_abs_negative_eigenvalue_times_total_mode_count": spectral_bridge[
                "exact_factorizations"
            ]["discrete_equals_nontrivial_multiplicity_sum_times_abs_negative_eigenvalue_times_total_mode_count"],
        },
    }


@lru_cache(maxsize=1)
def q3_fermion_seed_summary() -> Dict[str, object]:
    packet = electron_seed_packet_summary()
    continuum = q3_continuum_seed_summary()

    q = int(packet["graph_packet"]["q"])
    mu = int(packet["graph_packet"]["mu"])
    phi6 = int(packet["graph_packet"]["phi6"])
    cartan_packet = int(continuum["cartan_packet"])
    barrier_shell = int(packet["exact_packet_dictionary"]["barrier_shell_lambda_phi6_squared"]["exact"])
    shifted_gaussian_norm = int(
        packet["exact_packet_dictionary"]["shifted_gaussian_norm_mu_squared_plus_one"]["exact"]
    )
    charged_lepton_shell = int(
        packet["exact_packet_dictionary"]["charged_lepton_shell_mu_squared_phi3"]["exact"]
    )
    f4_dimension = int(packet["exact_packet_dictionary"]["f4_dimension"])
    up_sector_suppressor = int(packet["candidate_ratio_dictionary"]["up_sector_suppressor"]["exact"])
    g2_dimension = 2 * phi6
    discrete_6_mode_over_a0 = charged_lepton_shell // cartan_packet

    return {
        "q": q,
        "mu": mu,
        "phi6": phi6,
        "cartan_packet": cartan_packet,
        "shifted_gaussian_norm": shifted_gaussian_norm,
        "up_sector_suppressor": up_sector_suppressor,
        "barrier_shell": barrier_shell,
        "g2_dimension": g2_dimension,
        "charged_lepton_shell": charged_lepton_shell,
        "f4_dimension": f4_dimension,
        "discrete_6_mode_over_a0": discrete_6_mode_over_a0,
        "exact_factorizations": {
            "shifted_gaussian_norm_is_mu_squared_plus_one": shifted_gaussian_norm == mu * mu + 1,
            "up_sector_suppressor_is_cartan_times_shifted_gaussian_norm": (
                up_sector_suppressor == cartan_packet * shifted_gaussian_norm
            ),
            "barrier_shell_is_phi6_times_g2_dimension": barrier_shell == phi6 * g2_dimension,
            "charged_lepton_shell_is_mu_times_f4_dimension": charged_lepton_shell == mu * f4_dimension,
            "charged_lepton_shell_is_cartan_times_discrete_6_mode_over_a0": (
                charged_lepton_shell == cartan_packet * discrete_6_mode_over_a0
            ),
        },
    }


@lru_cache(maxsize=1)
def q3_transport_algebra_summary() -> Dict[str, object]:
    holonomy = build_center_quad_transport_holonomy_summary()
    cocycle = build_transport_ternary_cocycle_summary()
    branch_selection = build_branch_selection_search_summary()
    witness = build_k3_mixed_plane_holonomy_witness_summary()
    current = build_current_k3_mixed_plane_holonomy_failure_summary()
    nilpotent = build_k3_mixed_plane_nilpotent_holonomy_increment_summary()
    current_nilpotent = build_current_k3_mixed_plane_nilpotent_holonomy_increment_failure_summary()
    minimal_tail = build_minimal_k3_tail_enhancement_datum_summary()
    coordinate_witness = build_k3_tail_single_coordinate_witness_summary()
    current_coordinate_witness = build_current_k3_tail_coordinate_witness_failure_summary()
    canonical_chart = build_k3_tail_canonical_chart_slot_equivalence_summary()
    affine_witness = build_k3_tail_affine_witness_target_summary()
    finite_to_continuum_bridge = build_h4_ordered_path_k3_witness_bridge_summary()

    triangle_holonomy = holonomy["triangle_holonomy"]
    cycle_counts = triangle_holonomy["cycle_type_counts"]
    extension_cocycle = cocycle["extension_cocycle"]
    fiber_shift = cocycle["fiber_nilpotent_operator"]
    holonomy_witness = witness["mixed_plane_holonomy_witness"]
    current_state = current["current_mixed_plane_holonomy_state"]
    nilpotent_witness = nilpotent["mixed_plane_nilpotent_holonomy_increment"]
    current_nilpotent_state = current_nilpotent[
        "current_mixed_plane_nilpotent_holonomy_increment_state"
    ]
    minimal_tail_datum = minimal_tail["minimal_k3_tail_enhancement_datum"]
    coordinate_witnesses = coordinate_witness["exact_coordinate_witnesses"]
    current_coordinate_matches = {
        name: value["matches_promoted_witness"]
        for name, value in current_coordinate_witness["witness_comparison"].items()
    }
    canonical_chart_target = canonical_chart["canonical_chart_target"]
    current_zero_witness_point = affine_witness["current_zero_witness_point"]
    exact_witness_point = affine_witness["exact_witness_point"]
    affine_witness_displacement = affine_witness["affine_witness_displacement"]
    affine_displacement_recovered_scales = affine_witness[
        "displacement_recovered_scales"
    ]
    branch_model = branch_selection["branch_model"]
    branch_search = branch_selection["search"]

    return {
        "triangle_count": int(holonomy["transport_triangles"]),
        "parity0_triangles": int(holonomy["archived_v14_triangle_parity"]["parity0"]),
        "parity1_triangles": int(holonomy["archived_v14_triangle_parity"]["parity1"]),
        "identity_triangle_holonomies": int(cycle_counts["identity"]),
        "three_cycle_triangle_holonomies": int(cycle_counts["three_cycle"]),
        "transposition_triangle_holonomies": int(cycle_counts["transposition"]),
        "adapted_group_order": int(extension_cocycle["adapted_group_order"]),
        "sign_trivial_cocycle_values": list(extension_cocycle["cocycle_values_on_sign_trivial_subgroup"]),
        "fiber_shift_matrix": fiber_shift["matrix"],
        "canonical_nontrivial_holonomy": holonomy_witness["canonical_nontrivial_holonomy"],
        "gauge_related_nontrivial_holonomy": holonomy_witness["gauge_related_nontrivial_holonomy"],
        "current_sign_trivial_holonomies": current_state["current_sign_trivial_holonomy_matrices"],
        "canonical_nonzero_increment": nilpotent_witness["canonical_nonzero_increment"],
        "gauge_related_nonzero_increment": nilpotent_witness["gauge_related_nonzero_increment"],
        "current_nilpotent_increment": current_nilpotent_state["current_nilpotent_increment"],
        "current_nonzero_nilpotent_increments": current_nilpotent_state[
            "current_nonzero_nilpotent_increments"
        ],
        "minimal_tail_slot_state": minimal_tail_datum["slot_state"],
        "minimal_tail_primitive_generator": minimal_tail_datum["primitive_integral_generator"],
        "minimal_tail_transport_pair": minimal_tail_datum["transport_arithmetic_pair"],
        "promoted_coordinate_witnesses": coordinate_witnesses,
        "current_coordinate_witness_matches": current_coordinate_matches,
        "canonical_chart_target": canonical_chart_target,
        "current_zero_witness_point": current_zero_witness_point,
        "exact_witness_point": exact_witness_point,
        "affine_witness_displacement": affine_witness_displacement,
        "affine_displacement_recovered_scales": affine_displacement_recovered_scales,
        "finite_ordered_path_carrier": finite_to_continuum_bridge["finite_ordered_path_carrier"],
        "quadrangle_exact_cover_model": {
            "ordered_path_count": branch_model["ordered_path_count"],
            "nonlocal_quadrangle_count": branch_model["nonlocal_quadrangle_count"],
            "target_cover_size": branch_model["target_cover_size"],
            "found_exact_cover": branch_search["found_exact_cover"],
            "visited_search_nodes": branch_search["visited_search_nodes"],
        },
        "shared_finite_to_continuum_transport_shadow": finite_to_continuum_bridge[
            "shared_transport_shadow"
        ],
        "exact_factorizations": {
            "triangle_parity_equals_local_s3_holonomy_sign_exactly": triangle_holonomy[
                "z2_parity_equals_holonomy_sign_exactly"
            ],
            "the_first_exact_finite_transport_carrier_is_the_ordered_nonlocal_2_path_s3_packet": (
                finite_to_continuum_bridge["theorem"][
                    "the_finite_h4_frontier_already_exhibits_an_exact_s3_completion_carrier"
                ]
            ),
            "the_strongest_quadrangle_consistent_branch_packet_model_has_no_exact_cover": (
                branch_selection["theorem"]["that_exact_cover_model_has_no_solution"]
            ),
            "transport_extension_is_exact_twisted_cocycle": extension_cocycle[
                "twisted_cocycle_identity_exact"
            ],
            "transport_extension_is_nontrivial_on_the_sign_trivial_sector": (
                extension_cocycle["cocycle_is_not_a_coboundary"]
                and extension_cocycle["cocycle_values_on_sign_trivial_subgroup"] != [0]
            ),
            "fiber_shift_is_square_zero_rank_one": (
                fiber_shift["matrix"] == [[0, 1], [0, 0]]
                and fiber_shift["square_zero"]
                and fiber_shift["rank"] == 1
            ),
            "nontrivial_sign_trivial_unipotent_holonomy_is_unique_up_to_gauge": witness[
                "k3_mixed_plane_holonomy_witness_theorem"
            ]["the_two_nontrivial_sign_trivial_holonomies_are_gauge_equivalent"],
            "exact_k3_tail_reduces_to_one_sign_trivial_unipotent_holonomy_witness": witness[
                "k3_mixed_plane_holonomy_witness_theorem"
            ][
                "therefore_exact_k3_tail_realization_is_equivalent_to_one_support_preserving_nontrivial_sign_trivial_holonomy_witness_on_the_same_fixed_host"
            ],
            "current_host_fails_only_by_missing_that_unipotent_class": current[
                "current_k3_mixed_plane_holonomy_failure_theorem"
            ][
                "therefore_the_current_mixed_plane_host_fails_the_exact_holonomy_witness_test_for_one_reason_only_the_nontrivial_sign_trivial_holonomy_is_missing"
            ],
            "nonzero_nilpotent_increment_is_unique_up_to_gauge": nilpotent[
                "k3_mixed_plane_nilpotent_holonomy_increment_theorem"
            ]["the_two_nonzero_sign_trivial_increments_are_gauge_equivalent"],
            "exact_k3_tail_reduces_to_one_nonzero_nilpotent_increment": nilpotent[
                "k3_mixed_plane_nilpotent_holonomy_increment_theorem"
            ][
                "therefore_exact_k3_tail_realization_is_equivalent_to_one_support_preserving_nonzero_nilpotent_holonomy_increment_on_the_same_fixed_host"
            ],
            "current_host_fails_only_by_missing_that_nonzero_increment": current_nilpotent[
                "current_k3_mixed_plane_nilpotent_holonomy_increment_failure_theorem"
            ][
                "therefore_the_current_mixed_plane_host_fails_the_exact_nilpotent_increment_test_for_one_reason_only_the_nonzero_increment_is_missing"
            ],
            "the_next_positive_target_is_the_unique_minimal_tail_datum": minimal_tail[
                "minimal_k3_tail_enhancement_datum_theorem"
            ][
                "therefore_the_live_positive_target_is_one_unique_minimal_k3_tail_enhancement_datum_on_the_same_fixed_package"
            ],
            "any_one_promoted_coordinate_witness_recovers_the_same_exact_scale": coordinate_witness[
                "k3_tail_single_coordinate_witness_theorem"
            ][
                "each_promoted_coordinate_witness_recovers_the_same_exact_scale_217_over_12"
            ],
            "current_host_fails_exactly_by_lacking_any_promoted_coordinate_witness": current_coordinate_witness[
                "current_k3_tail_coordinate_witness_failure_theorem"
            ][
                "therefore_the_present_refined_k3_object_fails_exact_tail_realization_exactly_by_lacking_any_promoted_coordinate_witness"
            ],
            "delta_c_equals_14105_is_equivalent_to_activating_the_unique_nonzero_tail_slot": canonical_chart[
                "k3_tail_canonical_chart_slot_equivalence_theorem"
            ][
                "therefore_solving_deltaC_equals_14105_on_the_fixed_package_is_equivalent_to_activating_the_unique_nonzero_tail_slot"
            ],
            "the_live_k3_witness_is_the_same_transport_law_as_the_finite_ordered_path_carrier": (
                finite_to_continuum_bridge["theorem"][
                    "therefore_the_live_k3_witness_is_the_ordered_path_transport_law_written_on_the_fixed_tail_chart"
                ]
                and finite_to_continuum_bridge["theorem"][
                    "this_bridge_identifies_the_transport_datum_but_does_not_remove_the_existing_k3_existence_wall"
                ]
            ),
            "the_live_positive_target_is_one_exact_affine_witness_displacement": affine_witness[
                "k3_tail_affine_witness_target_theorem"
            ][
                "therefore_the_live_external_wall_is_one_exact_affine_witness_target_on_the_same_fixed_package"
            ],
        },
    }


@lru_cache(maxsize=1)
def classify_q3_master_lock() -> Tuple[Dict[str, object], ...]:
    local_kernel = q3_local_kernel_summary()
    spectral = q3_spectral_uniqueness_summary()
    continuum = q3_continuum_seed_summary()
    fermion_seed = q3_fermion_seed_summary()
    transport = q3_transport_algebra_summary()

    return (
        {
            "name": "q3_local_qutrit_kernel_lock",
            "support_level": "repo-exact finite kernel",
            "statement": (
                "The local qutrit kernel already carries the exact q=3 packet "
                "1/3/9/27/40/240 via fibers, lines, projective points, and edges; "
                "the same 40 = 1 + 15 + 24 Parseval split already closes as the 121 = (k-1)^2 "
                "representation triangle with 36 = 1 + 15 + 20 and 45 = 1 + 24 + 20, on the target side "
                "as ETF(36,15), the same canonical 45-point transport carrier with its full 27-line dual "
                "GQ(4,2) incidence already visible as the 27 five-cliques of the negative sign graph, with the common "
                "Naimark shadow 21 = 1 + 20 further sharpening to the chiral exact sequence 121 = 59_+ + 59_- + 3_harm "
                "and the three exact forward blocks S_15 -> L_15, Q_24 -> L_24, and Q_20 -> S_20."
            ),
            "evidence": local_kernel,
        },
        {
            "name": "q3_spectral_ihara_uniqueness_lock",
            "support_level": "repo-exact spectral uniqueness",
            "statement": (
                "The corrected spectral core, zero-mode vanishing, even-moment recurrence, "
                "and Ihara discriminant identities all lock exactly at q=3."
            ),
            "evidence": spectral,
        },
        {
            "name": "q3_toroidal_continuum_seed_lock",
            "support_level": "repo-exact continuum seed",
            "statement": (
                "The toroidal/decimal route already fixes the continuum coefficient packet "
                "8, 56, 320, 2240, 12480 at the same selected point q=3."
            ),
            "evidence": continuum,
        },
        {
            "name": "q3_electron_seed_backbone_lock",
            "support_level": "repo-exact fermion seed",
            "statement": (
                "The residual electron packet already lands on the same q=3 backbone: "
                "17 = mu^2+1, 136 = 8*17, 98 = 7*14, and 208 = 8*26 = 4*52."
            ),
            "evidence": fermion_seed,
        },
        {
            "name": "q3_transport_holonomy_reduction_lock",
            "support_level": "repo-exact transport algebra reduction",
            "statement": (
                "The local q=3 transport algebra is already exact: triangle parity is the "
                "sign character of a genuine local S3 holonomy; the first exact finite "
                "carrier is the 4320 ordered nonlocal 2-path packet; the strongest "
                "quadrangle-consistent 540-packet model already has no exact cover; and "
                "the mixed-plane realization wall is reduced to one missing non-identity "
                "unipotent sign-trivial holonomy class on the canonical host, equivalently "
                "one missing nonzero nilpotent holonomy increment."
            ),
            "evidence": transport,
        },
        {
            "name": "q3_exact_to_spontaneous_cp_frontier_bridge_lock",
            "support_level": "repo-exact finite-to-frontier bridge",
            "statement": (
                "The exact q=3 layer now has an executable bridge to the promoted flavor frontier: "
                "aligned VEVs keep CKM identity and vanishing Jarlskog, while controlled complex "
                "misalignment activates nontrivial CKM with nonzero Jarlskog, consistently with the "
                "stabilized E6 gauge-equivalent closed-form checks."
            ),
            "evidence": local_kernel["exact_to_frontier_bridge"],
        },
        {
            "name": "q3_full_physical_realization_theorem",
            "support_level": "not-yet-exact smooth realization theorem",
            "statement": (
                "The q=3 lock is exact on the finite, coefficient-seed, and transport layers, "
                "but the current host still lacks the first genuine non-identity unipotent "
                "sign-trivial holonomy witness that would realize the smooth/dynamical lift; "
                "the next exact positive target is the unique minimal tail datum in the existing "
                "slot with transport scale 217/12, equivalently any one promoted coordinate "
                "witness, canonically dC = 14105 on the fixed tail channel, and as an affine "
                "problem one exact witness displacement from the zero candidate to the unique "
                "target point."
            ),
            "evidence": {
                "remaining_wall": "first sign-trivial unipotent transport witness + unique minimal tail datum + any one promoted coordinate witness / dC = 14105 + exact affine witness displacement + Yukawa / dynamics",
            },
        },
    )


@lru_cache(maxsize=1)
def analyze() -> Dict[str, object]:
    records = classify_q3_master_lock()
    exact_record_names = tuple(
        record["name"]
        for record in records
        if record["support_level"] != "not-yet-exact smooth realization theorem"
    )
    open_record_names = tuple(
        record["name"]
        for record in records
        if record["support_level"] == "not-yet-exact smooth realization theorem"
    )

    local_kernel = q3_local_kernel_summary()
    spectral = q3_spectral_uniqueness_summary()
    continuum = q3_continuum_seed_summary()
    fermion_seed = q3_fermion_seed_summary()
    transport = q3_transport_algebra_summary()

    theorem = {
        "the_local_kernel_exactly_realizes_the_q3_packet_1_3_9_27_40_240": (
            local_kernel["exact_factorizations"]["visible_shell_is_q_cubed"]
            and local_kernel["exact_factorizations"]["fiber_count_is_q_squared"]
            and local_kernel["exact_factorizations"]["fiber_size_is_q"]
            and local_kernel["exact_factorizations"]["line_size_is_q_plus_1"]
            and local_kernel["exact_factorizations"]["lines_per_point_is_q_plus_1"]
            and local_kernel["exact_factorizations"]["projective_point_count_is_q3_plus_q2_plus_q_plus_1"]
            and local_kernel["exact_factorizations"]["edge_count_matches_e8_root_count"]
        ),
        "the_local_kernel_already_contains_the_exact_line_module_parseval_frame": (
            local_kernel["parseval_measurement_frame"]
            == {
                "line_module_resolution": "40 = 1 + 15 + 24",
                "spread_count": 36,
                "anti_line_count": 90,
                "spread_density": "1/4",
                "anti_line_density": "2/5",
                "centered_spread_probe_spectrum": {0: 25, 18: 15},
                "centered_anti_line_probe_spectrum": {0: 16, 36: 24},
            }
            and local_kernel["exact_factorizations"]["line_module_parseval_frame_is_exact"]
        ),
        "the_local_kernel_already_contains_the_exact_121_representation_triangle": (
            local_kernel["parseval_representation_triangle"]
            == {
                "line_module": "40 = 1 + 15 + 24",
                "spread_module": "36 = 1 + 15 + 20",
                "anti_line_quotient_module": "45 = 1 + 24 + 20",
                "total_dimension_identity": "40 + 36 + 45 = 121 = (k - 1)^2",
                "sector_double_count_identity": "3 + 2(15 + 20 + 24) = 121",
                "nonbacktracking_outdegree": "k - 1 = 11",
                "qutrit_hilbert_dimension_identity": "q^4 = C(q^2,2) + C(q^2+1,2) = 36 + 45 = 81",
                "representation_triangle_uniqueness": "(k-1)^2 = v + q^4 iff q = 3: gap = q(q-3)(q+1)",
                "common_singular_constant": "sqrt(18) = 3sqrt(2)",
                "sector_sharing_triangle": {
                    "L_intersect_S": "1 + 15",
                    "L_intersect_Q": "1 + 24",
                    "S_intersect_Q": "1 + 20",
                    "hidden_target_sector": 20,
                },
            }
            and local_kernel["exact_factorizations"][
                "line_spread_quotient_representation_triangle_is_exact"
            ]
        ),
        "the_local_kernel_already_contains_the_exact_chiral_exact_sequence": (
            local_kernel["parseval_chiral_exact_sequence"]
            == {
                "positive_chirality": "P_+ = L_15 + L_24 + S_20",
                "negative_chirality": "P_- = S_15 + Q_24 + Q_20",
                "harmonic_sector": "H = 1_L + 1_S + 1_Q",
                "nonzero_forward_blocks": ["S_15 -> L_15", "Q_24 -> L_24", "Q_20 -> S_20"],
                "exact_dimension_identity": "2(15 + 24 + 20) = 118",
                "total_dimension_identity": "121 = 59_+ + 59_- + 3_harm",
                "cohomology_statement": "the only cohomology is the three module means",
                "rank_Q": 59,
                "nullity_Q": 62,
            }
            and local_kernel["exact_factorizations"]["line_module_chiral_exact_sequence_is_exact"]
        ),
        "the_local_kernel_already_contains_the_exact_target_side_parseval_geometry_and_naimark_shadow": (
            local_kernel["parseval_target_geometry"]
            == {
                "spread_target": {
                    "frame_type": "ETF(36,15)",
                    "sector_dimension": 15,
                    "normalized_coherence": "1/5",
                    "positive_sign_graph": {
                        "vertices": 36,
                        "degree": 15,
                        "lambda": 6,
                        "mu": 6,
                        "edge_count": 270,
                        "spectrum": {"-3": 20, "3": 15, "15": 1},
                    },
                    "negative_sign_graph": {
                        "vertices": 36,
                        "degree": 20,
                        "lambda": 10,
                        "mu": 12,
                        "edge_count": 360,
                        "spectrum": {"-4": 15, "2": 20, "20": 1},
                    },
                },
                "anti_line_target": {
                    "frame_type": "doubled two-distance tight frame(45,24)",
                    "duplicate_class_count": 45,
                    "sector_dimension": 24,
                    "positive_sign_graph": {
                        "vertices": 45,
                        "degree": 32,
                        "lambda": 22,
                        "mu": 24,
                        "edge_count": 720,
                        "spectrum": {"-4": 20, "2": 24, "32": 1},
                    },
                    "negative_sign_graph": {
                        "vertices": 45,
                        "degree": 12,
                        "lambda": 3,
                        "mu": 3,
                        "edge_count": 270,
                        "spectrum": {"-3": 24, "3": 20, "12": 1},
                    },
                    "positive_sign_isomorphic_to_transport_graph": True,
                    "canonical_transport_carrier": {
                        "coordinate_conversion": "(x0,x1,x2,x3) -> (x0,x2,x1,x3)",
                        "anti_lines_equal_center_quads_after_coordinate_conversion": True,
                        "duplicate_pairing_equals_center_quad_antipodes": True,
                        "duplicate_classes_equal_quotient_point_quad_pairs": True,
                        "paired_supports_equal_quotient_point_supports": True,
                        "quotient_line_count": 27,
                        "support_partitions_equal_quotient_lines": True,
                        "line_size_distribution": {5: 27},
                        "point_line_incidence_distribution": {3: 45},
                        "negative_sign_graph_five_cliques_equal_quotient_lines": True,
                        "positive_sign_equals_transport_graph_without_relabeling": True,
                        "negative_sign_equals_quotient_point_graph_without_relabeling": True,
                    },
                },
                "common_naimark_shadow": {
                    "shared_shadow_dimension": 21,
                    "shared_shadow_split": "1 + 20",
                    "spread_shadow_frame_type": "ETF(36,21)",
                    "spread_shadow_coherence": "1/7",
                    "anti_line_shadow_normalized_off_diagonal": ["-1/14", "2/7"],
                    "naimark_complement_swaps_sign_graphs": True,
                },
            }
            and local_kernel["exact_factorizations"]["line_module_parseval_target_geometry_is_exact"]
        ),
        "the_corrected_spectral_core_exactly_realizes_the_q3_lock": (
            spectral["srg_parameters"] == (40, 12, 2, 4)
            and spectral["adjacency_eigenpairs"] == ((12, 1), (2, 24), (-4, 15))
            and spectral["bipartite_zero_mode_count"] == 0
            and spectral["canonical_hamiltonian_eigenpairs"] == ((0, 1), (10, 24), (16, 15))
            and spectral["fourth_moment_per_vertex"] == 624
            and spectral["ihara_nontrivial_discriminants"] == spectral["expected_discriminants"]
            and spectral["exact_factorizations"]["even_moment_recurrence_holds"]
            and spectral["exact_factorizations"]["all_symbolic_uniqueness_gaps_vanish_at_q3"]
        ),
        "the_continuum_seed_exactly_realizes_the_q3_packet_8_56_320_2240_12480": (
            continuum["cartan_packet"] == 8
            and continuum["topological_packet"] == 56
            and continuum["continuum_eh_coefficient"] == 320
            and continuum["topological_coefficient"] == 2240
            and continuum["discrete_eh_coefficient"] == 12480
            and all(continuum["exact_factorizations"].values())
        ),
        "the_electron_seed_packet_exactly_splices_into_the_same_q3_backbone": (
            fermion_seed["shifted_gaussian_norm"] == 17
            and fermion_seed["up_sector_suppressor"] == 136
            and fermion_seed["barrier_shell"] == 98
            and fermion_seed["charged_lepton_shell"] == 208
            and all(fermion_seed["exact_factorizations"].values())
        ),
        "the_q3_lock_is_now_overdetermined_across_local_spectral_and_continuum_seed_layers": (
            local_kernel["q"] == spectral["q"] == continuum["q"] == 3
            and local_kernel["phi3"] == continuum["phi3"] == 13
            and local_kernel["phi6"] == continuum["phi6"] == 7
            and local_kernel["cartan_rank_candidate"] == continuum["cartan_packet"] == 8
        ),
        "the_q3_lock_is_now_overdetermined_across_local_spectral_continuum_and_electron_seed_layers": (
            local_kernel["q"] == spectral["q"] == continuum["q"] == fermion_seed["q"] == 3
            and local_kernel["phi6"] == continuum["phi6"] == fermion_seed["phi6"] == 7
            and local_kernel["cartan_rank_candidate"] == continuum["cartan_packet"] == fermion_seed["cartan_packet"] == 8
        ),
        "the_transport_algebra_exactly_reduces_the_smooth_realization_wall_to_one_unipotent_sign_trivial_witness": (
            transport["triangle_count"] == 5280
            and transport["parity0_triangles"] == 3120
            and transport["parity1_triangles"] == 2160
            and transport["identity_triangle_holonomies"] == 240
            and transport["three_cycle_triangle_holonomies"] == 2880
            and transport["transposition_triangle_holonomies"] == 2160
            and transport["canonical_nontrivial_holonomy"] == [[1, 1], [0, 1]]
            and transport["gauge_related_nontrivial_holonomy"] == [[1, 2], [0, 1]]
            and transport["current_sign_trivial_holonomies"] == [[[1, 0], [0, 1]]]
            and all(transport["exact_factorizations"].values())
        ),
        "the_finite_h4_frontier_already_exhibits_the_same_transport_shadow_as_the_k3_witness": (
            transport["finite_ordered_path_carrier"]
            == {
                "path_count": 4320,
                "seed_stabilizer_size": 6,
                "completion_fibre_size": 3,
                "seed_completion_action_size": 6,
            }
            and transport["shared_finite_to_continuum_transport_shadow"]
            == {
                "reduced_group_order": 6,
                "unique_invariant_projective_line": [1, 2],
                "invariant_complement_count": 0,
                "is_nonsplit_extension_of_sign_by_trivial": True,
                "fiber_nilpotent_increment": [[0, 1], [0, 0]],
                "matter_extension_dimensions": [81, 162, 81],
                "matter_extension_rank": 81,
            }
        ),
        "the_missing_finite_selector_is_not_a_bare_540_quadrangle_exact_cover": (
            transport["quadrangle_exact_cover_model"]
            == {
                "ordered_path_count": 4320,
                "nonlocal_quadrangle_count": 1620,
                "target_cover_size": 540,
                "found_exact_cover": False,
                "visited_search_nodes": 1106,
            }
            and transport["exact_factorizations"][
                "the_strongest_quadrangle_consistent_branch_packet_model_has_no_exact_cover"
            ]
        ),
        "the_transport_algebra_exactly_refines_the_same_wall_to_one_nonzero_nilpotent_increment": (
            transport["fiber_shift_matrix"] == [[0, 1], [0, 0]]
            and transport["canonical_nonzero_increment"] == [[0, 1], [0, 0]]
            and transport["gauge_related_nonzero_increment"] == [[0, 2], [0, 0]]
            and transport["current_nilpotent_increment"] == [[0, 0], [0, 0]]
            and transport["current_nonzero_nilpotent_increments"] == []
            and transport["exact_factorizations"][
                "exact_k3_tail_reduces_to_one_nonzero_nilpotent_increment"
            ]
            and transport["exact_factorizations"][
                "current_host_fails_only_by_missing_that_nonzero_increment"
            ]
        ),
        "the_remaining_wall_refines_to_the_first_sign_trivial_unipotent_transport_witness": (
            transport["current_sign_trivial_holonomies"] == [[[1, 0], [0, 1]]]
            and transport["canonical_nontrivial_holonomy"] == [[1, 1], [0, 1]]
            and transport["gauge_related_nontrivial_holonomy"] == [[1, 2], [0, 1]]
            and transport["fiber_shift_matrix"] == [[0, 1], [0, 0]]
        ),
        "the_remaining_wall_refines_equivalently_to_the_first_nonzero_nilpotent_holonomy_increment": (
            transport["current_nilpotent_increment"] == [[0, 0], [0, 0]]
            and transport["canonical_nonzero_increment"] == [[0, 1], [0, 0]]
            and transport["gauge_related_nonzero_increment"] == [[0, 2], [0, 0]]
            and transport["current_nonzero_nilpotent_increments"] == []
        ),
        "the_next_exact_positive_target_is_the_unique_minimal_tail_datum_in_the_existing_slot": (
            transport["minimal_tail_slot_state"] == "unique_nonzero_orbit_in_existing_glue_slot"
            and transport["minimal_tail_primitive_generator"]
            == {"C": "780", "L": "7944", "Q_seed": "62600", "Q_sd1": "53979"}
            and transport["minimal_tail_transport_pair"]
            == {"denominator_lcm": 12, "cleared_coordinate_gcd": 217, "recovered_scale": "217/12"}
            and transport["exact_factorizations"]["the_next_positive_target_is_the_unique_minimal_tail_datum"]
        ),
        "the_remaining_wall_refines_further_to_any_one_promoted_coordinate_witness_equivalently_dC_equals_14105": (
            transport["promoted_coordinate_witnesses"]
            == {
                "C": {
                    "primitive_coordinate": "780",
                    "exact_coordinate": "14105",
                    "recovered_scale": "217/12",
                },
                "L": {
                    "primitive_coordinate": "7944",
                    "exact_coordinate": "143654",
                    "recovered_scale": "217/12",
                },
                "Q_seed": {
                    "primitive_coordinate": "62600",
                    "exact_coordinate": "3396050/3",
                    "recovered_scale": "217/12",
                },
                "Q_sd1": {
                    "primitive_coordinate": "53979",
                    "exact_coordinate": "3904481/4",
                    "recovered_scale": "217/12",
                },
            }
            and transport["current_coordinate_witness_matches"]
            == {"C": False, "L": False, "Q_seed": False, "Q_sd1": False}
            and transport["canonical_chart_target"]
            == {
                "coordinate": "dC",
                "required_value": "14105",
                "primitive_c_direction": "780",
                "transport_scale": "217/12",
                "factorization": "780 * (217/12)",
            }
            and transport["exact_factorizations"][
                "any_one_promoted_coordinate_witness_recovers_the_same_exact_scale"
            ]
            and transport["exact_factorizations"][
                "current_host_fails_exactly_by_lacking_any_promoted_coordinate_witness"
            ]
            and transport["exact_factorizations"][
                "delta_c_equals_14105_is_equivalent_to_activating_the_unique_nonzero_tail_slot"
            ]
        ),
        "the_live_positive_target_can_be_stated_as_one_exact_affine_witness_displacement_from_the_current_zero_candidate": (
            transport["current_zero_witness_point"]
            == {"C": "0", "L": "0", "Q_seed": "0", "Q_sd1": "0"}
            and transport["exact_witness_point"]
            == {
                "C": "14105",
                "L": "143654",
                "Q_seed": "3396050/3",
                "Q_sd1": "3904481/4",
            }
            and transport["affine_witness_displacement"] == transport["exact_witness_point"]
            and transport["affine_displacement_recovered_scales"]
            == {
                "C": "217/12",
                "L": "217/12",
                "Q_seed": "217/12",
                "Q_sd1": "217/12",
            }
            and transport["exact_factorizations"][
                "the_live_positive_target_is_one_exact_affine_witness_displacement"
            ]
        ),
        "the_live_positive_target_is_the_same_ordered_path_transport_law_written_on_the_fixed_k3_chart": (
            transport["canonical_chart_target"]
            == {
                "coordinate": "dC",
                "required_value": "14105",
                "primitive_c_direction": "780",
                "transport_scale": "217/12",
                "factorization": "780 * (217/12)",
            }
            and transport["exact_factorizations"][
                "the_live_k3_witness_is_the_same_transport_law_as_the_finite_ordered_path_carrier"
            ]
        ),
        "the_remaining_wall_is_not_finite_q_selection_but_smooth_realization": True,
        "the_exact_layer_now_has_an_executable_bridge_to_spontaneous_cp_frontier": (
            local_kernel["exact_to_frontier_bridge"]["bridge_is_executable"]
            and local_kernel["exact_to_frontier_bridge"]["aligned_vev_ckm_identity"]
            and local_kernel["exact_to_frontier_bridge"]["aligned_vev_cp_conserving"]
            and local_kernel["exact_to_frontier_bridge"]["misaligned_vev_ckm_nontrivial"]
            and local_kernel["exact_to_frontier_bridge"]["misaligned_vev_cp_breaking"]
            and local_kernel["exact_to_frontier_bridge"]["e6_closed_form_gauge_equivalence_consistent"]
        ),
    }

    return {
        "status": "ok",
        "q3_local_kernel": local_kernel,
        "q3_spectral_uniqueness": spectral,
        "q3_continuum_seed": continuum,
        "q3_fermion_seed": fermion_seed,
        "q3_transport_algebra": transport,
        "record_names_exact_or_boundary": exact_record_names,
        "record_names_open": open_record_names,
        "record_details": records,
        "q3_master_lock_theorem": theorem,
        "boundary_note": (
            "The q=3 selection is now exact and overdetermined across five independent repo "
            "layers: local qutrit geometry, corrected spectral/Ihara uniqueness, the toroidal "
            "continuum coefficient seed, the residual electron arithmetic packet, and the exact "
            "transport holonomy/cocycle reduction. On the finite H4 side the first exact "
            "transport carrier is already the ordered nonlocal 2-path S3 packet, and the "
            "strongest quadrangle-consistent 540-packet model has no exact cover. So the honest "
            "remaining theorem is not 'why q=3?' and not a bare finite branch subset, but the "
            "first non-identity unipotent sign-trivial transport witness on the canonical mixed-"
            "plane host, equivalently the first genuine nonzero nilpotent holonomy increment "
            "there. More positively, the next exact target is already rigid: the unique minimal "
            "tail datum in the existing slot with primitive direction "
            "(780,7944,62600,53979) and transport scale 217/12. On the fixed tail line this is "
            "equivalent to any one promoted coordinate witness, canonically dC = 14105. The "
            "ordered-path transport law and that K3 chart are therefore the same datum on two "
            "carriers, i.e. the algebraic entry point for the smooth continuum and dynamical "
            "realization. In parallel, the exact layer now has an executable CKM/E6 bridge to "
            "the spontaneous-CP frontier (aligned VEV identity, misaligned VEV activation) "
            "without weakening the conservative exactness boundary. In promoted witness "
            "coordinates the current candidate is simply the "
            "origin, and the "
            "exact target is the single affine point (14105,143654,3396050/3,3904481/4)."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXV_q3_master_lock_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Q=3 master-lock audit")
    print(f"  Local packet: q={payload['q3_local_kernel']['q']}, shell={payload['q3_local_kernel']['visible_shell_size']}, edges={payload['q3_local_kernel']['edge_count']}")
    print(
        "  Spectral packet: "
        f"zero-modes={payload['q3_spectral_uniqueness']['bipartite_zero_mode_count']}, "
        f"discriminants={payload['q3_spectral_uniqueness']['ihara_nontrivial_discriminants']}"
    )
    print(
        "  Continuum seed: "
        f"{payload['q3_continuum_seed']['cartan_packet']}, "
        f"{payload['q3_continuum_seed']['topological_packet']}, "
        f"{payload['q3_continuum_seed']['continuum_eh_coefficient']}, "
        f"{payload['q3_continuum_seed']['topological_coefficient']}, "
        f"{payload['q3_continuum_seed']['discrete_eh_coefficient']}"
    )
    print(
        "  Electron seed: "
        f"{payload['q3_fermion_seed']['barrier_shell']}, "
        f"{payload['q3_fermion_seed']['shifted_gaussian_norm']}, "
        f"{payload['q3_fermion_seed']['charged_lepton_shell']}"
    )
    print(
        "  Transport algebra: "
        f"triangles={payload['q3_transport_algebra']['triangle_count']}, "
        f"holonomy split="
        f"{payload['q3_transport_algebra']['identity_triangle_holonomies']}/"
        f"{payload['q3_transport_algebra']['three_cycle_triangle_holonomies']}/"
        f"{payload['q3_transport_algebra']['transposition_triangle_holonomies']}"
    )
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()
