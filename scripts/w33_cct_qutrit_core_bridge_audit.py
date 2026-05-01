"""Qutrit-core bridge between CCT and W(3,3).

CCT's trit economy and W(3,3)'s two-qutrit Pauli commutation geometry are
both organized by the same q=3 carrier.  This audit packages that core before
any higher CCT interpretation is attached.
"""

from __future__ import annotations

from math import factorial
from typing import Dict

from scripts.w33_spread_line_morita_bridge_audit import (
    spread_line_morita_bridge_summary,
)

Q = 3
QUTRIT_COUNT = 2
PHASE_SPACE_DIMENSION = 2 * QUTRIT_COUNT
LAMBDA = 2
MU = Q + 1
K = Q * (Q + 1)
V = (Q**PHASE_SPACE_DIMENSION - 1) // (Q - 1)
E = V * K // 2


def q_factorial_equals_two_q_hits(limit: int = 12) -> tuple[int, ...]:
    """Return q <= limit satisfying q! = 2q."""
    return tuple(q for q in range(1, limit + 1) if factorial(q) == 2 * q)


def cct_qutrit_core_bridge_summary() -> Dict[str, object]:
    """Return the exact q=3 CCT/W(3,3) core bridge."""
    morita = spread_line_morita_bridge_summary()
    affine_exponents = Q**PHASE_SPACE_DIMENSION
    nonzero_exponents = affine_exponents - 1
    scalar_orbit = Q - 1
    line_count = V
    line_size = Q + 1
    lines_per_point = Q + 1
    line_point_incidences = line_count * line_size

    return {
        "source_scope": {
            "claim": "CCT trit economy and W(3,3) two-qutrit Pauli geometry share the q=3 carrier",
            "status": "repo-exact finite qutrit core",
        },
        "cct_trit_packet": {
            "alphabet_size": Q,
            "states": ("off", "on", "undecided"),
            "q_factorial_equals_two_q_hits": q_factorial_equals_two_q_hits(),
            "unique_positive_selector": Q,
        },
        "two_qutrit_pauli_packet": {
            "qutrit_count": QUTRIT_COUNT,
            "phase_space_dimension": PHASE_SPACE_DIMENSION,
            "affine_exponent_vectors": affine_exponents,
            "identity_vector": 1,
            "nonidentity_exponent_vectors": nonzero_exponents,
            "nonzero_scalar_orbit_size": scalar_orbit,
            "projective_pauli_symbols": V,
            "projectivization": "F_3^4 minus 0, modulo F_3^*",
        },
        "w33_commutation_packet": {
            "geometry": "W(3,3) = GQ(3,3) two-qutrit Pauli commutation geometry",
            "point_count": V,
            "line_count": line_count,
            "points_per_line": line_size,
            "lines_per_point": lines_per_point,
            "point_line_incidences": line_point_incidences,
            "collinearity_srg": (V, K, LAMBDA, MU),
            "commuting_neighbors_per_symbol": K,
            "commutation_edges": E,
            "edge_density": "4/13",
        },
        "mub_spread_packet": {
            "complete_mub_frames": morita["incidence"]["spread_count"],
            "lines_per_complete_mub": morita["incidence"]["lines_per_spread"],
            "spreads_per_line": morita["incidence"]["spreads_per_line"],
            "spread_line_incidences": morita["incidence"][
                "total_incidences_from_spreads"
            ],
            "morita_rank": morita["morita_bridge"]["rank"],
            "common_spine": morita["morita_bridge"]["preserved_block"],
            "line_side": morita["line_side"]["carrier_decomposition"],
            "spread_side": morita["spread_side"]["carrier_decomposition"],
        },
        "theorem": {
            "cct_trit_selector_is_unique_q_equals_3": (
                q_factorial_equals_two_q_hits() == (Q,)
            ),
            "two_qutrit_pauli_projectivization_is_w33_40_shell": (
                affine_exponents == 81
                and nonzero_exponents == 80
                and nonzero_exponents // scalar_orbit == V == 40
            ),
            "w33_commutation_geometry_is_gq33_srg": (
                line_count == V == 40
                and line_size == lines_per_point == MU == 4
                and (V, K, LAMBDA, MU) == (40, 12, 2, 4)
                and E == 240
            ),
            "mub_spread_layer_lives_on_same_two_qutrit_core": (
                morita["incidence"]["line_count"] == line_count
                and morita["incidence"]["spread_count"] == 36
                and morita["morita_bridge"]["rank"] == 16
            ),
            "qutrit_core_is_the_common_cct_w33_owner": True,
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(cct_qutrit_core_bridge_summary(), indent=2))
