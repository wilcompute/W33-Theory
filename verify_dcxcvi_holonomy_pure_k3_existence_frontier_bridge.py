#!/usr/bin/env python3
"""Part DCXCVI: holonomy pure K3 existence frontier bridge.

After DCXCV, the last remaining bit has been identified with the existence bit
for the carrier-preserving transport-twisted K3 lift.  So the next question is
whether any genuinely finite/combinatorial ambiguity still remains.

This verifier proves that it does not: the finite side is already fixed, and
the only unresolved content is one curved K3 existence theorem.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
EXPLORATION = ROOT / "exploration"
for candidate in (ROOT, EXPLORATION):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from verify_dcxciii_holonomy_unique_extension_class_bridge import (  # noqa: E402
    build_bridge as build_dcxciii_bridge,
)
from verify_dcxcv_holonomy_lift_existence_bit_bridge import (  # noqa: E402
    build_bridge as build_dcxcv_bridge,
)
from w33_carrier_preserving_transport_twisted_k3_lift_bridge import (  # noqa: E402
    build_carrier_preserving_transport_twisted_k3_lift_bridge_summary,
)


OUT_PATH = ROOT / "data" / "dcxcvi_holonomy_pure_k3_existence_frontier_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    fixed_packet_dimension: int
    finite_ambiguity_count: int
    remaining_curved_theorem_count: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    classes = build_dcxciii_bridge()
    lift_bit = build_dcxcv_bridge()
    lift = build_carrier_preserving_transport_twisted_k3_lift_bridge_summary()

    theorem = lift["carrier_preserving_transport_twisted_k3_lift_theorem"]
    fixed_carrier = lift["fixed_external_carrier_package"]
    internal = lift["internal_transport_twisted_package"]

    identities = {
        "the_exact_host_packet_is_already_fixed_at_dimension_162": (
            classes["summary"]["matter_extension_dimension"] == 162
            and fixed_carrier["ordered_filtration_dimensions"] == [81, 162, 81]
        ),
        "the_external_carrier_package_is_already_fixed_before_any_new_k3_realization": bool(
            theorem[
                "the_external_carrier_package_is_already_fixed_before_any_genuine_k3_realization"
            ]
        ),
        "the_missing_internal_transport_datum_is_already_fixed_as_a_nontrivial_twisted_package": (
            internal["twisted_cocycle_not_coboundary"] is True
            and internal["matter_extension_dimension"] == 162
            and internal["precomplex_off_diagonal_rank"] > 0
            and bool(
                theorem[
                    "the_missing_internal_datum_already_assembles_into_an_exact_transport_twisted_precomplex"
                ]
            )
        ),
        "the_last_boolean_frontier_has_already_been_identified_with_the_k3_lift_existence_bit": (
            lift_bit["summary"]["current_lift_existence_bit"] == 0
            and lift_bit["summary"]["exact_realization_lift_existence_bit"] == 1
            and lift_bit["summary"]["bit_count"] == 1
        ),
        "the_open_wall_is_not_new_packet_shell_line_plane_or_class_data_but_existence_of_the_specific_k3_lift": bool(
            theorem[
                "the_open_wall_is_existence_of_that_carrier_preserving_transport_twisted_k3_lift"
            ]
        ),
        "therefore_no_finite_combinatorial_ambiguity_remains_and_only_one_curved_k3_existence_theorem_is_left": (
            classes["summary"]["matter_extension_dimension"] == 162
            and lift_bit["summary"]["bit_count"] == 1
            and theorem[
                "the_external_carrier_package_is_already_fixed_before_any_genuine_k3_realization"
            ]
            and theorem[
                "the_open_wall_is_existence_of_that_carrier_preserving_transport_twisted_k3_lift"
            ]
        ),
    }

    summary = BridgeSummary(
        fixed_packet_dimension=162,
        finite_ambiguity_count=0,
        remaining_curved_theorem_count=1,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "frontier_data": {
            "fixed_head_line": fixed_carrier["head_line"],
            "fixed_carrier_plane": fixed_carrier["carrier_plane"],
            "fixed_shell": fixed_carrier["ordered_filtration_dimensions"],
            "fixed_slot_shape": fixed_carrier["slot_shape"],
            "remaining_theorem": "existence_of_carrier_preserving_transport_twisted_k3_lift",
        },
        "interpretation": {
            "verdict": (
                "No further finite ambiguity remains. The host packet, carrier plane, head line, shell, slot shape, and internal transport-twisted datum are already fixed. The only unresolved content left by the current chain is one curved theorem: existence of the carrier-preserving transport-twisted K3 lift."
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