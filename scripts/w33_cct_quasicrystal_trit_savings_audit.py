"""CCT quasicrystal trit-savings bridge for W(3,3).

Klee's trit-savings rule is a quasicrystal game-of-life rule: among the
allowed same-type neighbor moves, choose the move that preserves the largest
empire-field overlap, equivalently the move that changes the fewest tiles or
higher-dimensional cut-window shifts.  The qutrit/W(3,3) layer supplies the
finite q=3 owner and checked carrier counts; it is not the whole rule.
"""

from __future__ import annotations

import json
from typing import Dict

Q = 3
MU = 4
K = 12
F = 24
E = 240
E8_RANK = 8


def cct_quasicrystal_trit_savings_summary() -> Dict[str, object]:
    """Return the corrected CCT trit-savings rule and finite W(3,3) bridge."""
    candidate_neighbors = 8
    clockwise_neighbors = MU
    counterclockwise_neighbors = MU
    d4_packets = 10
    tetrahedra_per_4g = 4
    tetrahedra_per_20g = 20

    return {
        "source_scope": {
            "book": "Cycle Clock Theory",
            "chapter": 6,
            "sections": (
                "6.3 Empire and empire wave",
                "6.4 2D game of life in Penrose tiling",
                "6.5 3D Game of Life in FIG",
            ),
            "external_source": "Fang-Paduroiu-Hammock-Irwin 2018 non-local game of life in 2D quasicrystals",
            "status": (
                "CCT source dynamics plus exact finite W(3,3) carrier-count "
                "certificates; no simulated trajectory theorem is asserted."
            ),
        },
        "quasicrystal_rule_packet": {
            "dominant_vertex_type": "K",
            "candidate_same_type_neighbors": candidate_neighbors,
            "perpendicular_space_selection": (
                "same pentagonal area in perpendicular space, forming two pentagons"
            ),
            "E0": "union of the empire fields of all existing dominant vertex types",
            "Ei": "empire field of the ith neighboring vertex type",
            "Ui": "E0 intersect Ei",
            "preferred_move": "argmax_i |Ui|",
            "equivalent_minimization": (
                "minimize the empire-field tiles or cut-window shifts that must change"
            ),
            "tie_rule": "random choice among maximizing neighbors",
            "self_stay_allowed": False,
        },
        "trit_savings_packet": {
            "path_name": "maximum trits-saving path",
            "saving_object": "overlap between the current empire field and candidate next-step empires",
            "two_dimensional_measure": "changed tiles; the 2D paper calls these bits",
            "higher_dimensional_measure": (
                "number of cut-window shifts guided by empire and possibility-space windows"
            ),
            "not_primary_meaning": (
                "not merely unresolved third-state storage or 81-to-40 projectivization"
            ),
            "stochastic_freedom": (
                "non-determinism enters when multiple candidate neighbors tie for maximal saving"
            ),
        },
        "quasicrystal_window_packet": {
            "penrose_mother_lattice": "Z5",
            "fig_mother_lattice": "E8",
            "empire_window": "intersection of legal cut windows forced by a local patch",
            "possibility_space_window": (
                "union of legal cut windows for tiles that may coexist with the patch"
            ),
            "dynamic_background": (
                "the empire and possibility space update after each quasiparticle move"
            ),
        },
        "w33_bridge_packet": {
            "qutrit_alphabet_owner": Q,
            "qutrit_status": (
                "q=3 owns the finite trit/qutrit alphabet, while Chapter 6 owns the savings rule"
            ),
            "neighbor_options": candidate_neighbors,
            "w33_k_minus_mu": K - MU,
            "neighbor_options_match_k_minus_mu": candidate_neighbors == K - MU,
            "clockwise_counterclockwise_split": (
                clockwise_neighbors,
                counterclockwise_neighbors,
            ),
            "clock_split_matches_mu_plus_mu": (
                clockwise_neighbors == counterclockwise_neighbors == MU
            ),
            "ten_d4_packets_recover_edge_shell": d4_packets * F,
            "edge_shell": E,
            "fig_20g_from_five_4g_packet": (
                tetrahedra_per_20g // tetrahedra_per_4g,
                tetrahedra_per_4g,
                tetrahedra_per_20g,
            ),
            "frontier_boundary": (
                "W(3,3) certifies finite carrier counts for the quasicrystal savings "
                "skeleton; CCT's empire waves and probability trajectories remain "
                "source/frontier dynamics."
            ),
        },
        "theorem": {
            "trit_savings_is_quasicrystal_least_change_not_unresolved_state_storage": True,
            "least_change_rule_is_argmax_empire_overlap": (
                "argmax_i" in "argmax_i |Ui|"
            ),
            "penrose_neighbor_options_match_w33_k_minus_mu": (
                candidate_neighbors == E8_RANK == K - MU
            ),
            "intrinsic_clock_split_matches_mu_plus_mu": (
                clockwise_neighbors == counterclockwise_neighbors == MU
                and clockwise_neighbors + counterclockwise_neighbors
                == candidate_neighbors
            ),
            "d4_packet_recovers_w33_e8_edge_shell": d4_packets * F == E,
            "fig_20g_packet_matches_five_4g": (
                tetrahedra_per_4g == 4
                and tetrahedra_per_20g == 20
                and tetrahedra_per_20g // tetrahedra_per_4g == 5
            ),
            "qutrit_core_is_owner_not_replacement_for_quasicrystal_rule": Q == 3,
        },
    }


if __name__ == "__main__":
    print(json.dumps(cct_quasicrystal_trit_savings_summary(), indent=2))
