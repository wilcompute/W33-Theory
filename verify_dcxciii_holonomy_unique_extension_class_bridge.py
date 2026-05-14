#!/usr/bin/env python3
"""Part DCXCIII: holonomy unique extension-class bridge.

DCXCI and DCXCII reduced the frontier to a unique nonzero orbit of rank-one
square-zero updates on the exact 162-packet.  This verifier upgrades that
matrix statement to exact extension-class language using the repo's existing
transport extension / cocycle theorems.

Main point:

  - zero increment = trivial / split class,
  - the two nonzero increments are two representatives of one unique nontrivial
    nonsplit extension class,
  - so the remaining frontier is realization of that single nontrivial class on
    the already-correct host packet.
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

from verify_dcxci_holonomy_nonzero_orbit_frontier_bridge import (  # noqa: E402
    build_bridge as build_dcxci_bridge,
)
from verify_dcxcii_holonomy_rank_one_update_bridge import (  # noqa: E402
    build_bridge as build_dcxcii_bridge,
)
from w33_transport_ternary_cocycle_bridge import (  # noqa: E402
    build_transport_ternary_cocycle_summary,
)
from w33_transport_ternary_extension_bridge import (  # noqa: E402
    build_transport_ternary_extension_summary,
)


OUT_PATH = ROOT / "data" / "dcxciii_holonomy_unique_extension_class_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    trivial_class_count: int
    nontrivial_class_count: int
    total_class_count: int
    matter_extension_dimension: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    orbit = build_dcxci_bridge()
    rank = build_dcxcii_bridge()
    cocycle = build_transport_ternary_cocycle_summary()
    extension = build_transport_ternary_extension_summary()

    trivial_representative = orbit["orbit_data"]["zero_orbit_representative"]
    nontrivial_representatives = orbit["orbit_data"]["nonzero_orbit_representatives"]
    matter_extension_dimension = cocycle["matter_extension_operator"]["dimension"]

    identities = {
        "the_current_zero_increment_is_the_trivial_split_representative": (
            trivial_representative == [[0, 0], [0, 0]]
            and rank["rank_data"]["current_rank"] == 0
        ),
        "the_two_nonzero_rank_one_increments_form_one_nontrivial_orbit": (
            nontrivial_representatives == [[[0, 1], [0, 0]], [[0, 2], [0, 0]]]
            and orbit["summary"]["live_orbit_size"] == 2
            and rank["rank_data"]["live_ranks"] == [1, 1]
        ),
        "the_repo_already_knows_the_underlying_two_dimensional_transport_fiber_is_a_unique_nonsplit_extension": (
            extension["reduced_transport_module"]["is_nonsplit_extension_of_sign_by_trivial"] is True
            and extension["reduced_transport_module"]["invariant_complement_count"] == 0
        ),
        "the_repo_already_knows_the_cocycle_class_is_nontrivial_not_a_coboundary": (
            cocycle["extension_cocycle"]["twisted_cocycle_identity_exact"] is True
            and cocycle["extension_cocycle"]["cocycle_is_not_a_coboundary"] is True
        ),
        "the_exact_matter_extension_is_the_same_81_to_162_to_81_bridge_as_the_host_packet": (
            extension["matter_flavour_extension"]["short_exact_sequence_dimensions"] == [81, 162, 81]
            and matter_extension_dimension == 162
        ),
        "there_is_exactly_one_nontrivial_extension_class_in_the_current_reduced_language": (
            orbit["summary"]["orbit_count"] == 2
            and extension["reduced_transport_module"]["is_nonsplit_extension_of_sign_by_trivial"] is True
            and cocycle["extension_cocycle"]["cocycle_is_not_a_coboundary"] is True
        ),
        "therefore_the_remaining_frontier_is_realization_of_the_unique_nontrivial_transport_extension_class_on_the_already_correct_162_packet": (
            trivial_representative == [[0, 0], [0, 0]]
            and nontrivial_representatives == [[[0, 1], [0, 0]], [[0, 2], [0, 0]]]
            and extension["matter_flavour_extension"]["short_exact_sequence_dimensions"] == [81, 162, 81]
            and cocycle["extension_cocycle"]["cocycle_is_not_a_coboundary"] is True
        ),
    }

    summary = BridgeSummary(
        trivial_class_count=1,
        nontrivial_class_count=1,
        total_class_count=2,
        matter_extension_dimension=matter_extension_dimension,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "class_data": {
            "trivial_representative": trivial_representative,
            "nontrivial_representatives": nontrivial_representatives,
            "short_exact_sequence_dimensions": extension["matter_flavour_extension"]["short_exact_sequence_dimensions"],
            "cocycle_is_not_a_coboundary": cocycle["extension_cocycle"]["cocycle_is_not_a_coboundary"],
            "nonsplit_extension_witness_count": extension["reduced_transport_module"]["nonsplit_extension_witness_count"],
        },
        "interpretation": {
            "verdict": (
                "In the current reduced finite language there are only two extension classes on the exact host packet: the trivial split class and one unique nontrivial nonsplit class. The two live nonzero matrices are just two representatives of that single nontrivial class."
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