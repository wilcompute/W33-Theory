"""The triality family sector is simultaneously 1⊕2 and qutrit.

The tomotope family carrier is the 3D triality sector.  Under the even
subgroup C3 it is the qutrit packet; under the full S3 it should split as the
real permutation representation

    3 = 1 ⊕ 2.

This bridge proves that exact dictionary and ties it back to the old
line/plane family flag:

    - the all-ones line is fixed by the full S3 quotient;
    - its orthogonal complement is the 2D standard plane;
    - transpositions have trace 1 and 3-cycles have trace 0 on the 3-sector;
    - those are exactly the character values of 1 ⊕ 2;
    - the old one-vs-two family flag is the real S3 shadow of the same qutrit
      carrier already isolated over C and mod 3.
"""

from __future__ import annotations

from collections import deque
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from exploration.w33_tomotope_mode_chart_action_bridge import user_tomotope_generators
from exploration.w33_tomotope_qutrit_family_bridge import _compose, _three_sector_matrix
from exploration.w33_yukawa_qutrit_collapse_bridge import build_yukawa_qutrit_collapse_summary


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_triality_family_flag_bridge_summary.json"


def _generate_quotient_group() -> set[tuple[float, ...]]:
    gens = user_tomotope_generators()
    matrices = [_three_sector_matrix(permutation) for permutation in gens.values()]
    identity = np.eye(3)
    group = {tuple(identity.reshape(-1))}
    queue = [identity]
    while queue:
        element = queue.pop()
        for generator in matrices:
            image = element @ generator
            key = tuple(np.round(image.reshape(-1), 12))
            if key not in group:
                group.add(key)
                queue.append(image)
    return group


def build_summary() -> dict[str, Any]:
    gens = user_tomotope_generators()
    p1 = _three_sector_matrix(gens["p1"])
    p2 = _three_sector_matrix(gens["p2"])
    cycle = _three_sector_matrix(_compose(gens["p2"], gens["p1"]))

    ones = np.array([1.0, 1.0, 1.0])
    standard_plane_basis = np.array(
        [
            [1.0, -1.0, 0.0],
            [1.0, 1.0, -2.0],
        ]
    ).T

    quotient_group = _generate_quotient_group()
    traces = {
        "identity": 3.0,
        "transposition_p1": float(np.trace(p1)),
        "transposition_p2": float(np.trace(p2)),
        "three_cycle_p2p1": float(np.trace(cycle)),
    }

    summary: dict[str, Any] = {
        "triality_generators": {
            "p1": p1.tolist(),
            "p2": p2.tolist(),
            "cycle_p2p1": cycle.tolist(),
        },
        "family_flag_packet": {
            "fixed_line_generator": ones.tolist(),
            "standard_plane_basis": standard_plane_basis.tolist(),
            "fixed_line_residual_p1": float(np.linalg.norm(p1 @ ones - ones)),
            "fixed_line_residual_p2": float(np.linalg.norm(p2 @ ones - ones)),
            "fixed_line_residual_cycle": float(np.linalg.norm(cycle @ ones - ones)),
            "plane_invariance_residual_p1": float(
                np.linalg.norm(
                    p1 @ standard_plane_basis
                    - standard_plane_basis
                    @ np.linalg.lstsq(standard_plane_basis, p1 @ standard_plane_basis, rcond=None)[0]
                )
            ),
            "plane_invariance_residual_p2": float(
                np.linalg.norm(
                    p2 @ standard_plane_basis
                    - standard_plane_basis
                    @ np.linalg.lstsq(standard_plane_basis, p2 @ standard_plane_basis, rcond=None)[0]
                )
            ),
            "plane_invariance_residual_cycle": float(
                np.linalg.norm(
                    cycle @ standard_plane_basis
                    - standard_plane_basis
                    @ np.linalg.lstsq(standard_plane_basis, cycle @ standard_plane_basis, rcond=None)[0]
                )
            ),
        },
        "character_packet": {
            "quotient_group_order": len(quotient_group),
            "trace_values": traces,
        },
        "upstream_qutrit_theorem": build_yukawa_qutrit_collapse_summary()["qutrit_collapse_theorem"],
        "triality_family_flag_theorem": {
            "the_triality_family_quotient_has_order_six": bool(len(quotient_group) == 6),
            "the_all_ones_line_is_fixed_by_the_full_triality_group": (
                bool(np.linalg.norm(p1 @ ones - ones) < 1e-12)
                and bool(np.linalg.norm(p2 @ ones - ones) < 1e-12)
                and bool(np.linalg.norm(cycle @ ones - ones) < 1e-12)
            ),
            "the_orthogonal_complement_is_an_invariant_two_plane": (
                bool(np.linalg.norm(
                    p1 @ standard_plane_basis
                    - standard_plane_basis
                    @ np.linalg.lstsq(standard_plane_basis, p1 @ standard_plane_basis, rcond=None)[0]
                )
                < 1e-12)
                and bool(np.linalg.norm(
                    p2 @ standard_plane_basis
                    - standard_plane_basis
                    @ np.linalg.lstsq(standard_plane_basis, p2 @ standard_plane_basis, rcond=None)[0]
                )
                < 1e-12)
                and bool(np.linalg.norm(
                    cycle @ standard_plane_basis
                    - standard_plane_basis
                    @ np.linalg.lstsq(standard_plane_basis, cycle @ standard_plane_basis, rcond=None)[0]
                )
                < 1e-12)
            ),
            "the_triality_character_is_exactly_the_real_one_plus_two_family_flag": (
                bool(traces["identity"] == 3.0)
                and bool(traces["transposition_p1"] == 1.0)
                and bool(traces["transposition_p2"] == 1.0)
                and bool(traces["three_cycle_p2p1"] == 0.0)
            ),
            "the_old_line_plane_family_flag_is_the_real_shadow_of_the_qutrit_carrier": (
                bool(build_yukawa_qutrit_collapse_summary()["qutrit_collapse_theorem"][
                    "repo_common_flag_matches_loewy_flag_of_regular_module"
                ])
                and bool(traces["three_cycle_p2p1"] == 0.0)
            ),
        },
        "interpretation": (
            "The family carrier is the same 3D object in three guises: as a qutrit "
            "under the even C3 subgroup, as the real 1⊕2 permutation module under "
            "the full triality S3, and as the old line/plane one-vs-two family flag."
        ),
    }
    return summary


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["triality_family_flag_theorem"], indent=2))


if __name__ == "__main__":
    main()
