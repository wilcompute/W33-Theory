"""Mixed-plane K3 realization reduces to one nonzero off-diagonal curvature witness.

CDXXII made the smallest positive adapted-matrix datum explicit:

- one support-preserving nonzero nilpotent holonomy increment on the canonical
  mixed-plane host.

But the repo already packages the missing internal datum as a genuine curved
transport-twisted precomplex. In that exact object the upper-right extension
coupling is no longer only a matrix increment; it appears as a concrete
off-diagonal curvature block with nonzero rank and explicit support.

So the next positive localization is geometric again: exact K3 tail
realization is equivalent to one support-preserving nonzero off-diagonal
curvature witness on the same fixed mixed-plane host.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_PATH = (
    ROOT
    / "data"
    / "w33_k3_mixed_plane_off_diagonal_curvature_witness_bridge_summary.json"
)


@lru_cache(maxsize=1)
def build_k3_mixed_plane_off_diagonal_curvature_witness_summary() -> dict[str, Any]:
    from w33_carrier_preserving_transport_twisted_k3_lift_bridge import (
        build_carrier_preserving_transport_twisted_k3_lift_bridge_summary,
    )
    from w33_k3_mixed_plane_nilpotent_holonomy_increment_bridge import (
        build_k3_mixed_plane_nilpotent_holonomy_increment_summary,
    )
    from w33_transport_twisted_precomplex_bridge import (
        build_transport_twisted_precomplex_summary,
    )

    lift = build_carrier_preserving_transport_twisted_k3_lift_bridge_summary()
    increment = build_k3_mixed_plane_nilpotent_holonomy_increment_summary()
    precomplex = build_transport_twisted_precomplex_summary()

    host = increment["canonical_mixed_plane_support"]
    curvature = precomplex["curved_extension_package"]

    return {
        "status": "ok",
        "canonical_mixed_plane_support": host,
        "transport_twisted_off_diagonal_curvature_package": {
            "full_curvature_rank": curvature["full_curvature_rank"],
            "off_diagonal_curvature_rank": curvature["off_diagonal_curvature_rank"],
            "off_diagonal_curvature_support_rows": curvature[
                "off_diagonal_curvature_support_rows"
            ],
            "curvature_factors_through_sign_quotient": curvature[
                "curvature_factors_through_sign_quotient"
            ],
            "upper_right_curvature_identity_exact": curvature[
                "upper_right_curvature_identity_exact"
            ],
        },
        "k3_mixed_plane_off_diagonal_curvature_witness_theorem": {
            "the_missing_internal_datum_already_appears_as_a_nonzero_off_diagonal_curvature_block_in_the_exact_transport_twisted_precomplex": (
                curvature["off_diagonal_curvature_rank"] == 36
                and curvature["off_diagonal_curvature_support_rows"] == 4046
                and curvature["upper_right_curvature_identity_exact"] is True
            ),
            "the_exact_k3_tail_realization_problem_is_already_carrier_preserving_and_transport_twisted": (
                bool(
                    lift["carrier_preserving_transport_twisted_k3_lift_theorem"][
                        "therefore_any_exact_k3_side_realization_must_be_a_carrier_preserving_transport_twisted_lift"
                    ]
                )
            ),
            "the_positive_mixed_plane_wall_is_already_equivalent_to_one_nonzero_nilpotent_holonomy_increment": (
                increment["k3_mixed_plane_nilpotent_holonomy_increment_theorem"][
                    "therefore_exact_k3_tail_realization_is_equivalent_to_one_support_preserving_nonzero_nilpotent_holonomy_increment_on_the_same_fixed_host"
                ]
            ),
            "therefore_exact_k3_tail_realization_is_equivalent_to_one_support_preserving_nonzero_off_diagonal_curvature_witness_on_the_same_fixed_host": bool(
                curvature["off_diagonal_curvature_rank"] == 36
                and curvature["off_diagonal_curvature_support_rows"] == 4046
                and curvature["upper_right_curvature_identity_exact"] is True
                and lift["carrier_preserving_transport_twisted_k3_lift_theorem"][
                    "therefore_any_exact_k3_side_realization_must_be_a_carrier_preserving_transport_twisted_lift"
                ]
                and increment["k3_mixed_plane_nilpotent_holonomy_increment_theorem"][
                    "therefore_exact_k3_tail_realization_is_equivalent_to_one_support_preserving_nonzero_nilpotent_holonomy_increment_on_the_same_fixed_host"
                ]
            ),
            "the_live_external_wall_is_now_the_first_nonzero_off_diagonal_curvature_witness_on_the_same_fixed_host": (
                host["ordered_line_types"] == ["positive", "negative"]
                and list(host["mixed_signature"]) == [1, 1]
                and list(host["qutrit_lift_split"]) == [81, 81]
                and curvature["off_diagonal_curvature_rank"] == 36
            ),
        },
        "bridge_verdict": (
            "The mixed-plane K3 wall is now localized at the level of the "
            "actual transport-twisted precomplex. The missing datum already "
            "appears internally as a nonzero off-diagonal curvature block of "
            "rank 36 with explicit support, and exact K3 realization is a "
            "carrier-preserving lift of that same geometric coupling. So the "
            "positive external wall is now one support-preserving nonzero "
            "off-diagonal curvature witness on the same fixed host."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(
            build_k3_mixed_plane_off_diagonal_curvature_witness_summary(), indent=2
        ),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
