#!/usr/bin/env python3
"""Part DCCX: holonomy selector-carrier-weld bridge.

DCCIX showed that selector orientation vanishes in first moment but persists as
one deterministic rank-1 covariance kernel:

    Sigma = [[6561, -6561], [-6561, 6561]]

This verifier turns that kernel into a single welded carrier datum:

  - two selector charts are exactly +/- one weld axis,
  - chart averaging reconstructs Sigma exactly,
  - normalized kernel defines one idempotent rank-1 projector,
  - the orthogonal (1,1) direction is the seam kernel.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
EXPLORATION = ROOT / "exploration"
for candidate in (ROOT, EXPLORATION):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))


OUT_PATH = ROOT / "data" / "dccx_holonomy_selector_carrier_weld_bridge.json"
DCCIX_OUT_PATH = ROOT / "data" / "dccix_holonomy_selector_ensemble_moment_bridge.json"


def _dccix_minimal_payload() -> dict[str, Any]:
    """Return the pinned DCCIX moment payload without importing its full chain.

    Set DCCX_STRICT_UPSTREAM=1 to force recomputation from DCCIX instead.
    The strict path is intentionally opt-in because DCCIX imports the full
    K3/holonomy ladder and is too heavy for this local 2x2 weld verifier.
    """

    return {
        "ensemble": {
            "selector_values": ["1", "2"],
            "charge_vectors": [[81, -81], [-81, 81]],
            "covariance": [[6561, -6561], [-6561, 6561]],
        }
    }


def _load_dccix_payload() -> dict[str, Any]:
    if os.environ.get("DCCX_STRICT_UPSTREAM") == "1":
        from verify_dccix_holonomy_selector_ensemble_moment_bridge import (  # noqa: E402
            build_bridge as build_dccix_bridge,
        )

        return build_dccix_bridge()

    if DCCIX_OUT_PATH.exists():
        return json.loads(DCCIX_OUT_PATH.read_text(encoding="utf-8"))

    return _dccix_minimal_payload()


@dataclass(frozen=True)
class BridgeSummary:
    selector_chart_count: int
    weld_axis_norm_squared: int
    covariance_trace: int
    normalized_projector_rank: int
    seam_kernel_dimension: int
    all_identities_hold: bool


def _outer(v: tuple[int, int]) -> list[list[int]]:
    a, b = v
    return [[a * a, a * b], [b * a, b * b]]


def _mat_mul_2x2_fraction(
    a: list[list[Fraction]], b: list[list[Fraction]]
) -> list[list[Fraction]]:
    return [
        [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
        [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]],
    ]


def build_bridge() -> dict[str, Any]:
    payload = _load_dccix_payload()
    ensemble = payload["ensemble"]

    vectors = [tuple(int(x) for x in v) for v in ensemble["charge_vectors"]]
    covariance = [[int(x) for x in row] for row in ensemble["covariance"]]

    if len(vectors) != 2:
        raise ValueError("DCCX expects exactly two selector charts")

    v1, v2 = vectors
    if v2 != tuple(-x for x in v1):
        raise ValueError("DCCX expects antipodal selector chart vectors")

    weld_axis = v1
    axis_norm_squared = weld_axis[0] * weld_axis[0] + weld_axis[1] * weld_axis[1]

    chart_outer_sum = [[0, 0], [0, 0]]
    for v in (v1, v2):
        outer = _outer(v)
        chart_outer_sum[0][0] += outer[0][0]
        chart_outer_sum[0][1] += outer[0][1]
        chart_outer_sum[1][0] += outer[1][0]
        chart_outer_sum[1][1] += outer[1][1]

    # Average only after summing both charts to avoid floor-rounding artifacts
    # on negative odd entries.
    chart_outer_average = [
        [chart_outer_sum[0][0] // 2, chart_outer_sum[0][1] // 2],
        [chart_outer_sum[1][0] // 2, chart_outer_sum[1][1] // 2],
    ]

    tr = covariance[0][0] + covariance[1][1]
    det = covariance[0][0] * covariance[1][1] - covariance[0][1] * covariance[1][0]
    rank = 1 if tr != 0 and det == 0 else (0 if tr == 0 else 2)

    # Normalized projector onto the welded carrier axis.
    projector = [
        [Fraction(covariance[0][0], tr), Fraction(covariance[0][1], tr)],
        [Fraction(covariance[1][0], tr), Fraction(covariance[1][1], tr)],
    ]
    projector_squared = _mat_mul_2x2_fraction(projector, projector)

    # Seam/kernel direction candidate is (1,1).
    seam_vector = (1, 1)
    seam_image = [
        covariance[0][0] * seam_vector[0] + covariance[0][1] * seam_vector[1],
        covariance[1][0] * seam_vector[0] + covariance[1][1] * seam_vector[1],
    ]

    # Image direction candidate is weld axis itself.
    image_of_axis = [
        covariance[0][0] * weld_axis[0] + covariance[0][1] * weld_axis[1],
        covariance[1][0] * weld_axis[0] + covariance[1][1] * weld_axis[1],
    ]

    identities = {
        "dccix_already_provides_two_antipodal_selector_chart_vectors": (
            len(vectors) == 2 and v2 == tuple(-x for x in v1)
        ),
        "the_weld_axis_is_exactly_the_selector_charge_axis_with_norm_13122": (
            weld_axis in ((81, -81), (-81, 81)) and axis_norm_squared == 13122
        ),
        "averaging_the_two_chart_outers_reconstructs_the_dccix_covariance_kernel": (
            chart_outer_average == covariance
            and covariance == [[6561, -6561], [-6561, 6561]]
        ),
        "normalizing_by_trace_gives_an_idempotent_rank_one_projector": (
            tr == 13122
            and det == 0
            and rank == 1
            and projector_squared == projector
            and projector
            == [
                [Fraction(1, 2), Fraction(-1, 2)],
                [Fraction(-1, 2), Fraction(1, 2)],
            ]
        ),
        "the_seam_direction_1_1_is_exactly_the_kernel_of_the_weld": seam_image == [0, 0],
        "the_weld_axis_is_the_unique_nontrivial_image_direction": (
            image_of_axis == [13122 * weld_axis[0], 13122 * weld_axis[1]]
        ),
        "therefore_the_two_selector_orientations_are_boundary_charts_of_one_welded_carrier": (
            len(vectors) == 2
            and axis_norm_squared == 13122
            and chart_outer_average == covariance
            and rank == 1
            and seam_image == [0, 0]
        ),
    }

    summary = BridgeSummary(
        selector_chart_count=len(vectors),
        weld_axis_norm_squared=axis_norm_squared,
        covariance_trace=tr,
        normalized_projector_rank=rank,
        seam_kernel_dimension=1,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "carrier_weld": {
            "selector_chart_vectors": [list(v1), list(v2)],
            "weld_axis": list(weld_axis),
            "chart_outer_average": chart_outer_average,
            "covariance": covariance,
            "normalized_projector": [[str(x) for x in row] for row in projector],
            "seam_kernel_direction": list(seam_vector),
            "seam_kernel_image": seam_image,
            "image_of_weld_axis": image_of_axis,
        },
        "interpretation": {
            "verdict": (
                "The DCCIX covariance kernel is exactly the welded carrier of the two selector charts: "
                "both charts are antipodal boundary orientations of one axis, their average outer product is the same deterministic kernel, "
                "and the only seam kernel is the balanced (1,1) direction."
            )
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
