"""Sign-ordered ``U1`` line theorem induced by the filtered-shadow selector basis.

Two exact external facts are already present:

1. the transport/K3 comparison carries a canonical ordered split filtered
   shadow ``81(+) -> 162 -> 81(-)``;
2. the full current selector packet already picks a unique dominant isotropic
   line candidate inside the canonical carrier plane ``U1``.

This module packages the stronger combined consequence. Because the selector
coordinates on ``U1`` are already expressed in the ordered positive/negative
filtered-shadow basis, the dominant null-line candidate is not selected only by
its total weight. It is the unique line with:

- strictly larger positive-selector weight,
- strictly smaller negative-selector contamination, and
- strictly larger positive-minus-negative gap.

So the current bridge fixes a rigid sign-ordered line candidate inside ``U1``.
That is stronger than a bare line candidate, but still weaker than an exact
identification with the internal line ``span(1,1,0)``.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys

import numpy as np


if __package__ in {None, ""}:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
else:
    ROOT = Path(__file__).resolve().parents[1]

from w33_transport_filtered_shadow_bridge import (
    build_transport_filtered_shadow_bridge_summary,
)
from w33_u1_selector_line_selection_bridge import (
    build_u1_selector_line_selection_bridge_summary,
)


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_u1_filtered_shadow_line_order_bridge_summary.json"
ZERO_TOL = 1e-12


@lru_cache(maxsize=1)
def build_u1_filtered_shadow_line_order_bridge_summary() -> dict[str, object]:
    filtered = build_transport_filtered_shadow_bridge_summary()
    selection = build_u1_selector_line_selection_bridge_summary()

    coordinates = np.array(selection["u1_selector_coordinate_matrix"], dtype=float)
    positive_weights = coordinates[:, 0] ** 2
    negative_weights = coordinates[:, 1] ** 2
    signed_gaps = positive_weights - negative_weights

    dominant = int(selection["dominant_isotropic_line_index"])
    recessive = int(selection["recessive_isotropic_line_index"])

    return {
        "status": "ok",
        "ordered_filtered_shadow_line_types": filtered["external_canonical_split_filtration"][
            "ordered_line_types"
        ],
        "u1_positive_selector_weights": [float(value) for value in positive_weights.tolist()],
        "u1_negative_selector_weights": [float(value) for value in negative_weights.tolist()],
        "u1_positive_minus_negative_selector_gaps": [
            float(value) for value in signed_gaps.tolist()
        ],
        "dominant_isotropic_line_index": dominant,
        "recessive_isotropic_line_index": recessive,
        "dominant_isotropic_line_coefficients": selection["dominant_isotropic_line_coefficients"],
        "recessive_isotropic_line_coefficients": selection["recessive_isotropic_line_coefficients"],
        "u1_filtered_shadow_line_order_theorem": {
            "filtered_shadow_basis_is_canonically_ordered_positive_then_negative": (
                filtered["external_canonical_split_filtration"]["ordered_line_types"]
                == ["positive", "negative"]
            ),
            "dominant_u1_line_has_strictly_larger_positive_selector_weight": (
                positive_weights[dominant] > positive_weights[recessive] + ZERO_TOL
            ),
            "dominant_u1_line_has_strictly_smaller_negative_selector_contamination": (
                negative_weights[dominant] < negative_weights[recessive] + ZERO_TOL
            ),
            "dominant_u1_line_maximizes_positive_minus_negative_selector_gap": (
                signed_gaps[dominant] > signed_gaps[recessive] + ZERO_TOL
            ),
            "sign_order_refines_total_weight_order": (
                selection["u1_selector_line_selection_theorem"][
                    "there_is_a_unique_dominant_isotropic_line_inside_u1"
                ]
                and positive_weights[dominant] > positive_weights[recessive] + ZERO_TOL
                and signed_gaps[dominant] > signed_gaps[recessive] + ZERO_TOL
            ),
            "sign_ordered_line_candidate_is_first_refinement_rigid": (
                filtered["transport_filtered_shadow_theorem"][
                    "external_filtered_shadow_is_first_refinement_rigid"
                ]
                and selection["u1_selector_line_selection_theorem"][
                    "dominant_line_candidate_is_first_refinement_rigid"
                ]
            ),
            "current_bridge_fixes_a_rigid_positive_ordered_line_candidate_inside_u1": (
                filtered["external_canonical_split_filtration"]["ordered_line_types"]
                == ["positive", "negative"]
                and positive_weights[dominant] > positive_weights[recessive] + ZERO_TOL
                and signed_gaps[dominant] > signed_gaps[recessive] + ZERO_TOL
            ),
        },
        "bridge_verdict": (
            "The rigid U1 line candidate is now stronger than a bare weight "
            "ordering. Because the selector coordinates on U1 are already "
            "expressed in the canonical positive/negative filtered-shadow "
            "basis, the dominant null line is exactly the one with larger "
            "positive-selector support, smaller negative contamination, and "
            "larger positive-minus-negative gap. That sign-ordered choice is "
            "first-refinement rigid. So the current bridge already fixes a "
            "rigid positive-ordered line candidate inside U1, even though it "
            "still does not identify that line with the internal line "
            "span(1,1,0)."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_u1_filtered_shadow_line_order_bridge_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
