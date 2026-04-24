"""Exact symmetry ladder for the W(3,3) qutrit/Clifford backbone.

The active paper uses the single number ``51840`` as the "two-qutrit Clifford"
hardware count. The repo already knows the sharper finite picture:

1. The exact projective symplectic / projective Clifford action on the 40
   projective two-qutrit Pauli observables has order

       25920 = |PSp(4,3)| = 40 * 648.

2. The full graph symmetry of the W(3,3) commutation graph has order

       51840 = |Aut(W33)| = 2 * 25920 = 40 * 1296.

   This is the anti-symplectic extension already used in the local neighbor
   action analysis.

3. At a base vertex, the full point stabilizer of order ``1296`` induces a
   ``432``-element affine action on the 12-neighborhood, with exact data:

       432 = 9 * 48,
       translation subgroup order 9,
       triangle action order 24 = S4,
       involution split 45 = 36 + 9.

4. On the complementary H27 shell, the exact local affine group has order
   ``1296`` while the local projective subgroup has order ``648``, matching the
   full and projective point stabilizers respectively.

So the clean finite ladder is:

    projective Clifford kernel     25920
    full graph symmetry            51840
    local affine/H27 stabilizer     1296
    local projective/Hessian         648
    induced 12-neighbor action       432.

This resolves the paper-facing ambiguity:
- ``25920`` is the exact projective Clifford action on observables;
- ``51840`` is the exact full graph-symmetry extension;
- the local computation bus is the exact affine 432-layer.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_qutrit_symmetry_ladder_bridge_summary.json"

for candidate in (ROOT, ROOT / "scripts", ROOT / "tools"):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from scripts.w33_exact_lie_bridge_audit import (  # noqa: E402
    local_h27_affine_symmetry_summary,
    projective_symplectic_action_summary,
)
from scripts.w33_qutrit_operator_algebra import analyze as analyze_qutrit_operator_layer  # noqa: E402
from tools.analyze_w33_neighbor_action_agl23 import build_report  # noqa: E402


@lru_cache(maxsize=1)
def build_qutrit_symmetry_ladder_summary() -> dict[str, Any]:
    projective = projective_symplectic_action_summary()
    local = local_h27_affine_symmetry_summary()
    neighbor = build_report(base_vertex=0)
    operator = analyze_qutrit_operator_layer()

    projective_order = int(projective["enumerated_group_order"])
    full_order = int(local["full_graph_group_order"])
    projective_point_stabilizer = int(projective["point_stabilizer_order"])
    full_point_stabilizer = int(local["full_graph_point_stabilizer_order"])
    induced_neighbor_order = int(neighbor["neighbor_action"]["induced_group_order"])
    translation_order = int(neighbor["neighbor_action"]["translations"]["order"])
    triangle_action_order = int(neighbor["neighbor_action"]["triangle_action_order"])
    edge_count = int(projective["edge_orbit_size"])

    return {
        "symmetry_ladder_dictionary": {
            "projective_layer": {
                "group_label": "PSp(4,3)",
                "hardware_label": "projective two-qutrit Clifford action on observables",
                "order": projective_order,
                "point_orbit_size": int(projective["point_orbit_size"]),
                "point_stabilizer_order": projective_point_stabilizer,
                "edge_orbit_size": edge_count,
                "edge_stabilizer_order": projective_order // edge_count,
                "generator_names": list(operator["symplectic_action"]["generator_names"]),
            },
            "full_graph_layer": {
                "group_label": "Aut(W33)",
                "hardware_label": "full graph symmetry / anti-symplectic extension",
                "order": full_order,
                "point_stabilizer_order": full_point_stabilizer,
                "edge_stabilizer_order": full_order // edge_count,
            },
            "local_h27_layer": {
                "affine_group_order": int(local["local_affine_group_order"]),
                "projective_subgroup_order": int(local["local_projective_subgroup_order"]),
                "full_point_stabilizer_matches_local_affine": bool(
                    local["matches_full_graph_local_order"]
                ),
                "projective_point_stabilizer_matches_local_projective": bool(
                    local["matches_projective_local_order"]
                ),
            },
            "neighbor_bus_layer": {
                "neighbor_count": int(neighbor["neighborhood"]["neighbor_count"]),
                "induced_group_order": induced_neighbor_order,
                "kernel_from_full_stabilizer_order": int(
                    neighbor["neighbor_action"]["kernel_order"]
                ),
                "triangle_action_order": triangle_action_order,
                "triangle_action_is_s4": bool(
                    neighbor["neighbor_action"]["triangle_action_is_S4"]
                ),
                "triangle_kernel_order": int(
                    neighbor["neighbor_action"]["triangle_kernel_order"]
                ),
                "translation_subgroup_order": translation_order,
                "translation_subgroup_is_normal_abelian": bool(
                    neighbor["neighbor_action"]["translations"]["is_normal"]
                    and neighbor["neighbor_action"]["translations"]["is_abelian"]
                    and neighbor["neighbor_action"]["translations"]["is_subgroup"]
                ),
                "involution_count": int(neighbor["involutions"]["count"]),
                "reflection_count": int(neighbor["involutions"]["reflection_count"]),
                "rotation_count": int(neighbor["involutions"]["rotation_count"]),
                "reflection_centralizer_matches_d12": bool(
                    neighbor["involutions"][
                        "reflection_centralizer_matches_d12_fingerprint"
                    ]
                ),
            },
            "exact_factorizations": {
                "projective_order_factorization": "25920 = 40 * 648 = 240 * 108",
                "full_order_factorization": "51840 = 2 * 25920 = 40 * 1296 = 240 * 216",
                "neighbor_action_factorization": "432 = 9 * 48",
                "point_stabilizer_factorization": "1296 = 2 * 648",
            },
        },
        "symmetry_ladder_theorem": {
            "projective_clifford_order_is_25920": projective_order == 25920,
            "full_graph_symmetry_order_is_51840": full_order == 51840,
            "full_graph_symmetry_doubles_the_projective_clifford_layer": (
                full_order == 2 * projective_order
            ),
            "projective_point_stabilizer_is_648": (
                projective_point_stabilizer == 648
            ),
            "full_point_stabilizer_is_1296": full_point_stabilizer == 1296,
            "local_h27_affine_group_matches_the_full_point_stabilizer": bool(
                local["matches_full_graph_local_order"]
                and int(local["local_affine_group_order"]) == 1296
            ),
            "local_h27_projective_group_matches_the_projective_point_stabilizer": bool(
                local["matches_projective_local_order"]
                and int(local["local_projective_subgroup_order"]) == 648
            ),
            "the_12_neighbor_bus_is_the_exact_432_affine_layer": (
                induced_neighbor_order == 432 and neighbor["claim_holds"] is True
            ),
            "the_neighbor_bus_contains_the_exact_order_9_translation_packet": (
                translation_order == 9
                and neighbor["neighbor_action"]["translations"]["is_subgroup"] is True
                and neighbor["neighbor_action"]["translations"]["is_abelian"] is True
                and neighbor["neighbor_action"]["translations"]["is_normal"] is True
            ),
            "the_neighbor_bus_acts_by_s4_on_the_four_neighbor_triangles": (
                triangle_action_order == 24
                and neighbor["neighbor_action"]["triangle_action_is_S4"] is True
            ),
            "the_involution_layer_splits_exactly_as_36_reflections_plus_9_rotations": (
                int(neighbor["involutions"]["count"]) == 45
                and int(neighbor["involutions"]["reflection_count"]) == 36
                and int(neighbor["involutions"]["rotation_count"]) == 9
            ),
            "the_reflection_centralizer_has_the_exact_d12_fingerprint": bool(
                neighbor["involutions"]["reflection_centralizer_matches_d12_fingerprint"]
            ),
        },
        "boundary_note": (
            "This bridge closes the exact symmetry ladder and fixes the paper-level "
            "25920 versus 51840 ambiguity. It does not prove explicit magic-state "
            "injection or universality from the cubic invariant; that remains a "
            "separate boundary beyond the exact finite group data."
        ),
        "bridge_verdict": (
            "The qutrit/Clifford hardware is now exact at the group-action level. "
            "The projective Clifford layer on observables has order 25920, the "
            "full W33 graph symmetry doubles it to 51840, the H27 local affine "
            "layer has order 1296, and the 12-neighbor computation bus closes as "
            "the exact 432-element affine packet with translation subgroup 9 and "
            "triangle quotient S4."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_qutrit_symmetry_ladder_summary(), indent=2),
        encoding="utf-8",
    )
    return path


if __name__ == "__main__":
    write_summary()
