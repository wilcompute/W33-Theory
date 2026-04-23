#!/usr/bin/env python3
"""Exact ternary-extension audit for Witting packet transport.

This lifts the packet-side mod-3 transport shadow from an invariant line to the
full indecomposable 2-dimensional transport fiber over F3:

    0 -> 1 -> rho -> sgn -> 0

Tensoring that packet-side fiber with the exact 81-dimensional ternary W33
logical sector gives the exact 81 -> 162 -> 81 matter-flavour bridge.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
import time
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "scripts", ROOT / "exploration", ROOT / "pillars"):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from exploration.w33_flat_ac_spectral_action import build_flat_product_summary  # noqa: E402
from exploration.w33_ternary_homological_code_bridge import build_ternary_homological_code_summary  # noqa: E402
from exploration.w33_transport_ternary_extension_bridge import (  # noqa: E402
    _adapted_basis,
    _all_projective_lines_f3,
    _group_closure_mod_3,
    _line_is_invariant,
    build_transport_ternary_extension_summary,
)
from scripts.w33_witting_packet_transport_path_groupoid_audit import gauge_fixed_edge_matrix  # noqa: E402
from scripts.w33_witting_packet_transport_local_system_audit import _packet_transport_seed  # noqa: E402


MODULUS = 3


def reduced_transport_group() -> list[np.ndarray]:
    graph = _packet_transport_seed()[0]
    directed = []
    for left, right in sorted(graph.edges()):
        directed.append(gauge_fixed_edge_matrix(left, right) % MODULUS)
        directed.append(gauge_fixed_edge_matrix(right, left) % MODULUS)
    return _group_closure_mod_3(directed)


@lru_cache(maxsize=1)
def analyze() -> dict[str, Any]:
    reduced_group = reduced_transport_group()
    projective_lines = _all_projective_lines_f3()
    invariant_lines = [line for line in projective_lines if _line_is_invariant(reduced_group, line)]
    if len(invariant_lines) != 1:
        raise AssertionError("expected a unique invariant projective line")
    invariant_line = invariant_lines[0]

    basis, basis_inverse = _adapted_basis(invariant_line)
    adapted_group = [(basis_inverse @ matrix @ basis) % MODULUS for matrix in reduced_group]
    top_character_values = sorted({int(matrix[0, 0]) for matrix in adapted_group})
    bottom_character_values = sorted({int(matrix[1, 1]) for matrix in adapted_group})
    invariant_complements = [
        line
        for line in projective_lines
        if line != invariant_line and _line_is_invariant(reduced_group, line)
    ]
    off_diagonal_nonzero = sum(int(matrix[0, 1] != 0) for matrix in adapted_group)
    quotient_matches_determinant = all(
        int(matrix[1, 1]) == int(round(float(np.linalg.det(matrix)))) % MODULUS
        for matrix in adapted_group
    )

    ternary_code = build_ternary_homological_code_summary()
    flat = build_flat_product_summary()
    center_summary = build_transport_ternary_extension_summary()

    logical_qutrits = ternary_code["ternary_css_code"]["logical_qutrits"]
    total_dimension = 2 * logical_qutrits

    theorem = {
        "the_packet_reduced_transport_module_is_a_nonsplit_extension_of_sign_by_trivial": (
            len(reduced_group) == 6
            and invariant_line == (1, 2)
            and len(invariant_lines) == 1
            and len(invariant_complements) == 0
            and top_character_values == [1]
            and bottom_character_values == [1, 2]
            and off_diagonal_nonzero > 0
        ),
        "the_packet_quotient_character_equals_the_determinant_sign_shadow": (
            quotient_matches_determinant is True
        ),
        "the_packet_matter_flavour_extension_has_dimensions_81_162_81": (
            logical_qutrits == 81
            and total_dimension == 162
            and total_dimension == flat["coefficients"]["internal_dimension"]
        ),
        "the_packet_extension_recovers_the_same_exact_nonsplit_162sector_as_the_centerquad_route": (
            center_summary["reduced_transport_module"]["unique_invariant_line"] == list(invariant_line)
            and center_summary["reduced_transport_module"]["invariant_complement_count"] == len(invariant_complements)
            and center_summary["reduced_transport_module"]["nonsplit_extension_witness_count"] == off_diagonal_nonzero
            and center_summary["matter_flavour_extension"]["short_exact_sequence_dimensions"]
            == [logical_qutrits, total_dimension, logical_qutrits]
        ),
    }
    theorem["the_witting_packet_layer_carries_the_exact_nonsplit_ternary_transport_extension"] = all(
        theorem.values()
    )

    return {
        "status": "ok",
        "reduced_transport_module": {
            "field": "F3",
            "dimension": 2,
            "holonomy_group_order": len(reduced_group),
            "projective_line_count": len(projective_lines),
            "unique_invariant_line": list(invariant_line),
            "invariant_projective_line_count": len(invariant_lines),
            "invariant_complement_count": len(invariant_complements),
            "adapted_group_is_upper_triangular": all(int(matrix[1, 0]) == 0 for matrix in adapted_group),
            "top_character_values": top_character_values,
            "quotient_character_values": bottom_character_values,
            "quotient_character_equals_determinant_character": quotient_matches_determinant,
            "nonsplit_extension_witness_count": off_diagonal_nonzero,
            "is_nonsplit_extension_of_sign_by_trivial": (
                top_character_values == [1]
                and bottom_character_values == [1, 2]
                and len(invariant_complements) == 0
                and off_diagonal_nonzero > 0
            ),
        },
        "matter_flavour_extension": {
            "base_logical_qutrits": logical_qutrits,
            "submodule_dimension": logical_qutrits,
            "total_dimension": total_dimension,
            "quotient_dimension": logical_qutrits,
            "short_exact_sequence_dimensions": [logical_qutrits, total_dimension, logical_qutrits],
            "matches_flat_internal_dimension_exactly": total_dimension == flat["coefficients"]["internal_dimension"],
        },
        "invariant_crosswalk": {
            "unique_invariant_line_matches_centerquad": (
                center_summary["reduced_transport_module"]["unique_invariant_line"] == list(invariant_line)
            ),
            "nonsplit_witness_count_matches_centerquad": (
                center_summary["reduced_transport_module"]["nonsplit_extension_witness_count"] == off_diagonal_nonzero
            ),
            "short_exact_sequence_matches_centerquad": (
                center_summary["matter_flavour_extension"]["short_exact_sequence_dimensions"]
                == [logical_qutrits, total_dimension, logical_qutrits]
            ),
        },
        "packet_transport_ternary_extension_theorem": theorem,
        "bridge_verdict": (
            "Over F3 the packet-side reduced transport fiber is already the exact non-split local system "
            "0 -> 1 -> rho -> sgn -> 0: the unique invariant line is trivial, the quotient line carries the "
            "binary sign shadow, and there is no invariant complementary line. Tensoring with the exact "
            "81-dimensional W33 ternary logical sector gives 0 -> 81 -> 162 -> 81 -> 0. So the packet route "
            "recovers the same structural 162-sector explanation as the older center-quad transport bridge."
        ),
    }


def main() -> int:
    timer = time.perf_counter()
    payload = analyze()
    output_dir = ROOT / "checks"
    output_dir.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXXVIII_witting_packet_transport_ternary_extension_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2, default=int), encoding="utf-8")

    print("W33 Witting packet transport ternary-extension audit")
    for key, value in payload["packet_transport_ternary_extension_theorem"].items():
        print(f"  [{'PASS' if value else 'FAIL'}] {key}")
    print(f"  Wrote: {output_path}")
    print(f"  Runtime: {time.perf_counter() - timer:.3f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
