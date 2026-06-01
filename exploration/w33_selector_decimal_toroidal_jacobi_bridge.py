"""Selector / decimal / toroidal / Jacobi bridge at q = 3.

This module consolidates several exact repo-native packets that have been
verified independently but not yet pressed into one executable surface:

  - the local 3-branch qutrit selector is exact S3 of order 6;
  - the global selector / host packet is exact
      162 = 6*27 = 2*81 = 81 + 81;
  - the decimal/toroidal shell is exact
        84 = 12*7 = 14*6 = 21*4;
  - the qutrit-native cyclotomic atoms satisfy
        q^3 - (Phi3 + 2 Phi6) = (q - 3) Phi4,
    so at q = 3 one gets
        27 = 13 + 14,
        81 = 39 + 42,
        162 = 78 + 84;
  - the Z3-graded E8 Jacobi checker closes with the explicit exact-rational
    scales (+1/6, -1/6).

The point is not to replace the qutrit-native theory with decimal numerology.
Rather, base 10 is treated here as the readable shadow Phi4 = q^2 + 1 = 10 at
q = 3, while the structural identities remain expressed in qutrit-native atoms.

Honesty boundary:
  - this script gives an exact source for +1/6 as the local S3 averaging
    coefficient on the 3-branch selector;
  - it does NOT yet derive the negative sign of -1/6 conceptually.  On the
    local 3-point permutation representation the sign projector vanishes, so the
    negative coefficient remains a dual/oriented-sector frontier.
"""

from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
import json
from pathlib import Path
import sys
from typing import Any, Sequence

import numpy as np


if __package__ in {None, ""}:
    ROOT = Path(__file__).resolve().parents[1]
    for candidate in (ROOT, ROOT / "exploration"):
        if str(candidate) not in sys.path:
            sys.path.insert(0, str(candidate))
else:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT / "exploration") not in sys.path:
        sys.path.insert(0, str(ROOT / "exploration"))

from PART_CLXIII_DECIMAL_REPTEND_COMPILER import (  # noqa: E402
    PHI3,
    PHI4,
    PHI6,
    Q,
    RANK_SEED,
    decimal_reptend_compiler_audit,
)
from verify_dccxxii_mod12_toroidal_synthesis import build_bridge as build_dccxxii_bridge  # noqa: E402
from scripts.w33_h4_s3_selector_holonomy_audit import (  # noqa: E402
    h4_s3_selector_holonomy_summary,
)
from verify_dclxiv_holonomy_qutrit_transvection_bridge import (  # noqa: E402
    build_bridge as build_dclxiv_bridge,
)
from w33_k3_mixed_plane_nilpotent_holonomy_increment_bridge import (  # noqa: E402
    build_k3_mixed_plane_nilpotent_holonomy_increment_summary,
)


DATA_DIR = ROOT / "data"
ARTIFACT_PATH = ROOT / "artifacts" / "toe_e8_z3graded_jacobi.json"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_selector_decimal_toroidal_jacobi_bridge_summary.json"
FLOAT_TOL = 1e-12


def _permutation_matrix(action: Sequence[int]) -> np.ndarray:
    size = len(action)
    matrix = np.zeros((size, size), dtype=float)
    for column, image in enumerate(action):
        matrix[image, column] = 1.0
    return matrix


def _compose(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return tuple(left[index] for index in right)


def _closure(generators: Sequence[Sequence[int]]) -> list[tuple[int, ...]]:
    generators = [tuple(generator) for generator in generators]
    identity = tuple(range(len(generators[0])))
    seen = {identity}
    frontier = [identity]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            candidate = _compose(generator, current)
            if candidate not in seen:
                seen.add(candidate)
                frontier.append(candidate)
    return sorted(seen)


def _permutation_parity(action: Sequence[int]) -> int:
    inversions = 0
    for i, value_i in enumerate(action):
        for value_j in action[i + 1 :]:
            if value_i > value_j:
                inversions += 1
    return -1 if inversions % 2 else 1


def _fraction_string(value: float | Fraction, *, max_denominator: int = 84) -> str:
    if isinstance(value, Fraction):
        frac = value
    else:
        frac = Fraction(str(float(value))).limit_denominator(max_denominator)
    if frac.denominator == 1:
        return str(frac.numerator)
    return f"{frac.numerator}/{frac.denominator}"


def _matrix_fraction_strings(matrix: np.ndarray, *, max_denominator: int = 84) -> list[list[str]]:
    return [
        [_fraction_string(entry, max_denominator=max_denominator) for entry in row]
        for row in matrix
    ]


def _matrix_rank(matrix: np.ndarray) -> int:
    return int(np.linalg.matrix_rank(matrix, tol=1e-10))


def _load_jacobi_artifact(path: Path = ARTIFACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def build_selector_decimal_toroidal_jacobi_summary() -> dict[str, Any]:
    dclxiv = build_dclxiv_bridge()
    selector_summary = h4_s3_selector_holonomy_summary()
    k3_nilpotent = build_k3_mixed_plane_nilpotent_holonomy_increment_summary()
    dccxxii = build_dccxxii_bridge()
    decimal_compiler = decimal_reptend_compiler_audit()
    jacobi = _load_jacobi_artifact()

    selector_order = int(selector_summary["s3_selector_theorem_packet"]["stabilizer"]["order"])
    local_bulk = int(dclxiv["summary"]["affine_bulk_count"])
    ordered_adjacent_pairs = int(selector_summary["heisenberg_transport_packet"]["ordered_adjacent_pairs"])
    global_selector_carrier = int(selector_summary["h4_alignment_packet"]["nonlocal_quadrangle_carrier"])
    local_fiber_count = int(dclxiv["summary"]["affine_fiber_count"])
    global_qutrit_fiber_count = ordered_adjacent_pairs * local_fiber_count
    common_packet = selector_order * local_bulk
    host_support = k3_nilpotent["canonical_mixed_plane_support"]
    positive_support_size, negative_support_size = [
        int(value) for value in host_support["qutrit_lift_split"]
    ]
    host_support_total = positive_support_size + negative_support_size
    deterministic_frame_size = positive_support_size

    decimal_period = int(decimal_compiler["reptend_core"]["period_ord_den_base"])
    genus_denominator = int(dccxxii["summary"]["codec"])
    heawood_shell = int(dccxxii["summary"]["heawood"])
    heawood_vertices = int(dccxxii["heawood_graph"]["vertices"])
    heawood_edges = int(dccxxii["heawood_graph"]["edges"])
    tetra_fixed_point = int(dccxxii["polyhedra"]["tetrahedron_g0"]["V"])
    shell_84 = genus_denominator * heawood_shell

    translation = (1, 2, 0)
    reflection = (0, 2, 1)
    local_group = _closure([translation, reflection])
    permutation_matrices = [_permutation_matrix(element) for element in local_group]
    parities = [_permutation_parity(element) for element in local_group]
    trivial_projector = sum(permutation_matrices) / selector_order
    sign_projector = sum(
        parity * matrix for parity, matrix in zip(parities, permutation_matrices, strict=True)
    ) / selector_order
    standard_projector = np.eye(3, dtype=float) - trivial_projector - sign_projector

    q_cubic = Q**3
    phi3_plus_two_phi6 = PHI3 + 2 * PHI6
    q_cubic_splice_defect = q_cubic - phi3_plus_two_phi6
    q_cubic_splice_rhs = (Q - 3) * PHI4

    exact_gradient_39 = Q * PHI3
    toroidal_cell_chart_42 = sum(dccxxii["polyhedra"]["csaszar_g1"][key] for key in ("V", "E", "F"))
    protected_sector_81 = positive_support_size
    e6_packet_78 = selector_order * PHI3

    jacobi_scale_sl3 = float(jacobi["scales"]["scale_sl3"])
    jacobi_scale_g2g2 = float(jacobi["scales"]["scale_g2g2"])
    expected_plus_one_sixth = Fraction(1, 6)
    expected_minus_one_sixth = Fraction(-1, 6)

    one_over_shell_dictionary = {
        "1_over_6": _fraction_string(Fraction(heawood_vertices, shell_84)),
        "1_over_7": _fraction_string(Fraction(genus_denominator, shell_84)),
        "1_over_12": _fraction_string(Fraction(heawood_shell, shell_84)),
    }

    return {
        "status": "ok",
        "base10_qutrit_shadow": {
            "q": Q,
            "phi3": PHI3,
            "phi4": PHI4,
            "phi6": PHI6,
            "rank_seed_2q": RANK_SEED,
            "readable_shadow": (
                "Base 10 is treated here as the readable shadow Phi4 = q^2 + 1 = 10 at q = 3, "
                "not as the fundamental ontology. The underlying identities remain qutrit-native."
            ),
        },
        "local_selector_packet": {
            "selector_order": selector_order,
            "local_bulk": local_bulk,
            "ordered_adjacent_pairs": ordered_adjacent_pairs,
            "global_selector_carrier": global_selector_carrier,
            "global_qutrit_fiber_count": global_qutrit_fiber_count,
            "elements": [list(element) for element in local_group],
            "parities": parities,
            "average_weight": _fraction_string(expected_plus_one_sixth),
            "trivial_projector": {
                "matrix": trivial_projector.tolist(),
                "rational_matrix": _matrix_fraction_strings(trivial_projector),
                "rank": _matrix_rank(trivial_projector),
            },
            "sign_projector": {
                "matrix": sign_projector.tolist(),
                "rational_matrix": _matrix_fraction_strings(sign_projector),
                "rank": _matrix_rank(sign_projector),
            },
            "standard_projector": {
                "matrix": standard_projector.tolist(),
                "rational_matrix": _matrix_fraction_strings(standard_projector),
                "rank": _matrix_rank(standard_projector),
            },
            "theorem": {
                "selector_order_is_exactly_six": selector_order == 6,
                "global_scaling_is_exactly_60_times_27_equals_1620": (
                    ordered_adjacent_pairs * local_bulk == global_selector_carrier == 1620
                ),
                "plus_one_sixth_is_exact_local_selector_average": np.allclose(
                    trivial_projector,
                    np.ones((3, 3), dtype=float) / 3.0,
                    atol=FLOAT_TOL,
                ),
                "sign_projector_vanishes_on_the_three_branch_permutation_rep": np.allclose(
                    sign_projector,
                    0.0,
                    atol=FLOAT_TOL,
                ),
                "standard_projector_has_rank_two": _matrix_rank(standard_projector) == 2,
            },
        },
        "decimal_toroidal_shell_packet": {
            "decimal_period": decimal_period,
            "heawood_shell": heawood_shell,
            "genus_denominator": genus_denominator,
            "heawood_vertices": heawood_vertices,
            "heawood_edges": heawood_edges,
            "tetra_fixed_point": tetra_fixed_point,
            "single_surface_flags": shell_84,
            "fraction_dictionary": one_over_shell_dictionary,
            "reptend": decimal_compiler["reptend_core"]["reptend"],
            "q_axis_missing_denominators": decimal_compiler["digit_partition_1_to_9"]["q_axis_missing_denominators"],
            "theorem": {
                "decimal_period_equals_local_selector_order": decimal_period == selector_order == 6,
                "shell_84_factorization_holds": (
                    shell_84 == genus_denominator * heawood_shell == heawood_vertices * decimal_period == heawood_edges * tetra_fixed_point
                ),
                "one_over_six_is_heawood_vertices_over_shell_84": one_over_shell_dictionary["1_over_6"] == "1/6",
                "one_over_seven_is_genus_denominator_over_shell_84": one_over_shell_dictionary["1_over_7"] == "1/7",
                "one_over_twelve_is_heawood_shell_over_shell_84": one_over_shell_dictionary["1_over_12"] == "1/12",
            },
        },
        "common_packet_packet": {
            "common_packet": common_packet,
            "deterministic_frame_size": deterministic_frame_size,
            "host_support_total": host_support_total,
            "host_support_split": [positive_support_size, negative_support_size],
            "q_cubic_identity": {
                "q_cubic": q_cubic,
                "phi3_plus_two_phi6": phi3_plus_two_phi6,
                "splice_defect": q_cubic_splice_defect,
                "splice_rhs": q_cubic_splice_rhs,
                "formula": "q^3 - (Phi3 + 2 Phi6) = (q - 3) Phi4",
            },
            "exact_splices": {
                "27_equals_13_plus_14": [q_cubic, PHI3, 2 * PHI6],
                "81_equals_39_plus_42": [protected_sector_81, exact_gradient_39, toroidal_cell_chart_42],
                "162_equals_78_plus_84": [common_packet, e6_packet_78, shell_84],
            },
            "theorem": {
                "common_packet_is_exactly_6_times_27": common_packet == selector_order * local_bulk == 162,
                "common_packet_is_exactly_2_times_81": common_packet == 2 * deterministic_frame_size == 162,
                "common_packet_is_exactly_81_plus_81": common_packet == host_support_total == positive_support_size + negative_support_size == 162,
                "q_cubic_splits_exactly_as_phi3_plus_two_phi6_at_q3": q_cubic == phi3_plus_two_phi6 == 27,
                "protected_81_sector_splits_as_39_plus_42": protected_sector_81 == exact_gradient_39 + toroidal_cell_chart_42 == 81,
                "common_162_packet_splits_as_78_plus_84": common_packet == e6_packet_78 + shell_84 == 162,
            },
        },
        "jacobi_packet": {
            "artifact_path": str(ARTIFACT_PATH),
            "status": jacobi["status"],
            "scales": jacobi["scales"],
            "jacobi": jacobi["jacobi"],
            "theorem": {
                "artifact_status_is_ok": jacobi["status"] == "ok",
                "scale_sl3_is_exact_plus_one_sixth": abs(jacobi_scale_sl3 - float(expected_plus_one_sixth)) < FLOAT_TOL,
                "scale_g2g2_is_exact_minus_one_sixth": abs(jacobi_scale_g2g2 - float(expected_minus_one_sixth)) < FLOAT_TOL,
                "jacobi_closes_at_exact_plus_minus_one_sixth": (
                    jacobi["status"] == "ok"
                    and abs(jacobi_scale_sl3 - float(expected_plus_one_sixth)) < FLOAT_TOL
                    and abs(jacobi_scale_g2g2 - float(expected_minus_one_sixth)) < FLOAT_TOL
                ),
            },
        },
        "frontier_packet": {
            "exact_read": (
                "+1/6 is now explained by exact local selector averaging on the 3-branch qutrit fiber, "
                "and the same q=3 shell also supports the exact arithmetic splices 27=13+14, 81=39+42, and 162=78+84."
            ),
            "unresolved_read": (
                "The local 3-point permutation representation has zero sign projector, so the negative Jacobi coefficient "
                "-1/6 is not explained by a literal local sign-projection. The remaining problem is to derive that minus sign "
                "from the dual/oriented g2 sector."
            ),
        },
        "bridge_theorem": {
            "local_selector_average_explains_plus_one_sixth": np.allclose(
                trivial_projector,
                np.ones((3, 3), dtype=float) / 3.0,
                atol=FLOAT_TOL,
            ),
            "decimal_period_matches_selector_order": decimal_period == selector_order == 6,
            "shell_84_is_exactly_12_times_7_equals_14_times_6": (
                shell_84 == genus_denominator * heawood_shell == heawood_vertices * selector_order
            ),
            "q_cubic_identity_specializes_exactly_at_q3": q_cubic == phi3_plus_two_phi6 == 27,
            "protected_81_packet_splits_as_39_plus_42": protected_sector_81 == exact_gradient_39 + toroidal_cell_chart_42,
            "common_162_packet_splits_as_78_plus_84": common_packet == e6_packet_78 + shell_84,
            "jacobi_closes_at_exact_plus_minus_one_sixth": (
                jacobi["status"] == "ok"
                and abs(jacobi_scale_sl3 - float(expected_plus_one_sixth)) < FLOAT_TOL
                and abs(jacobi_scale_g2g2 - float(expected_minus_one_sixth)) < FLOAT_TOL
            ),
            "minus_one_sixth_remains_dual_orientation_frontier": np.allclose(sign_projector, 0.0, atol=FLOAT_TOL),
        },
        "bridge_verdict": (
            "The decimal/toroidal hints are not a distraction from the selector frontier. They sharpen it. "
            "At q=3, base 10 is the readable shadow Phi4=q^2+1, the local qutrit selector has exact average weight 1/6, "
            "the decimal/toroidal shell is the exact packet 84=12*7=14*6=21*4, and the exact common selector/host packet "
            "admits the arithmetic splice 162=78+84. The positive Jacobi coefficient +1/6 is therefore explained by the exact local selector average, "
            "while the negative coefficient -1/6 remains the dual/oriented-sector problem."
        ),
        "source_files": [
            "verify_dclxiv_holonomy_qutrit_transvection_bridge.py",
            "scripts/w33_h4_s3_selector_holonomy_audit.py",
            "exploration/w33_k3_mixed_plane_nilpotent_holonomy_increment_bridge.py",
            "PART_CLXIII_DECIMAL_REPTEND_COMPILER.py",
            "verify_dccxxii_mod12_toroidal_synthesis.py",
            "artifacts/toe_e8_z3graded_jacobi.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_selector_decimal_toroidal_jacobi_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
