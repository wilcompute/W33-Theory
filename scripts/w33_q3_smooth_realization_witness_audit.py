#!/usr/bin/env python3
"""Exact q=3 smooth-realization witness audit.

This module isolates the finite witness conditions that remain after the q=3
master lock reductions. It packages three executable checks:

1. Witness existence: a non-identity sign-trivial unipotent holonomy matrix
   exists with nilpotent increment N^2 = 0.
2. Witness uniqueness: the two nontrivial sign-trivial holonomies are
   gauge-equivalent, so the witness is unique up to gauge.
3. Witness embedding: the same witness datum sits on the fixed K3 channel and
   on the canonical 45-point quotient carrier used by the finite bridge.

The output is an auditable dict suitable for direct pytest assertions.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
import time
from typing import Any, Dict

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
EXPLORATION = ROOT / "exploration"
for candidate in (ROOT, EXPLORATION):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from w33_k3_mixed_plane_holonomy_witness_bridge import (  # noqa: E402
    build_k3_mixed_plane_holonomy_witness_summary,
)
from w33_k3_tail_affine_witness_target_bridge import (  # noqa: E402
    build_k3_tail_affine_witness_target_summary,
)
from w33_h4_ordered_path_k3_witness_bridge import (  # noqa: E402
    build_h4_ordered_path_k3_witness_bridge_summary,
)
from w33_center_quad_gq42_e6_bridge import quotient_points  # noqa: E402


@lru_cache(maxsize=1)
def verify_witness_existence() -> Dict[str, Any]:
    """Verify existence of a nontrivial sign-trivial unipotent witness."""
    summary = build_k3_mixed_plane_holonomy_witness_summary()
    witness = summary["mixed_plane_holonomy_witness"]
    theorem = summary["k3_mixed_plane_holonomy_witness_theorem"]

    canonical = np.array(witness["canonical_nontrivial_holonomy"], dtype=int)
    identity = np.eye(2, dtype=int)
    nilpotent = canonical - identity

    eigvals = np.linalg.eigvals(canonical.astype(float))
    all_eigenvalues_one = bool(np.allclose(eigvals, np.ones_like(eigvals)))

    return {
        "canonical_holonomy": witness["canonical_nontrivial_holonomy"],
        "determinant": int(round(float(np.linalg.det(canonical)))),
        "is_nontrivial": bool(np.array_equal(canonical, identity) is False),
        "is_sign_trivial": int(round(float(np.linalg.det(canonical)))) == 1,
        "is_unipotent": all_eigenvalues_one,
        "nilpotent_increment": nilpotent.astype(int).tolist(),
        "nilpotent_square": (nilpotent @ nilpotent).astype(int).tolist(),
        "nilpotent_square_is_zero": bool(np.array_equal(nilpotent @ nilpotent, np.zeros((2, 2), dtype=int))),
        "bridge_theorem_support": theorem[
            "a_nonzero_sign_trivial_cocycle_value_is_equivalent_to_a_nonidentity_unipotent_adapted_holonomy_matrix"
        ],
        "witness_existence_verified": (
            theorem[
                "a_nonzero_sign_trivial_cocycle_value_is_equivalent_to_a_nonidentity_unipotent_adapted_holonomy_matrix"
            ]
            and int(round(float(np.linalg.det(canonical)))) == 1
            and all_eigenvalues_one
            and bool(np.array_equal(canonical, identity) is False)
            and bool(np.array_equal(nilpotent @ nilpotent, np.zeros((2, 2), dtype=int)))
        ),
    }


@lru_cache(maxsize=1)
def verify_witness_uniqueness() -> Dict[str, Any]:
    """Verify uniqueness up to gauge in the sign-trivial sector."""
    summary = build_k3_mixed_plane_holonomy_witness_summary()
    witness = summary["mixed_plane_holonomy_witness"]
    theorem = summary["k3_mixed_plane_holonomy_witness_theorem"]

    nontrivial = sorted(witness["nontrivial_sign_trivial_holonomy_matrices"])

    return {
        "nontrivial_sign_trivial_holonomies": nontrivial,
        "expected_two_holonomies": [[[1, 1], [0, 1]], [[1, 2], [0, 1]]],
        "gauge_conjugated_matrix": witness["conjugated_matrix"],
        "theorem_gauge_equivalent": theorem[
            "the_two_nontrivial_sign_trivial_holonomies_are_gauge_equivalent"
        ],
        "witness_uniqueness_verified": (
            nontrivial == [[[1, 1], [0, 1]], [[1, 2], [0, 1]]]
            and witness["conjugated_matrix"] == [[1, 2], [0, 1]]
            and theorem["the_two_nontrivial_sign_trivial_holonomies_are_gauge_equivalent"] is True
            and theorem[
                "therefore_exact_k3_tail_realization_is_equivalent_to_one_support_preserving_nontrivial_sign_trivial_holonomy_witness_on_the_same_fixed_host"
            ]
            is True
        ),
    }


@lru_cache(maxsize=1)
def verify_witness_embedding() -> Dict[str, Any]:
    """Verify embedding of the witness into the fixed finite/continuum carriers."""
    affine = build_k3_tail_affine_witness_target_summary()
    h4_bridge = build_h4_ordered_path_k3_witness_bridge_summary()

    points_45 = len(quotient_points())

    affine_theorem = affine["k3_tail_affine_witness_target_theorem"]
    h4_theorem = h4_bridge["theorem"]

    return {
        "quotient_point_carrier_size": points_45,
        "k3_fixed_channel": affine["fixed_k3_tail_exactness_channel"],
        "h4_ordered_path_carrier": h4_bridge["finite_ordered_path_carrier"],
        "k3_chart_target": h4_bridge["k3_witness_chart"],
        "affine_target_theorem": affine_theorem[
            "therefore_the_live_external_wall_is_one_exact_affine_witness_target_on_the_same_fixed_package"
        ],
        "shared_transport_theorem": h4_theorem[
            "therefore_the_live_k3_witness_is_the_ordered_path_transport_law_written_on_the_fixed_tail_chart"
        ],
        "witness_embedding_verified": (
            points_45 == 45
            and affine_theorem[
                "therefore_the_live_external_wall_is_one_exact_affine_witness_target_on_the_same_fixed_package"
            ]
            is True
            and h4_theorem[
                "therefore_the_live_k3_witness_is_the_ordered_path_transport_law_written_on_the_fixed_tail_chart"
            ]
            is True
            and h4_bridge["k3_witness_chart"]["target_coordinate"] == "dC"
            and h4_bridge["k3_witness_chart"]["required_value"] == "14105"
        ),
    }


@lru_cache(maxsize=1)
def analyze() -> Dict[str, Any]:
    """Return the complete smooth-realization witness audit packet."""
    existence = verify_witness_existence()
    uniqueness = verify_witness_uniqueness()
    embedding = verify_witness_embedding()

    theorem = {
        "witness_existence_verified": existence["witness_existence_verified"],
        "witness_uniqueness_verified": uniqueness["witness_uniqueness_verified"],
        "witness_embedding_verified": embedding["witness_embedding_verified"],
    }
    theorem["smooth_realization_predicate_passes"] = all(theorem.values())

    return {
        "status": "ok",
        "q3_smooth_realization_witness": {
            "existence_packet": existence,
            "uniqueness_packet": uniqueness,
            "embedding_packet": embedding,
        },
        "q3_smooth_realization_witness_theorem": theorem,
        "boundary_note": (
            "This audit certifies finite witness existence, uniqueness up to gauge, "
            "and fixed-carrier embedding. It does not claim a full smooth global "
            "realization theorem beyond these executable witness predicates."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_B_q3_smooth_realization_witness_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[ok] wrote {output_path}")


if __name__ == "__main__":
    main()
